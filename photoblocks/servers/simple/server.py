# This file starts up a server
from .handler import Handler
from http.server import HTTPServer
import logging
import json

def serve(node, seeds):
    logging.basicConfig(level=logging.INFO)
    server_address = (node.network, node.port)
    httpd = HTTPServer(server_address, Handler)
    logging.info('Starting httpd...\nSeeds listening at {0}.'.format(seeds))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info('Stopping httpd...\n')

