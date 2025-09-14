# OpenRouter API Key Setup Guide

## Issue
You're seeing the error: "Connection Error: Failed to connect to the AI service" because the current OpenRouter API key in the configuration is invalid or expired.

## Solution
To fix this issue, you need to create your own OpenRouter account and generate a new API key.

## Step-by-Step Instructions

### 1. Create an OpenRouter Account
1. Go to [https://openrouter.ai/](https://openrouter.ai/)
2. Click on "Sign Up" to create a new account
3. Complete the registration process

### 2. Generate a New API Key
1. After logging in, go to your profile or account settings
2. Look for "API Keys" or a similar section
3. Click "Generate New Key" or "Create API Key"
4. Copy the generated API key (it should start with `sk-or-v1-`)

### 3. Update Your Configuration
1. Open the `.env` file in your backend directory:
   ```
   c:\Users\teja.kanchi\Desktop\AI co-developer\ai-app-builder\backend\.env
   ```

2. Find the line with `OPENROUTER_API_KEY` and replace the existing key with your new one:
   ```env
   OPENROUTER_API_KEY=your_new_api_key_here
   ```

3. Save the file

### 4. Restart Your Servers
1. Stop both frontend and backend servers if they're running
2. Start the backend server:
   ```bash
   cd c:\Users\teja.kanchi\Desktop\AI co-developer\ai-app-builder\backend
   python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
   ```

3. In a new terminal, start the frontend server:
   ```bash
   cd c:\Users\teja.kanchi\Desktop\AI co-developer\ai-app-builder\frontend
   npm start
   ```

### 5. Test the AI Chat
1. Open your browser and go to `http://localhost:3000`
2. Log in with the test credentials:
   - Email: `test@example.com`
   - Password: `testpassword123`
3. Try using the AI chat feature

## Alternative: Use Free Models
OpenRouter provides access to several free models. The application is configured to use `mistralai/mistral-7b-instruct` which is free to use.

## Troubleshooting
If you still encounter issues:

1. Verify your API key is correct and doesn't have extra spaces
2. Check that you're connected to the internet
3. Make sure your firewall isn't blocking the connection
4. Check the backend server logs for more detailed error messages

## Need Help?
If you continue to have issues, please check:
- The backend console output for detailed error messages
- Your OpenRouter account dashboard for any usage limits
- The OpenRouter status page for service outages