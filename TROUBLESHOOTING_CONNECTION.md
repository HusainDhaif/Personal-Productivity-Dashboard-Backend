# Troubleshooting: "Cannot connect to server at http://127.0.0.1:8000"

## Step-by-Step Solution

### Step 1: Verify the Server is Actually Running

**Open a WSL terminal** and run:

```bash
cd /home/husaindhaif/code/ga/projects/Personal-Productivity-Dashboard-Backend

# Check if server is running
ps aux | grep uvicorn | grep -v grep

# Check if port 8000 is in use
netstat -tuln | grep :8000
```

**If you see no output**, the server is NOT running. Continue to Step 2.

**If you see output**, the server IS running but you still can't connect. Skip to Step 5.

---

### Step 2: Run Pre-Flight Checks

Before starting the server, check for issues:

```bash
python3 check_server.py
```

This will tell you:
- ✓ If dependencies are installed
- ✓ If .env file exists
- ✓ If the application can be imported
- ✓ If database connection works

**Fix any issues** reported by the check script before proceeding.

---

### Step 3: Create .env File (if missing)

If you don't have a `.env` file, create one:

```bash
# Generate a secure JWT secret
JWT_SECRET=$(python3 -c "import secrets; print(secrets.token_urlsafe(32))")

# Create .env file
cat > .env << EOF
DATABASE_URL=sqlite:///./productivity.db
JWT_SECRET=$JWT_SECRET
ENVIRONMENT=development
EOF
```

**Note**: If you're using PostgreSQL, replace `DATABASE_URL` with your actual connection string:
```
DATABASE_URL=postgresql://username:password@localhost:5432/dbname
```

---

### Step 4: Start the Server

**Option A: Use the startup script (recommended)**
```bash
chmod +x start_server.sh
./start_server.sh
```

**Option B: Use the simple startup script**
```bash
chmod +x start_server_simple.sh
./start_server_simple.sh
```

**Option C: Start manually**
```bash
python3 -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**You should see:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

**If you see errors**, note them down and see the "Common Errors" section below.

---

### Step 5: Verify Server is Accessible

**In the same WSL terminal**, open a new tab/window and test:

```bash
# Test with curl
curl http://127.0.0.1:8000/health
curl http://localhost:8000/health

# Or use the test script
python3 test_server_connection.py
```

**Expected output:**
```json
{"status":"healthy","service":"Personal Productivity Dashboard API"}
```

**If curl works but browser doesn't**, see Step 6.

---

### Step 6: Test from Windows Browser

Since you're using WSL, try accessing from Windows:

1. Open Windows browser (Chrome, Edge, Firefox)
2. Visit: `http://localhost:8000/docs`
3. Or visit: `http://127.0.0.1:8000/health`

**If this works**, your frontend might be using the wrong URL. Make sure your frontend is connecting to:
- `http://localhost:8000` or
- `http://127.0.0.1:8000`

**NOT** `https://` (use `http://`)

---

### Step 7: Check Firewall (if still not working)

**Windows Firewall:**
1. Open Windows Defender Firewall
2. Check if port 8000 is blocked
3. Temporarily disable firewall to test (re-enable after testing)

**WSL Networking:**
WSL should automatically forward localhost ports, but if it doesn't work:
1. Try accessing from Windows using `localhost` instead of `127.0.0.1`
2. Or try accessing from WSL using `127.0.0.1`

---

## Common Errors and Solutions

### Error: "ModuleNotFoundError: No module named 'fastapi'"

**Solution:**
```bash
pip3 install fastapi uvicorn sqlalchemy psycopg2-binary bcrypt passlib pyjwt python-dotenv pydantic[email] requests
```

Or if using pipenv:
```bash
pipenv install
```

---

### Error: "Address already in use" or "Port 8000 already in use"

**Solution:**
Find and kill the process using port 8000:
```bash
# Find the process
lsof -i :8000
# Or
netstat -tuln | grep :8000

# Kill it (replace PID with actual process ID)
kill -9 <PID>
```

Or use a different port:
```bash
python3 -m uvicorn main:app --reload --host 0.0.0.0 --port 8001
```
Then update your frontend to use port 8001.

---

### Error: "DATABASE_URL is not set" or Database connection errors

**Solution:**
1. Create `.env` file (see Step 3)
2. For quick testing, use SQLite (no setup needed):
   ```
   DATABASE_URL=sqlite:///./productivity.db
   ```
3. For PostgreSQL, ensure PostgreSQL is running:
   ```bash
   sudo service postgresql status
   sudo service postgresql start  # if not running
   ```

---

### Error: "JWT_SECRET is not configured"

**Solution:**
Add `JWT_SECRET` to your `.env` file:
```bash
# Generate a secret
python3 -c "import secrets; print(secrets.token_urlsafe(32))"

# Add to .env file
echo "JWT_SECRET=your-generated-secret-here" >> .env
```

---

### Server starts but immediately crashes

**Check the error message:**
1. Look at the full error output in the terminal
2. Common causes:
   - Missing environment variables
   - Database connection failure
   - Import errors
   - Port already in use

**Solution:**
Run the check script to identify the issue:
```bash
python3 check_server.py
```

---

## Still Not Working?

1. **Check server logs**: Look at the terminal where you started the server for error messages
2. **Verify server is running**: Run `ps aux | grep uvicorn` to confirm
3. **Test locally first**: Try `curl http://127.0.0.1:8000/health` from WSL
4. **Check CORS**: The server now allows all localhost ports, so CORS shouldn't be the issue
5. **Try different ports**: Use port 8001 or 3001 to rule out port-specific issues

---

## Quick Test Checklist

- [ ] Server process is running (`ps aux | grep uvicorn`)
- [ ] Port 8000 is listening (`netstat -tuln | grep :8000`)
- [ ] Can access from WSL (`curl http://127.0.0.1:8000/health`)
- [ ] Can access from Windows browser (`http://localhost:8000/docs`)
- [ ] .env file exists with DATABASE_URL and JWT_SECRET
- [ ] All dependencies installed (`python3 check_server.py`)
- [ ] No firewall blocking port 8000

If all checkboxes are checked but still can't connect, the issue is likely with your frontend configuration, not the backend.

