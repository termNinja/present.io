#! /usr/bin/env bash

echo "This script will create a symbolic link to the file presention.py, so make sure you don't delete this directory later on."

# Get the current directory from which the script was called.
dir=$(pwd)

# Create a symbolic link so the user can later invoke the script from anywhere.
sudo ln -s $dir/presentio.py /usr/bin/presentio
