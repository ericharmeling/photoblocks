import socket
import logging


class ClientSock:
    """Client socket
    """

    def __init__(self, network, node, db):
        self.node = node
        self.network = network
        self.db = db
        self.peers = network["peers"]
        self.seeds = self.fetchseeds()

        self.sync()

    def sync(self):
        """Updates peer list and blockchain. This function is run on a background thread.
        """
        if len(self.seeds) is 0:
            logging.info(
                f'\nNo seeds to validate data. You should add more seeds!')
            return
        else:
            while True:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                    self.updatepeers(sock)
                    self.updatechain(sock)
                self.store()

    def fetchseeds(self):
        """Returns seeds from initial scanner.
        """
        seeds = []
        ports = [7000, 7001]
        if self.node.port == 7000:
            ports = ports[1:]
        for ip in self.network["peers"]:
            for port in ports:
                if self.network["peers"][ip][port] is 1:
                    logging.info(f'\nReading in scanned seed at {ip}:{port}.')
                    seeds.append((ip, port))
                else:
                    logging.info(f'\nNo seed found at {ip}:{port}.')
        if len(seeds) is 0:
            logging.info(
                f'\nThe data on this node has not been validated against other nodes. You should add more seeds!')
        return seeds

    def updatepeers(self, sock):
        """Updates the list of peer nodes on the network.
        """
        seed_peerlist = {}
        for address in self.seeds:
            ip = address[0]
            port = address[1]
            try:
                logging.info(f'\nConnecting to seed node at {ip}:{port}...')
                sock.connect((ip, port))
                logging.info(f'\nConnected to node at {ip}:{port}.')
                sock.sendall('peerlist'.encode())
                logging.info(
                    f'\nFetching peer list from node at {ip}:{port}...')
                response = sock.recv(1024).decode()
                if response:
                    seed_peerlist[address] = response
                else:
                    logging.info(
                        f'\nNo response received from node at {ip}:{port}.')
                    raise socket.error
            except socket.error as e:
                logging.info(
                    f'\nError retrieving pack information from node at {ip}:{port}.')
                logging.info(f'\n{e}.')
                continue
        if len(seed_peerlist) == 0:
            logging.info(
                f'\nUnable to fetch data from existing seed nodes. Try again!')
            return
        else:
            last_peerlist = None
            for peerlist in seed_peerlist:
                if self.peers == peerlist:
                    logging.info(
                        f'\nLocal peerlist validated against seed node peerlist.')
                    break
                elif last_peerlist and peerlist == last_peerlist:
                    logging.info(
                        f'\nSeed peerlist validated against seed node peerlist.')
                    self.peers = peerlist
                    break
                last_peerlist = peerlist

    def updatechain(self, sock):
        """Updates the blockchain.
        """
        chains = {}
        for address in self.seeds:
            ip = address[0]
            port = address[1]
            try:
                logging.info(f'\nConnecting to seed node at {ip}:{port}...')
                sock.connect((self.node.host, port))
                logging.info(f'\nConnected to node at {ip}:{port}.')
                sock.sendall('chain'.encode())
                logging.info(
                    f'\nFetching blockchain from node at {ip}:{port}...')
                response = sock.recv(1024).decode()
                if response:
                    chains[address] = response
                else:
                    logging.info(
                        f'\nNo response received from node at {ip}:{port}.')
                    raise socket.error
            except socket.error as e:
                logging.info(
                    f'\nError retrieving blockchain from node at {ip}:{port}.')
                logging.info(f'\n{e}.')
                continue
        if len(chains) == 0:
            logging.info(
                f'\nUnable to fetch data from existing seed nodes. Try again!')
            return
        else:
            for n in range(len(chains)):
                chain = list(chains.values())[n]
                if chain == list(chains.values())[n-1]:
                    logging.info(f'\nBlockchain validated.')
                    self.node.blockchain = chain
                    return
                else:
                    continue
            allchains = list(chains.values()).append(self.node.blockchain)
            self.node.blockchain = allchains[allchains.index(
                max(allchains))]
            return

    def store(self):
        """Stores seeds, peers, and blockchain data on a local Redis server.
        """
        self.db.set("seeds", str(self.seeds))
        self.db.set("peers", str(self.peers))
        self.db.set("chain", str(self.node.blockchain))
        pack = {
            "id": self.node.node_id,
            "ip": self.node.ip,
            "port": self.node.port
        }
        self.db.set('pack', str(pack))
