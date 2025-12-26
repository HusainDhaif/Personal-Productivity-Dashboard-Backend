# How to Start the Backend Server

## Quick Start

Open a terminal in WSL (Windows Subsystem for Linux) and run:

```bash
cd /home/husaindhaif/code/ga/projects/Personal-Productivity-Dashboard-Backend

# Install dependencies if needed
pip3 install fastapi uvicorn sqlalchemy psycopg2-binary bcrypt passlib pyjwt python-dotenv pydantic[email]

# Start the server (accessible on both 127.0.0.1:8000 and localhost:8000)
python3 -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Alternative: If you prefer to bind only to localhost
# python3 -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

Or use the startup script:
```bash
chmod +x start_server.sh
./start_server.sh
```

## Verify Server is Running

Once started, you should see output like:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

You can test it by visiting:
- http://localhost:8000/ (root endpoint)
- http://127.0.0.1:8000/ (root endpoint)
- http://localhost:8000/docs (API documentation)
- http://127.0.0.1:8000/docs (API documentation)
- http://localhost:8000/health (health check)
- http://127.0.0.1:8000/health (health check)

Or using curl:
```bash
curl http://localhost:8000/
curl http://127.0.0.1:8000/health
```

## Test Server Connection

Use the test script to verify the server is running:

```bash
# Install requests if needed
pip3 install requests

# Run the test script
python3 test_server_connection.py
```

Or test manually:
```bash
curl http://127.0.0.1:8000/health
curl http://localhost:8000/health
```

## Troubleshooting

### 1. **Cannot connect to server at http://127.0.0.1:8000**

**Step 1: Verify the server is running**
- Check your terminal for the message: `INFO: Uvicorn running on http://0.0.0.0:8000`
- If you don't see this, the server is not running. Start it using the commands above.

**Step 2: Test the connection**
```bash
# In WSL terminal
curl http://127.0.0.1:8000/health

# Or use the test script
python3 test_server_connection.py
```

**Step 3: Check for common issues**

- **WSL Networking**: If using WSL, try accessing from Windows browser: `http://localhost:8000/docs`
- **Port already in use**: Check if another process is using port 8000
  ```bash
  # In WSL
  netstat -tuln | grep 8000
  # Or
  lsof -i :8000
  ```
- **Firewall**: Windows Firewall might be blocking. Try temporarily disabling it to test.
- **Wrong host binding**: Make sure you're using `--host 0.0.0.0` (not `127.0.0.1`) to allow connections from Windows

**Step 4: Try alternative ports**
If port 8000 is blocked, try a different port:
```bash
python3 -m uvicorn main:app --reload --host 0.0.0.0 --port 8001
```
Then update your frontend to use `http://127.0.0.1:8001`

### 2. **CORS errors**

The server is now configured to allow requests from any localhost port in development mode. If you still see CORS errors:
- Make sure `ENVIRONMENT` is not set to "production" in your `.env` file (or leave it unset for development)
- Check that your frontend is using `http://localhost` or `http://127.0.0.1` (not `https://`)

### 3. **Database connection error**

- Make sure PostgreSQL is running: `sudo service postgresql status` (in WSL)
- Verify `.env` file exists with correct `DATABASE_URL`
- Test database connection separately

### 4. **Port 8000 already in use**

Change the port with `--port 8001` and update the frontend API_BASE_URL

### 5. **Module not found**

Install missing dependencies:
```bash
pip3 install fastapi uvicorn sqlalchemy psycopg2-binary bcrypt passlib pyjwt python-dotenv pydantic[email] requests
```

### 6. **Server starts but immediately crashes**

- Check the terminal output for error messages
- Verify all environment variables are set in `.env`
- Check database connection settings
- Look for import errors in the logs

