# consensus.py
# Implements longest-chain consensus algorithm
import requests

def validate_chain(host, nodes):
    longest_chain = None
    n = len(chainchain)

    for node in nodes:
        chain = requests.get('{}:{}/chain'.format(node["port"].))
        length = response.json()['length']
        chain = response.json()['chain']
        if length > n and blockchain.is_valid_chain(chain):
            n = length
            longest_chain = chain

    if longest_chain:
        blockchain = longest_chain
        return True

    return False
