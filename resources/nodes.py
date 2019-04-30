from flask import request


def add_node(chain):
    node_name = request.form['node_name']
    node_id = request.form['node_id']
    node_type = request.form['node_type']
    node_key = request.form['node_key']

    chain.nodes.append({node_name, node_id, node_type, node_key})
