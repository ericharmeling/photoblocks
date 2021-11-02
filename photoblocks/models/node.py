import socket
from .chain import Chain
from uuid import uuid4
import time


class Node:
    """
    Represents a node on the network.
    """

    def __init__(self, address):
        self.node_id = str(uuid4()).replace('-', '')
        self.node_key = str(uuid4()).replace('-', '')
        self.ip = address[0]
        self.port = address[1]
        if self.port == 7000:
            self.blockchain = Chain()
        else:
            self.blockchain = None
