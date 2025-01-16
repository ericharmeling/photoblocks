#!/bin/bash
set -e

usage() { echo "Usage: start.sh <head|seed|full> <--skip-init>";}

# Validate input
if [ -z "$1" ]; then
    echo "Error: Node type required (head, seed, or full)"
    exit 1
fi

# Run network scanner on host machine if not skipping init
if [ "$2" != "--skip-init" ]; then
    python3 scan.py "$1"
fi

# Start containers with network config from host
docker-compose up --build -d

# Follow logs
docker-compose logs -f photoblocks
