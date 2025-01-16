import socket
import logging
import time
from photoblocks.exceptions import StorageError, NetworkError, ValidationError


def serversock(storage):
    """Broadcasts local node, peer, and blockchain data on network."""
    try:
        # Get pack data for binding
        pack_data = storage.get_pack()
        if not pack_data:
            raise ValidationError("Invalid or missing pack data")

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            logging.info('Node server socket open for connections.')
            sock.bind(("", pack_data["port"]))
            sock.listen(5)
            
            while True:
                try:
                    peer, _ = sock.accept()
                    with peer:
                        data = peer.recv(1024).decode()
                        if not data:
                            logging.info('No client data received yet...')
                            continue

                        if data not in ['chain', 'pack', 'peerlist', 'ping']:
                            raise ValidationError(f"Invalid request type: {data}")

                        response = {
                            'chain': storage.get_blockchain,
                            'pack': storage.get_pack,
                            'peerlist': storage.get_peers,
                            'ping': lambda: 'hello'
                        }[data]() # dispatch table
                        
                        if response is None and data != 'ping':
                            raise StorageError(f"Missing {data} data in storage")
                            
                        # Convert response to string if needed
                        if not isinstance(response, (str, bytes)):
                            response = str(response)
                            
                        # Ensure we're sending bytes
                        peer.send(response.encode() if isinstance(response, str) else response)
                        
                except Exception as e:
                    logging.error(f"Error handling peer request: {e}")
                    continue
                    
    except Exception as e:
        raise NetworkError(f"Server socket error: {e}")
