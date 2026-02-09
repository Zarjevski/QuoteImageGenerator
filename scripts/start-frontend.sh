#!/bin/bash
# Simple script to start just the frontend

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
# Change to project root (one level up from scripts folder)
cd "$SCRIPT_DIR/.."

cd client
npm start
