#!/bin/bash

cd "$(dirname "$0")"

echo "=========================================="
echo "Starting FastAPI Backend Server"
echo "=========================================="

if [ ! -f .env ]; then
    echo "⚠️  Warning: .env file not found!"
    echo "   The server may not work without DATABASE_URL and JWT_SECRET"
    echo "   Create a .env file with these variables (see .env.example)"
    echo ""
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

if ! python3 -m uvicorn --version &> /dev/null; then
    echo "Installing uvicorn and fastapi..."
    python3 -m pip install uvicorn fastapi
fi

if command -v netstat &> /dev/null; then
    if netstat -tuln 2>/dev/null | grep -q ":8000 "; then
        echo "⚠️  Warning: Port 8000 appears to be in use"
        echo "   Another process may be using this port"
        echo ""
    fi
fi

echo ""
echo "Running pre-flight checks..."
if python3 check_server.py; then
    echo ""
    echo "Starting server on http://0.0.0.0:8000"
    echo "Press CTRL+C to stop the server"
    echo "=========================================="
    echo ""
    
    python3 -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
else
    echo ""
    echo "⚠️  Pre-flight checks failed. Please fix the issues above."
    echo "   You can still try to start the server, but it may not work correctly."
    echo ""
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo ""
        echo "Starting server on http://0.0.0.0:8000"
        echo "Press CTRL+C to stop the server"
        echo "=========================================="
        echo ""
        python3 -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
    else
        exit 1
    fi
fi

