import pytest
from unittest.mock import patch, Mock
from photoblocks.networking.scanner import validate_node_type, get_local_ip, scan_network
from photoblocks.exceptions import ValidationError

def test_validate_node_type_valid():
    assert validate_node_type('head') == 'head'
    assert validate_node_type('seed') == 'seed'
    assert validate_node_type('full') == 'full'

def test_validate_node_type_invalid():
    with pytest.raises(ValidationError):
        validate_node_type('invalid')

@patch('socket.socket')
def test_get_local_ip(mock_socket):
    mock_sock = Mock()
    mock_sock.getsockname.return_value = ('192.168.1.1', 0)
    mock_socket.return_value.__enter__.return_value = mock_sock
    
    assert get_local_ip() == '192.168.1.1'

@patch('photoblocks.networking.scanner.arping')
def test_scan_network(mock_arping):
    # Create specific mock objects before the function call
    mock_answered = [Mock()]
    mock_unanswered = Mock()
    mock_arping.return_value = (mock_answered, mock_unanswered)
    
    result = scan_network('192.168.1.1')
    
    # Verify the function call
    mock_arping.assert_called_once_with('192.168.1.1')
    
    # Verify we got back the same tuple we passed in
    assert result == (mock_answered, mock_unanswered) 