# AI App Builder

A full-stack AI application builder that allows you to create applications using natural language.

## Prerequisites

- Python 3.8+
- Node.js 14+
- MySQL (optional, SQLite fallback included)

## Quick Start

**Easiest Way to Start:**
Run the provided startup scripts:

**Windows (PowerShell):**
```powershell
.\START_APPLICATION.ps1
```

**Windows (Command Prompt):**
```cmd
START_APPLICATION.bat
```

This will automatically start both backend and frontend services in separate windows.

## Setup Instructions

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure OpenRouter API Key:**
   The AI features require an OpenRouter API key. Follow the setup guide:
   ```bash
   OPENROUTER_SETUP.md
   ```
   
   Or run the verification script:
   ```bash
   # Windows Command Prompt
   verify_openrouter_key.bat
   
   # PowerShell
   .\verify_openrouter_key.ps1
   
   # Direct Python script
   python verify_openrouter_key.py
   ```

4. Start the backend server using one of these methods:
   
   **Method 1: Direct command**
   ```bash
   python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```
   
   **Method 2: Batch file (Windows)**
   ```bash
   .\start_server.bat
   ```
   
   **Method 3: PowerShell script**
   ```bash
   .\start_server.ps1
   ```

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install Node dependencies:
   ```bash
   npm install
   ```

3. Start the frontend server:
   ```bash
   npm start
   ```

   Alternatively, you can use the provided batch file:
   ```bash
   run_frontend.bat
   ```

### Running Both Services

To start both the backend and frontend services simultaneously, run:
```bash
start.bat
```

Or use the new unified scripts:
```bash
START_APPLICATION.bat
```
or
```bash
.\START_APPLICATION.ps1
```

## Accessing the Application

Once both services are running:

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

**IMPORTANT:** 
- Do NOT use http://0.0.0.0:8000 in your browser - this will not work
- Use http://localhost:8000 instead to access the backend
- Use http://localhost:3000 to access the frontend application

## Testing Server Connection

To verify that the backend server is running properly, you can:

1. Open `TEST_CONNECTION.html` in your browser
2. Visit http://localhost:8000 in your browser
3. Check the API documentation at http://localhost:8000/docs

## Troubleshooting

### Common Issues and Solutions

#### 1. "0.0.0.0 took too long to respond" Error

**Problem:** You're trying to access http://0.0.0.0:8000 directly in your browser.
**Solution:** Access http://localhost:8000 instead.

- `0.0.0.0` means "all network interfaces" - it's for the server to listen on
- `localhost` (127.0.0.1) is what you use to access the server from your browser

#### 2. PowerShell Command Not Found Error

**Problem:** 
```bash
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

#### 3. AI Chat Not Working

**Problem:** Backend AI service works but frontend AI chat doesn't work.

**Checklist:**
1. Verify both frontend (port 3000) and backend (port 8000) are running
2. Check that your OpenRouter API key is properly configured in `backend/.env`
3. Verify CORS settings in `backend/.env` include `http://localhost:3000`
4. Check browser console (F12) for any errors
5. Test the connection using `TEST_CONNECTION.html`

#### 4. Connection Error: Failed to connect to the AI service

**Problem:** Frontend shows "Connection Error: Failed to connect to the AI service"

**Solutions:**
1. Verify backend server is running: http://localhost:8000
2. Check OpenRouter API key in `backend/.env`:
   ```
   OPENROUTER_API_KEY=sk-or-v1-...
   ```
3. Test the API key with:
   ```bash
   # Windows Command Prompt
   verify_openrouter_key.bat
   
   # PowerShell
   .\verify_openrouter_key.ps1
   
   # Direct Python script
   python verify_openrouter_key.py
   ```
4. Follow the detailed setup guide in `OPENROUTER_SETUP.md`

### Server Not Accessible in Browser

If you can't access the server in your browser:

1. Make sure you're using the correct command:
   ```bash
   python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

2. Check that the server is running without errors in the terminal.

3. Verify the server is listening on the correct port:
   ```bash
   netstat -an | findstr :8000
   ```

4. Test the connection with the provided test file:
   Open `TEST_CONNECTION.html` in your browser to verify the backend is responding.

### Database Issues

The application will automatically fall back to SQLite if MySQL is not available. Make sure you have the proper database credentials in your `.env` file.

## API Endpoints

- `GET /` - Root endpoint
- `GET /health` - Health check
- `POST /api/auth/login` - User login
- `POST /api/auth/register` - User registration
- `GET /api/projects` - List projects
- `POST /api/builder/generate` - Generate application code
- `POST /api/deployment/deploy` - Deploy application

For a complete list of endpoints, visit the API documentation at http://localhost:8000/docs when the server is running.

## Additional Resources

- OpenRouter Setup Guide: `OPENROUTER_SETUP.md`
- API Key Verification Scripts: `verify_openrouter_key.bat`, `verify_openrouter_key.ps1`, `verify_openrouter_key.py`
- Detailed fix instructions: `FIX_INSTRUCTIONS.md`
- Service status checker: `CHECK_SERVICES.py`
- Connection tester: `TEST_CONNECTION.html`
- AI service tester: `TEST_AI_SERVICE.py`