# node.py
# Defines the Node class, a data structure that represents a node
import socket
from models.chain import Chain
import logging
from uuid import uuid4
from networking.socks import ClientSock
import threading
import time


class Node:
    """
    Defines node objects.
    """
    def __init__(self, config):
        """
        Node class constructor.

        Args:
            config (dict): contains configuration information for node.
        """
        self.node_id = str(uuid4()).replace('-', '')
        self.node_key = str(uuid4()).replace('-', '')
        self.node_type = config["type"]
        self.node_store = config["store"]
        self.seedports = config["seedports"]
        self.host = socket.gethostbyname("")
        self.port = None
        self.dbport = None

        if self.node_type == 'head':
            self.blockchain = Chain()
            self.port = 6000
        else:
            self.blockchain = self.getchain(self.seedlist)
            if self.node_type == 'seed':
                for port in self.seedports:
                    if port in self.seedlist:
                        logging.info(
                            f'Seed port {port} in use. Looking for other ports.')
                    else:
                        logging.info(
                            f'Seed port {port} is open. Promoting to seed node at port {port}.')
                        self.port = port
                if not self.port:
                    logging.info(
                        'No seed port is open. Demoting to full node.')
                    self.setport()
                    logging.info(
                        f'Full node now listening at {self.port}.')
            else:
                self.setport()

        self.dbport = self.port+1000

        self.pack = {
            "type": self.node_type,
            "key": self.node_key,
            "id": self.node_id,
            "port": self.port
        }


# Class property functions

    @property
    def peerlist(self):
        """
        List of node packs.

        Returns:
            [type]: [description]
        """
        logging.info('Retrieving node packs from network.')
        sock = ClientSock(self)
        return sock.packs

    @property
    def seedlist(self):
        logging.info('Retrieving seed node information available on network.')
        sock = ClientSock(self)
        return sock.seeds

# Class methods

    def getchain(self, seeds):
        logging.info("Retrieving validated blockchain.")
        chain = ClientSock(self)
        return chain

    def setport(self):
        if self.port == None:
            ports = []
            for peer in self.peerlist:
                ports.append(peer["peer"])
            port = ports[-1]+1
            self.port = port
        else:
            logging.info(f'Port already set to {self.port}.')

