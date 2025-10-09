#!/usr/bin/env bash
set -euo pipefail

# Run Python unit tests
# Usage:
#   - WSL/Linux/macOS: bash ./test.sh
#   - Windows PowerShell: use `bash ./test.sh` (requires WSL) or run tests from PyCharm
python3 -m unittest discover -s tests -p "test_*.py" -v
