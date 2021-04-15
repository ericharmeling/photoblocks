import falcon
import inspect
import logging

class BaseResource(object):
    def __init__(self, pack, db):
        self.db = db
        self.pack = pack

class PackResource(BaseResource):
    def on_get(self, req, resp):
        resp.data = self.pack
        resp.status = falcon.HTTP_200

class PeerResource(BaseResource):
    def on_get(self, req, resp, id=None):
        if id:
            if id == self.pack["id"]:
                resp.data = self.pack
            else:
                try:
                    resp.data = self.db.get(id)
                except Exception:
                    logging.info('Checking for existing seeds.')  
        else:
            resp.data = self.db.get('nodes')
        resp.status = falcon.HTTP_200

    def on_post(self, req, resp):
        data = req.stream.read()
        if id:
            self.db.set(id, data)
        else:
            self.db.set('nodes', data)
        resp.status = falcon.HTTP_201

class ChainResource(BaseResource):
    def on_get(self, req, resp):
        self.db.get('chain')
        resp.status = falcon.HTTP_200

    def on_post(self, req, resp):
        data = req.stream.read()
        self.db.set('chain', data)
        resp.status = falcon.HTTP_201

class MineResource(BaseResource):
    def on_post(self, req, resp):
        data = req.stream.read()
        resp.status = falcon.HTTP_201
