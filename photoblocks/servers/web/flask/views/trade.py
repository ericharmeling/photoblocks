from flask.views import MethodView
from flask import request


class TransactionNewResource(MethodView):
    def post(self):
        sender = request.form["sender"]
        recipient = request.form["recipient"]
        quantity = request.form["quantity"]
        fields = [sender, recipient, quantity]

        for field in fields:
            if not field:
                return "Invalid Data", 404

        blockchain.add_transaction_fields(sender, recipient, quantity)

        return fields, 200


class TransactionListResource(MethodView):
    def get(self):
        return blockchain.transactions
