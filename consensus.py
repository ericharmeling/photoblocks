# consensus.py
# Implements longest-chain consensus algorithm
import requests


def consensus(blockchain):

    longest_chain = None
    n = len(blockchain.chain)

    for node in blockchain.nodes:
        response = requests.get('http://{}/chain'.format(node))
        length = response.json()['length']
        chain = response.json()['chain']
        if length > n and blockchain.is_valid_chain(chain):
            n = length
            longest_chain = chain

    if longest_chain:
        blockchain = longest_chain
        return True

    return False
