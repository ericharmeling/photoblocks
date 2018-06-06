import flask

node = flask.Flask(__name__)

transactions = []

@node.route('/transaction')
def transaction():
    """"""
