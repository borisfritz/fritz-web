#!/usr/bin/env bash
set -euo pipefail

# Build site for GitHub Pages into ./docs with base path /fritz-web/
python3 -m src.main "/fritz-web/"
