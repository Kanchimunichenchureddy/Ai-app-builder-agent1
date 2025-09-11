# AI App Builder - Troubleshooting Guide

## Common Issues and Solutions

### 1. "0.0.0.0 took too long to respond" Error

**Problem:** You're trying to access `http://0.0.0.0:8000` directly in your browser.

**Solution:** 
- ❌ Do NOT use: `http://0.0.0.0:8000`
- ✅ Use instead: `http://localhost:8000`

**Explanation:**
- `0.0.0.0` means "all network interfaces" - it's for the server to listen on all interfaces
- `localhost` (127.0.0.1) is what you use to access the server from your browser

### 2. PowerShell Command Not Found Error

**Problem:**
```
start_server.bat : The term 'start_server.bat' is not recognized
```

**Solution:** Use the `.\` prefix in PowerShell:
```powershell
.\start_server.bat
```
or
```powershell
.\start_server.ps1
```

### 3. Frontend Loads But Shows Blank Page

**Problem:** The frontend application loads but shows a blank page or connection errors.

**Solutions:**
1. **Check if both services are running:**
   - Backend should be accessible at: http://localhost:8000
   - Frontend should be accessible at: http://localhost:3000

2. **Wait for compilation:**
   - The first time you start the frontend, it may take 1-2 minutes to compile
   - Look for "webpack compiled successfully" message in the frontend terminal

3. **Check CORS configuration:**
   - Ensure `CORS_ORIGINS` in `backend/.env` includes `http://localhost:3000`

### 4. AI Chat Not Working

**Problem:** Backend AI service works but frontend AI chat doesn't work.

**Checklist:**
1. Verify both frontend (port 3000) and backend (port 8000) are running
2. Check that your OpenRouter API key is properly configured in `backend/.env`
3. Verify CORS settings in `backend/.env` include `http://localhost:3000`
4. Check browser console (F12) for any errors
5. Test the connection using `VERIFY_CONNECTION.html`

### 5. Connection Error: Failed to connect to the AI service

**Problem:** Frontend shows "Connection Error: Failed to connect to the AI service"

**Solutions:**
1. Verify backend server is running: http://localhost:8000
2. Check OpenRouter API key in `backend/.env`:
   ```
   OPENROUTER_API_KEY=sk-or-v1-...
   ```
3. Test the API key with:
   ```bash
   python VERIFY_SERVICES.py
   ```

## Diagnostic Tools

### 1. Verify Services Script
Run the verification script to check if services are running:
```bash
python VERIFY_SERVICES.py
```

### 2. Connection Test HTML
Open `VERIFY_CONNECTION.html` in your browser to test connections.

### 3. Manual Verification
Check each service manually:
- Backend: http://localhost:8000
- Frontend: http://localhost:3000
- API Docs: http://localhost:8000/docs

## Step-by-Step Startup Process

### 1. Start Backend
```powershell
cd backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Look for this message:
```
INFO:     Application startup complete.
```

### 2. Start Frontend (in a new terminal)
```powershell
cd frontend
npm start
```

Look for this message:
```
webpack compiled successfully
```

### 3. Access Application
- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- Docs: http://localhost:8000/docs

## Port Issues

### Check if ports are in use:
```bash
netstat -an | findstr :8000
netstat -an | findstr :3000
```

### Kill processes using ports (if needed):
```bash
taskkill /f /pid <PID>
```

## Environment Configuration

### Check backend/.env file:
```
OPENROUTER_API_KEY=sk-or-v1-... (should be present)
CORS_ORIGINS=http://localhost:3000,http://localhost:3001
```

### Check frontend/.env file:
```
REACT_APP_API_URL=http://localhost:8000/api
```

## Browser Issues

### Clear cache and cookies:
1. Press Ctrl+Shift+Delete
2. Select "All time" for time range
3. Check "Cookies and other site data" and "Cached images and files"
4. Click "Clear data"

### Try incognito/private mode:
- Chrome: Ctrl+Shift+N
- Firefox: Ctrl+Shift+P
- Edge: Ctrl+Shift+N

### Try a different browser:
Sometimes switching browsers can help identify if the issue is browser-specific.

## Network Issues

### Check firewall settings:
1. Windows Security → Firewall & network protection
2. Ensure Windows Defender Firewall is not blocking the ports

### Test local network connectivity:
```bash
ping localhost
ping 127.0.0.1
```

## Advanced Troubleshooting

### 1. Check backend logs:
Look for any error messages in the backend terminal window.

### 2. Check frontend logs:
Look for any error messages in the frontend terminal window.

### 3. Check browser console:
1. Press F12 to open Developer Tools
2. Click on the "Console" tab
3. Look for any error messages

### 4. Check network tab:
1. Press F12 to open Developer Tools
2. Click on the "Network" tab
3. Refresh the page
4. Look for failed requests (shown in red)

## Still Having Issues?

1. **Restart everything:**
   - Close all terminal/command windows
   - Run `LAUNCH_APP.bat` or `LAUNCH_APP.ps1`

2. **Check the logs:**
   - Look at the terminal output for error messages
   - Check if there are any Python or Node.js errors

3. **Verify installation:**
   - Make sure you've installed all dependencies:
     ```bash
     cd backend
     pip install -r requirements.txt
     cd ../frontend
     npm install
     ```

4. **Contact support:**
   - If none of these solutions work, please provide:
     - Screenshots of the error messages
     - Terminal output from both backend and frontend
     - Results from running `VERIFY_SERVICES.py`