#!/usr/bin/env python3
import logging
from utils.configure import makeconfig, parse
import json
from models.node import Node
import redis
from networking.socks import ClientSock, ServerSock
import threading
import time

def main():
    logging.basicConfig(level=logging.INFO)
    logging.info('\nStarting node server...')

    # Load node server configuration
    logging.info('\nConfiguring node...')
    args = parse()
    if args.file:
        with open("config.json") as f:
            config = json.load(f)           
    else:
        config = makeconfig(args)
    logging.info('\nNode configured.')

    # Connect to database
    logging.info(f'\nStarting connection to the local database server...')
    db = redis.Redis(host='127.0.0.1', port=6379)
    logging.info(f'\nConnected to the local database server.')

    # Construct Node object
    logging.info('\nCreating Node data structure from configuration...')
    node = Node(port=config["port"])
    logging.info(f'\n{node.node_type} node data structure created.')
    
    # Start a node socket client
    logging.info('\nStarting node socket client on background thread...')
    thread = threading.Thread(target=ClientSock, args=(node, config["seedports"], db))
    logging.info('\nThread process created.')
    thread.daemon = True 
    thread.start()
    logging.info('\nThread process started.')


    # Start node socket server
    logging.info('\nStarting node socket server on background thread...')
    thread = threading.Thread(target=ServerSock, args=(db))
    logging.info('\nThread process created.')
    thread.daemon = True 
    thread.start()
    logging.info('\nThread process started.')

    while True:
        time.sleep(5)

if __name__ == '__main__':
    main()
