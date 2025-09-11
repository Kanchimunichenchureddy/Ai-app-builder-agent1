# AI App Builder - AI Chat Troubleshooting Guide

This guide helps you test and troubleshoot AI chat functionality in the AI App Builder.

## Testing Tools

### 1. Connection Test
Tests the connection between frontend and backend for AI chat functionality.

**Run:**
```bash
python TEST_AI_CONNECTION.py
```
or double-click `TEST_AI_CONNECTION.bat`

### 2. OpenRouter Key Test
Verifies that the OpenRouter API key is properly configured.

**Run:**
```bash
python TEST_OPENROUTER_KEY.py
```
or double-click `TEST_OPENROUTER_KEY.bat`

### 3. AI Chat Functionality Test
Tests the AI chat functionality with real interactions.

**Run:**
```bash
python TEST_AI_CHAT_FUNCTIONALITY.py
```
or double-click `TEST_AI_CHAT_FUNCTIONALITY.bat`

## Common Issues and Solutions

### 1. "Connection Error: Failed to connect to the AI service"

**Possible Causes:**
- Backend server not running
- Incorrect API key configuration
- Network connectivity issues
- CORS configuration problems

**Solutions:**
1. Verify backend is running: http://localhost:8000
2. Check OpenRouter API key in `backend/.env`
3. Run connection test: `TEST_AI_CONNECTION.py`
4. Verify CORS settings allow http://localhost:3000

### 2. AI Chat Returns Generic/Fallback Responses

**Possible Causes:**
- Invalid or expired OpenRouter API key
- Quota limits reached
- Model not available

**Solutions:**
1. Test OpenRouter key: `TEST_OPENROUTER_KEY.py`
2. Check your OpenRouter account for quota information
3. Verify the model is available in your OpenRouter account

### 3. Slow AI Responses

**Possible Causes:**
- High demand on AI service
- Complex requests
- Network latency

**Solutions:**
- Simplify your requests
- Check OpenRouter status page
- Be patient - first requests may be slower

### 4. "404 Not Found" Errors for AI Endpoints

**Possible Causes:**
- Backend not fully started
- API routes changed
- Version mismatch

**Solutions:**
1. Restart backend server
2. Check API documentation: http://localhost:8000/docs
3. Verify backend health: http://localhost:8000/health

## Testing Steps

### Step 1: Verify Backend is Running
1. Open browser to http://localhost:8000
2. You should see a welcome message about AI App Builder
3. Check API docs at http://localhost:8000/docs

### Step 2: Test OpenRouter Configuration
1. Run `TEST_OPENROUTER_KEY.py`
2. Verify API key is present and correctly formatted
3. Check that the key starts with "sk-or-"

### Step 3: Test Connection
1. Run `TEST_AI_CONNECTION.py`
2. Verify all tests pass
3. Check CORS configuration is working

### Step 4: Test AI Functionality
1. Run `TEST_AI_CHAT_FUNCTIONALITY.py`
2. Verify chat interactions work
3. Verify code generation works

## Environment Variables

Ensure your `backend/.env` file contains:

```env
# AI Services - Using OpenRouter
OPENROUTER_API_KEY=sk-or-v1-...your-key-here...

# CORS Settings
CORS_ORIGINS=http://localhost:3000,http://localhost:3001
```

## Browser Console Debugging

If AI chat isn't working in the browser:

1. Press F12 to open Developer Tools
2. Click on the "Console" tab
3. Look for error messages
4. Check the "Network" tab for failed API requests
5. Look for CORS errors or 401/403 status codes

## Frontend Service Configuration

Check `frontend/src/services/aiChatService.js` for correct API configuration:

```javascript
const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL || 'http://localhost:8000/api',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});
```

## Backend Service Configuration

Check `backend/app/services/ai_agent.py` for correct OpenRouter integration:

```python
class AIAgentService:
    def __init__(self):
        self.openrouter_service = OpenRouterService()
        self.active_llm_service = "openrouter"
```

## Testing with cURL

You can also test the API directly with cURL:

```bash
# Test backend connectivity
curl http://localhost:8000/

# Test health endpoint
curl http://localhost:8000/health

# Test AI chat (requires JSON data)
curl -X POST http://localhost:8000/api/ai/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello, what can you help me with?", "context": {}}'
```

## Logs and Debugging

### Backend Logs
Check the terminal where you started the backend for:
- Error messages
- Startup completion messages
- Request handling logs

### Frontend Logs
Check the browser console for:
- JavaScript errors
- Network request failures
- CORS errors

## Still Having Issues?

1. **Restart everything:**
   - Stop both frontend and backend
   - Start backend first
   - Start frontend after backend is fully running

2. **Check all tests:**
   - Run all three test scripts
   - Fix any issues they identify

3. **Verify environment:**
   - Check that all dependencies are installed
   - Verify Python version (3.8+ recommended)
   - Check Node.js version (14+ recommended)

4. **Check documentation:**
   - Review `README.md` for setup instructions
   - Check `DEPENDENCY_MANAGEMENT.md` for dependency issues

5. **Contact support:**
   - If none of these solutions work, please provide:
     - Screenshots of error messages
     - Terminal output from both backend and frontend
     - Results from running the test scripts