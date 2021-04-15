#!/bin/bash

usage() { echo "Usage: start.sh <head|seed|full>";}

python3 -m pip install python-nmap
export PORT=$(scan.py $1)
docker-compose up
