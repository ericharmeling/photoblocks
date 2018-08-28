from blocks import Chain
from flask import Flask, request, render_template
from resources.nodes import *
from resources.trade import *
from resources.mine import *
from resources.chain import *
from resources.users import *
from uuid import uuid4
import requests

# Assign variable to Flask WSGI instance
app = Flask(__name__)


# Define head node initialization variables
head_node_name = "Head Node"
head_node_id = str(uuid4()).replace('-', '')
head_node_type = "HEAD"
head_node_key = 0

# Initialize blockchain
blockchain = Chain()

# Initialize nodes
nodes = list()
nodes.append({'node_name': head_node_name, 'node_id': head_node_id, 'node_type': head_node_type,
              'node_key': head_node_key})

# Initialize users
users = list()

# Assign temporary store directory
temp_store = '/temp/'


# Add routes to pages (located in templates)

@app.route('/')
def index():
    return render_template('home.html')


@app.route('/trade')
def trade_page():
    return render_template('trade.html')


@app.route('/mine')
def mine_page():
    return render_template('mine.html')


@app.route('/register')
def register_page():
    global nodes
    return render_template('register.html')


@app.route('/login')
def login_page():
    return render_template('login.html')


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


# Add routes to resources

# Users

app.add_url_rule('/users/register', view_func=UserRegisterResource.as_view('user_register_resource'), methods=['POST'])
app.add_url_rule('/users/login', view_func=UserLoginResource.as_view('user_login_resource'), methods=['POST'])


# Nodes

app.add_url_rule('/nodes/register', view_func=NodeRegisterResource.as_view('node_register_resource'), methods=['POST'])
app.add_url_rule('/nodes/list', view_func=NodeListResource.as_view('node_list_resource'), methods=['GET'])


# Trading

app.add_url_rule('/transaction/new', view_func=TransactionNewResource.as_view('transaction_new_resource'), methods=['POST'])
app.add_url_rule('/transaction/list', view_func=TransactionListResource.as_view('transaction_list_resource'), methods=['GET'])


# Mining

app.add_url_rule('/mine', view_func=MineResource.as_view('mine_resource'), methods=['POST'])


# Chain

app.add_url_rule('/chain', view_func=ChainResource.as_view('chain_resource'), methods=['GET'])


# big to-do here...
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
