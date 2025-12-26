# Quick Start Guide

## Step 1: Set Up Environment Variables

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit `.env` and set:
- `DATABASE_URL` - Your database connection string
- `JWT_SECRET` - A secret key for JWT tokens (generate with: `python3 -c "import secrets; print(secrets.token_urlsafe(32))"`)

## Step 2: Install Dependencies

If using pipenv (recommended):
```bash
pipenv install
```

Or using pip:
```bash
pip3 install fastapi uvicorn sqlalchemy psycopg2-binary bcrypt passlib pyjwt python-dotenv pydantic[email] requests
```

## Step 3: Start the Server

**Option A: Using the startup script (recommended)**
```bash
chmod +x start_server.sh
./start_server.sh
```

**Option B: Manual start**
```bash
python3 -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## Step 4: Verify Server is Running

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Application startup complete.
```

Test the connection:
```bash
# Run the test script
python3 test_server_connection.py

# Or visit in browser:
# http://localhost:8000/docs
# http://localhost:8000/health
```

## Troubleshooting

### "Cannot connect to server"

1. **Check if server is running**: Look for "Uvicorn running" message in terminal
2. **Test connection**: Run `python3 test_server_connection.py`
3. **Check port**: Make sure port 8000 is not blocked by firewall
4. **WSL users**: Try accessing from Windows browser at `http://localhost:8000/docs`

### "Module not found"

Install missing dependencies:
```bash
pip3 install <module-name>
```

### "Database connection error"

- Ensure PostgreSQL is running (if using PostgreSQL)
- Verify `DATABASE_URL` in `.env` is correct
- Check database credentials

### "Port 8000 already in use"

Use a different port:
```bash
python3 -m uvicorn main:app --reload --host 0.0.0.0 --port 8001
```

Then update your frontend to use the new port.

## Next Steps

Once the server is running:
- Visit http://localhost:8000/docs for interactive API documentation
- Test endpoints using the Swagger UI
- Connect your frontend application

For more details, see [START_SERVER.md](START_SERVER.md)

