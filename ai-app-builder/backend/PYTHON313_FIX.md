# Python 3.13 Compatibility Fix Guide

This document explains how to fix the package import issues that occur with Python 3.13 compatibility.

## Issues Identified

1. **typing.Annotated errors** with fastapi and openai
2. **Missing packages**: jose, dotenv, pydantic_settings, google.generativeai, google.auth
3. **Google authentication packages**: google-auth-oauthlib, google-auth-httplib2, google-api-python-client
4. **SQLAlchemy compatibility** (already fixed in previous step)

## Root Causes

1. **typing.Annotated**: Python 3.13 has changes to the typing module that affect how `typing.Annotated` is handled
2. **Missing packages**: Packages may not be installed or installed in user site-packages instead of virtual environment
3. **Import conflicts**: User site-packages interfering with virtual environment packages
4. **Version incompatibility**: Some package versions are not compatible with Python 3.13

## Solution Options

### Option 1: Run the Fix Scripts (Recommended)

#### PowerShell Script:
```powershell
# Navigate to backend directory
cd c:\Users\teja.kanchi\Desktop\AI co-developer\ai-app-builder\backend

# Run the PowerShell script
.\fix_packages.ps1
```

#### Batch Script:
```cmd
# Navigate to backend directory
cd c:\Users\teja.kanchi\Desktop\AI co-developer\ai-app-builder\backend

# Run the batch script
fix_packages.bat
```

#### Python Script:
```bash
# Navigate to backend directory
cd c:\Users\teja.kanchi\Desktop\AI co-developer\ai-app-builder\backend

# Run the Python script
python fix_packages.py
```

#### Targeted Google Package Fix:
```bash
# Navigate to backend directory
cd c:\Users\teja.kanchi\Desktop\AI co-developer\ai-app-builder\backend

# Run the targeted Google package fix
python fix_google_packages.py
```

### Option 2: Manual Fix Steps

1. **Set environment variable** to disable user site-packages:
   ```cmd
   set PYTHONNOUSERSITE=1
   ```

2. **Install typing_extensions** for better typing compatibility:
   ```cmd
   pip install typing_extensions --force-reinstall
   ```

3. **Reinstall problematic packages**:
   ```cmd
   pip uninstall fastapi openai python-jose python-dotenv pydantic-settings google-generativeai google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client -y
   pip install fastapi==0.104.1 openai==1.3.7 python-jose[cryptography]==3.3.0 python-dotenv==1.0.0 pydantic-settings==2.1.0 google-generativeai==0.3.2 google-auth==2.23.4 google-auth-oauthlib==1.2.0 google-auth-httplib2==0.2.0 google-api-python-client==2.110.0 --force-reinstall --no-cache-dir
   ```

4. **Verify installations**:
   ```bash
   python -c "import fastapi; print('FastAPI OK')"
   python -c "import openai; print('OpenAI OK')"
   python -c "import jose; print('Jose OK')"
   python -c "import dotenv; print('Dotenv OK')"
   python -c "import pydantic_settings; print('Pydantic-settings OK')"
   python -c "import google.generativeai; print('Google Generative AI OK')"
   python -c "import google.auth; print('Google Auth OK')"
   python -c "import google.auth.oauthlib; print('Google Auth OAuthlib OK')"
   python -c "import google_auth_httplib2; print('Google Auth HTTPLib2 OK')"
   python -c "import googleapiclient; print('Google API Client OK')"
   ```

## Additional Troubleshooting

### Check Package Locations
```bash
pip show fastapi
pip show openai
pip show sqlalchemy
```

### Clear Pip Cache
```bash
pip cache purge
```

### Check Python Path
```bash
python -c "import sys; print('\n'.join(sys.path))"
```

### Reinstall in Clean Environment
If issues persist:
1. Delete the virtual environment
2. Create a new virtual environment
3. Install packages fresh

## Prevention

To prevent future issues:
1. Keep packages updated to versions that support your Python version
2. Use virtual environments to avoid conflicts
3. Regularly update dependencies
4. Set PYTHONNOUSERSITE=1 in your environment

After applying these fixes, you should be able to run the backend without package import errors.