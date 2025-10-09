#!/usr/bin/env bash
set -euo pipefail

# Generate the site into ./private
python3 -m src.main

# Serve ./private on port 8888
python3 -m http.server 8888 --directory private
