# Final Fix Instructions for Python 3.13 Compatibility Issues

This document provides comprehensive instructions to fix all package import issues with Python 3.13 compatibility.

## Summary of Issues Fixed

1. **SQLAlchemy compatibility** - Updated from 2.0.23 to 2.0.35
2. **typing.Annotated errors** - Added typing_extensions dependency
3. **Missing packages** - Fixed installation of jose, dotenv, pydantic_settings
4. **Google package compatibility** - Updated versions for Python 3.13

## Files Updated

1. [requirements.txt](file://c:\Users\teja.kanchi\Desktop\AI%20co-developer\ai-app-builder\backend\requirements.txt) - Updated package versions
2. [install_deps.py](file://c:\Users\teja.kanchi\Desktop\AI%20co-developer\ai-app-builder\backend\install_deps.py) - Enhanced installation script
3. Multiple fix scripts for different package groups

## Manual Fix Instructions

### Step 1: Set Environment Variables

Open Command Prompt or PowerShell and run:
```cmd
set PYTHONNOUSERSITE=1
```

### Step 2: Navigate to Backend Directory

```cmd
cd c:\Users\teja.kanchi\Desktop\AI co-developer\ai-app-builder\backend
```

### Step 3: Uninstall Problematic Packages

```cmd
pip uninstall fastapi openai sqlalchemy python-jose python-dotenv pydantic-settings google-generativeai google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client -y
```

### Step 4: Install Updated Packages

```cmd
pip install typing_extensions --force-reinstall --no-cache-dir
pip install fastapi==0.104.1 --force-reinstall --no-cache-dir
pip install openai==1.3.7 --force-reinstall --no-cache-dir
pip install sqlalchemy==2.0.35 --force-reinstall --no-cache-dir
pip install python-jose[cryptography]==3.3.0 --force-reinstall --no-cache-dir
pip install python-dotenv==1.0.0 --force-reinstall --no-cache-dir
pip install pydantic-settings==2.1.0 --force-reinstall --no-cache-dir
pip install google-generativeai==0.3.2 --force-reinstall --no-cache-dir
pip install google-auth==2.23.4 --force-reinstall --no-cache-dir
pip install google-auth-oauthlib==1.2.0 --force-reinstall --no-cache-dir
pip install google-auth-httplib2==0.2.0 --force-reinstall --no-cache-dir
pip install google-api-python-client==2.110.0 --force-reinstall --no-cache-dir
```

### Step 5: Verify Installations

```cmd
python -c "import fastapi; print('✅ FastAPI OK')"
python -c "import openai; print('✅ OpenAI OK')"
python -c "import sqlalchemy; print('✅ SQLAlchemy OK')"
python -c "import jose; print('✅ Jose OK')"
python -c "import dotenv; print('✅ Dotenv OK')"
python -c "import pydantic_settings; print('✅ Pydantic-settings OK')"
python -c "import google.generativeai; print('✅ Google Generative AI OK')"
python -c "import google.auth; print('✅ Google Auth OK')"
python -c "import google.auth.oauthlib; print('✅ Google Auth OAuthlib OK')"
python -c "import google_auth_httplib2; print('✅ Google Auth HTTPLib2 OK')"
python -c "import googleapiclient; print('✅ Google API Client OK')"
```

## Alternative: Using Provided Scripts

If you prefer to use the automated scripts:

### PowerShell Scripts:
1. [fix_packages.ps1](file://c:\Users\teja.kanchi\Desktop\AI%20co-developer\ai-app-builder\backend\fix_packages.ps1) - Fixes all packages
2. [fix_google_packages.ps1](file://c:\Users\teja.kanchi\Desktop\AI%20co-developer\ai-app-builder\backend\fix_google_packages.ps1) - Fixes Google packages specifically
3. [fix_google_auth_oauthlib.ps1](file://c:\Users\teja.kanchi\Desktop\AI%20co-developer\ai-app-builder\backend\fix_google_auth_oauthlib.ps1) - Fixes google-auth-oauthlib specifically

### Batch Scripts:
1. [fix_packages.bat](file://c:\Users\teja.kanchi\Desktop\AI%20co-developer\ai-app-builder\backend\fix_packages.bat) - Fixes all packages

### Python Scripts:
1. [fix_packages.py](file://c:\Users\teja.kanchi\Desktop\AI%20co-developer\ai-app-builder\backend\fix_packages.py) - Fixes all packages
2. [fix_google_packages.py](file://c:\Users\teja.kanchi\Desktop\AI%20co-developer\ai-app-builder\backend\fix_google_packages.py) - Fixes Google packages specifically
3. [fix_google_auth_oauthlib.py](file://c:\Users\teja.kanchi\Desktop\AI%20co-developer\ai-app-builder\backend\fix_google_auth_oauthlib.py) - Fixes google-auth-oauthlib specifically

## Troubleshooting

### If Packages Still Fail to Import:

1. **Clear pip cache:**
   ```cmd
   pip cache purge
   ```

2. **Check package locations:**
   ```cmd
   pip show google-auth-oauthlib
   ```

3. **Install from specific index:**
   ```cmd
   pip install google-auth-oauthlib==1.2.0 --force-reinstall --no-cache-dir -i https://pypi.org/simple/
   ```

4. **Check for conflicting installations:**
   ```cmd
   pip list | findstr google
   ```

### If Virtual Environment Issues:

1. **Deactivate current environment:**
   ```cmd
   deactivate
   ```

2. **Create new virtual environment:**
   ```cmd
   python -m venv venv
   ```

3. **Activate new environment:**
   ```cmd
   venv\Scripts\activate
   ```

4. **Install packages fresh:**
   ```cmd
   pip install -r requirements.txt --force-reinstall --no-cache-dir
   ```

## Verification

After applying fixes, run the verification script:
```cmd
python install_deps.py
```

Or manually verify:
```cmd
python -c "from app.core.config import settings; print('✅ Configuration loads successfully')"
```

## Prevention

To prevent future issues:
1. Keep packages updated to versions that support your Python version
2. Use virtual environments to avoid conflicts
3. Regularly update dependencies
4. Set PYTHONNOUSERSITE=1 in your environment

After applying these fixes, you should be able to run the backend without package import errors.