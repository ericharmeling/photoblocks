# block.py
# Defines Block class, a data structure for transactional data

import hashlib
import json


class Block:
    """
    The Block class contains transactional data.
    """

    def __init__(self, index, timestamp, location, data, image, label, last_hash, nonce=0):
        """
        Create instance of Block class.
        :param index: The index for the block.
        :param timestamp: The time and date the block was created.
        :param location: The geolocation of the block's creation. This is specified as City, State/Province, Country.
        :param data: The transactional data associated with the block.
        :param image: The image on the block.
        :param label: The image label.
        :param last_hash: The hash of the previous block in the chain.
        """
        self.index = index
        self.timestamp = timestamp
        self.location = location
        self.data = data
        self.image = image
        self.label = label
        self.last_hash = last_hash
        self.nonce = nonce

    def hash_block(self):
        """
        Run hash algorithm on block object to create fingerprint.
        :return: Returns the block's hash key.
        """
        block = json.dumps(self.__dict__, sort_keys=True)
        return hashlib.sha3_256(block.encode()).hexdigest()
