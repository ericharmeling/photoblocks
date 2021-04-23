import hashlib
import json


class Block:
    """Represents a block in the blockchain.
    """

    def __init__(self, index, timestamp, data, image, label, last_hash, nonce=0):
        self.index = index
        self.timestamp = str(timestamp)
        self.data = data
        self.image = image
        self.label = label
        self.last_hash = last_hash
        self.nonce = nonce

    def hash_block(self):
        block = json.dumps(self.__dict__, sort_keys=True)
        return hashlib.sha3_256(block.encode()).hexdigest()
