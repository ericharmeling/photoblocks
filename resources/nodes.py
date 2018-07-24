from flask import request
from flask.views import MethodView
# import json

class NodeRegisterResource(MethodView):
    def post(self):
        node_name = request.form['node_name']
        node_id = request.form['node_id']
        node_type = request.form['node_type']
        node_key = request.form['node_key']
        fields = [node_name, node_id, node_type, node_key]
        
        for field in fields:
            if not field:
                return "Invalid Data", 404
        
        nodes.append({node_name, node_id, node_type, node_key})
        return nodes, 200
        
class NodeListResource(MethodView):
    def get(self):
        return nodes, 200
