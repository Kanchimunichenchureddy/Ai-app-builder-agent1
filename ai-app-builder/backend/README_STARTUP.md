# AI App Builder - Backend Startup Guide

## Environment Configuration

Your backend is already configured with the necessary environment variables in the `.env` file. The following services are configured:

### AI Services
- ✅ OpenAI API Key: Configured
- ✅ DeepSeek API Key: Configured
- ✅ Gemini API Key: Configured

### Database Configuration
- ✅ MySQL Database: Configured
- Host: localhost
- Port: 3306
- User: root
- Password: tejadot12345
- Database:  ai_app_builder

### Security Configuration
- ✅ Secret Key: Configured
- ✅ Algorithm: HS256
- ✅ Access Token Expiry: 30 minutes

### External Services
- ✅ Google OAuth: Configured
- ✅ Stripe: Configured (test keys)

## Dependency Management

### Check Dependencies
First, verify that all dependencies are properly installed:

```bash
cd backend
python check_dependencies.py
```

### Check Package Versions
Check the exact versions of installed packages:

```bash
cd backend
python check_versions.py
```

### Check SQLAlchemy Specifically
Check SQLAlchemy installation and fix compatibility issues:

```bash
cd backend
python check_sqlalchemy.py
```

### Fix Pydantic Installation Issues
Fix Pydantic installation issues:

```bash
cd backend
python fix_pydantic.py
```

### Fix Environment Conflicts
Fix environment conflicts that may cause import issues:

```bash
cd backend
python fix_sqlalchemy_env.py
```

### Install/Reinstall Dependencies
If dependencies are missing or there are issues:

```bash
cd backend
python install_deps.py
```

This script will:
1. Check your Python environment for conflicts
2. Upgrade pip to the latest version
3. Install all required packages from requirements.txt with --force-reinstall
4. If that fails, install packages individually with special handling for Pydantic
5. Verify that all packages can be imported
6. Fix common SQLAlchemy, Pydantic, and environment compatibility issues

### Manual Installation
If the script doesn't work, you can manually install:

```bash
cd backend
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

## Troubleshooting Common Issues

### Environment Conflicts
If you see errors indicating packages are being imported from user site-packages (like `Roaming\Python` paths), this indicates an environment conflict:

1. Check your environment:
   ```bash
   python -c "import sys; [print(p) for p in sys.path if 'Roaming' in p]"
   ```

2. Fix environment conflicts:
   ```bash
   python fix_sqlalchemy_env.py
   ```

3. Or manually disable user site-packages:
   ```bash
   set PYTHONNOUSERSITE=1
   pip install sqlalchemy==2.0.23 --force-reinstall
   ```

### Pydantic Compatibility Issues
If you see errors like "No module named 'pydantic._internal'", this indicates a version compatibility issue:

1. Check your Pydantic version:
   ```bash
   python -c "import pydantic; print(pydantic.__version__)"
   ```

2. Fix Pydantic installation:
   ```bash
   python fix_pydantic.py
   ```

3. Or manually reinstall with correct versions:
   ```bash
   pip install pydantic==2.5.0 pydantic-settings==2.1.0 --force-reinstall
   ```

4. Or run the installation helper:
   ```bash
   python install_deps.py
   ```

### SQLAlchemy Compatibility Issues
If you see errors like "Class <class 'sqlalchemy.sql.elements.SQLCoreOperations'> directly inherits TypingOnly but has additional attributes", this indicates a SQLAlchemy compatibility issue:

1. Check your SQLAlchemy version:
   ```bash
   python -c "import sqlalchemy; print(sqlalchemy.__version__)"
   ```

2. Try reinstalling with force:
   ```bash
   pip install sqlalchemy==2.0.23 --force-reinstall
   ```

3. Or try an older compatible version:
   ```bash
   pip install sqlalchemy==1.4.46 --force-reinstall
   ```

4. Or run the installation helper:
   ```bash
   python install_deps.py
   ```

### Missing Packages
If you see "ModuleNotFoundError" errors:

1. Run the dependency checker:
   ```bash
   python check_dependencies.py
   ```

2. Install missing dependencies:
   ```bash
   python install_deps.py
   ```

### Network/Import Errors in Tests
If network connectivity tests fail with import errors:

1. Check package versions:
   ```bash
   python check_versions.py
   ```

2. Reinstall dependencies:
   ```bash
   python install_deps.py
   ```

## Testing Your Configuration

### 1. Configuration Test
Run the configuration test to verify all environment variables are properly loaded:

```bash
cd backend
python test_ai_connectivity.py
```

### 2. Network Connectivity Test
Test network connectivity to AI services:

```bash
cd backend
python test_network_connectivity.py
```

### 3. Backend Service Test
Test that the backend can be initialized without errors:

```bash
cd backend
python start_services.py
```

## Starting the Services

### Start the Backend Server
Once all tests pass, start the backend server:

```bash
cd backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Or use the provided batch file:

```bash
cd backend
start_backend.bat
```

### Start the Frontend Server
In a separate terminal, start the frontend:

```bash
cd frontend
npm start
```

## Verification

After starting both services, you can verify they're working correctly:

1. **Backend API Documentation**: Visit `http://localhost:8000/docs`
2. **Frontend Interface**: Visit `http://localhost:3000`
3. **Health Check**: Visit `http://localhost:8000/health`

## Troubleshooting

### Common Issues

1. **CORS Errors**: Already configured for localhost:3000 and localhost:3001
2. **Database Connection**: Ensure MySQL is running on localhost:3306
3. **API Key Issues**: Verify API keys in the `.env` file are valid
4. **Port Conflicts**: Ensure ports 3000 and 8000 are available
5. **Missing Dependencies**: Run `python check_dependencies.py` to verify

### Dependency Issues

If you see "ModuleNotFoundError" errors:

1. Run the dependency checker:
   ```bash
   python check_dependencies.py
   ```

2. Install missing dependencies:
   ```bash
   python install_deps.py
   ```

3. If that fails, try:
   ```bash
   cd backend
   pip install --upgrade pip
   pip install -r requirements.txt --force-reinstall
   ```

4. Restart your terminal and reactivate your virtual environment:
   ```bash
   deactivate
   # Activate your virtual environment again
   # On Windows:
   venv\Scripts\activate
   ```

### Environment Conflicts

If you see errors indicating packages are being imported from user site-packages:

1. Check for conflicts:
   ```bash
   python fix_sqlalchemy_env.py
   ```

2. Or manually fix:
   ```bash
   pip uninstall sqlalchemy pydantic --user
   pip install -r requirements.txt --force-reinstall
   ```

3. Or disable user site-packages:
   ```bash
   set PYTHONNOUSERSITE=1
   pip install -r requirements.txt --force-reinstall
   ```

### Pydantic Version Issues

If you see errors related to "pydantic._internal":

1. Check your current Pydantic version:
   ```bash
   python -c "import pydantic; print(pydantic.__version__)"
   ```

2. Fix Pydantic installation:
   ```bash
   python fix_pydantic.py
   ```

3. Or ensure you have the correct version (2.5.0):
   ```bash
   pip install pydantic==2.5.0 pydantic-settings==2.1.0 --force-reinstall
   ```

4. Or run the installation helper:
   ```bash
   python install_deps.py
   ```

### SQLAlchemy Compatibility Issues

If you see errors like "Class <class 'sqlalchemy.sql.elements.SQLCoreOperations'> directly inherits TypingOnly":

1. Check your current SQLAlchemy version:
   ```bash
   python -c "import sqlalchemy; print(sqlalchemy.__version__)"
   ```

2. Try reinstalling with force:
   ```bash
   pip install sqlalchemy==2.0.23 --force-reinstall
   ```

3. If that doesn't work, try an older compatible version:
   ```bash
   pip install sqlalchemy==1.4.46 --force-reinstall
   ```

4. Or run the installation helper:
   ```bash
   python install_deps.py
   ```

### Checking API Keys

To verify your API keys are working:

```bash
cd backend
python test_network_connectivity.py
```

### Database Setup

Ensure your MySQL database is set up:

1. Create database ` ai_app_builder`
2. Ensure user `root` with password `tejadot12345` has access
3. Run database migrations if needed

## Next Steps

1. Start the backend service
2. Start the frontend service
3. Visit the application at `http://localhost:3000`
4. Begin building AI-powered applications!

## Support

If you encounter any issues:
1. Check the logs in the terminal
2. Verify all environment variables in `.env`
3. Ensure all required services are running
4. Check network connectivity to AI services
5. Run `python check_dependencies.py` to verify dependencies

For persistent issues:
1. Close and reopen your terminal
2. Deactivate and reactivate your virtual environment
3. Run `python install_deps.py` again
4. Check for environment conflicts
5. Check for Pydantic version compatibility issues
6. Check for SQLAlchemy compatibility issues