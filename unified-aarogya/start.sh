#!/bin/bash

# Aarogya Unified Startup Script
echo "🏥 Starting Aarogya Unified Health Platform..."

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "Creating Python virtual environment..."
    python -m venv .venv
fi

# Activate virtual environment
echo "Activating Python virtual environment..."
source .venv/bin/activate

# Install Python dependencies
echo "Installing Python dependencies..."
cd backend
pip install -r requirements.txt
cd ..

# Install Node dependencies if not already installed
if [ ! -d "node_modules" ]; then
    echo "Installing root Node dependencies..."
    npm install
fi

if [ ! -d "frontend/node_modules" ]; then
    echo "Installing frontend Node dependencies..."
    cd frontend
    npm install
    cd ..
fi

# Start both servers
echo "🚀 Starting both frontend and backend servers..."
echo "Frontend: http://localhost:5174"
echo "Backend: http://localhost:5001"
echo "Press Ctrl+C to stop both servers"

npm run dev
