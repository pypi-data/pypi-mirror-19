# coding:utf8


from fastweb import coroutine
from fastweb import ioloop
from fastweb.utils.log import recorder
from fastweb.exception import ConfigError


#不可用状态
UNUSED = 0
#空闲可用状态
IDLE = 1
#忙碌不可用状态
USED = 2
#错误不可用状态
ERROR = 3


class BaseComponent(object):
    """组件基类"""
    
    eattr = {}
      
    def __init__(self, **kwargs):
        """name:组件名称
           recorder:日志记录方法
           status:当前状态
           kwargs:传入参数"""

        self.kwargs = {}
        self.name = None
        self.recorder = None
        self.status = UNUSED
        self.exceptions = []
        self._check_attr(kwargs)

    def _check_attr(self, kwargs):
        """检查组件属性是否合法"""
        
        for attr,tp in self.eattr.iteritems():
            v = kwargs.get(attr)
            if not v:
                recorder('ERROR', '<{attr}> is ensential attr of <{name}>'.format(attr=attr, name=self.name) )
                raise ConfigError
            else:
                try:
                    self.kwargs[attr] = tp(v)
                except Exception as ex:
                    recorder('ERROR', "<{attr}> can't convert to {tp} of <{name}> ({e})".format(attr=attr, tp=tp, name=self.name, e=ex) )
                    raise ConfigError

    def set_used(self, logfunc):
        """设置为忙碌可用状态"""

        self.recorder = logfunc
        self.status = USED

    def set_idle(self):
        """设置为空闲可用状态"""

        self.status = IDLE
        self.recorder = None

    def set_error(self, ex):
        """设置为错误状态,等待回收"""

        self.status = ERROR
        self.exceptions.append(ex)


class ProxyCall(object):
    """调用代理,用来解决__getattr__无法传递多个参数的问题"""

    def __init__(self, proxy, method):
        self._proxy = proxy
        self._method = method

    @coroutine
    def __call__(self, *arg, **kwargs):
        with fastweb.utils.tool.timing('ms', 8) as t:
            try:
                yield getattr(self._proxy._other, self._method)(*arg, **kwargs)
            except Exception as ex:
                yield self._proxy._connect()

        recorder('INFO', 'call proxy <{time}>'.format(time=t) )

