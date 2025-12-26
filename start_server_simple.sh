#!/bin/bash

cd "$(dirname "$0")"

echo "Starting FastAPI server..."
echo "If you see errors, check:"
echo "  1. Dependencies are installed: pip3 install fastapi uvicorn sqlalchemy python-dotenv"
echo "  2. .env file exists with DATABASE_URL and JWT_SECRET"
echo "  3. Port 8000 is not already in use"
echo ""
echo "Starting on http://0.0.0.0:8000"
echo "Press CTRL+C to stop"
echo ""

python3 -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

