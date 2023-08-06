# coding:utf-8

"""组件管理模块"""


import json

from fastweb import ioloop
import fastweb.loader
from fastweb.utils.log import recorder, colored
from fastweb import coroutine, Return, gen
from fastweb.component import (USED, IDLE, ERROR)
from fastweb.component.db.fmysql import (AsynMysql, Mysql)
from fastweb.component.db.fredis import (AsynRedis, Redis)
from fastweb.component.db.fmongo import (AsynMongo, Mongo)
from fastweb.component.rpc.fthrift import (AsynRpc, SyncRpc)
from fastweb.exception import ConfigError, ComponentError


DEFAULT_POOL_SIZE = 5
ASYN_MANAGER_TUPLE = [('mysql', AsynMysql, DEFAULT_POOL_SIZE),
                      ('redis', AsynRedis, DEFAULT_POOL_SIZE),
                      ('mongo', AsynMongo, DEFAULT_POOL_SIZE),
                      ('rpc', AsynRpc, DEFAULT_POOL_SIZE)]
SYNC_MANAGER_TUPLE = [('mysql', Mysql, DEFAULT_POOL_SIZE),
                     ('redis', Redis, DEFAULT_POOL_SIZE),
                     ('mongo', Mongo, DEFAULT_POOL_SIZE),
                     ('rpc', SyncRpc, DEFAULT_POOL_SIZE)]


class Manager(object):
    """组件管理器
       组件名称不可以重复"""

    def __init__(self, isAsyn=True):
        self._managers = {}
        self._logger = None
        self._isAsyn = isAsyn
        self._idle_components = {}
        self._used_components = {}
        self._error_components = {}

    @coroutine
    def reset(self):
        """组件初始化"""

        if fastweb.loader.gl.config_handler:
            for (cpre, cls, num) in ASYN_MANAGER_TUPLE if self._isAsyn else SYNC_MANAGER_TUPLE:
                components = fastweb.loader.gl.config_handler.get_components(
                    cpre)
                for name, value in components.items():
                    config = fastweb.loader.gl.config[name]
                    max = int(config.get('max', num) )
                    pool = []

                    if config:
                        if value['object'] in self._managers.keys():
                            recorder('DEBUG',
                                'config section duplicate <{section}>'.format(
                                    section=value['object']) )
                            continue
                        for x in range(max):
                            try:
                                obj = cls(**config)
                                if self._isAsyn:
                                    yield obj.connect()
                                else:
                                    obj.connect()
                            except ComponentError as ex:
                                recorder('ERROR', 'component create error {cls}\n<{name}>\n{conf}'.format(cls=cls, name=name, conf=json.dumps(config, indent=4) ) )
                                recorder('CRITICAL', 'please check connection configuration')
                                raise ComponentError
                            obj.name = value['object']
                            pool.append(obj)
                            recorder('DEBUG',
                                'component create successful {obj}'.format(
                                    obj=obj))
                        self._idle_components['{name}'.format(name=value['object'])] = (cls, config, pool)
            recorder('INFO', 'component pool create successful')

    def add_idle_component(self, component):
        """向管理器中加入空闲组件"""

        component.set_idle()
        self._idle_components[component.name][2].append(component)

    def __getattr__(self, name):
        """获取组件
           返回一个状态正常的组件,如果没有状态正常组件返回None"""

        cls, config, components = self._idle_components.get(name, (None, None, None))

        if cls and config:
            if components:
                component = components.pop()
                return component
            
            component = cls(**config)
        else:
            return None
