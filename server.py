from blocks import Chain
from flask import Flask, request
import datetime
import requests
import json

app = Flask(__name__)

blockchain = Chain()

peers = set()

@app.route('/transaction', methods=['POST'])
def new_transaction():
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
    data = []
    for block in blockchain.chain:
        data.append(block.__dict__)
    return json.dumps({"length": len(data), "chain": data})

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
