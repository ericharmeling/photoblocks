#!/bin/bash

usage() { echo "Usage: start.sh <head|seed|full> <--skip-init>";}
if [ "$2" != "--skip-init" ]; then
  python scan.py "$1"
fi
docker-compose up
