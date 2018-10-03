# PhotoBlocks

## Contents
* [Overview](#overview)
* [Prerequisites](#prerequisites)
* [Registration](#registration)
* [Mining](#mining)
* [Trading](#trading)
* [Recommended Reading](#recommended-reading)

## Overview
PhotoBlocks is a blockchain platform built on an image labeling mining system. You can earn coins by mining blocks, and you can 
trade coins with others.


## Server Prerequisites
To run the PhotoBlocks server, you'll need the following third-party libraries:
* `flask`
* `geocoder`
* `tensorflow`
* TensorFlow's [`classify_image`](https://www.tensorflow.org/tutorials/image_recognition) module

I recommend that you start the server from a virtual environment. With Python 3.4+, run the following from the terminal:
```shell
$ cd my-directory
$ python -m venv pbenv
$ source pbenv/bin/activate
(pbenv)
```

If you're using a bash shell (e.g. Git bash) on Windows, source the virtual environment from the Scripts directory:
```shell
$ source pbenv/Scripts/activate
(pbenv)
```

You can `pip install` the `flask`, `geocoder`, and `tensorflow` libraries to the virtual environment.

The `classify_image` module is not available on PyPi. You need to clone the `models` repository to disk. You can find the module at `models/tutorials/image/imagenet/classify_image.py`.

To start a new PhotoBlocks server, run the following:
```shell
python server.py
```

The terminal should return the following:
```shell
* Serving Flask app "server" (lazy loading)
 * Environment: production
   WARNING: Do not use the development server in a production environment.
   Use a production WSGI server instead.
 * Debug mode: on
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: some-pin-number
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

You can then navigate to http://127.0.0.1:5000/ in any web browser and interact with the front-end of the PhotoBlocks server.

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

## Recommended Reading
I found the following resources inspirational and extremely helpful. Thank you, Daniel van Flymen, Adil Moujahid, and Satwik Kansal!

* [A Practical Introduction to Blockchain with Python](http://adilmoujahid.com/posts/2018)
* [Learn Blockchains by Building One](https://hackernoon.com/learn-blockchains-by-building-one-117428612f46)
* [ibm_blockchain](https://github.com/satwikkansal/ibm_blockchain)
