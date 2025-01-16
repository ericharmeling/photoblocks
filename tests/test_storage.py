import pytest
import redis
import json
from unittest.mock import Mock
from photoblocks.storage import NodeStorage
from photoblocks.exceptions import StorageError

@pytest.fixture
def mock_redis():
    mock = Mock(spec=redis.Redis)
    mock.get.return_value = b'{"test": "data"}'
    mock.set.return_value = True
    mock.execute_command.return_value = True
    return mock

@pytest.fixture
def storage(mock_redis):
    return NodeStorage(mock_redis)

def test_load_network_config(storage, tmp_path):
    # Create test network.json
    test_config = {
        "local": {"ip": "192.168.1.1", "port": 7000},
        "peers": {"192.168.1.2": {7001: 1}}
    }
    config_file = tmp_path / "network.json"
    config_file.write_text(json.dumps(test_config))
    
    # Test loading
    result = storage.load_network_config(str(config_file))
    assert result == test_config
    storage.redis.set.assert_called_with('pack', json.dumps(test_config['local']))

def test_store_blockchain(storage):
    test_chain = ["block1", "block2"]
    storage.store_blockchain(test_chain)
    storage.redis.set.assert_called_with('chain', str(test_chain))

def test_get_blockchain_missing(storage):
    storage.redis.get.return_value = None
    result = storage.get_blockchain()
    assert result is None

def test_redis_error_handling(storage):
    storage.redis.get.side_effect = redis.RedisError("Connection failed")
    with pytest.raises(StorageError):
        storage.get_blockchain()