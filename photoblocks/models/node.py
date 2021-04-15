# node.py
# Defines the Node class, a data structure that represents a node
import socket
from photoblocks.models.chain import Chain
from uuid import uuid4
import time


class Node:
    def __init__(self, node_type):
        self.node_id = str(uuid4()).replace('-', '')
        self.node_key = str(uuid4()).replace('-', '')
        self.host = socket.gethostbyname(socket.gethostname())
        self.port = port
        if self.port == 7000:
            self.blockchain = Chain()
        else:
            self.blockchain = None

