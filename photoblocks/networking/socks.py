import socket
import logging
import time
import threading

class ClientSock:
    def __init__(self, network, node, db):
        self.node = node
        self.network = network
        self.db = db
        self.peers = network["peers"]
        self.seeds = self.setseeds()

        self.sync()


    def sync(self):
        if len(self.seeds) is 0:
            logging.info(f'\nNo seeds to validate data. You should add more seeds!')  
            return
        else:
            while True:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                    self.updatepeers(sock)
                    self.updatechain(sock)
                self.store()
        


    def setseeds(self):
        seeds = []
        ports = [7000, 7001]
        if self.node.port == 7000:
            ports = ports[1:]
        for ip in self.network["peers"]:
            for port in ports:
                if self.network["peers"][ip][port] is 1:
                    logging.info(f'\nReading in scanned seed at {ip}:{port}.')
                    seeds.extend((ip,port))
                else:
                    logging.info(f'\nNo seed found at {ip}:{port}.')
        if len(seeds) is 0:
            logging.info(f'\nThe data on this node has not been validated against other nodes. You should add more seeds!')    
        return seeds


    def updatepeers(self, sock):
        seed_peerlist = {}
        for address in self.seeds:
            ip = address[0]
            port = address[1]
            try:
                logging.info(f'\nConnecting to seed node at {ip}:{port}...')
                sock.connect((ip, port))
                logging.info(f'\nConnected to node at {ip}:{port}.')
                sock.sendall('peerlist'.encode())
                logging.info(f'\nFetching peer list from node at {ip}:{port}...')
                response = sock.recv(1024).decode()
                if response:
                    seed_peerlist[address] = response
                else:
                    logging.info(f'\nNo response received from node at {ip}:{port}.')
                    raise socket.error
            except socket.error as e:
                logging.info(f'\nError retrieving pack information from node at {ip}:{port}.')
                logging.info(f'\n{e}.')
                continue
        if len(seed_peerlist) == 0:
            logging.info(f'\nUnable to fetch data from existing seed nodes. Try again!')
            return
        else:
            last_peerlist = None
            for peerlist in seed_peerlist:
                if self.peers == peerlist:
                    logging.info(f'\nLocal peerlist validated against seed node peerlist.')
                    break
                elif last_peerlist and peerlist == last_peerlist:
                    logging.info(f'\nSeed peerlist validated against seed node peerlist.')
                    self.peers = peerlist
                    break
                last_peerlist = peerlist


    def updatechain(self, sock):
        chainlist = {}
        for address in self.seeds:
            ip = address[0]
            port = address[1]
            try:
                logging.info(f'\nConnecting to seed node at {ip}:{port}...')
                sock.connect((self.node.host, port))
                logging.info(f'\nConnected to node at {ip}:{port}.')
                sock.sendall('chain'.encode())
                logging.info(f'\nFetching blockchain from node at {ip}:{port}...')
                response = sock.recv(1024).decode()
                if response:
                    chainlist[address] = response
                else:
                    logging.info(f'\nNo response received from node at {ip}:{port}.')
                    raise socket.error
            except socket.error as e:
                logging.info(f'\nError retrieving blockchain from node at {ip}:{port}.')
                logging.info(f'\n{e}.')
                continue
        if len(chainlist) == 0:
            logging.info(f'\nUnable to fetch data from existing seed nodes. Try again!')
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
