#encoding: utf-8

import pyssdb

class SSDB(object):

    def __init__(self,**kvargs):
        pass
        self._client = None  
        self.reset(kvargs)

    def reset(self,kvargs):
        pass
        host = kvargs.get('host') 
        port = int(kvargs.get('port'))

        self._client = pyssdb.Client(host,port)
       
    def close(self):
        self._client.disconnect()

    def __del__(self):
        self.close()

    def get(self,key): 
        return self._client.get(key)
