# Photoblocks

Photoblocks is an in-development blockchain platform built on an image-labeling mining system.

For a more detailed architecture specification, see [docs/architecture.md](docs/architecture.md).

## Requirements

- Docker
- Python 3

## Start a blockchain

To start a node on the blockchain, do the following:

```
$ ./start.sh <type>
```

Where `type` specifies the type of node that you want to start. For example, to start the head node of a blockchain (i.e., to start a new blockchain):

```
$ ./start.sh head
```
