# AI Chat Connection Error Troubleshooting Guide

## Common Issue: "Connection Error: Failed to connect to the AI service"

This error typically occurs when the AI service cannot be reached or is not properly configured. Here's how to resolve it:

## 1. Check Backend Server Status

First, ensure the backend server is running:

1. Open a terminal/command prompt
2. Navigate to the backend directory:
   ```bash
   cd C:\Users\teja.kanchi\Desktop\AI co-developer\ai-app-builder\backend
   ```
3. Start the server:
   ```bash
   python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```
   Or use the provided scripts:
   ```bash
   start_server.bat
   ```
   or
   ```bash
   .\start_server.ps1
   ```

4. Verify the server is running by visiting http://localhost:8000 in your browser

## 2. Verify OpenRouter API Key

Check that your OpenRouter API key is correctly configured:

1. Open the `.env` file in the backend directory
2. Verify that `OPENROUTER_API_KEY` is set with a valid key
3. The key should start with `sk-or-`

## 3. Check OpenRouter Account Status

The "402 Payment Required" error indicates an account balance issue:

1. Visit [https://openrouter.ai/](https://openrouter.ai/) and log in
2. Check your account balance and billing information
3. Add funds if needed or use free models

## 4. Test AI Services

Run the test scripts to verify service connectivity:

```bash
cd C:\Users\teja.kanchi\Desktop\AI co-developer\ai-app-builder\backend
python test_openrouter.py
python check_openrouter_key.py
```

## 5. Use Free Models

We've configured the system to use free models by default:

- Model: `mistralai/mistral-7b-instruct` (free)
- This should work without requiring payment

## 6. Check Internet Connection

Ensure you have a stable internet connection:

1. Test connectivity to OpenRouter:
   ```bash
   ping openrouter.ai
   ```
2. Check firewall settings that might block outgoing connections

## 7. Restart Services

Sometimes a simple restart can resolve connectivity issues:

1. Stop the backend server (Ctrl+C)
2. Restart the backend server
3. Refresh the frontend application

## 8. Check Browser Console

For frontend issues, check the browser's developer console:

1. Press F12 to open developer tools
2. Go to the "Console" tab
3. Look for any error messages related to API calls

## 9. Verify CORS Configuration

Ensure CORS is properly configured to allow requests from the frontend:

1. Check the `.env` file for `CORS_ORIGINS`
2. It should include `http://localhost:3000` and `http://localhost:3001`

## 10. Fallback Mode

When the AI service is unavailable, the system uses fallback responses:

- You'll still be able to use the application
- Features will work with limited AI capabilities
- Code generation will use template-based responses

## Still Having Issues?

If you continue to experience problems:

1. Check the backend server logs for detailed error messages
2. Verify all dependencies are installed:
   ```bash
   pip install -r requirements.txt
   ```
3. Ensure your Python environment is activated:
   ```bash
   venv\Scripts\activate  # Windows
   ```
4. Contact OpenRouter support for account-related issues

## Contact Support

For persistent issues, you can:

1. Check the OpenRouter documentation: https://openrouter.ai/docs
2. Visit the OpenRouter Discord community
3. File an issue on the project's GitHub repository