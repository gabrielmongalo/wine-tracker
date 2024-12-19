#!/bin/bash

# Set up Python virtual environment
PYTHON_VERSION=${PYTHON_VERSION:-"python3.12"}
VENV_DIR=".venv"

echo "Setting up Python environment using $PYTHON_VERSION..."

# Check if Python is installed
if ! command -v $PYTHON_VERSION &> /dev/null; then
    echo "$PYTHON_VERSION not found. Please install Python 3.12."
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "$VENV_DIR" ]; then
    $PYTHON_VERSION -m venv $VENV_DIR
    echo "Virtual environment created in $VENV_DIR"
fi

# Activate the virtual environment
source $VENV_DIR/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies from requirements.txt if available
if [ -f "requirements.txt" ]; then
    echo "Installing dependencies from requirements.txt..."
    pip install -r requirements.txt
else
    echo "Installing specific dependencies..."
    pip install \
        fastapi>=0.100.0 \
        uvicorn[standard]>=0.23.2 \
        qdrant-client[fastembed]>=1.12.1 \
        pytest>=7.4.2 \
        datasets>=2.14.0,<3.0.0

fi

echo "Environment setup complete. Activate it with: source $VENV_DIR/bin/activate"
