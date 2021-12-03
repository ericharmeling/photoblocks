#!/usr/bin/env python3

# Imports
import logging
import json
import redis
import threading
import time

# Local module imports
from models.node import Node
from networking.clientsock import ClientSock
from networking.serversock import serversock


def main():
    """
    Main process for blockchain node.
    """
    logging.basicConfig(level=logging.INFO)
    logging.info('\nStarting node server...')

    # Unpack network file
    with open("./photoblocks/network.json") as f:
        network = json.load(f)

    # Test local db connection
    db = redis.Redis(host='redis', port=6379)
    while True:
        try:
            if db.execute_command('PING'):
                logging.info(f'\nConnected to the local database server.')
                break
            else:
                continue
        except Exception as e:
            logging.error(f'\n{e}')
            continue

    # Construct Node object
    logging.info('\nCreating Node data structure from configuration...')
    node = Node(network["local"])
    logging.info(f'\nNode data structure created.')

    # Start a node socket client
    logging.info('\nStarting node socket client on background thread...')
    thread = threading.Thread(target=ClientSock, args=(network, node))
    logging.info('\nThread process created.')
    thread.daemon = True
    thread.start()
    logging.info('\nThread process started.')
    time.sleep(5)

    # Start node socket server
    logging.info('\nStarting node socket server on background thread...')
    thread = threading.Thread(target=serversock, args=())
    logging.info('\nThread process created.')
    thread.daemon = True
    thread.start()
    logging.info('\nThread process started.')

    while True:
        time.sleep(5)


if __name__ == '__main__':
    main()
