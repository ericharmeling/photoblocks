import hashlib
import datetime
import geocoder
import subprocess
import json

class Block:
    """
    The Block class contains transactional data.
    """
    def __init__(self, index, timestamp, location, data, last_hash):
        """
        Create instance of Block class.
        :param index: The index for the block.
        :param timestamp: The time and date the block was created.
        :param location: The geolocation of the block. This is specified as City, State/Province, Country.
        :param data: The transactional data associated with the block.
        :param last_hash: The hash of the previous block in the chain.
        """
        self.index = index
        self.timestamp = timestamp
        self.location = location
        self.data = data
        self.last_hash = last_hash

    def hash_block(self):
        """
        Run hash algorithm on block object to create fingerprint.
        :return: Returns the block's hash key.
        """
        block = json.dumps(self.__dict__, sort_keys=True)
        return hashlib.sha3_256(block.encode()).hexdigest()

class Genesis(Block):
    """
    The Genesis class inherits from the Block class and defines the Genesis Block.
    """
    def __init__(self):
        """
        Create instance of Genesis class.
        """
        self.index = 0
        self.timestamp = datetime.datetime.now()
        self.data = {"name": "The First Block", "sender": "God", "recipient": "Mankind", "quantity": 0}
        self.location = str(geocoder.ip('me')[0])
        self.last_hash = "0"

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
        genesis = Genesis()
        self.chain.append(genesis)

    @property
    def last_block(self):
        return self.chain[-1]

    def proof_of_work(self, block):
        """
        Tries different nonce values until the hash matches.
        :param block: block object
        :return: Returns matching hash.
        """
        block.nonce = 0

        this_hash = block.hash_block()
        while this_hash.startswith('0')
            block.nonce += 1
            this_hash = block.hash_block()

        return this_hash

    def add_block(self):
        """
        Add new block to chain.
        :return: Returns the block added.
        """
        index = len(self.chain) + 1
        timestamp = datetime.datetime.now()
        location = str(geocoder.ip('me')[0])
        data = self.transactions[index]
        last_hash = self.last_block.hash
        block = Block(index, timestamp, data, location, last_hash)
        block.hash = block.hash_block()
        self.chain.append(block)
        return block

    def is_valid_hash(self, block, block_hash):
        return block_hash.startswith('0') and block_hash == block.hash_block()

    def add_transaction_fields(self, sender, recipient, quantity):
        """
        Add a new transaction with field data. The latest transaction data is placed in the data attribute of the latest block.
        :param sender: Specifies the sender.
        :param recipient: Specifies the recipient.
        :param quantity: Specifies the quantity.
        :return:
        """
        data = {"sender": sender, "recipient": recipient, "quantity": quantity}
        self.transactions.append(data)

    def add_transaction_data(self, data):
        """
        Add a new transaction from JSON data. The latest transaction data is placed in the data attribute of the latest block.
        :param data: Specifies the data (JSON).
        :return:
        """
        self.transactions.append(data)

    @classmethod
    def is_valid_chain(cls, chain):
        result = True
        last_hash = "0"

        for block in chain:
            block_hash = block.hash
            delattr(block, "hash")

            if not cls.is_valid_hash(block, block.hash) or last_hash != block.last_hash:
                result = False
                break

            block.hash, last_hash = block_hash, block_hash

        return result


    @staticmethod
    def image_match(file, target):
        """
        :param file: Input image file
        :param target: Target image category
        :return: True if image from file matches image category, False if not.
        """
        image = subprocess.run(["models/tutorials/image/imagenet/classify_image.py", "--image-file" + file])
        return image == target
