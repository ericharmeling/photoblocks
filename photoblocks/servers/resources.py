import falcon
import json
import logging
import redis
from photoblocks.exceptions import StorageError, ValidationError

class BaseResource:
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
        """Get node configuration package"""
        try:
            resp.media = self.pack
            resp.status = falcon.HTTP_200
        except Exception as e:
            raise falcon.HTTPInternalServerError(
                title='Server Error',
                description=str(e)
            )

class PeerResource(BaseResource):
    def on_get(self, req, resp, id=None):
        """Get peer information"""
        try:
            if id:
                if id == self.pack["id"]:
                    resp.media = self.pack
                else:
                    resp.media = json.loads(self._safe_db_get(id))
            else:
                resp.media = json.loads(self._safe_db_get('nodes'))
            resp.status = falcon.HTTP_200
        except StorageError as e:
            raise falcon.HTTPNotFound(
                title='Peer Not Found',
                description=str(e)
            )

    def on_post(self, req, resp):
        """Register new peer"""
        try:
            data = req.media
            if 'id' in data:
                self._safe_db_set(data['id'], json.dumps(data))
            else:
                self._safe_db_set('nodes', json.dumps(data))
            resp.status = falcon.HTTP_201
        except (ValidationError, StorageError) as e:
            raise falcon.HTTPBadRequest(
                title='Invalid Peer Data',
                description=str(e)
            )

class ChainResource(BaseResource):
    def on_get(self, req, resp):
        """Get current blockchain state"""
        try:
            chain_data = self._safe_db_get('chain')
            resp.media = json.loads(chain_data)
            resp.status = falcon.HTTP_200
        except StorageError as e:
            raise falcon.HTTPServiceUnavailable(
                title='Storage Error',
                description=str(e)
            )

    def on_post(self, req, resp):
        """Update blockchain state"""
        try:
            chain_data = req.media
            self._validate_chain(chain_data)
            self._safe_db_set('chain', json.dumps(chain_data))
            resp.status = falcon.HTTP_201
        except ValidationError as e:
            raise falcon.HTTPBadRequest(
                title='Invalid Chain Data',
                description=str(e)
            )

class MineResource(BaseResource):
    def on_post(self, req, resp):
        """Initiate mining process"""
        try:
            mining_data = req.media
            # TODO: Implement mining logic
            resp.status = falcon.HTTP_202  # Accepted
        except Exception as e:
            raise falcon.HTTPInternalServerError(
                title='Mining Error',
                description=str(e)
            ) 

class HealthResource(BaseResource):
    def on_get(self, req, resp):
        """Health check endpoint"""
        try:
            # Check Redis connection
            self.db.ping()
            
            resp.media = {
                'status': 'healthy',
                'redis': 'connected'
            }
            resp.status = falcon.HTTP_200
            
        except redis.RedisError:
            resp.media = {
                'status': 'unhealthy',
                'redis': 'disconnected'
            }
            resp.status = falcon.HTTP_503 