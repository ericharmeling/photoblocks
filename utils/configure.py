# These functions set configuration variables
import argparse
from uuid import uuid4
import json

def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('type', help='The type of the node. Valid options include "head", "seed", "full", and "light"')
    parser.add_argument('--debug', default=True, help='Run the node in debug mode.')
    parser.add_argument('--seedports', default=[7000,7001,7002,7003], help='The ports on which to run the head and seed nodes.')
    parser.add_argument('--file', default=None, help='Use file to load configuration.')
    args = parser.parse_args()
    return args

def makeconfig(args):

    options = {
        "type": args.type,
        "debug": args.debug,
        "seedports": args.seedports
    }

    with open("./config.json", mode="w") as f:
        f.write(json.dumps(options))
    
    return options
