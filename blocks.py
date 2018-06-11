import hashlib
import datetime
import geocoder
import json
from images import image_match

class Block:
    """
    The Block class contains transactional data.
    """
    def __init__(self, index, timestamp, location, data, image, last_hash, proof):
        """
        Create instance of Block class.
        :param index: The index for the block.
        :param timestamp: The time and date the block was created.
        :param location: The geolocation of the block's creation. This is specified as City, State/Province, Country.
        :param data: The transactional data associated with the block.
        :param last_hash: The hash of the previous block in the chain.
        """
        self.index = index
        self.timestamp = timestamp
        self.location = location
        self.data = data
        self.image = image
        self.last_hash = last_hash
        self.proof = proof
        self.nonce = 0

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
        self.chain = []
        gen_data = {"name": "The First Block", "sender": "God", "recipient": "Mankind", "quantity": 0}
        gen_location = str(geocoder.ip('me')[0])
        gen_image = []
        genesis = Block(0, datetime.datetime.now(), gen_location, gen_data, gen_image, "0", "0")
        self.chain.append(genesis)

    @property
    def last_block(self):
        return self.chain[-1]

    @staticmethod
    def proof_of_work(block, target_image):
        """
        Tries different nonce values until the hash matches.
        :param block: block object
        :param target_image: Image to match with photo.
        :return: Returns matching hash.
        """

        this_hash = block.hash_block()
        while this_hash.startswith('0'):
            block.nonce += 1
            this_hash = block.hash_block()

        if image_match(block.image, target_image):
            return this_hash

    def add_block(self, proof, image, data="0"):
        """
        Add new block to chain.
        :return: Returns the block added.
        """
        index = len(self.chain) + 1
        timestamp = datetime.datetime.now()
        location = str(geocoder.ip('me')[0])
        last_hash = self.last_block.hash_block()
        block = Block(index, timestamp, location, data, image, last_hash, proof)
        self.chain.append(block)
        return block

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
        data = {"sender": sender, "recipient": recipient, "quantity": quantity}
        self.transactions.append(data)

    def add_transaction_data(self, data):
        """
        Add a new transaction from JSON data object. The latest transaction data is placed in the data attribute of the
        latest block.
        :param data: Specifies the data (JSON).
        :return:
        """
        self.transactions.append(data)

    def is_valid_chain(self, chain):
        """
        Checks if chain is valid. Might not be needed.
        :param chain:
        :return:
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
