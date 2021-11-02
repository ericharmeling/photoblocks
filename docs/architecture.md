# Photoblocks Architecture Specification

This document provides an architecture specification for the Photoblocks application.

The following sections provide more detail about specific aspects of the application:

- [Nodes](#nodes)
- [Networking](#networking)
- [Mining](#mining)

## Nodes

Photoblocks is a blockchain application. Each instance of the application participates as a node in a peer-to-peer network of other nodes.

### Node types

As is common in traditional blockchains, different types of nodes take on more responsibility than others. The different types of nodes on the network are as follows:

- [Full nodes](#full-nodes)
- [Seed nodes](#seed-nodes)
- [Head node](#head-node)

Each node technically runs the [same main processes](#main-node-process). Logic throughout the application determines node behavior, based on the node type.

#### Full nodes

Full nodes store the entirety of the blockchain. They participate in consensus and continuously validate their local copy of the blockchain, and their list of peers in the network, against other nodes in the network. 

#### Seed nodes

Seed nodes are full nodes that serve on a specific port. The seed node ports (including the head node port) are the first ports from which data is requested from a client socket. In this respect, seed nodes function a little like load-balancers. 

Only a select number of nodes on any given machine can be a seed node.

#### Head node

The head node is the seed node that creates the blockchain and the first block (i.e., the Genesis Block). The head node serves the blockchain at the first seed port. 

There is only one head node for the blockchain.

### Main node process

The main node process does the following:

- Connects to a running Redis database server, for storing node and blockchain data locally. For details, see [Local node storage](#local-node-storage).
- Starts a websocket server that pings other nodes for consensus. For details, see [Sockets](#sockets).
- Starts a websocket server that broadcasts local data on the network. For details, see [Sockets](#sockets).

### Local node storage

Each node records its copy of the blockchain, and some networking metadata, on a local Redis server.

## Networking

In all blockchain architectures, maintaining a peer-to-peer network is integral to maintaining data integrity. Each node that joins the network needs to know about the peers on the network, both before joining the network, and after joining. 

### Start script

To start a local blockchain, first run the `start.sh` script, with `head` as the primary argument.

The `start.sh` script does the following:

- Starts a [network scanner](#scanner).
- Creates a Docker container, which runs a the [main node process](#main-process) and a [local Redis server](#local-database).

### Scanner

The initial scanner ([`scan.py`](../scan.py)) maps out the machines on the network, and determines which ports are free and which ports are taken, for each host in the network. This information informs the node's type and port, and it also initializes the subsequent (and continual) [consensus checks](#consensus).

The scanner does the following:

1. Attempts to open a socket connection to all ports on the same host, to determine if other nodes are running at a given port, on the same machine. Running multiple nodes on a single machine can be helpful for debugging.

2. Runs an [ARP](https://en.wikipedia.org/wiki/Address_Resolution_Protocol) scan on the network, and then attempts to open a socket connection to each photoblock-serving host/port combination on the network.

3. Returns a three-level dictionary of all the detected machines running on the network, with information about each host/port combination.

### Consensus

After the network has been mapped, the main python process (`main.py`) runs on the node until manually terminated.

#### Sockets

To ensure that the blockchain on a given node is, in fact, valid, the blockchain must be validated by a consensus of the nodes on the network. Photoblocks implements a consensus algorithm with [BSD sockets](https://docs.python.org/3/library/socket.html).

##### Client socket

All nodes run a continual client socket on a background thread. 

##### Server socket

All nodes run a continual server socket on a background thread. 

## Mining 

### Mining API

The Photoblocks mining API is the interface by which users can create blocks in the block chain (and receive coins).

This API is only accessible to users with full, running nodes. Each request made through the API must be authenticated.

### Mining Authentication

In order to interact with the mining API, the user request must be authenticated.

To authenticate, the user passes the unique ID of the full node and their username and passcode. The credential management system validates the credentials in the request, and checks the blockchain to see if the credentials match the node ID stored on the chain.

### Proof-of-Work

Nodes create new blocks by solving a Proof-of-Work (PoW) algorithm. To solve the PhotoBlocks PoW, the node finds the nonce value that matches the new block's hashed data to a simple pattern. Once the hashed data matches the pattern, the node has solved the PoW algorithm, the block is created, and the miner is awarded a coin.

Photoblocks uses image recognition to simplify the PoW. Rather than attempting to mine with brute-force, a miner can send an image and a label to the blockchain to the network. Each candidate image is sent through a trained TensorFlow image-recognition neural network. If the label that you provide matches a string in output of the scored image, your node will attempt to solve a simplified PoW algorithm. 

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
