from blocks import Chain
from flask import Flask, request, render_template
from uuid import uuid4
import requests
import json

app = Flask(__name__)

node_id = str(uuid4()).replace('-', '')  # unique node ID
node_key = 0  # node public key (for mining rewards)

blockchain = Chain()

temp_store = 'path'  # temporary image store location

nodes = set()


@app.route('/')
def index():
    return render_template('home.html')


@app.route('/trade')
def trade_page():
    return render_template('trade.html')


@app.route('/mine')
def mine_page():
    return render_template('mine.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/nodes/register', methods=['POST'])
def register():
    pass


@app.route('/transaction', methods=['POST'])
def transaction():
    """
    Posts new transaction to chain.
    :return:
    """
    sender = request.form["sender"]
    recipient = request.form["recipient"]
    quantity = request.form["quantity"]

    fields = [sender, recipient, quantity]

    for field in fields:
        if not field:
            return "Invalid Data", 404

    blockchain.add_transaction_fields(sender, recipient, quantity)

    return "OK", 201


@app.route('/chain', methods=['GET'])
def chain():
    """
    Get request to return chain.
    :return: Returns chain length and block data.
    """
    data = []
    for block in blockchain.chain:
        data.append(block.__dict__)
    return json.dumps({"length": len(data), "chain": data})


@app.route('/mine', methods=['POST', 'GET'])
def mine():
    if request.method == 'POST':
        image_file = request.file['file']
        label = request.form['label']
    else:
        image_file = []
        label = "Nothing"

    new_block = blockchain.new_block(image_file, label, blockchain.transactions)
    proof = blockchain.proof_of_work(new_block)

    block = blockchain.new_block(image_file, label, blockchain.transactions, proof)
    blockchain.add_block(block)

    blockchain.transactions = []
    blockchain.add_transaction_fields(sender="God", recipient=node_key, quantity=1)


def consensus():
    global blockchain

    longest_chain = None
    n = len(blockchain.chain)

    for node in nodes:
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


if __name__ == '__main__':
    app.run(debug=True)
