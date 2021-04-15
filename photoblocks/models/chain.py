# chain.py
# Defines the Chain class, a data structure of linked blocks

import datetime
import geocoder
from photoblocks.models.block import Block
#from models.image import Image


class Chain:
    def __init__(self):
        self.transactions = []
        self.last_labels = []
        self.chain = []
        gen_data = {"name": "The First Block", "sender": "God", "recipient": "Mankind", "quantity": 0}
        gen_location = 'my location' #str(geocoder.ip('me')[0])
        gen_image = None
        gen_label = "The Void"
        genesis = Block(index=0, timestamp=datetime.datetime.now(), location=gen_location, data=gen_data, image=gen_image, label=gen_label, last_hash="0")
        self.chain.append(genesis)

    @property
    def last_block(self):
        return self.chain[-1]


    def new_block(self, location, image, label, data=None, nonce=0):
        index = len(self.chain) + 1
        timestamp = datetime.datetime.now()
        last_hash = self.last_block.hash_block()
        block = Block(index, timestamp, location, data, image, label, last_hash, nonce)
        return block

    def add_block(self, block):
        self.chain.append(block)

    @staticmethod
    def is_valid_hash(block):
        block_hash = block.hash_block()
        if block_hash.startswith('0') or block_hash.startswith('0'*4):
            return True

    def add_transaction_fields(self, sender, recipient, quantity):
        timestamp = datetime.datetime.now()
        data = {"sender": sender, "recipient": recipient, "quantity": quantity, "timestamp": timestamp}
        self.transactions.append(data)

    def add_transaction_data(self, data):
        data['timestamp'] = datetime.datetime.now()
        self.transactions.append(data)

    def is_valid_chain(self, chain):

        for block in chain:
            if not self.is_valid_hash(block) or block.last_hash != chain.last_block.hash_block():
                result = False
            else:
                result = True

        return result


"""
    @staticmethod
    def proof_of_work(self, block):
        new_block = block

        print(f"Running image processor")
        if image_match(image=new_block.image, label=new_block.label):
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
"""