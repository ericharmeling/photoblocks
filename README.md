# Photoblocks

## Contents

* [Overview](#overview)
* [Prerequisites](#prerequisites)
* [Registration](#registration)
* [Mining](#mining)
* [Trading](#trading)
* [Recommended Reading](#recommended-reading)

## Overview

Photoblocks is an in-development blockchain platform built on an image-labeling mining system.

For a more detailed architecture specification, see [docs/architecture.md](docs/architecture.md).

## Start a blockchain

To start the head node of a blockchain, do the following:

1. Start a database server. 

    This database will store the blockchain and a list of all nodes on the network. Photoblocks uses [redis](https://github.com/redis/redis). 
    
    Get redis, and then configure and start a server to run at port .


1. Make a config file with `utils/makeconfig.py`.

1. Start a virtual environment and download the dependencies.

1. Start a photoblocks process.

To start a new Photoblocks blockchain, run the following:

~~~ shell
python3 main.py --new
~~~

To join an existing Photoblocks blockchain:

~~~ shell
python3 main.py --join --url '<gateway address>'
~~~
