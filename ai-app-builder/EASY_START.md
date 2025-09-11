# AI App Builder - Easy Start Guide

## 🚀 Quick Start (Recommended)

### Option 1: Double-click Method (Windows)
1. Navigate to the `ai-app-builder` folder
2. Double-click on `LAUNCH_APP.bat`
3. Wait for both services to start (1-2 minutes)
4. Your browser will automatically open http://localhost:3000

### Option 2: PowerShell Method
1. Open PowerShell in the `ai-app-builder` folder
2. Run:
   ```powershell
   .\LAUNCH_APP.ps1
   ```
3. Wait for both services to start
4. Your browser will automatically open http://localhost:3000

## 🎯 Correct URLs to Access

✅ **Frontend Application:** http://localhost:3000  
✅ **Backend API:** http://localhost:8000  
✅ **API Documentation:** http://localhost:8000/docs  

❌ **NEVER use:** http://0.0.0.0:8000

## 🔧 What This Does

When you run the launcher:
1. Starts the **Backend Server** on port 8000
2. Starts the **Frontend Application** on port 3000
3. Opens your browser to the correct URL
4. Keeps both services running in separate windows

## 📋 Manual Startup (If needed)

### Start Backend:
```powershell
cd backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Start Frontend (in new terminal):
```powershell
cd frontend
npm start
```

## ✅ Verification

After starting both services:

1. **Check backend:** Visit http://localhost:8000 in your browser
   - You should see a welcome message about AI App Builder

2. **Check frontend:** Visit http://localhost:3000 in your browser
   - You should see the AI App Builder interface

3. **Run verification script:**
   ```powershell
   python VERIFY_SERVICES.py
   ```

4. **Test connection:** Open `VERIFY_CONNECTION.html` in your browser

## 🆘 Troubleshooting

If you have issues:

1. **Wait longer:** First-time startup can take 1-2 minutes
2. **Check both windows:** Make sure both backend and frontend terminals are still running
3. **Check URLs:** Make sure you're using `localhost`, not `0.0.0.0`
4. **Run verification:** Use `VERIFY_SERVICES.py` to check what's running
5. **Check guide:** Read `TROUBLESHOOTING.md` for detailed solutions

## 📁 Files Created to Help You

- `LAUNCH_APP.bat` - Easy startup script (double-click)
- `LAUNCH_APP.ps1` - PowerShell startup script
- `VERIFY_SERVICES.py` - Check if services are running
- `VERIFY_CONNECTION.html` - Test frontend-backend connection
- `TROUBLESHOOTING.md` - Detailed troubleshooting guide
- `EASY_START.md` - This guide

## 🎉 Success Indicators

When everything is working:

1. **Backend terminal** shows:
   ```
   INFO:     Application startup complete.
   INFO:     Uvicorn running on http://0.0.0.0:8000
   ```

2. **Frontend terminal** shows:
   ```
   webpack compiled successfully
   Local:            http://localhost:3000
   ```

3. **Browser at http://localhost:3000** shows the AI App Builder interface
4. **Browser at http://localhost:8000** shows backend information
5. **Running `VERIFY_SERVICES.py`** shows both services as running

## ⚠️ Important Reminders

1. **Keep terminals open:** Don't close the backend or frontend terminal windows
2. **Use correct URLs:** Always use `localhost`, never `0.0.0.0`
3. **Be patient:** First-time startup takes longer due to compilation
4. **Check both services:** Both backend and frontend must be running

## 🆗 Still Having Issues?

1. Make sure you've installed dependencies:
   ```powershell
   cd backend
   pip install -r requirements.txt
   cd ../frontend
   npm install
   ```

2. Check the troubleshooting guide: `TROUBLESHOOTING.md`

3. Run the verification script:
   ```powershell
   python VERIFY_SERVICES.py
   ```

4. Test the connection: Open `VERIFY_CONNECTION.html`