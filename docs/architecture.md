# Photoblocks Architecture Specification

This document provides an architecture specification for the Photoblocks application.

## Networking

To ensure the integrity of the data stored on a blockchain, the machines that comprise a blockchain's network must share computation and storage responsibilities in a way that limits single points of failure. Sharing computational and storage responsibilities (i.e., participating in the consensus algorithm and storing and validating the blockchain itself) across nodes on a network is not possible in a conventional, centralized network architecture of many requesting clients and few responding servers. In order for a blockchain to exist, a large number of the nodes on the network must act as both client and server (i.e., as peers). Peer-to-peer networking is integral to all blockchain architectures. 

Because this application is designed for mobile clients as the primary end users, I propose a semi-distributed blockchain network, wherein a distributed network of computers function as nodes in a traditional blockchain (i.e., peers in a peer-to-peer network), and mobile clients can access the blockchain through a representative node (i.e., a mobile "server") that only partially participates in mining and consensus. 

As is common in traditional blockchains, different types of nodes take on more responsibility than others. The different types of nodes on the network are as follows:

- Mobile nodes
- Full nodes
- Seed nodes
- A head node

Each node runs the [same few processes](#node-processes), with slight variations in their functions in the network.

### Mobile nodes

The primary function of mobile nodes is to serve as representatives in the blockchain for mobile clients. As such, mobile nodes serve a simple REST API that accepts mining requests from mobile applications, and then performs the Proof-of-Work algorithm on behalf of the mobile client. Light nodes are the most server-like of the nodes on the network.

In addition to performing the mobile PoW, light nodes store a subset of the blockchain that they regularly check against data on larger nodes, for consensus.

### Full nodes

Full nodes store the entirety of the blockchain. They participate in the consensus algorithm, continuously validating the blockchain against other nodes in the network. 

### Seed nodes

Seed nodes are full nodes that listen for new nodes to which to send the validated blockchain and peerlist. In addition to performing the functions of a full node (i.e., store and validate the blockchain), they catalogue new nodes on the network and respond to requests from new nodes scanning the network for existing nodes. In this respect, seed nodes function a little like load-balancers.

### Head node

The head node is the seed node that creates the blockchain and the first block (i.e., the Genesis Block). The head node serves the blockchain at the first seed port. There is only one head one.

## Node processes

Every node runs a script (`main.py`) that starts the following processes on that node:

- A websocket server that pings other nodes for consensus. For details, see [Networking](#networking).
- A Redis database server, for storing node and blockchain data locally. For details, see [Storage](#storage).

Mobile nodes also feature a lightweight REST API. For details, see [Interfaces](#interfaces).

In the future, it would be nice to also have a Docker container, loaded with all dependencies (Redis, non-standard python libraries, etc.).

## Networking

### Client sockets

Each node is represented in memory by a Node object (defined in `models/node.py`). The Node class contains some property functions that open up a client socket connection with any existing seed nodes on the network. Client socket connections are opened and closed each time 

### Server sockets 


### Consensus


## Storage

Each node runs a Redis server locally. Redis makes storing pythonic objects more convenient than SQL databases, at the cost of some amount of row integrity. The integrity of stored data isn't as important in the context of a blockchain, as the data is continually validated.

Each node's Redis server stores the following components:

- Node metadata
- Blockchain data

### Node metadata storage

Each `Node` object has a corresponding *pack* (represented by the `Node.pack` attribute). A pack contains the following information:

- Node type (`Node.node_type`)
- Node key (`Node.node_key`)
- Node ID (`Node.node_id`)
- Node port (`Node.port`)

All nodes store the node packs of all other nodes on the network. The packs are stored in Redis with the *node ID* as the key and a string representation of the *node pack* as the value.

In addition to storing all node packs at the very top of the database hierarchy, each node stores a full list of all nodes in the network (i.e., the "peer list").

### Blockchain data storage

Like `Node` objects, `Block` objects have corresponding packs, which contain the following information:

- Block type
- Block id
- Block hash
- Last block hash

All nodes store all blocks.

## Interfaces

 types of users:

- Mobile users
- Miners
- Operators

Each user type corresponds to a node type, and each node type has a user-specific interface.

### Mobile interface

The primary interface for mobile users is the mobile application. This application 

### Miner interface

### Operator interface


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
