import hashlib
import datetime
import geocoder

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
        hash = hashlib.sha3_256()
        hash.update(str(self.index) +
                   str(self.timestamp) +
                   str(self.location) +
                   str(self.data) +
                   str(self.previous_hash))
        return hash.hexdigest()

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

    def add_block(self):
        """
        Add new block to chain.
        :return: Returns the block added.
        """
        index = len(self.chain) + 1
        timestamp = datetime.datetime.now()
        location = str(geocoder.ip('me')[0])
        data = self.transactions[index]
        last_hash = self.chain[-1]
        block = Block(index, timestamp, data, location, last_hash)
        self.chain.append(block)
        return block

    def transaction(self, sender, recipient, quantity):
        """
        Create a new transaction. The latest transaction data is placed in the data attribute of the latest block.
        :param sender: Specifies the sender.
        :param recipient: Specifies the recipient.
        :param quantity: Specifies the quantity.
        :return:
        """
        data = {"sender": sender, "recipient": recipient, "quantity": quantity}
        self.transactions.append(data)