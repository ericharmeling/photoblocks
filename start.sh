#!/bin/bash

usage() { echo "Usage: start.sh <head|seed|full|light>";}

docker run -d -p 6379:6379 --name pbr redis redis-server --appendonly yes
python3 -m venv pbenv
source $(pwd)/pbenv/bin/activate
python3 -m pip install -r requirements.txt
python3 main.py $1
