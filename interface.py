from blocks import Chain
from flask import Flask, request, render_template
from uuid import uuid4
import requests
import json

# HEAD NODE INITIALIZATION VARIABLES

app = Flask(__name__)

head_node_name = "Head Node"
head_node_id = str(uuid4()).replace('-', '')  # head node's unique node ID for identification
head_node_type = "HEAD"
head_node_key = 0

blockchain = Chain()  # initialize blockchain
nodes = list()  # initialize nodes
nodes.append({'node_name': head_node_name, 'node_id': head_node_id, 'node_type': head_node_type,
              'node_key': head_node_key})

temp_store = '/temp/'  # temporary image store location


# WEB PAGES

@app.route('/')
def index():
    return render_template('home.html')


@app.route('/trade')
def trade_page():
    return render_template('trade.html')


@app.route('/mine')
def mine_page():
    return render_template('mine.html')


@app.route('/nodes')
def nodes_page():
    global nodes
    return render_template('nodes.html', peers=nodes)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


# WEB REQUESTS

# Nodes

@app.route('/nodes/register', methods=['POST'])
def register():
    if request.method == 'POST':
        node_name = request.form['node_name']
        node_id = request.form['node_id']
        node_type = request.form['node_type']
        node_key = request.form['node_key']
        nodes.append({node_name, node_id, node_type, node_key})

    return nodes


@app.route('/nodes/list', methods=['GET'])
def list_nodes():
    return nodes


# Trading


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


# Mining


@app.route('/mine', methods=['POST', 'GET'])
def mine():
    if request.method == 'POST':
        image_file = request.form['file']
        label = request.form['label']
        last_label = request.form['last_label']
    else:
        image_file = []
        label = "Nothing"

    new_block = blockchain.new_block(image_file, label, blockchain.transactions)
    proof = blockchain.proof_of_work(new_block)

    block = blockchain.new_block(image_file, label, blockchain.transactions, proof)
    blockchain.add_block(block)

    blockchain.transactions = []
    blockchain.add_transaction_fields(sender="God", recipient=node_key, quantity=1)

    return blockchain


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
