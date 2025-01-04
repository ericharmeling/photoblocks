from typing import Dict, Any
import json
import redis
from photoblocks.exceptions import StorageError, ConfigurationError

class NodeStorage:
    """Manages all node data across file system and Redis"""
    
    def __init__(self, redis_client: redis.Redis):
        self.redis = redis_client
        
    def load_network_config(self, filepath: str) -> Dict:
        """Load network config written by scanner"""
        try:
            with open(filepath) as f:
                network = json.load(f)
                # Store network info in Redis for node access
                self.redis.set('pack', json.dumps(network['local']))
                self.redis.set('peers', json.dumps(network.get('peers', {})))
                return network
        except (IOError, json.JSONDecodeError) as e:
            raise ConfigurationError(f"Failed to load network config: {e}")
            
    def store_blockchain(self, chain: Any) -> None:
        """Store blockchain data"""
        try:
            self.redis.set('chain', str(chain))
        except redis.RedisError as e:
            raise StorageError(f"Failed to store blockchain: {e}")
            
    def get_blockchain(self) -> Any:
        """Get blockchain data"""
        try:
            data = self.redis.get('chain')
            return data.decode('utf-8') if data else None
        except redis.RedisError as e:
            raise StorageError(f"Failed to get blockchain: {e}")
            
    def update_peers(self, peers: Dict) -> None:
        """Update peer information"""
        try:
            self.redis.set('peers', json.dumps(peers))
        except redis.RedisError as e:
            raise StorageError(f"Failed to update peers: {e}") 
            
    def save_network_config(self, network: Dict) -> None:
        """Save network configuration from scanner"""
        try:
            with open("./photoblocks/network.json", "w") as f:
                json.dump(network, f, indent=2)
        except IOError as e:
            raise ConfigurationError(f"Failed to save network config: {e}") 

    def get_seeds(self) -> str:
        """Get seed node information"""
        try:
            data = self.redis.get('seeds')
            return data.decode('utf-8') if data else None
        except redis.RedisError as e:
            raise StorageError(f"Failed to get seeds: {e}")

    def get_peers(self) -> str:
        """Get peer information"""
        try:
            data = self.redis.get('peers')
            return data.decode('utf-8') if data else None
        except redis.RedisError as e:
            raise StorageError(f"Failed to get peers: {e}") 

    def get_pack(self) -> Dict:
        """Get node package information"""
        try:
            data = self.redis.get('pack')
            if not data:
                return None
            return json.loads(data.decode('utf-8'))
        except (redis.RedisError, json.JSONDecodeError) as e:
            raise StorageError(f"Failed to get pack: {e}") 