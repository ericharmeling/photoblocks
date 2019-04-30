from chain import Chain
from networking import *
from flask import Flask, render_template
from resources.mine import mine
from resources.nodes import *
from resources.trade import *
# from resources.chain import *
from resources.users import *
import json
import requests
from requests import HTTPError

# VARIABLES
# Assign variable to Flask WSGI instance
app = Flask(__name__)

# Pull in configuration file
with open("config.json") as f:
    config_json = json.load(f)

# Define node initialization variables
node_name = config_json["_nodename"]
node_id = config_json["_nodeid"]
node_type = config_json["_nodetype"]
node_key = config_json["_key"]

# Define network URL
URL = config_json["_url"]

# Initialize peer node set
nodes = dict()

# Scan network for other nodes and set port
node_port = scan(URL, 5000, nodes)
ENDPOINT = URL + node_port

# Set variables for other peers
node_pack = {
    "name": node_name,
    "id": node_id,
    "type": node_type,
    "key": node_key
}
# Add node variables to node map
nodes[node_port] = node_pack

# Set debug mode
DEBUG = config_json["_debug"]

# Define local image matcher config variables
image_dir = config_json["_imagedir"]


# BLOCKCHAIN
# Initialize blockchain
blockchain = Chain(image_dir)

# Populate nodes structure with collected node data
blockchain.nodes = nodes


# ROUTES
# Check nodes
@app.route('/', methods=['GET'])
def check():
    return json.dumps(node_pack), 200

# Home page
@app.route('/home', methods=['GET'])
def index():
    return render_template('home.html')

# Trade page
@app.route('/trade', methods=['GET'])
def trade_page():
    return render_template('trade.html')

# Mine page and mine submission
@app.route('/mine', methods=['GET', 'POST'])
def mine_route():
    if request.method == 'POST':
        try:
            list_response = requests.get(url=ENDPOINT + 'nodes/list')
            if request.form['node_id'] not in list_response.text:
                return 'The node ID you gave is not registered!', 200
            else:
                bc = mine(blockchain)
                return render_template('reward.html', block=bc)
        except HTTPError as http_error:
            print(f'HTTP error: {http_error}\n')
        except Exception as error:
            print(f'Error: {error}\n')
    else:
        return render_template('mine.html', listchain=blockchain.chain)


# Nodes page
@app.route('/nodes', methods=['GET'])
def nodes_page():
    return render_template('nodes.html', peers=blockchain.nodes)


# Register node
@app.route('/nodes/register', methods=['POST'])
def nodes_register():
    try:
        add_node(blockchain)
        return render_template('nodes.html', peers=blockchain.nodes)
    except HTTPError as http_error:
        print(f'HTTP error: {http_error}\n')
    except Exception as error:
        print(f'Error: {error}\n')


# List node (for proof of work)
@app.route('/nodes/list', methods=['GET'])
def nodes_list():
    try:
        return blockchain.nodes
    except HTTPError as http_error:
        print(f'HTTP error: {http_error}\n')
    except Exception as error:
        print(f'Error: {error}\n')


# Register page
@app.route('/register')
def register_page():
    return render_template('register.html')


# Login page
@app.route('/login')
def login_page():
    return render_template('login.html')


# About page
@app.route('/about')
def about():
    return render_template('about.html')


# Contact page
@app.route('/contact')
def contact():
    return render_template('contact.html')


# Trading
app.add_url_rule('/transaction/new', view_func=TransactionNewResource.as_view('transaction_new_resource'),
                 methods=['POST'])
app.add_url_rule('/transaction/list', view_func=TransactionListResource.as_view('transaction_list_resource'),
                 methods=['GET'])

# Chain

# app.add_url_rule('/chain', view_func=ChainResource.as_view('chain_resource'), methods=['GET'])


if __name__ == '__main__':
    app.run(host=URL, port=node_port, debug=DEBUG)
