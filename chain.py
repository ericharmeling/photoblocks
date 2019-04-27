# chain.py
# Defines Chain class, a data structure of linked blocks

import datetime
import geocoder
from block import Block
from images import image_match


class Chain:
    """
    The Chain class implements the blockchain: a list of linked blocks.
    """
    def __init__(self, directory="."):
        """
        Create instance of Chain class.
        """
        self.transactions = []
        self.last_labels = []
        self.nodes = []
        self.chain = []
        self.dir = directory
        gen_data = {"name": "The First Block", "sender": "God", "recipient": "Mankind", "quantity": 0}
        gen_location = str(geocoder.ip('me')[0])
        gen_image = []
        gen_label = "The Void"
        genesis = Block(0, datetime.datetime.now(), gen_location, gen_data, gen_image, gen_label, "0", ".")
        self.chain.append(genesis)

    @property
    def last_block(self):
        return self.chain[-1]

    # @staticmethod
    def proof_of_work(self, block):
        """
        Tries different nonce values until the hash meets the PoW requirements.
        If a unique image is provided, the PoW difficulty decreases.
        :param block: Candidate block.
        :return: Returns the matching nonce value.
        """

        new_block = block
        image_dir = self.dir

        print(f"Running image processor")
        if image_match(image_dir, new_block.image, new_block.label):
            new_hash = new_block.hash_block()
            print(f"Image matched!\n Starting simplified PoW...")
            while new_hash.startswith('0') is False:
                new_block.nonce += 1
                new_hash = new_block.hash_block()
                print(new_hash)
            return new_block.nonce
        else:
            print(f"No image match found\n Starting PoW...")
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
    def is_valid_hash(block):
        block_hash = block.hash_block()
        if block_hash.startswith('0') or block_hash.startswith('0'*4):
            return True

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
        Iterates through each block on the chain, hashing the block and its previous block to ensure that the chain is
        valid.
        :param chain: Chain to check
        :return: Returns True if chain is valid.
        """

        for block in chain:
            if not self.is_valid_hash(block) or block.last_hash != chain.last_block.hash_block():
                result = False

            else:
                result = True

        return result
