import socket
import logging
import time

class ClientSock:
    def __init__(self, node):
        self.seeds = []
        self.packs = []
        self.chain = []
        self.node = node

        self.sync(node)

    def sync(self, node):
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                for port in node.seedports:
                    try:
                        sock.connect((node.host, port))
                        logging.info(
                            f'Connecting to seed node on port {port}...')
                        sock.sendall('ping'.encode())
                        response = sock.recv(1024).decode()
                        if response:
                            logging.info(
                                f'Connected to seed node on port {port}.')
                            self.seeds.append(port)
                            logging.info(
                            f'Retrieving packs from seed node on port {port}.')
                            self.setpacks(sock, port)
                            self.setchain(sock, port)
                        else:
                            logging.info(f'Error connecting to seed node on port {port}.')
                    except Exception:
                        logging.info(
                            f'Error retrieving pack information from seed port {port}.')


    def setpacks(self, sock, port):
        packs = None
        logging.info(
            f'Retrieving packs from seed node on port {port}.')
        sock.sendall('packs'.encode())
        response = sock.recv(1024).decode()
        if response:
            packs = response
            if not self.packs:
                self.packs = packs
            elif self.packs == packs:
                logging.info(
                    f'Packs on node at port {port} validated against existing seed node.')
                return
            else:
                logging.info(
                    f'Packs on node at port {port} not valid. Restarting pack collection.')
                return self.sync()

    def setchain(self, sock, port):
        chain = None
        sock.sendall('chain'.encode())
        response = sock.recv(1024).decode()
        if response:
            chain = response
            if not self.chain:
                self.chain = chain
            elif self.chain == chain:
                logging.info(
                    f'Chain on node at port {port} validated against existing seed node.')
                return
            else:
                logging.info(
                    f'Chain on node at port {port} not valid. Restarting chain collection.')
                return self.sync()

def serversock(node):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        logging.info('Node server socket open for connections.')
        sock.bind((node.host, node.port))
        sock.listen(5)
        while True:
            try:
                peer, address = sock.accept()
                data = peer.recv(1024).decode()
                if data:
                    if data != 'chain':
                        peer.send(node.pack.encode())
                    else:
                        peer.send(node.blockchain.encode())
                else:
                    time.sleep(5)
                    logging.info('No client data received yet...')
            except:
                peer.close()
                return False