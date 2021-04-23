import socket
import logging
import time


def serversock(self, db):
    """Broadcasts local node, peer, and blockchain data on network.
    """
    pack = db.get("pack")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        logging.info('\nNode server socket open for connections.')
        try:
            sock.bind((pack.host, pack.port))
            sock.listen(5)
            while True:
                try:
                    peer, address = sock.accept()
                    data = peer.recv(1024).decode()
                    if data:
                        if data == 'chain':
                            chain = db.get("chain")
                            peer.send(chain.encode())
                        elif data == 'pack':
                            pack = db.get("pack")
                            peer.send(pack.encode())
                        elif data == 'peerlist':
                            peerlist = db.get("peers")
                            peer.send(peerlist.encode())
                        elif data == 'ping':
                            peer.send('hello'.encode())
                    else:
                        time.sleep(5)
                        logging.info('\nNo client data received yet...')
                except Exception as e:
                    logging.info('\n{e}.')
                    peer.close()
                    return
        except socket.error as e:
            if e.errno == 98:
                logging.info(
                    f'\n{pack.port} is already in use. You should reset the node port')
            return
