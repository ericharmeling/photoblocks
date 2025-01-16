#!/usr/bin/env python3
import socket
import logging
import argparse
import scapy.all as scapy
import re
import json
from photoblocks.storage import NodeStorage
from photoblocks.exceptions import NetworkError, ConfigurationError


def scan(ip, ports, sock):
    """
    Attempts to establish a socket connection from the local machine to a host, at a given list of ports.
    Port values:
    0: availability unknown.
    1: port occupied by a node.
    2: port occupied by something that is not a node.
    3: port illegal on current node (e.g., free on the node, but taken by another host).
    4: port free
    5: current process' port
    """
    pdict = {}
    for port in ports:
        try:
            logging.info(f'\nChecking for node at {ip}:{port}...')
            sock.connect((ip, port))
            sock.sendall('ping'.encode())
            response = sock.recv(1024).decode()
            if response:
                logging.info(f'\n{response}.')
                logging.info(f'\nNode serving at port {ip}:{port}.')
                pdict[port] = 1
            else:
                logging.info(
                    f'\nSomething is serving at {ip}:{port} (but its not a node).')
                pdict[port] = 2
        except socket.error:
            logging.info(f'\nPort {port} free on {ip}.')
            pdict[port] = 4
    return pdict


def parse():
    """
    Parses node type passed from start script.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'type', help='The type of the node. Valid options include "head", "seed", and "full"')
    args = parser.parse_args()
    return args


def main():
    """
    Main process for initial network scanner.
    """
    logging.basicConfig(level=logging.INFO)
    logging.info('\nScanning network for available ports...')

    # Initialize network data
    network = {
        "local": {},
        "peers": {}
    }

    # Initialize list of possible ports
    PORTS = list(range(7000, 7005))

    # Open UDP socket connection with GC public DNS for local machine IP address
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.connect(("8.8.8.8", 80))
        LOCAL_IP = str(s.getsockname()[0])

    # nodes is a dict of dicts; each top-level key is an IP address; each bottom-level key is a port, with a value in 0-5.
    # nodes = {LOCAL_IP: dict.fromkeys(PORTS, 0)}
    nodes = {}

    # Set port from type input
    args = parse()
    if args.type == 'head':
        local_port = PORTS[0]
    elif args.type == 'seed':
        local_port = PORTS[1]
    else:
        local_port = PORTS[2]

    # Attempt TCP socket connections on local machine ports
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        nodes[LOCAL_IP] = scan(LOCAL_IP, PORTS, sock)
        for port in PORTS[PORTS.index(local_port):]:
            if nodes[LOCAL_IP][port] in [1, 2]:
                logging.info(f'\nPort {port} occupied on local machine.')
                if port == PORTS[0]:
                    logging.info(
                        f'\nOnly one head node is allowed on the blockchain. Demoting to seed node.')
                    continue
                elif port == PORTS[1]:
                    logging.info(
                        f'\nOnly one seed node is allowed on any one machine. Demoting to full node.')
                    continue
                elif port == PORTS[-1]:
                    logging.info(
                        f'\nNo node ports are available on local machine! Free up a port between 7002 and 7004, and try again.')
                    return
            else:
                logging.info(f'\nPort {port} is available on local machine.')
                local_port = port
                logging.info(
                    f'\nLocal node set port to {local_port}. Scanning network for existing nodes.')
                break
        hosts = scapy.arping(LOCAL_IP)
        for host in hosts[0]:
            ip = host[1][0].src 
            if ip == LOCAL_IP:
                continue
            nodes[ip] = scan(ip, PORTS, sock)
            if nodes[ip][PORTS[0]] is 1 and local_port == PORTS[0]:
                logging.info(
                    f'\nHead node port in use by node on machine at {ip}.')
                logging.info(
                    f'\nOnly one head node is allowed on the blockchain. Demoting local machine node.')
                if nodes[LOCAL_IP][PORTS[1]] is 4:
                    logging.info(
                        f'\nSeed node port free on machine on local machine at {LOCAL_IP}. Demoting to seed node.')
                    local_port = PORTS[1]
                else:
                    logging.info(
                        f'\nSeed node port in use by node on local machine at {LOCAL_IP}.')
                    logging.info(
                        f'\nOnly one seed node is allowed on any one machine. Demoting to full node.')
                    for port in PORTS[2:]:
                        if nodes[LOCAL_IP][port] is 4:
                            local_port = port
                            break
                        if port == PORTS[-1]:
                            logging.info(
                                f'\nNo node ports are available on local machine! Free up a port between 7002 and 7007, and try again.')
                            return

    nodes[LOCAL_IP][local_port] = 5
    local_address = (LOCAL_IP, local_port)
    network["local"] = local_address
    network["peers"] = nodes

    # After scanning, store results using NodeStorage
    try:
        storage = NodeStorage(None)  # No Redis client needed for file operations
        storage.save_network_config(network)  # New method to handle file writing
        logging.info("Network configuration saved successfully")
    except ConfigurationError as e:
        logging.error(f"Failed to save network config: {e}")
        raise

    return


if __name__ == '__main__':
    main()
