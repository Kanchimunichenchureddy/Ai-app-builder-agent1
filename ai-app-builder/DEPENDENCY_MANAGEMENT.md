# AI App Builder - Dependency Management

This document explains how to manage dependencies for the AI App Builder backend.

## Required Dependencies

The AI App Builder backend requires the following Python packages:

- fastapi==0.104.1
- uvicorn[standard]==0.24.0
- sqlalchemy==2.0.35
- pymysql==1.1.0
- python-multipart==0.0.6
- python-jose[cryptography]==3.3.0
- passlib[bcrypt]==1.7.4
- python-dotenv==1.0.0
- pydantic==2.5.0
- pydantic-settings==2.1.0
- alembic==1.13.0
- httpx==0.25.2
- stripe==7.8.0
- jinja2==3.1.2
- aiofiles==23.2.1
- docker==6.1.3
- gitpython==3.1.40
- requests==2.31.0

## Installing Dependencies

### Option 1: Install from requirements.txt (Recommended)

From the `backend` directory:
```bash
pip install -r requirements.txt
```

### Option 2: Install individual packages

```bash
pip install fastapi==0.104.1
pip install uvicorn[standard]==0.24.0
pip install sqlalchemy==2.0.35
pip install pymysql==1.1.0
pip install python-multipart==0.0.6
pip install python-jose[cryptography]==3.3.0
pip install passlib[bcrypt]==1.7.4
pip install python-dotenv==1.0.0
pip install pydantic==2.5.0
pip install pydantic-settings==2.1.0
pip install alembic==1.13.0
pip install httpx==0.25.2
pip install stripe==7.8.0
pip install jinja2==3.1.2
pip install aiofiles==23.2.1
pip install docker==6.1.3
pip install gitpython==3.1.40
pip install requests==2.31.0
```

## Dependency Verification Tools

### Check Dependencies Script
Run the dependency check to see what's installed:
```bash
python CHECK_DEPENDENCIES.py
```

Or double-click on `CHECK_DEPENDENCIES.bat`

### Install Missing Dependencies Script
Automatically install missing dependencies:
```bash
python INSTALL_MISSING_DEPS.py
```

Or double-click on `INSTALL_MISSING_DEPS.bat`

### Verify Installation Script
Verify that all dependencies are working correctly:
```bash
python VERIFY_INSTALLATION.py
```

Or double-click on `VERIFY_INSTALLATION.bat`

## Common Issues and Solutions

### "No module named X" errors

If you see errors like "No module named 'multipart'" or "No module named 'jose'", install the missing packages:

```bash
pip install python-multipart python-jose[cryptography] python-dotenv pydantic-settings gitpython
```

### Version conflicts

If you encounter version conflicts, try installing with `--force-reinstall`:

```bash
pip install -r requirements.txt --force-reinstall
```

### Virtual Environment Issues

Make sure you're in the correct virtual environment:

1. Activate your virtual environment:
   ```bash
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

2. Then install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Permission Errors

If you get permission errors, try installing with the `--user` flag:

```bash
pip install -r requirements.txt --user
```

## Updating Dependencies

To update dependencies to the latest compatible versions:

```bash
pip install -r requirements.txt --upgrade
```

## Checking Installed Versions

To see what versions are currently installed:

```bash
pip list
```

## Troubleshooting

### If pip is not recognized

Make sure Python and pip are in your PATH:

1. Check if Python is installed:
   ```bash
   python --version
   ```

2. Check if pip is installed:
   ```bash
   pip --version
   ```

3. If pip is not found, install it:
   ```bash
   python -m ensurepip --upgrade
   ```

### If you're still having issues

1. Try creating a fresh virtual environment:
   ```bash
   python -m venv fresh_venv
   fresh_venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. Check for conflicting Python installations:
   ```bash
   where python
   ```

3. Make sure you're using Python 3.8 or higher:
   ```bash
   python --version
   ```

## Best Practices

1. Always use a virtual environment for Python projects
2. Keep your requirements.txt file up to date
3. Pin specific versions to ensure reproducible builds
4. Regularly update dependencies to get security fixes
5. Test your application after updating dependencies

## Next Steps

After installing dependencies:

1. Run the verification script:
   ```bash
   python VERIFY_INSTALLATION.py
   ```

2. Start the backend server:
   ```bash
   python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

3. Verify the backend is running:
   ```bash
   python VERIFY_BACKEND.py
   ```