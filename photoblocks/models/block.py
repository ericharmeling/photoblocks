# block.py
# Defines the Block class, a data structure for transactional data

import hashlib
import json


class Block:
    def __init__(self, index, timestamp, location, data, image, label, last_hash, nonce=0):
        self.index = index
        self.timestamp = str(timestamp)
        self.location = location
        self.data = data
        self.image = image
        self.label = label
        self.last_hash = last_hash
        self.nonce = nonce

    def hash_block(self):
        block = json.dumps(self.__dict__, sort_keys=True)
        return hashlib.sha3_256(block.encode()).hexdigest()
