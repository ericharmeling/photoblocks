import pytest
from unittest.mock import Mock
from photoblocks.networking.clientsock import ClientSock
from photoblocks.models.node import Node
from photoblocks.storage import NodeStorage

@pytest.fixture
def mock_storage():
    storage = Mock(spec=NodeStorage)
    storage.get_seeds.return_value = '{}'
    storage.get_peers.return_value = '{}'
    return storage

@pytest.fixture
def mock_node():
    node = Mock(spec=Node)
    node.node_id = 'test_id'
    node.ip = '192.168.1.1'
    node.port = 7000
    node.blockchain = ['block1']
    return node

@pytest.fixture
def client_sock(mock_storage, mock_node):
    network = {"local": {"ip": "192.168.1.1", "port": 7000}}
    return ClientSock(network, mock_node, mock_storage)

def test_client_sock_init(client_sock):
    assert client_sock.seeds == {}
    assert client_sock.peers == {}

def test_store_data(client_sock, mock_storage):
    # Configure all required mock methods
    mock_storage.update_seeds = Mock()
    mock_storage.update_pack = Mock()
    mock_storage.store_blockchain = Mock()
    mock_storage.update_peers = Mock()
    
    # Call the store method
    client_sock.store()
    
    # Verify all methods were called
    mock_storage.update_seeds.assert_called_once_with(client_sock.seeds)
    mock_storage.store_blockchain.assert_called_once()
    mock_storage.update_peers.assert_called_once()
    mock_storage.update_pack.assert_called_once()

def test_validate_chains(client_sock):
    chains = {
        "node1": ["block1", "block2"],
        "node2": ["block1", "block2"]
    }
    client_sock._validate_chains(chains)
    assert client_sock.node.blockchain == ["block1", "block2"] 