#!/usr/bin/env bash

set -e

echo "Setting up Password Security Platform..."

# Create virtual environment
if [ ! -d "venv" ]; then
  echo "Creating virtual environment..."
  python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "Installing requirements..."
pip install -r requirements.txt

# Create necessary directories
echo "Creating project directories..."
mkdir -p data/wordlists
mkdir -p data/reports
mkdir -p logs

# Create .env if not exists
if [ ! -f ".env" ]; then
  echo "Creating .env file..."
  cat <<EOF > .env
HOST=127.0.0.1
PORT=8000
DEBUG=true
LOG_LEVEL=INFO
EOF
fi

echo "Setup complete!"
echo "Run the app using: ./scripts/run.sh"
