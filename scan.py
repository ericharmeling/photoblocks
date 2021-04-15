#!/usr/bin/env python3
import socket
import logging
import time
import threading
import argparse
import os
import re

def main():

    logging.basicConfig(level=logging.INFO)
    logging.info('\nScanning network for available ports...')

    HOST = socket.gethostbyname(socket.gethostname())
    port = None

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.connect(("8.8.8.8", 80))
        global ip
        ip = str(s.getsockname()[0])


    args = parse()

    if args.type == 'head':
        port = 7000
    elif args.type == 'seed':
        port = 7001
    elif args.type == 'full':
        port = 7004
    else:
        port = 7006

    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            scanports(sock, HOST, port)
            return
    
    def scanports(sock, host, port):
        logging.info(f'\nScanning local network first (hostname {host}).')
        while True:
            try:
                logging.info(f'\nChecking for node at {host}:{port}...')
                sock.connect((host, port))
                sock.sendall('ping'.encode())
                response = sock.recv(1024).decode()
                if response:
                    logging.info(f'\n{response}.')
                    logging.info(f'\nNode already serving at port {host}:{port}.')
                else:
                    logging.info(f'\nSomething is serving at {host}:{port} (but its not a node).')
                if port == 7000:
                    logging.info(f'\nHead node port occupied on local machine. Demoting to seed node.')
                    port = port+1
                elif port == 7003:
                    logging.info(f'\nSeed node ports occupied on local machine. Demoting to full node.')
                    port = port+1
                elif port == 7007:
                    logging.info(f'\nNo node ports are available on local machine! Free up a port between 7000 and 7007, and try again.')
            except socket.error:
                logging.info(f'\nPort {port} free on {host}.')
                if port > 7003:
                    logging.info(f' Setting port to {port}.')
                    print(port)
                elif port == 7000:
                    logging.info(f' Scanning network for existing head nodes.')
                    with os.popen('arp -a') as f:
                        data = f.read()
                    network = data.split("?")
                    for line in network:
                        host = re.findall(re.escape("(")+"(.*)"+re.escape(")"), line)
                        if host and host not == ip:


    def parse():
        parser = argparse.ArgumentParser()
        parser.add_argument('type', help='The type of the node. Valid options include "head", "seed", "full", and "light"')
        args = parser.parse_args()
        return args

if __name__ == '__main__':
    main()

