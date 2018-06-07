from blocks import Chain, Block, Genesis
import flask

app = flask.Flask(__name__)

blockchain = Chain()
