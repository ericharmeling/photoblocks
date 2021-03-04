# These functions set configuration variables
from uuid import uuid4
import json

def makeconfig(args):

    options = {
        "type": args.type,
        "debug": args.debug,
        "seedports": args.seedports
    }

    with open("./config.json", mode="w") as f:
        f.write(json.dumps(options))
    
    return options
