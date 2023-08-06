# coding:utf8

import os
import re
import yaml
import logging
import logging.config
from logging import getLogger
from termcolor import colored
from logging.handlers import (RotatingFileHandler, TimedRotatingFileHandler)
from logging import (DEBUG, INFO, WARNING, ERROR, CRITICAL)


DEFAULT_LOGGING_CONF_EVN = 'LOG_CFG'
DEFAULT_LOGGING_CONF_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, 'setting/default_logging.yaml') ) 


def get_logging_config(path=DEFAULT_LOGGING_CONF_PATH, env_key=DEFAULT_LOGGING_CONF_EVN):
    """获取logging配置文件
       先从环境变量env_key获取配置文件
       如果不存在则从path中获取配置文件"""

    value = os.getenv(env_key, None)
    path = value if value else path

    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = yaml.safe_load(f.read() )

    return config

def setup_logging(config, level=INFO):
    """根据字典加载配置文件"""

    if config:
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=level)

def recorder(level, msg):
    """日志记录"""

    level = level.lower()
    level_dict = { 
        'info': (getLogger('system_logger').info, 'white'),
        'debug': (getLogger('system_logger').debug, 'green'),
        'warn': (getLogger('system_logger').warn, 'yellow'),
        'error': (getLogger('system_logger').error, 'red'),
        'critical': (getLogger('system_logger').critical, 'magenta')
    }   

    if level not in level_dict.keys():
        system_logger.error(
            'unsupport log level <{level}>'.farmat(level=level))

    logger_func, logger_color = level_dict[level]
    logger_func(colored(msg, logger_color, attrs=['bold']) )    

if __name__ == '__main__':
    setup_logging()

    logger = logging.getLogger('sys_logger')
    logger.info('我爱北京')
    logger.error('错误信息')
