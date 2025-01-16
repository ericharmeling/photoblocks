import socket
import logging
from photoblocks.exceptions import NetworkError, ConsensusError, ValidationError, StorageError
import json


class ClientSock:
    """
    Client socket
    """

    def __init__(self, network, node, storage):
        self.storage = storage
        self.node = node
        
        # Initialize from storage
        try:
            self.seeds = json.loads(self.storage.get_seeds() or '{}')
            self.peers = json.loads(self.storage.get_peers() or '{}')
        except (json.JSONDecodeError, StorageError) as e:
            logging.error(f"Failed to initialize from storage: {e}")
            self.seeds = {}
            self.peers = {}

    def _parse_peers(self, peer_data):
        """Safely parse peer data"""
        try:
            return {
                peer: {int(port): values for port, values in ports.items()}
                for peer, ports in peer_data.items()
            }
        except (ValueError, AttributeError) as e:
            raise ValidationError(f"Invalid peer data format: {e}")

    def sync(self):
        """
        Updates peer list and blockchain. This function is run on a background thread.
        """
        if len(self.seeds) == 0:
            logging.info(
                f'\nNo seeds to validate data. You should add more seeds!')
        else:
            while True:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                    self.updatepeers(sock)
                    self.updatechain(sock)
        self.store()
        return

    def fetchseeds(self):
        """
        Returns seeds from initial scanner.
        """
        seeds = []
        ports = [7000, 7001]
        if self.node.port == 7000:
            ports = ports[1:]
        for ip in self.peers:
            for port in ports:
                if self.peers[ip][port] == 1:
                    logging.info(f'\nReading in scanned seed at {ip}:{port}.')
                    seeds.append((ip, port))
                else:
                    logging.info(f'\nNo seed found at {ip}:{port}.')
        if len(seeds) == 0:
            logging.info(
                f'\nThe data on this node has not been validated against other nodes. You should add more seeds!')
        return seeds

    def updatepeers(self, sock):
        """
        Updates the list of peer nodes on the network.
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
        """
        Updates the blockchain.
        """
        chains = {}
        valid_chains = 0
        
        for address in self.seeds:
            try:
                chain = self._fetch_chain(sock, address)
                if chain:
                    chains[address] = chain
                    valid_chains += 1
            except NetworkError as e:
                logging.warning(f"Failed to fetch chain from {address}: {e}")
                continue

        if not chains:
            raise ConsensusError("Unable to fetch chain from any seed nodes")
            
        return self._validate_chains(chains)

    def _fetch_chain(self, sock, address):
        """
        Fetches the blockchain from a seed node.
        """
        ip = address[0]
        port = address[1]
        try:
            logging.info(f'\nConnecting to seed node at {ip}:{port}...')
            sock.connect((ip, port))
            logging.info(f'\nConnected to node at {ip}:{port}.')
            sock.sendall('chain'.encode())
            logging.info(
                f'\nFetching blockchain from node at {ip}:{port}...')
            response = sock.recv(1024).decode()
            if response:
                return response
            else:
                logging.info(
                    f'\nNo response received from node at {ip}:{port}.')
                raise socket.error
        except socket.error as e:
            logging.info(
                f'\nError retrieving blockchain from node at {ip}:{port}.')
            logging.info(f'\n{e}.')
            raise NetworkError(f"Failed to fetch chain from {ip}:{port}: {e}")

    def _validate_chains(self, chains):
        """
        Validates the blockchain.
        """
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
        """Store node data using storage interface"""
        try:
            self.storage.store_blockchain(self.node.blockchain)
            self.storage.update_peers(self.peers)
            self.storage.update_seeds(self.seeds)
            pack = {
                "id": self.node.node_id,
                "ip": self.node.ip,
                "port": self.node.port
            }
            self.storage.update_pack(pack)
        except StorageError as e:
            logging.error(f"Failed to store node data: {e}")
            return
