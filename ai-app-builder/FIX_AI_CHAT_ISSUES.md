# AI App Builder - AI Chat Issues Fix Guide

This guide helps you fix the AI chat issues identified in your connection test.

## Issues Identified and Fixes

### 1. Database SQL Expression Error
**Error:** "Textual SQL expression 'SELECT 1' should be explicitly declared as text('SELECT 1')"

**Fix Applied:** Updated the health check function in `backend/app/main.py` to use `text("SELECT 1")` instead of just `"SELECT 1"`.

### 2. AI Capabilities Endpoint Not Found (404)
**Issue:** The test was looking for `/api/ai/capabilities` but the actual endpoint is `/api/builder/capabilities`.

**Fix:** Updated the test script to use the correct endpoint path.

### 3. CORS Configuration Returning 404
**Issue:** The CORS test was making a request to an incorrect endpoint.

**Fix:** Updated the CORS test to use the correct endpoint and proper headers.

### 4. AI Chat Endpoint Returning 401 (Unauthorized)
**Issue:** The AI chat endpoint requires authentication, but the test was making requests without authentication.

**Fix:** Created a new authentication test script that demonstrates proper authentication flow.

## Files Modified

1. **`backend/app/main.py`** - Fixed the database health check SQL expression
2. **`TEST_AI_CONNECTION.py`** - Updated to use correct endpoint paths
3. **`TEST_AI_CHAT_AUTH.py`** - New script to test AI chat with proper authentication

## How to Apply the Fixes

### 1. Restart the Backend Server
After the fixes, restart your backend server:

```bash
cd backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### 2. Run the Updated Connection Test
```bash
python TEST_AI_CONNECTION.py
```

### 3. Run the Authentication Test
```bash
python TEST_AI_CHAT_AUTH.py
```

## Frontend AI Chat Troubleshooting

### If AI Chat Still Not Working in Frontend:

1. **Check Authentication:**
   - Make sure you're logged in with demo credentials:
     - Email: `demo@appforge.dev`
     - Password: `demo123`

2. **Check Browser Console:**
   - Press F12 to open Developer Tools
   - Check the Console tab for errors
   - Check the Network tab to see if API requests are failing

3. **Check OpenRouter API Key:**
   - Verify your `backend/.env` file has a valid OpenRouter API key:
     ```
     OPENROUTER_API_KEY=sk-or-v1-...your-key-here...
     ```

4. **Test OpenRouter Key:**
   ```bash
   cd backend
   python TEST_OPENROUTER_KEY.py
   ```

## Backend API Endpoints

### Authentication
- **POST** `/api/auth/login` - User login
- **POST** `/api/auth/register` - User registration

### AI Builder (Requires Authentication)
- **POST** `/api/builder/chat` - Chat with AI assistant
- **POST** `/api/builder/analyze` - Analyze project requirements
- **POST** `/api/builder/generate` - Generate project code
- **GET** `/api/builder/capabilities` - Get AI capabilities (No auth required)
- **GET** `/api/builder/templates` - Get project templates
- **POST** `/api/builder/template/{id}` - Create project from template

### AI Chat (Requires Authentication)
- **POST** `/api/ai/chat` - Chat with AI
- **POST** `/api/ai/explain` - Explain concepts
- **POST** `/api/ai/debug` - Debug code
- **POST** `/api/ai/optimize` - Optimize code

## Common Error Solutions

### 401 Unauthorized Errors
- Make sure you're logged in
- Check that your token is valid and not expired
- In demo mode, the frontend handles authentication specially

### 404 Not Found Errors
- Verify the endpoint path is correct
- Check the API documentation at http://localhost:8000/docs

### 500 Internal Server Errors
- Check backend logs for detailed error messages
- Verify all dependencies are installed
- Check OpenRouter API key configuration

## Testing with cURL

### Login
```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "demo@appforge.dev", "password": "demo123"}'
```

### Chat with AI (replace YOUR_TOKEN with actual token)
```bash
curl -X POST http://localhost:8000/api/builder/chat \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello, what can you help me with?", "context": {}}'
```

### Get Capabilities (no auth required)
```bash
curl http://localhost:8000/api/builder/capabilities
```

## Still Having Issues?

1. **Check all test scripts:**
   - Run `TEST_AI_CONNECTION.py`
   - Run `TEST_AI_CHAT_AUTH.py`
   - Run `TEST_OPENROUTER_KEY.py`

2. **Verify environment:**
   - Check that all dependencies are installed
   - Verify Python and Node.js versions
   - Check .env files in both frontend and backend

3. **Check documentation:**
   - Review `AI_CHAT_TROUBLESHOOTING.md`
   - Check `README.md` for setup instructions

4. **Restart everything:**
   - Stop both frontend and backend
   - Start backend first
   - Start frontend after backend is fully running