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
            try:
                sock.bind(("", pack_data["port"]))
                sock.listen(5)
                
                while True:
                    try:
                        peer, _ = sock.accept()
                        with peer:
                            data = peer.recv(1024).decode()
                            if not data:
                                time.sleep(5)
                                logging.info('No client data received yet...')
                                continue

                            if data not in ['chain', 'pack', 'peerlist', 'ping']:
                                raise ValidationError(f"Invalid request type: {data}")

                            try:
                                response = {
                                    'chain': lambda: storage.get_blockchain(),
                                    'pack': lambda: storage.get_pack(),
                                    'peerlist': lambda: storage.get_peers(),
                                    'ping': lambda: 'hello'.encode()
                                }[data]()
                                
                                if not response and data != 'ping':
                                    raise StorageError(f"Missing {data} data in storage")
                                    
                                peer.send(response if isinstance(response, bytes) else response.encode())
                                
                            except StorageError as e:
                                logging.error(f"Storage error while fetching {data}: {e}")
                                continue
                                
                    except Exception as e:
                        logging.error(f"Error handling peer request: {e}")
                        continue
                        
            except Exception as e:
                raise NetworkError(f"Socket error: {e}")
                
    except Exception as e:
        raise NetworkError(f"Server socket error: {e}")
