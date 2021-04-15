# These functions set configuration variables
import argparse
from uuid import uuid4
import json

def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('port', help='The node port. Photoblocks determines the type of node from the port selected.')
    parser.add_argument('--debug', default=True, help='Run the node in debug mode.')
    parser.add_argument('--file', default=None, help='Use file to load configuration.')
    args = parser.parse_args()
    return args

def makeconfig(args):

    options = {
        "port": args.port,
        "debug": args.debug
    }

    with open("./config.json", mode="w") as f:
        f.write(json.dumps(options))
    
    return options
