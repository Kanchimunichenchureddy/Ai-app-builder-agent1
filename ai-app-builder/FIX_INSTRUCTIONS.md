# AI App Builder - Fix Instructions

## Issue 1: Server Access Problem

**Problem**: You're trying to access `http://0.0.0.0:8000` directly in the browser.
**Solution**: Access `http://localhost:8000` instead.

- `0.0.0.0` means "all network interfaces" - it's for the server to listen on all interfaces
- `localhost` (127.0.0.1) is what you use to access the server from your browser

## Issue 2: PowerShell Command Problem

**Problem**: PowerShell requires `.\` prefix to run files in the current directory.
**Solution**: Use the correct command format.

### Option 1: Run PowerShell Script
```powershell
.\start_server.ps1
```

### Option 2: Run Batch File in PowerShell
```powershell
.\start_server.bat
```

### Option 3: Run Direct Command
```powershell
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## Issue 3: Frontend-Backend Communication

**Problem**: Frontend AI chat is not working despite backend AI service working.
**Solution**: Ensure both frontend and backend are running and can communicate.

### Start Backend Server:
1. Navigate to backend directory:
   ```powershell
   cd "C:\Users\teja.kanchi\Desktop\AI co-developer\ai-app-builder\backend"
   ```

2. Start the server:
   ```powershell
   python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

3. Verify server is running by accessing in browser:
   - Main app: http://localhost:8000
   - API docs: http://localhost:8000/docs

### Start Frontend:
1. Open a new terminal
2. Navigate to frontend directory:
   ```powershell
   cd "C:\Users\teja.kanchi\Desktop\AI co-developer\ai-app-builder\frontend"
   ```

3. Install dependencies (if not already done):
   ```powershell
   npm install
   ```

4. Start frontend:
   ```powershell
   npm start
   ```

5. Access frontend in browser:
   - http://localhost:3000

## Testing the Connection

1. Make sure both backend (port 8000) and frontend (port 3000) are running
2. Open browser and go to http://localhost:3000
3. Try using the AI chat feature
4. Check browser console (F12) for any errors
5. Check backend terminal for any error messages

## Common Troubleshooting Steps

### If you get "Connection Error: Failed to connect to the AI service":

1. Verify OpenRouter API key in backend/.env file:
   ```
   OPENROUTER_API_KEY=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
   ```

2. Test the API key:
   ```powershell
   python test_openrouter.py
   ```

3. Check if backend server is running:
   - Should see "🚀 AI App Builder Agent v1.0.0 started successfully!" message
   - Should be able to access http://localhost:8000

### If frontend can't connect to backend:

1. Check CORS configuration in backend/app/main.py:
   ```python
   app.add_middleware(
       CORSMiddleware,
       allow_origins=settings.CORS_ORIGINS_LIST,
       allow_credentials=True,
       allow_methods=["*"],
       allow_headers=["*"],
   )
   ```

2. Verify CORS_ORIGINS in backend/.env:
   ```
   CORS_ORIGINS=http://localhost:3000,http://localhost:3001
   ```

3. Check frontend API configuration in frontend/src/services/api.js:
   ```javascript
   const api = axios.create({
     baseURL: process.env.REACT_APP_API_URL || 'http://localhost:8000/api',
     timeout: 30000,
     headers: {
       'Content-Type': 'application/json',
     },
   });
   ```

4. Verify frontend .env file:
   ```
   REACT_APP_API_URL=http://localhost:8000/api
   ```

## Quick Start Commands

### Backend (PowerShell):
```powershell
cd "C:\Users\teja.kanchi\Desktop\AI co-developer\ai-app-builder\backend"
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Frontend (PowerShell in new terminal):
```powershell
cd "C:\Users\teja.kanchi\Desktop\AI co-developer\ai-app-builder\frontend"
npm start
```

## Access Points

- Backend API: http://localhost:8000/api
- Backend Docs: http://localhost:8000/docs
- Frontend App: http://localhost:3000