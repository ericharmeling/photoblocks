import pytest
from unittest.mock import Mock, patch
from photoblocks.networking.serversock import serversock

@pytest.fixture
def mock_storage():
    storage = Mock()
    storage.get_pack.return_value = {"port": 7000}
    storage.get_blockchain.return_value = "test_chain"
    storage.get_peers.return_value = "test_peers"
    return storage

@patch('socket.socket')
def test_serversock_bind(mock_socket, mock_storage):
    mock_sock = Mock()
    # Make accept() raise an exception to break the server loop
    mock_sock.accept.side_effect = KeyboardInterrupt()
    mock_socket.return_value.__enter__.return_value = mock_sock
    
    with pytest.raises(KeyboardInterrupt):  # Now we expect KeyboardInterrupt specifically
        serversock(mock_storage)
    
    # Verify the server was set up correctly before the exception
    mock_sock.bind.assert_called_with(("", 7000))
    mock_sock.listen.assert_called_with(5)

@patch('socket.socket')
def test_serversock_handle_request(mock_socket, mock_storage):
    mock_sock = Mock()
    mock_peer = Mock()
    # Add context manager support to mock_peer
    mock_peer.__enter__ = Mock(return_value=mock_peer)
    mock_peer.__exit__ = Mock(return_value=None)
    
    mock_peer.recv.return_value = b'chain'
    mock_storage.get_blockchain.return_value = "test_chain"
    
    # Set up accept() to return our mock peer once, then raise an exception
    mock_sock.accept.side_effect = [(mock_peer, ('192.168.1.2', 7001)), KeyboardInterrupt()]
    mock_socket.return_value.__enter__.return_value = mock_sock

    with pytest.raises(KeyboardInterrupt):  # Should raise after handling one request
        serversock(mock_storage)

    mock_peer.send.assert_called_once_with(b"test_chain") 