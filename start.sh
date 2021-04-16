#!/bin/bash

usage() { echo "Usage: start.sh <head|seed|full>";}
export NETPACK=$(scan.py $1)
docker-compose up
