#!/usr/bin/env python3
import logging
import argparse
from utils.configure import makeconfig, makeconf
import json
from models.node import Node
from subprocess import run
import redis
from networking.socks import serversock
import threading

#from servers.rest.api import api

def main():
    logging.basicConfig(level=logging.INFO)
    logging.info('Starting node servers...\n')

    # Load node server configuration
    logging.info('Loading node configuration...\n')
    args = parse()
    if args.file:
        with open("config.json") as f:
            config = json.load(f)           
    else:
        config = makeconfig(args)

    # Construct Node object
    logging.info('Creating Node data structure from configuration...\n')
    node = Node(config=config)
    logging.info(f'{node.node_type} node data structure created.\n')

    # Start node socket server
    logging.info('Starting node socket server on background thread...\n')
    thread = threading.Thread(target=serversock, args=node)
    logging.info('Thread process created.\n')
    thread.daemon = True 
    thread.start()
    logging.info('Thread process started.\n')

    # Start and connect to database
    logging.info(f'Starting local database server at {node.dbport}...\n')
    makeconf(node.dbport)
    run("redis-server", input="./db/photoblocks.conf")
    db = redis.Redis(host=node.host, port=node.dbport)
    logging.info(f'Local database server now listening at {node.dbport}.\n')

    # Store head node pack
    logging.info('Loading database with node data.')
    db.set('nodes', str(node.pack))

    # Create peerlist
    logging.info('Scanning for peer nodes and storing peerlist on database.')
    db.set('nodes', node.peerlist)


def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('type', help='The type of the node. Valid options include "head", "seed", "full", and "light"')
    parser.add_argument('--store', default='./db', help='The local store directory for blockchain and network data.')
    parser.add_argument('--debug', default=False, help='Run the node in debug mode.')
    parser.add_argument('--seedports', default=[6000,6001,6002], help='The ports on which to run seed nodes.')
    parser.add_argument('--file', default=None, help='Use file to load configuration.')
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    main()
