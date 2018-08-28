from flask.views import MethodView
import json


class ChainResource(MethodView):
    def get(self):
        data = []

        for block in blockchain.chain:
            data.append(block.__dict__)

        return json.dumps({"length": len(data), "chain": data}), 200
