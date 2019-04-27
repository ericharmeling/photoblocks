from flask.views import MethodView
from flask import request, Response


class MineResource(MethodView):
    def post(self, blockchain, id):
        image_file = request.form['file']
        label = request.form['label']
        last_label = request.form['last_label']

        blockchain.last_labels.append(last_label)

        iter_block = blockchain.new_block(image_file, label, blockchain.transactions)
        proof = blockchain.proof_of_work(iter_block)
        block = blockchain.new_block(image_file, label, blockchain.transactions, proof)

        blockchain.add_block(block)
        blockchain.transactions = []
        blockchain.add_transaction_fields(sender="God", recipient=node_key, quantity=1)

        return Response(status=200, headers={"block": block})
