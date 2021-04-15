from flask import Flask
from views.mine import mine
from views.nodes import *
from views.trade import *
from views.chain import *
from views.users import *
import json
import requests
from requests import HTTPError

app = Flask(__name__)

# ROUTES
# Seed manager
@app.route('/', methods=['GET'])
def check():
    return json.dumps(node_pack), 200


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
    app.run(host=network, port=node_port, debug=DEBUG)
