# makeconfig.py
# This script generates secret keys, unique node IDs, and sets other configuration variables

from uuid import uuid4
import json


class Config:
    def __init__(self, params):
        self._nodename = params["name"]
        self._nodetype = params["ntype"]
        self._imagedir = params["imagedir"]
        self._key = params["key"]
        self._nodeid = params["nid"]
        self._debug = params["debug"]
        self._url = params["url"]

    def as_json(self):
        return json.dumps(self.__dict__)


# default values
cwd = "."
dkey = str(uuid4()).replace('-', '')
did = str(uuid4()).replace('-', '')
durl = "localhost"
dde = True
dvals = {
    "imagedir": cwd,
    "key": dkey,
    "nid": did,
    "url": durl,
    "debug": dde
}

if __name__ == "__main__":

    n = input("What name do you want to give to your node? (Required)\n")
    t = input("What type of node do you have? (Required, \"full\"|\"light\")\n")
    indir = input("What directory is your Tensor Flow \"models\" folder in? (Optional, default is CWD)\n")
    inkey = input("Enter your node's unique public key, for mining rewards.\n"
              "(If you do not enter a key, one will be created for you.)\n")
    inid = input("Enter your node unique ID.\n"
              "(If you do not enter an ID, one will be created for you.)\n")
    inurl = input("Enter the URL for your local network. (Optional, default is \"localhost\")\n")
    inde = input("Run in debug mode? (Optional, default is True.)\n")
    inde = inde == "True"
    invals = {
        "name": n,
        "ntype": t,
        "imagedir": indir,
        "key": inkey,
        "nid": inid,
        "url": inurl,
        "debug": inde
    }

    vals = []

    for key, value in invals.items():
        if value is "":
            invals[key] = dvals[key]

    config = Config(invals)

    with open("./config.json", mode="w") as f:
        print(config.as_json(), file=f)
