###
# Utility functions for networking
###
import requests
from requests import HTTPError


# Scan for nodes on network
def scan(u, p, n):
    try:
        response = requests.get(url=u + p)
    except HTTPError as http_error:
        print(f'HTTP error: {http_error}\n Using {p} as node port\n')
        return p
    except Exception as error:
        print(f'Error: {error}\n')
        return p
    else:
        n[p] = (response.json())
        p += 1
        scan(u, p+1)


# Handle
def hand(f):
    try:
        f
    except HTTPError as http_error:
        print(f'HTTP error: {http_error}\n')
    except Exception as error:
        print(f'Error: {error}\n')
