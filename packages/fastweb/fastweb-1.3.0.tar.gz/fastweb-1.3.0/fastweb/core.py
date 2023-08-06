# coding:utf8

"""核心模块"""


import json
import types
import shlex
import threading
import traceback
import subprocess

from tornado import ioloop, web
from tornado.locks import Condition
from tornado.process import Subprocess
from tornado.gen import coroutine, Task, Return
from tornado.httpclient import HTTPClient, AsyncHTTPClient, HTTPRequest as Request, HTTPError

from fastweb.loader import gl
from fastweb.utils.tool import timing
from fastweb.utils.base import uniqueid
from fastweb.utils.python import to_plain
from fastweb.utils.log import recorder, getLogger, colored
from fastweb.exception import ComponentError, HttpError, SubProcessError


class CeleryTask():
    """TODO:增加task类"""
    pass


class Component(object):
    """组件基类"""

    _blacklist = ['requestid', '_new_cookie', 'include_host',
                  '_active_modules', '_current_user', '_locale']

    def __init__(self):
        self.config = gl.config
        self._thread_lock = threading.Lock()
        self.loader = gl
        self.errcode = gl.errcode

        # 组件缓冲池,确保同一请求对同一组件只获取一次
        self._components = {}
        # gl.manager.set_logger(self.recorder)

    def __getattr__(self, name):
        """获取组件"""

        if name in self._blacklist:
            raise AttributeError

        obj = self._components.get(name)

        if not obj:
            self._thread_lock.acquire()
            obj = getattr(gl.manager, name)
            obj.set_used(self.recorder)
            self._thread_lock.release()

            if not obj:
                recorder('ERROR',
                    "can't acquire idle component <{name}>".format(name=name))
                raise ComponentError

            self._components[name] = obj
            return obj
        else:
            return obj

    def gen_requestid(self):
        """生成requestid"""

        return uniqueid()

    def add_blacklist(self, attr):
        """增加类属性黑名单"""

        self._blacklist.append(attr)

    def add_function(self, **kwargs):
        """增加方法到对象中"""

        for callname, func in kwargs.iteritems():
            setattr(self, '{callname}'.format(
                callname=callname), types.MethodType(func, self))

    def recorder(self, level, msg):
        """日志记录"""

        level = level.lower()
        level_dict = {
            'important': (getLogger('request_logger').info, 'cyan'),
            'info': (getLogger('request_logger').info, 'white'),
            'debug': (getLogger('request_logger').debug, 'green'),
            'warn': (getLogger('request_logger').warn, 'yellow'),
            'error': (getLogger('request_logger').error, 'red'),
            'critical': (getLogger('request_logger').critical, 'magenta')
        }

        if level not in level_dict.keys():
            recorder('ERROR',
                'unsupport log level <{level}>'.farmat(level=level))

        logger_func, logger_color = level_dict[level]
        logger_func(colored(msg, logger_color, attrs=['bold']), extra={
                    'requestid': self.requestid})

    def release(self):
        """释放组件"""

        for component in self._components.values():
            gl.manager.add_idle_component(component)

        self.recorder('INFO', 'idle all used components')


class SyncComponent(Component):
    """同步组件类"""

    def __init__(self):
        super(SyncComponent, self).__init__()

    def http_request(self, request):
        """http请求"""

        self.recorder(
            'INFO', 'http request start <{request}>'.format(request=request))

        with timing('ms', 8) as t:
            try:
                response = HTTPClient(request)
            except HTTPError as ex:
                self.recorder('ERROR', 'http request error <request> <{time}> {e}'.format(
                    request=request, time=t, e=ex))
                raise HttpError

        self.recorder('INFO', 'http request success <{request}> <{time}>'.format(
            request=request, time=t))
        return response

    def call_subprocess(self, command, stdin_data=None):
        """命令行调用"""

        self.recorder(
            'INFO', 'call subprocess start <{cmd}>'.format(cmd=command))

        with timing('ms', 8) as t:
            sub_process = subprocess.Popen(shlex.split(command),
                                           stdout=subprocess.PIPE,
                                           stderr=subprocess.PIPE)
            try:
                result, error = sub_process.communicate(stdin_data)
            except (OSError, ValueError) as ex:
                self.recorder('ERROR', 'call subprocess <{cmd} <{time}> {e} {msg}'.format(
                    cmd=command, time=t, e=ex, msg=result.strip() if result else error.strip()))
                raise SubProcessError

        if sub_process.returncode != 0:
            self.recorder('ERROR', 'call subprocess <{cmd}> <{time}> {msg}'.format(
                cmd=command, time=t, msg=result.strip() if result else error.strip()))
            raise SubProcessError

        self.recorder('INFO', 'call subprocess <{cmd}> <{time} {msg}>'.format(
            command=command, time=t, msg=result.strip() if result else error.strip()))
        return result, error


class AsynComponent(Component):
    """异步组件基类,异步组件操作"""

    def __init__(self):
        super(AsynComponent, self).__init__()

    @coroutine
    def http_request(self, request):
        """http请求"""

        self.recorder(
            'INFO', 'http request start <{request}>'.format(request=request))

        with timing('ms', 8) as t:
            try:
                response = yield AsyncHTTPClient(request)
            except HTTPError as ex:
                self.recorder('ERROR', 'http request error <request> <{time}> {e}'.format(
                    request=request, time=t, e=ex))
                raise HttpError

        self.recorder('INFO', 'http request success <{request}> <{time}>'.format(
            request=request, time=t))
        raise Return(response)

    @coroutine
    def call_subprocess(self, command, stdin_data=None, stdin_async=True):
        """命令行调用"""

        self.recorder(
            'INFO', 'call subprocess start <{cmd}>'.format(cmd=command))

        with timing('ms', 8) as t:
            stdin = Subprocess.STREAM if stdin_async else subprocess.PIPE
            sub_process = Subprocess(shlex.split(command),
                                     stdin=stdin,
                                     stdout=Subprocess.STREAM,
                                     stderr=Subprocess.STREAM)
            try:
                if stdin_data:
                    if stdin_async:
                        yield Task(sub_process.stdin.write, stdin_data)
                    else:
                        sub_process.stdin.write(stdin_data)

                if stdin_async or stdin_data:
                    sub_process.stdin.close()

                result, error = yield [Task(sub_process.stdout.read_until_close),
                                       Task(sub_process.stderr.read_until_close)]
            except (OSError, ValueError) as ex:
                self.recorder('ERROR', 'call subprocess <{cmd} <{time}> {e} {msg}'.format(
                    cmd=command, time=t, e=ex, msg=result.strip() if result else error.strip()))
                raise SubProcessError

        if sub_process.returncode != 0:
            self.recorder('ERROR', 'call subprocess <{cmd}> <{time}> {msg}'.format(
                cmd=command, time=t, msg=result.strip() if result else error.strip()))
            raise SubProcessError

        self.recorder('INFO', 'call subprocess <{cmd}> <{time} {msg}>'.format(
            command=command, time=t, msg=result.strip() if result else error.strip()))
        raise Return((result, error))


class Api(web.RequestHandler, AsynComponent):
    """Api操作基类"""

    def __init__(self, application, request, **kwargs):
        super(Api, self).__init__(application, request, **kwargs)

        self.uri = request.uri
        self.remoteip = request.remote_ip
        self.host = request.host
        self.arguments = self.request.arguments
        self.requestid = self.get_argument('requestid') if self.get_argument(
            'requestid', None) else self.gen_requestid()
        self.recorder(
            'IMPORTANT',
            'Api request <{ip}> <{host}{uri}> <{arguments}> <{ua}>'.format(
                ip=self.remoteip,
                host=self.host,
                uri=self.uri,
                arguments=self.request.body,
                ua=self.request.headers['User-Agent']))

    def log_exception(self, typ, value, tb):
        """日志记录异常,并自动返回系统错误"""

        self.recorder('ERROR', '{message}'.format(
            message=traceback.format_exc()))
        self.end('SVR')

    def set_ajax_cors(self, allow_ip):
        """设置cors"""

        headerkey = 'Access-Control-Allow-Origin'
        self.set_header(headerkey, allow_ip)
        self.recorder('INFO', 'set header <{key}:{ip}>'.format(
            key=headerkey, ip=allow_ip))

    def set_header_json(self):
        """设置返回格式为json"""

        headerkey = 'Content-type'
        self.add_header(headerkey, 'text/json')
        self.recorder('INFO', 'set header <{key}:{type}>'.format(
            key=headerkey, type='text/json'))

    def end(self, code='SUC', logRet=True, **kwargs):
        """请求结束"""

        ret = gl.errcode[code]
        ret = dict(ret, **kwargs)
        self.write(json.dumps(ret))
        self.finish()
        self.release()
        t = (self.request._finish_time-self.request._start_time)*1000

        if logRet:
            self.recorder(
                'IMPORTANT',
                'Api response <{ip}> <{host}{uri}> <{ret}> <{time}ms>'.format(
                    ip=self.remoteip, host=self.host, uri=self.uri, ret=ret, time=t) )
        else:
            self.recorder(
                'IMPORTANT',
                'Api response <{ip}> <{host}{uri}> <{time}ms>'.format(
                    ip=self.remoteip, host=self.host, uri=self.uri, time=t) )


class Page(web.RequestHandler, AsynComponent):
    """Page操作基类"""

    def __init__(self, application, request, **kwargs):
        super(Page, self).__init__(application, request, **kwargs)

        self._ret = {}
        self._uri = request.uri
        self._remote_ip = request.remote_ip
        self._host = request.host
        self.arguments = self.request.arguments
        self.requestid = ''.join(self.request.arguments.get(
            'requestid')) if self.request.arguments.get('requestid') else self.requestid

        self.recorder(
            'INFO',
            'Page IN -- remote_ip[%s] -- api[%s%s] -- arg[%s] -- User-Agent[%s]' %
            (self._remote_ip,
             self._host,
             self._uri,
             self.request.arguments,
             self.request.headers['User-Agent']))

    def log_exception(self, typ, value, tb):
        """日志记录异常"""

        self.recorder('error', '{message}'.format(
            message=traceback.format_exc()))

    def end(self, template=None, log=True, **kwargs):
        """ 请求结束"""

        if template:
            self.render(template, **kwargs)

        # 释放掉组件使用权
        self.release()
        if log:
            self.recorder(
                'info', 'page out -- remote_ip[{ip}] -- api[{host}{uri}] -- template[{template}] -- variable[{variable}]'.format(
                    ip=self._remote_ip, host=self._host, uri=self._uri, template=template, variable=kwargs))
        else:
            self.recorder(
                'info',
                'api out -- remote_ip[{ip}] -- api[{host}{uri}] -- template[{template}]'.format(
                    ip=self._remote_ip, host=self._host, uri=self._uri, template=template))


def checkArgument(convert=None, **ckargs):
    """检查并转换请求参数是否合法并转换参数类型"""

    def _deco(fn):
        def _wrap(cls, *args, **kwargs):
            if convert:
                for cname, ctype in convert.iteritems():
                    cvalue = cls.request.arguments.get(cname)
                    cvalue = to_plain(cvalue)
                    if cvalue:
                        cls.request.arguments[cname] = ctype(cvalue)

            for cname, ctype in ckargs.iteritems():
                cvalue = cls.request.arguments.get(cname)
                cvalue = to_plain(cvalue)

                def invalid_recorder(msg):
                    diff = set(cls.request.arguments.keys()
                               ).symmetric_difference(set(ckargs.keys()))
                    cls.recorder('error', 'check arguements invalid <{diff}> {msg}'.format(
                        msg=msg, diff=to_plain(diff)))
                    cls.end('SVR')

                if cvalue:
                    if ctype is int:
                        if not cvalue.isdigit():
                            invalid_recorder('argument type error')
                            return
                    elif not isinstance(cvalue, ctype):
                        invalid_recorder('argument type error')
                        return
                else:
                    if isinstance(cls, Api):
                        invalid_recorder('argument empty')
                        return
                    elif isinstance(cls, Page):
                        invalid_recorder('argument empty')
                        return
                cls.request.arguments[cname] = ctype(cvalue)
            return fn(cls, *args, **kwargs)
        return _wrap
    return _deco
