#!/usr/bin/env python3

# Imports
import logging
import json
import redis
import threading
import time
from photoblocks.exceptions import StorageError, NetworkError, ConfigurationError
import sys

# Local module imports
from models.node import Node
from networking.clientsock import ClientSock
from networking.serversock import serversock
from servers.api import create_api, run_server


def initialize_redis(max_retries=3, retry_delay=5):
    """Initialize Redis connection with retry logic"""
    db = redis.Redis(host='redis', port=6379)
    for attempt in range(max_retries):
        try:
            if db.execute_command('PING'):
                logging.info('Connected to the local database server.')
                return db
        except redis.ConnectionError as e:
            if attempt == max_retries - 1:
                raise StorageError(f"Failed to connect to Redis after {max_retries} attempts: {e}")
            logging.warning(f"Redis connection attempt {attempt + 1} failed, retrying...")
            time.sleep(retry_delay)
    raise StorageError("Redis connection failed")

def start_thread(target, args, thread_name):
    """Start a thread with proper error handling"""
    try:
        thread = threading.Thread(target=target, args=args, name=thread_name)
        thread.daemon = True
        thread.start()
        return thread
    except Exception as e:
        raise NetworkError(f"Failed to start {thread_name}: {e}")

def main():
    try:
        logging.basicConfig(level=logging.INFO)
        logging.info('Starting node server...')

        # Load network configuration
        try:
            with open("./photoblocks/network.json") as f:
                network = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            raise ConfigurationError(f"Failed to load network configuration: {e}")

        # Initialize Redis
        db = initialize_redis()

        # Initialize node
        try:
            node = Node(network["local"])
        except KeyError as e:
            raise ConfigurationError(f"Invalid network configuration: {e}")

        # Start P2P network threads
        client_thread = start_thread(
            target=ClientSock,
            args=(network, node),
            thread_name="client_socket"
        )
        
        server_thread = start_thread(
            target=serversock,
            args=(),
            thread_name="server_socket"
        )

        # Start REST API server in main thread
        run_server(
            pack=network["local"],
            db=db,
            host=node.host,
            port=node.port
        )

    except Exception as e:
        logging.error(f"Critical error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
