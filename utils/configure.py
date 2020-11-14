# These functions set configuration variables
from uuid import uuid4
import json

def makeconfig(args):

    options = {
        "type": args.type,
        "store": args.store,
        "debug": args.debug,
        "seedports": args.seedports
    }

    with open("./config.json", mode="w") as f:
        f.write(json.dumps(options))
    
    return options

def makeconf(port):

    dboptions = """
            # db/photoblocks.conf
            port              {0}
            daemonize         yes
            save              60 1
            bind              127.0.0.1
            tcp-keepalive     300
            dbfilename        dump.rdb
            dir               ./
            rdbcompression    yes
            """

    with open("./photoblocks.conf", mode="w") as f:
        f.write(dboptions.format(port))
