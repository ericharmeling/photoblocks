import socket
import logging
import time
import threading

class ClientSock:
    def __init__(self, node, seedports, db):
        self.node = node
        self.seedports = seedports
        self.seeds = []
        self.peers = []
        self.db = db

        self.sync()


    def sync(self):
        while True:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                self.setseeds(sock)
                self.setpeers(sock)
                self.setchain(sock)
            self.store()
        


    def setseeds(self, sock):
        for port in self.seedports:
            if self.node.port == port:
                if self.node.port not in self.seedports:
                    self.seeds.append(port)
                continue
            else:
                try:
                    logging.info(
                        f'\nLooking for seed node on port {port}...')
                    sock.connect((self.node.host, port))
                    sock.sendall('ping'.encode())
                    response = sock.recv(1024).decode()
                    if response:
                        logging.info(
                        f'\nFound node on port {port}.')
                        self.seeds.extend(port)
                    else:
                        logging.info(f'\nError connecting to node on port {port}.')
                        raise socket.error
                except socket.error as e:
                    logging.info(
                        f'\nError retrieving peer information from seed port {port}.')
                    logging.info(f'\n{e}.')
                    continue
        logging.info(
                f'\n{len(self.seeds)} seed nodes detected on the network.')
        if len(self.seeds) == 1:
            logging.info(
                f'\nNote that the data on this node has not been validated against other nodes. You should add more seeds!')    
        return


    def setpeers(self, sock):
        seed_peerlist = {}
        if self.peers:
            seed_peerlist[self.node.port] = self.peers
        for port in self.seeds:
            if self.node.port == port:
                continue
            else:
                try:
                    logging.info(
                        f'\nConnecting to seed node on port {port}...')
                    sock.connect((self.node.host, port))
                    logging.info(
                        f'\nConnected to seed node on port {port}.')
                    sock.sendall('peerlist'.encode())
                    logging.info(
                        f'\nFetching peer list from seed node on port {port}...')
                    response = sock.recv(1024).decode()
                    if response:
                        seed_peerlist[port] = response
                    else:
                        logging.info(f'\nNo response received from node on port {port}.')
                        raise socket.error
                except socket.error as e:
                    logging.info(
                        f'\nError retrieving pack information from seed port {port}.')
                    logging.info(f'\n{e}.')
                    continue
        if len(seed_peerlist) == 0:
            logging.info(
                f'\nNo peers detected. Add some!')
        elif len(seed_peerlist) == 1:
            if self.peers:
                return
            else:
                logging.info(
                f'\nUsing peerlist from node at port {list(seed_peerlist.keys())[0][0]}.')
                self.peers = list(seed_peerlist.values())[0][0]
        else:
            for n in range(len(seed_peerlist)):
                try:
                    peerlist = list(seed_peerlist.values())[0][n]
                    if peerlist == list(seed_peerlist.values())[0][n-1]:
                        self.peers = peerlist
                        return
                    else:
                        continue
                except TypeError:
                    peerlists = list(seed_peerlist.values())
                    self.peers = peerlists[peerlists.index(max(peerlists))]
                    return


    def setport(self, sock):
        if self.node.node_type == 'seed':
            port = self.node.seeds[-1]+1
        elif self.peers:
            port = self.peers[-1]+1
        else:
            port = self.seedlist[-1]+1
        while True:
            try: 
                logging.info(f'\Checking port {port}...')
                sock.connect((self.node.host, port))
                sock.sendall('ping'.encode())
                response = sock.recv(1024).decode()
                if response:
                    logging.info(
                        f'\nNode already serving at port {port}.')
                    port = port+1
                else:
                    logging.info(f'\nNo response received from node at port {port}.')
                    raise socket.error
            except socket.error:
                logging.info(f'Port {port} free.')
                self.node.port = port
                return


    def setchain(self, sock):
        chainlist = {}
        for port in self.seeds:
            if self.node.port == port:
                if self.node.blockchain:
                    chainlist[port] = self.node.blockchain
                continue
            else:
                try:
                    logging.info(
                        f'\nConnecting to seed node on port {port}...')
                    sock.connect((self.node.host, port))
                    logging.info(
                        f'\nConnected to seed node on port {port}.')
                    sock.sendall('chain'.encode())
                    logging.info(
                        f'\nFetching blockchain from seed node on port {port}...')
                    response = sock.recv(1024).decode()
                    if response:
                        chainlist[port] = response
                    else:
                        logging.info(f'\nNo response received from node on port {port}.')
                        raise socket.error
                except socket.error as e:
                    logging.info(
                        f'\nError retrieving blockchain from seed port {port}.')
                    logging.info(f'\n{e}.')
                    continue
        if len(chainlist) == 1:
            if not self.node.blockchain:
                logging.info(f'\nOnly the head node has a blockchain. Using the head node blockchain.')
                self.node.blockchain = list(chainlist.values())[0][0]
                return
            else:
                return
        else:
            for n in range(len(chainlist)):
                try:
                    chain = list(chainlist.values())[0][n]
                    if chain == list(chainlist.values())[0][n-1]:
                        logging.info(f'\nBlockchain validated.')
                        self.node.blockchain = chain
                        return
                    else:
                        continue
                except TypeError:
                    allchains = list(chainlist.values())
                    self.node.blockchain = allchains[allchains.index(max(allchains))]
                    return


    def store(self):
        self.db.set("seeds", str(self.seeds))
        self.db.set("peers", str(self.peers))
        self.db.set("chain", str(self.node.blockchain))
        pack = {
            "type": self.node.node_type,
            "id": self.node.node_id,
            "host": self.node.host,
            "port": self.node.port
        }
        self.db.set('pack', str(pack))


class ServerSock:
    def __init__(self, db):
        self.broadcast(db)


    def broadcast(self, db):
        pack = db.get("pack")
        print(pack)
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
                        return False
            except socket.error as e:
                    if e.errno == 98:
                        logging.info(
                            f'\n{self.node.port} is already in use. You should reset the node port')
                    return False
