import pytest
import falcon
from falcon import testing
from unittest.mock import Mock
from photoblocks.servers.resources import PackResource, PeerResource
from unittest.mock import patch

@pytest.fixture
def mock_storage():
    storage = Mock()
    storage.get_pack.return_value = {"port": 7000}
    storage.get_blockchain.return_value = "test_chain"
    storage.get_peers.return_value = "test_peers"
    return storage

@pytest.fixture
def client(mock_storage):
    app = falcon.API()
    mock_pack = {"id": "test_id", "ip": "192.168.1.1", "port": 7000}
    
    app.add_route('/pack', PackResource(pack=mock_pack, db=mock_storage))
    app.add_route('/nodes', PeerResource(pack=mock_pack, db=mock_storage))
    app.add_route('/nodes/{id}', PeerResource(pack=mock_pack, db=mock_storage))
    
    return testing.TestClient(app)

def test_get_pack(client):
    response = client.simulate_get('/pack')
    assert response.status_code == 200
    assert response.json == {"id": "test_id", "ip": "192.168.1.1", "port": 7000}

@patch('photoblocks.servers.resources.PeerResource._safe_db_get')
def test_get_peers(mock_safe_db_get, client):
    # Mock the direct method that's being called
    mock_safe_db_get.return_value = '{"peers": []}'
    
    response = client.simulate_get('/nodes')
    assert response.status_code == 200
    assert response.json == {"peers": []}

def test_register_peer(client):
    peer_data = {"id": "peer1", "ip": "192.168.1.2", "port": 7001}
    response = client.simulate_post('/nodes', json=peer_data)
    assert response.status_code == 201 