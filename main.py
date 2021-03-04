#!/usr/bin/env python3
import logging
import argparse
from utils.configure import makeconfig
import json
from models.node import Node
import redis
from networking.socks import ClientSock, ServerSock
import threading

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
    node = Node(node_type=config["type"])
    logging.info(f'\n{node.node_type} node data structure created.')

    # Store node pack
    logging.info('\nLoading database with node metadata...')
    logging.info('\nDatabase loaded with with node metadata.')

    # Start a node socket client
    logging.info('\nStarting node socket client on background thread...')
    thread = threading.Thread(target=ClientSock, args=(node, config["seedports"], db))
    logging.info('\nThread process created.')
    thread.daemon = True 
    thread.start()
    logging.info('\nThread process started.')


    # Start node socket server
    logging.info('\nStarting node socket server on background thread...')
    thread = threading.Thread(target=ServerSock, args=(node))
    logging.info('\nThread process created.')
    thread.daemon = True 
    thread.start()
    logging.info('\nThread process started.')


def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('type', help='The type of the node. Valid options include "head", "seed", "full", and "light"')
    parser.add_argument('--debug', default=True, help='Run the node in debug mode.')
    parser.add_argument('--seedports', default=[7000,7001,7002,7003], help='The ports on which to run the head and seed nodes.')
    parser.add_argument('--file', default=None, help='Use file to load configuration.')
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    main()
