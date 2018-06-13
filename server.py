from blocks import Chain
from flask import Flask, request
from flask_cors import CORS
import datetime
import requests
import json

app = Flask(__name__)
CORS(app)

node_id =

global_target = "Car"

blockchain = Chain()

temp_store = 'path' # temporary image store location

peers = set()

@app.route('/nodes/register', methods=['POST'])
def register_node():
    nodes = request.form

@app.route('/transaction', methods=['POST'])
def new_transaction():
    """
    Posts new transaction to chain.
    :return:
    """
    data = request.get_json()
    fields = ["sender", "recipient", "quantity"]

    for field in fields:
        if not data.get(field):
            return "Invalid Data", 404

    data["timestamp"] = datetime.datetime.now()

    blockchain.add_transaction_data(data)

    return "OK", 201


@app.route('/chain', methods=['GET'])
def get_chain():
    """
    Get request to return chain.
    :return: Returns chain length and block data.
    """
    data = []
    for block in blockchain.chain:
        data.append(block.__dict__)
    return json.dumps({"length": len(data), "chain": data})

@app.route('/mine', methods=['POST'])
def mine():
    image_file = request.file['file']
    image_file.save(temp_store)

    last_block = blockchain.last_block
    proof = blockchain.proof_of_work(last_block, image_file, global_target)

    blockchain.add_transaction_fields(sender="God", recipient=node_id, quantity=1)

    block = blockchain.new_block(image_file, blockchain.transactions, proof)
    blockchain.add_block(block)

def consensus():

    global blockchain

    longest_chain = None
    n = len(blockchain.chain)

    for node in peers:
        response = requests.get('http://{}/chain'.format(node))
        length = response.json()['length']
        chain = response.json()['chain']
        if length > n and blockchain.is_valid_chain(chain):
            n = length
            longest_chain = chain

    if longest_chain:
        blockchain = longest_chain
        return True

    return False
