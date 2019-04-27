from chain import Chain
from mine import mine
from flask import Flask, render_template
from resources.nodes import *
from resources.trade import *
# from resources.mine import *
# from resources.chain import *
from resources.users import *
import json
import requests
from requests import HTTPError

# Pull in configuration file
with open("config.json") as f:
    config_json = json.load(f)

#################
# SET VARIABLES #
#################
# Assign variable to Flask WSGI instance
app = Flask(__name__)

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
def scan(u, p):
    try:
        response = requests.get(url=u + p)
    except HTTPError as http_error:
        print(f'HTTP error: {http_error}\n Using {p} as node port\n')
        return p
    except Exception as error:
        print(f'Error: {error}\n')
        return p
    else:
        nodes[p] = (response.json())
        p += 1
        scan(u, p+1)


node_port = scan(URL, 5000)

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

######################
# BLOCKCHAIN PROCESS #
######################
# Initialize blockchain
blockchain = Chain(image_dir)

# Populate nodes structure with collected node data
blockchain.nodes = nodes

##############
# WEB ROUTES #
##############
@app.route('/')
def check():
    return json.dumps(node_pack), 200

# Add routes to pages (located in templates)
@app.route('/home')
def index():
    return render_template('home.html')


@app.route('/trade')
def trade_page():
    return render_template('trade.html')


@app.route('/mine', methods=['GET', 'POST'])
def mine_route():
    if request.method == 'POST':
        try:
            bc = mine(blockchain)
            return str(bc)
        except HTTPError as http_error:
            print(f'HTTP error: {http_error}\n')
        except Exception as error:
            print(f'Error: {error}\n')
    else:
        return render_template('mine.html', listchain=blockchain.chain)


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


#############
# RESOURCES #
#############
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

# app.add_url_rule('/mine', view_func=MineResource.as_view('mine_resource'), methods=['POST'])

# Chain

# app.add_url_rule('/chain', view_func=ChainResource.as_view('chain_resource'), methods=['GET'])


if __name__ == '__main__':
    app.run(host=URL, port=node_port, debug=DEBUG)
