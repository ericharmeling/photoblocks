# PhotoBlocks

## Contents
* [Overview](#overview)
* [Mining](#mining)
* [Trading](#trading)

## Overview

PhotoBlocks is a blockchain built on an image labeling mining system. You can earn coins by mining blocks, and you can 
trade coins with others.

To learn more about PhotoBlocks, and to mine and trade on the PhotoBlocks platform, access the PhotoBlocks web nterface.

## Mining
Full nodes create new blocks by solving a Proof-of-Work (PoW) algorithm. To solve the PhotoBlocks PoW, the node finds 
the nonce value that matches the new block's hashed data to a pattern.

The algorithm difficulty decreases if you provide:
* A label for an image that the server provides
* A unique image and that image's corresponding label

## Trading
To trade PhotoBlock coins:

* Navigate to the "Trade" page of the PhotoBlocks interface. 
* Provide the sender's private and public key, the recipient's public key, and the quantity in the "Transactions" form.
* Click **Confirm** to process the transaction.
 
After you confirm a transaction, the transaction data is added to the transaction buffer on the blockchain. When a new 
block is mined, valid transactions are moved from the buffer to the block.

## Recommended Reading
I found the following resources inspirational and extremely helpful. Thank you, Daniel van Flymen, Adil Moujahid, and Satwik Kansal!

* [A Practical Introduction to Blockchain with Python](http://adilmoujahid.com/posts/2018)
* [Learn Blockchains by Building One](https://hackernoon.com/learn-blockchains-by-building-one-117428612f46)
* [Develop a blockchain application from scratch in Python](https://www.ibm.com/developerworks/cloud/library/cl-develop-blockchain-app-in-python/index.html)
