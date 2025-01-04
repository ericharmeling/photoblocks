import socket
import logging
import json
from scapy.all import arping
from photoblocks.exceptions import NetworkError, ValidationError, ConfigurationError

def validate_node_type(node_type):
    """Validate node type input"""
    valid_types = ['head', 'seed', 'full']
    if node_type not in valid_types:
        raise ValidationError(f"Invalid node type. Must be one of: {', '.join(valid_types)}")
    return node_type

def get_local_ip():
    """Get local IP address with error handling"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            return str(s.getsockname()[0])
    except socket.error as e:
        raise NetworkError(f"Failed to determine local IP: {e}")

def scan_network(local_ip):
    """Perform network scan with error handling"""
    try:
        hosts = arping(local_ip)
        if not hosts[0]:
            logging.warning("No hosts found on network")
        return hosts
    except Exception as e:
        raise NetworkError(f"Network scan failed: {e}")

def write_network_config(network_data):
    """Write network configuration with error handling"""
    try:
        with open("./photoblocks/network.json", mode="w") as f:
            json.dump(network_data, f, indent=2)
    except (IOError, OSError) as e:
        raise ConfigurationError(f"Failed to write network configuration: {e}") 