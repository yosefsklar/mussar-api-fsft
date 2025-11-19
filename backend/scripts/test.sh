#!/usr/bin/env bash

set -e
set -x

# Ensure uv is in PATH
export PATH="$HOME/.local/bin:$PATH"

# Install uv if not already installed
if ! command -v uv &> /dev/null; then
    echo "uv not found, installing..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
fi

# Sync dependencies with Python 3.12 (creates venv if needed and installs from pyproject.toml)
uv sync --python 3.12

# Activate virtual environment and run tests with coverage
source .venv/bin/activate
coverage run -m pytest tests/
coverage report
coverage html --title "${@-coverage}"