from blocks import Chain, Block, Genesis
from flask import Flask
import datetime
import requests
import json

app = Flask(__name__)

blockchain = Chain()

peers = set()

@app.route('/transaction', methods=['POST'])
def new_transaction():
    data = requests.get_json()
    fields = ["sender", "recipient", "quantity"]

    for field in fields:
        if not data.get(field):
            return "Invalid Data", 404

    data["timestamp"] = datetime.datetime.now()

    blockchain.add_transaction(data)

    return "OK", 201

@app.route('/chain', methods=['GET'])
def get_chain():
    data = []
    for block in blockchain.chain:
        data.append(block.__dict__)
    return json.dumps({"length": len(data), "chain": data})

@app.route('/mine', methods=['GET'])
