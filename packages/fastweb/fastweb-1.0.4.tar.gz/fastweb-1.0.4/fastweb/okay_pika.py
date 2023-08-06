#encoding: utf-8

import json

from pika import PlainCredentials
from pika import BlockingConnection 
from pika import ConnectionParameters


class Pika(object):

    def __init__(self,**args):
        self.reset(**args)

    def reset(self,**args):
        self._credentials = PlainCredentials(args['user'], args['password']) 
        self._connection = BlockingConnection(ConnectionParameters(args['host'], int(args['port']), args['uri'], self._credentials)) 



 

