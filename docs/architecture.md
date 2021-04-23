# Photoblocks Architecture Specification

This document provides an architecture specification for the Photoblocks application.

## Start script

The `start.sh` script does the following:

- Starts a [network scanner](#initial-scanner).
- Starts a Docker container, which runs a the [main node process](#main-process) and a [local Redis server](#local-database).

## Networking

In all blockchain architectures, establishing a peer-to-peer network is integral to maintaining data integrity.

### Initial scanner

The initial scanner ([`scan.py`](../scan.py)) maps out the machines on the network, and determines which ports are free and which ports are taken, for each host in the network.

1. The scanner first attempts to open a socket connection to all ports on the same host, to determine if other nodes are running at a given port.

2. The scanner then runs an ARP scan and returns a list of all of the detected machines running on the 

### Consensus

The 

Every node runs a script (`main.py`) that starts the following processes on that node:

- A websocket server that pings other nodes for consensus. For details, see [Networking](#networking).
- A Redis database server, for storing node and blockchain data locally. For details, see [Storage](#storage).

Mobile nodes also feature a lightweight REST API. For details, see [Interfaces](#interfaces).

In the future, it would be nice to also have a Docker container, loaded with all dependencies (Redis, non-standard python libraries, etc.).

## Nodes

### Node types

As is common in traditional blockchains, different types of nodes take on more responsibility than others. The different types of nodes on the network are as follows:

- [Head node](#head-node)
- [Seed nodes](#seed-nodes)
- [Full nodes](#full-nodes)

Each node runs the [same main processes](#main-process).

#### Head node

The head node is the seed node that creates the blockchain and the first block (i.e., the Genesis Block). The head node serves the blockchain at the first seed port. There is only one head one.

### Full nodes

Full nodes store the entirety of the blockchain. They participate in the consensus algorithm, continuously validating the blockchain against other nodes in the network. 

### Seed nodes

Seed nodes are full nodes that listen for new nodes to which to send the validated blockchain and peerlist. In addition to performing the functions of a full node (i.e., store and validate the blockchain), they catalogue new nodes on the network and respond to requests from new nodes scanning the network for existing nodes. In this respect, seed nodes function a little like load-balancers.

<!-- 
## Registration

There are two types of accounts in PhotoBlocks: *Trader* and *Miner*.
Traders can only trade, and miners can trade and mine.

### *Trader*
To register as a trader, navigate to the "Users" page of the PhotoBlocks web interface. After you fill out some forms, you'll be given a public and private key. Your name and public key are
visible to the public. Keep the private key private.

### *Miner*
To mine blocks, you need to register your node. To register a node, navigate to the "Nodes" page, and fill out the forms.

## Mining
To start mining blocks on a node, navigate to the "Mine" page of the PhotoBlocks web interface. You'll be asked to provide the 
following:
* The miner's public key
* The node's ID
* A candidate image to be placed in the candidate block
* A label for the candidate image
* A label for the image on the last block in the chain

Each candidate image is sent through a basic TensorFlow image-recognition neural network. If the label that you provide matches a string in output of the
scored image, your node will start to solve the PoW algorithm. 

Nodes create new blocks by solving a Proof-of-Work (PoW) algorithm. To solve the PhotoBlocks PoW, the node finds 
the nonce value that matches the new block's hashed data to a simple pattern. Once the hashed data matches the pattern, the node has 
solved the PoW algorithm and the miner is awarded a coin.
 
## Trading
To start trading coins, navigate to the "Trade" page of the PhotoBlocks web interface. You'll be asked to provide the following:
* The sender's private and public key
* The recipient's public key
* The quantity of coins to trade
 
After you confirm a transaction, the transaction data is added to the transaction buffer on the blockchain. When a new 
block is mined, valid transactions are moved from the buffer to the block.
-->

## Recommended Reading

* [A Practical Introduction to Blockchain with Python](http://adilmoujahid.com/posts/2018)
* [Learn Blockchains by Building One](https://hackernoon.com/learn-blockchains-by-building-one-117428612f46)
* [ibm_blockchain](https://github.com/satwikkansal/ibm_blockchain)
* [An Intro to Threading in Python](https://realpython.com/intro-to-python-threading/)
* [Socket Programming in Python](https://realpython.com/python-sockets/)
