# SQLAlchemy Python 3.13 Compatibility Fix

This document explains how to fix the SQLAlchemy import error that occurs with Python 3.13:

```
AssertionError: Class <class 'sqlalchemy.sql.elements.SQLCoreOperations'> directly inherits TypingOnly but has additional attributes {'__firstlineno__', '__static_attributes__'}.
```

## Root Cause

The error occurs because SQLAlchemy version 2.0.23 is not fully compatible with Python 3.13's typing system. The `SQLCoreOperations` class inherits from `TypingOnly` but has additional attributes that aren't allowed in Python 3.13.

## Solution Options

### Option 1: Update SQLAlchemy Version (Recommended)

Update to SQLAlchemy 2.0.35 or later which has Python 3.13 compatibility:

```bash
# Navigate to backend directory
cd c:\Users\teja.kanchi\Desktop\AI co-developer\ai-app-builder\backend

# Update requirements.txt
# Change sqlalchemy==2.0.23 to sqlalchemy==2.0.35

# Install updated version
pip install sqlalchemy==2.0.35 --force-reinstall
```

### Option 2: Use PowerShell Script

Run the provided PowerShell script:

```powershell
# Navigate to backend directory
cd c:\Users\teja.kanchi\Desktop\AI co-developer\ai-app-builder\backend

# Run the PowerShell script
.\update_sqlalchemy.ps1
```

### Option 3: Use Batch Script

Run the provided batch script:

```cmd
# Navigate to backend directory
cd c:\Users\teja.kanchi\Desktop\AI co-developer\ai-app-builder\backend

# Run the batch script
update_sqlalchemy.bat
```

### Option 4: Emergency Fix Script

If the above options don't work, use the emergency fix script:

```bash
# Navigate to backend directory
cd c:\Users\teja.kanchi\Desktop\AI co-developer\ai-app-builder\backend

# Run the emergency fix script
python emergency_sqlalchemy_fix.py
```

## Manual Fix Steps

If scripts don't work, manually fix the issue:

1. Set environment variable to disable user site-packages:
   ```cmd
   set PYTHONNOUSERSITE=1
   ```

2. Uninstall existing SQLAlchemy:
   ```cmd
   pip uninstall sqlalchemy -y
   ```

3. Install compatible version:
   ```cmd
   pip install sqlalchemy==2.0.35 --force-reinstall
   ```

## Verification

Test that SQLAlchemy imports correctly:

```bash
python -c "import sqlalchemy; print(f'SQLAlchemy version: {sqlalchemy.__version__}')"
```

If successful, you should see:
```
SQLAlchemy version: 2.0.35
```

## Additional Troubleshooting

If you still have issues:

1. Check if you're in the correct virtual environment:
   ```bash
   where python
   ```

2. Check installed packages:
   ```bash
   pip list | findstr sqlalchemy
   ```

3. Clear pip cache:
   ```bash
   pip cache purge
   ```

4. Reinstall in clean environment:
   ```bash
   pip uninstall sqlalchemy -y
   pip install sqlalchemy==2.0.35 --no-cache-dir --force-reinstall
   ```

## Prevention

To prevent future issues:
1. Keep SQLAlchemy updated to versions that support your Python version
2. Use virtual environments to avoid conflicts
3. Regularly update dependencies

After applying the fix, you should be able to run the backend without SQLAlchemy import errors.