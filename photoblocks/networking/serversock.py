import socket
import logging
import time
import redis


def serversock():
    """
    Broadcasts local node, peer, and blockchain data on network.
    """
    db = redis.Redis(host='redis', port=6379)
    if db.execute_command('PING'):
        pack = eval(db.get('pack').decode("utf-8"))
    else:
        logging.error(
            f'\nUnable to connect to local Redis server. Please restart the node.')
        return
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        logging.info('\nNode server socket open for connections.')
        try:
            sock.bind(("", pack["port"]))
            sock.listen(5)
            while True:
                try:
                    peer, address = sock.accept()
                    data = peer.recv(1024).decode()
                    if data:
                        if data == 'chain':
                            chain = db.get("chain").decode("utf-8")
                            peer.send(chain.encode())
                        elif data == 'pack':
                            pack = db.get("pack").decode("utf-8")
                            peer.send(pack.encode())
                        elif data == 'peerlist':
                            peerlist = db.get("peers").decode("utf-8")
                            peer.send(peerlist.encode())
                        elif data == 'ping':
                            peer.send('hello'.encode())
                    else:
                        time.sleep(5)
                        logging.info('\nNo client data received yet...')
                except Exception as e:
                    logging.info('\n{e}.')
                    peer.close()
                    continue
        except Exception as e:
            if e == socket.error and e.errno in (98,99):
                logging.info(
                    f'\n{pack["port"]} is already in use. You should reset the node port.')
            else:
                logging.info(f'\n{e}.')
            return
