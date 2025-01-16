#!/bin/bash
set -e

# Create and activate virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install test dependencies
if [[ $(uname -m) == 'arm64' ]]; then
    # For Apple Silicon Macs
    pip3 install --upgrade pip
    pip3 install tensorflow-macos
else
    # For Intel Macs and other systems
    pip3 install tensorflow
fi

pip3 install -r requirements.txt

# Run pytest with coverage
python3.11 -m pytest

# Deactivate virtual environment
deactivate 