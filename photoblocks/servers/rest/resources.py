import falcon
import logging
import redis
from photoblocks.exceptions import StorageError, ValidationError

class BaseResource(object):
    def __init__(self, pack, db):
        self.db = db
        self.pack = pack

    def _safe_db_get(self, key):
        """Safely retrieve data from Redis"""
        try:
            data = self.db.get(key)
            if data is None:
                raise StorageError(f"No data found for key: {key}")
            return data.decode('utf-8')
        except redis.RedisError as e:
            raise StorageError(f"Redis error: {e}")

    def _safe_db_set(self, key, value):
        """Safely set data in Redis"""
        try:
            return self.db.set(key, value)
        except redis.RedisError as e:
            raise StorageError(f"Redis error: {e}")

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
        try:
            resp.data = self._safe_db_get('chain')
            resp.status = falcon.HTTP_200
        except StorageError as e:
            raise falcon.HTTPServiceUnavailable(
                title='Storage Error',
                description=str(e)
            )

    def on_post(self, req, resp):
        try:
            data = req.stream.read()
            self._validate_chain_data(data)
            self._safe_db_set('chain', data)
            resp.status = falcon.HTTP_201
        except ValidationError as e:
            raise falcon.HTTPBadRequest(
                title='Invalid Chain Data',
                description=str(e)
            )

class MineResource(BaseResource):
    def on_post(self, req, resp):
        data = req.stream.read()
        resp.status = falcon.HTTP_201
