import datetime
from .block import Block
from models.image import Image
import logging


class Chain:
    """
    Represents the blockchain.
    """

    def __init__(self):
        self.transactions = []
        self.last_labels = []
        self.chain = [self.gen_block()]

    @property
    def last_block(self):
        """
        Returns the last block in the blockchain.
        """
        return self.chain[-1]

    @staticmethod
    def gen_block():
        """
        Creates and returns the first block in the blockchain.
        """
        gen_data = {"name": "The First Block", "sender": "God",
                    "recipient": "Mankind", "quantity": 0}
        gen_image = None
        gen_label = "The Void"
        genesis = Block(index=0, timestamp=datetime.datetime.now(
        ), data=gen_data, image=gen_image, label=gen_label, last_hash="0")
        return genesis

    def new_block(self, image, label, data=None, nonce=0):
        """
        Creates a new block from and image and a label.
        """
        index = len(self.chain) + 1
        timestamp = datetime.datetime.now()
        last_hash = self.last_block.hash_block()
        block = Block(index, timestamp, data, image, label, last_hash, nonce)
        return block

    def add_block(self, block):
        self.chain.append(block)

    @staticmethod
    def is_valid_hash(block):
        """
        Validates hash.
        """
        block_hash = block.hash_block()
        if (block.image and block_hash.startswith('0')) or block_hash.startswith('0'*4):
            return True
        else:
            return False

    def add_transaction(self, sender, recipient, quantity):
        """
        Adds transaction to block data.
        """
        timestamp = datetime.datetime.now()
        data = {"sender": sender, "recipient": recipient,
                "quantity": quantity, "timestamp": timestamp}
        self.transactions.append(data)

    def is_valid_chain(self, chain):
        """
        Validates chain.
        """
        for block in chain:
            if not self.is_valid_hash(block) or block.last_hash != chain.last_block.hash_block():
                result = False
            else:
                result = True
        return result


    @staticmethod
    def proof_of_work(block):
        """
        Implements proof of work.
        """
        new_block = block
        image = Image(image=new_block.image, label=new_block.label)

        logging.info(f"Running image processor")
        if image.image_match():
            new_hash = new_block.hash_block()
            logging.info(f"Image matched!\n Starting simplified PoW...")
            while new_hash.startswith('0') is False:
                new_block.nonce += 1
                new_hash = new_block.hash_block()
                logging.info(new_hash)
            return new_block.nonce
        else:
            logging.info(f"No image match found\n Starting PoW...")
            new_hash = new_block.hash_block()
            while new_hash.startswith('0' * 4) is False:
                new_block.nonce += 1
            return new_block.nonce
