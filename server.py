from blocks import Chain, Block, Genesis
import flask
import datetime

app = flask.Flask(__name__)

blockchain = Chain()

@app.route('/transaction', methods=['POST'])
def new_transaction():
    data = request.get_json()
    fields = ["sender", "recipient", "quantity"]

    for field in fields:
        if not data.get(field):
            return "Invalid Data", 404

    data["timestamp"] = datetime.datetime.now()

    blockchain.add_transaction(data)

    return "OK", 201

