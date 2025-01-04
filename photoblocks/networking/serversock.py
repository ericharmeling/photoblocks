import socket
import logging
import time
import redis
from photoblocks.exceptions import StorageError, NetworkError, ValidationError


def serversock():
    """
    Broadcasts local node, peer, and blockchain data on network.
    
    Raises:
        StorageError: If Redis connection fails
        NetworkError: If socket operations fail
        ValidationError: If data validation fails
    """
    try:
        db = redis.Redis(host='redis', port=6379)
        if not db.execute_command('PING'):
            raise StorageError("Unable to connect to local Redis server")
        
        pack = eval(db.get('pack').decode("utf-8"))
        if not pack:
            raise ValidationError("Invalid or missing pack data")

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            logging.info('Node server socket open for connections.')
            try:
                sock.bind(("", pack["port"]))
                sock.listen(5)
                
                while True:
                    try:
                        peer, address = sock.accept()
                        with peer:  # Ensure socket gets closed
                            data = peer.recv(1024).decode()
                            if not data:
                                time.sleep(5)
                                logging.info('No client data received yet...')
                                continue

                            if data not in ['chain', 'pack', 'peerlist', 'ping']:
                                raise ValidationError(f"Invalid request type: {data}")

                            try:
                                response = {
                                    'chain': lambda: db.get("chain"),
                                    'pack': lambda: db.get("pack"),
                                    'peerlist': lambda: db.get("peers"),
                                    'ping': lambda: 'hello'.encode()
                                }[data]()
                                
                                if not response and data != 'ping':
                                    raise StorageError(f"Missing {data} data in storage")
                                    
                                peer.send(response if isinstance(response, bytes) else response.decode("utf-8").encode())
                                
                            except redis.RedisError as e:
                                raise StorageError(f"Redis error while fetching {data}: {e}")
                                
                    except (socket.error, ValidationError, StorageError) as e:
                        logging.error(f"Connection error: {e}")
                        continue
                        
            except socket.error as e:
                if e.errno in (98, 99):
                    raise NetworkError(f"Port {pack['port']} already in use")
                raise NetworkError(f"Socket error: {e}")
                
    except Exception as e:
        logging.error(f"Critical server error: {e}")
        raise
