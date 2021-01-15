# block.py
# Defines the Block class, a data structure for transactional data

import hashlib
import json


class Block:
    """
    The Block class contains transactional data.
    """
    def __init__(self, index, timestamp, location, data, image, label, last_hash, nonce=0):
        """
        Creates an instance of the Block class.
        :param index: The index for the block.
        :param timestamp: The time and date the block was created.
        :param location: The geolocation of the block's creation.
        :param data: The transactional data associated with the block.
        :param image: The encoded image on the block.
        :param label: The image label.
        :param last_hash: The hash of the previous block in the chain.
        :param nonce: The nonce of the block.
        """
        self.index = index
        self.timestamp = str(timestamp)
        self.location = location
        self.data = data
        self.image = image
        self.label = label
        self.last_hash = last_hash
        self.nonce = nonce

    def hash_block(self):
        """
        Runs a hash algorithm on block object to create fingerprint.
        :return: Returns the block's hash key.
        """
        block = json.dumps(self.__dict__, sort_keys=True)
        return hashlib.sha3_256(block.encode()).hexdigest()
