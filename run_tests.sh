#!/usr/bin/env bash

# run_tests.sh — Automates setup and test execution in a CI/CD-friendly way
set -e  # Exit on any command failure

echo "Checking Python 3.9 installation..."
if ! python3.9 --version &>/dev/null; then
  echo "Python 3.9 is not installed. Attempting installation using pyenv..."
  if ! command -v pyenv &>/dev/null; then
    echo "pyenv not found. Please install Python 3.9 manually or install pyenv."
    exit 1
  fi
  pyenv install 3.9.18
  pyenv global 3.9.18
else
  echo "Python 3.9 found."
fi

# Setup virtual environment
echo "Setting up virtual environment..."
if [ ! -d "venv" ]; then
  python3.9 -m venv venv
fi
source venv/bin/activate

# Upgrade pip and install dependencies
echo "Installing requirements..."
pip install --upgrade pip
if [ -f "requirements.txt" ]; then
  pip install -r requirements.txt
else
  echo "requirements.txt not found. Installing manually known packages..."
  pip install dash plotly pandas pytest selenium
fi

# Run the test suite
echo "Running tests..."
pytest tests/test_app.py
status=$?

# Deactivate environment
deactivate

echo "Test script completed with status code: $status"
exit $status
