# PhotoBlocks

## Contents
* [Overview](#overview)
* [Registration](#registration)
* [Mining](#mining)
* [Trading](#trading)
* [Recommended Reading](#recommended-reading)

## Overview
PhotoBlocks is a blockchain platform built on an image labeling mining system. You can earn coins by mining blocks, and you can 
trade coins with others.

To learn more about PhotoBlocks, and to mine and trade on the PhotoBlocks platform, access the PhotoBlocks web interface.

To start a new PhotoBlocks server, run `python server.py` from the command line.

## Registration
To mine blocks and trade coins on PhotoBlocks, you need to be a registered user. To register as a user, navigate to the "Users" page 
of the PhotoBlocks web interface. After you fill out some forms, you'll be given a public and private key. Your name and public key are 
visible to the public. Keep the private key private.

To mine blocks, you also need to register your node. To register a node, navigate to the "Nodes" page, and fill out the forms.

## Mining
To start mining blocks on a node, navigate to the "Mine" page of the PhotoBlocks web interface. You'll be asked to provide the 
following:
* The miner's public key
* The node's ID
* A candidate image to be placed in the candidate block
* A label for the candidate image
* A label for the image on the last block in the chain

Each candidate image is sent through a basic image-recognition neural network provided by
[TensorFlow](https://www.tensorflow.org/tutorials/image_recognition). If the label that you provide matches a string in output of the 
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

## Recommended Reading
I found the following resources inspirational and extremely helpful. Thank you, Daniel van Flymen, Adil Moujahid, and Satwik Kansal!

* [A Practical Introduction to Blockchain with Python](http://adilmoujahid.com/posts/2018)
* [Learn Blockchains by Building One](https://hackernoon.com/learn-blockchains-by-building-one-117428612f46)
* [Develop a blockchain application from scratch in Python](https://www.ibm.com/developerworks/cloud/library/cl-develop-blockchain-app-in-python/index.html)
