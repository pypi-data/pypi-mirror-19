# coding:utf8

"""全局变量记载模块"""


import json

from fastweb import ioloop
from fastweb.manager import Manager
from fastweb.utils.base import Configer
from fastweb.utils.log import get_logging_config, setup_logging, getLogger, colored, recorder


class Loader(object):
    """系统全局变量加载器"""

    def __init__(self):
        self.config = {}
        self.config_handler = None
        self.logging_config = None
        self.errcode = {}
        self.mime = {}
        self.manager = None
        self.logger = None
        self.request_logger = None
        self.system_logger = None

    def load_config(self, config_path):
        """加载配置文件"""

        configer = Configer(config_path)
        self.config_handler = configer
        self.config = configer.config
        recorder('INFO', 'setup component configuration\n{conf}'.format(conf=json.dumps(self.config, indent=4) ) )

    def load_errcode(self):
        """加载系统错误码"""

        errcode = {
            'SUC': {'code': 0, 'message': 'success'},
            'ARG': {'code': 1001, 'message': 'invalid arguments'},
            'SVR': {'code': 2001, 'message': 'server error'},
            'TOKEN': {'code': 3995, 'message': 'token invalid'},
            'KEY': {'code': 4001, 'message': 'key not exist'},
            'EXT': {'code': 4002, 'message': 'key exist'},
            'PWD': {'code': 4003, 'message': 'password wrong'},
            'FMT': {'code': 4004, 'message': 'format error'},
            'FT': {'code': 4005, 'message': 'upload file type not support'},
        }

        self.errcode = errcode
        return errcode

    def load_mime(self):
        """加载mime值"""

        mime = {
            'image/gif': '.gif',
            'image/x-png': '.png',
            'image/x-jpeg': '.jpeg',
            'image/jpeg': '.jpeg',
            'image/png': '.png'
        }

        self.mime = mime
        return mime

    def load_manager(self, isAsyn=True):
        """加载管理器"""

        self.manager = Manager(isAsyn=isAsyn)
        ioloop.IOLoop.instance().run_sync(self.manager.reset)

    def load_logger(self, request_log_path, system_log_path=None):
        """加载日志对象"""

        self.logging_config = get_logging_config()
        self.logging_config['handlers']['request_file_time_handler'][
            'filename'] = request_log_path
        self.logging_config['handlers']['norequest_file_size_handler'][
            'filename'] = system_log_path if system_log_path else request_log_path
        setup_logging(self.logging_config)
        self.system_logger = getLogger('system_logger')
        self.request_logger = getLogger('request_logger')
        recorder('INFO', 'setup logging configuration\n{conf}'.format(conf=json.dumps(self.logging_config, indent=4) ) )


gl = Loader()
