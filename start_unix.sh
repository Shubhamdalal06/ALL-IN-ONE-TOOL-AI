#!/bin/bash

# AI All-in-One Tool Startup Script for macOS/Linux

echo "========================================"
echo "AI All-in-One Data Tool - Startup"
echo "========================================"
echo ""

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo ""
fi

# Activate virtual environment
source venv/bin/activate

# Install/update dependencies
echo "Installing dependencies..."
pip install -r backend/requirements.txt > /dev/null 2>&1

# Create data directory
mkdir -p data

# Create .env if it doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    cp .env.example .env
    echo ""
    echo "IMPORTANT: Edit .env and add your ANTHROPIC_API_KEY"
    echo ""
fi

# Start backend
echo ""
echo "Starting backend server on http://localhost:8000"
echo ""
cd backend
python main.py
