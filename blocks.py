# blocks.py
# Defines Block class, a data structure for transactional data

import hashlib
import datetime
import geocoder
import json
from images import image_match


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


class Chain:
    """
    The Chain class implements the blockchain: a list of linked blocks.
    """

    def __init__(self):
        """
        Create instance of Chain class.
        """
        self.transactions = []
        self.last_labels = []
        self.chain = []
        gen_data = {"name": "The First Block", "sender": "God", "recipient": "Mankind", "quantity": 0}
        gen_location = str(geocoder.ip('me')[0])
        gen_image = []
        gen_label = "The Void"
        genesis = Block(0, datetime.datetime.now(), gen_location, gen_data, gen_image, gen_label, "0")
        self.chain.append(genesis)

    @property
    def last_block(self):
        return self.chain[-1]

    @staticmethod
    def proof_of_work(block):
        """
        Tries different nonce values until the hash meets the PoW requirements.
        If a unique image is provided, the PoW difficulty decreases.
        :param block: Candidate block.
        :return: Returns the matching nonce value.
        """

        new_block = block

        if image_match(new_block.image, new_block.label):
            new_hash = new_block.hash_block()

            while new_hash.startswith('0') is False:
                new_block.nonce += 1

            return new_block.nonce
        else:
            new_hash = new_block.hash_block()

            while new_hash.startswith('0' * 4) is False:
                new_block.nonce += 1

            return new_block.nonce

    def new_block(self, image, label, data="0", nonce=0):
        """
        Creates a new block with image, proof, and transaction data.
        :param image: The image of the proven block.
        :param label: The label of the image.
        :param nonce: The nonce selected for the proven block.
        :param data: The transactions of the proven block.
        :return: Returns the block.
        """
        index = len(self.chain) + 1
        timestamp = datetime.datetime.now()
        location = str(geocoder.ip('me')[0])
        last_hash = self.last_block.hash_block()
        block = Block(index, timestamp, location, data, image, label, last_hash, nonce)
        return block

    def add_block(self, block):
        """
        Adds new block to chain.
        :param block: Block to add to chain
        :return:
        """
        self.chain.append(block)

    @staticmethod
    def is_valid_hash(block, block_hash):
        return block_hash.startswith('0') and block_hash == block.hash_block()

    def add_transaction_fields(self, sender, recipient, quantity):
        """
        Add a new transaction with field data. The latest transaction data is placed in the data attribute of the latest
        block.
        :param sender: Specifies the sender.
        :param recipient: Specifies the recipient.
        :param quantity: Specifies the quantity.
        :return:
        """
        timestamp = datetime.datetime.now()
        data = {"sender": sender, "recipient": recipient, "quantity": quantity, "timestamp": timestamp}
        self.transactions.append(data)

    def add_transaction_data(self, data):
        """
        Add a new transaction from JSON data object. The latest transaction data is placed in the data attribute of the
        latest block.
        :param data: Specifies the data (JSON).
        :return:
        """
        data['timestamp'] = datetime.datetime.now()
        self.transactions.append(data)

    def is_valid_chain(self, chain):
        """
        Checks if chain is valid.
        :param chain: Chain to check
        :return: Returns True if chain is valid.
        """
        result = True
        last_hash = "0"

        for block in chain:
            block_hash = block.proof
            delattr(block, "proof")

            if not self.is_valid_hash(block, block.proof) or last_hash != block.last_hash:
                result = False
                break

        return result
