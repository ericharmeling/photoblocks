from chain import Chain
from flask import Flask, render_template
from resources.nodes import *
from resources.trade import *
from resources.mine import *
# from resources.chain import *
from resources.users import *
import json

# Pull in configuration file
with open("config.json") as f:
    config_json = json.load(f)

# Assign variable to Flask WSGI instance
app = Flask(__name__)

# Define node initialization variables
node_name = config_json["_nodename"]
node_id = config_json["_nodeid"]
node_type = config_json["_nodetype"]
node_key = config_json["_key"]

# Define local image matcher config variables
image_dir = config_json["_imagedir"]

# Initialize blockchain
blockchain = Chain(image_dir)

# initialize node list, you will add to this list with the consensus algorithm
blockchain.nodes.append({'node_name': node_name, 'node_id': node_id, 'node_type': node_type,
                         'node_key': node_key})

# Initialize users
users = list()


# Add routes to pages (located in templates)


@app.route('/')
def index():
    return render_template('home.html')


@app.route('/trade')
def trade_page():
    return render_template('trade.html')


@app.route('/mine')
def mine_page():
    return render_template('mine.html', listchain=blockchain.__dict__)


@app.route('/register')
def register_page():
    return render_template('register.html')


@app.route('/login')
def login_page():
    return render_template('login.html')


@app.route('/nodes')
def nodes_page():
    return render_template('nodes.html', peers=blockchain.nodes)


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

app.add_url_rule('/transaction/new', view_func=TransactionNewResource.as_view('transaction_new_resource'),
                 methods=['POST'])
app.add_url_rule('/transaction/list', view_func=TransactionListResource.as_view('transaction_list_resource'),
                 methods=['GET'])

# Mining

app.add_url_rule('/mine', view_func=MineResource.as_view('mine_resource'), methods=['POST'])

# Chain

# app.add_url_rule('/chain', view_func=ChainResource.as_view('chain_resource'), methods=['GET'])

if __name__ == '__main__':
    app.run(debug=True)
