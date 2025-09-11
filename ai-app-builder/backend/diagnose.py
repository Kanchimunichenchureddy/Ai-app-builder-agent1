#!/usr/bin/env python3
"""
Diagnostic script to check the status of the AI App Builder backend
"""
import os
import sys
import importlib

def check_python_environment():
    print("=== Python Environment Check ===")
    print(f"Python version: {sys.version}")
    print(f"Python executable: {sys.executable}")
    print(f"Current working directory: {os.getcwd()}")
    print(f"Python path: {sys.path[:5]}")
    print()

def check_virtual_environment():
    print("=== Virtual Environment Check ===")
    venv_path = os.environ.get('VIRTUAL_ENV')
    if venv_path:
        print(f"Virtual environment active: {venv_path}")
    else:
        print("No virtual environment detected")
    
    # Check if we're in the expected venv
    expected_venv = os.path.join(os.getcwd(), 'venv')
    if os.path.exists(expected_venv):
        print(f"Virtual environment directory exists: {expected_venv}")
    else:
        print(f"Virtual environment directory not found: {expected_venv}")
    print()

def check_dependencies():
    print("=== Dependency Check ===")
    dependencies = [
        'fastapi',
        'uvicorn',
        'sqlalchemy',
        'pydantic',
        'pydantic_settings',
        'pymysql'
    ]
    
    for dep in dependencies:
        try:
            module = importlib.import_module(dep)
            if hasattr(module, '__version__'):
                print(f"✓ {dep}: {module.__version__}")
            else:
                print(f"✓ {dep}: imported successfully")
        except ImportError as e:
            print(f"✗ {dep}: failed to import - {e}")
        except Exception as e:
            print(f"✗ {dep}: error - {e}")
    print()

def check_environment_variables():
    print("=== Environment Variables Check ===")
    required_vars = [
        'DB_HOST',
        'DB_PORT',
        'DB_USER',
        'DB_PASSWORD',
        'DB_NAME',
        'SECRET_KEY'
    ]
    
    for var in required_vars:
        value = os.environ.get(var, 'NOT SET')
        if var in ['DB_PASSWORD', 'SECRET_KEY'] and value != 'NOT SET':
            # Mask sensitive values
            value = '*' * min(len(value), 8) + '...' if len(value) > 3 else '*' * len(value)
        print(f"{var}: {value}")
    print()

def check_imports():
    print("=== Import Check ===")
    modules_to_check = [
        'app.main',
        'app.core.config',
        'app.core.database',
        'app.api.auth',
        'app.api.projects',
        'app.api.builder'
    ]
    
    for module in modules_to_check:
        try:
            importlib.import_module(module)
            print(f"✓ {module}: imported successfully")
        except ImportError as e:
            print(f"✗ {module}: failed to import - {e}")
        except Exception as e:
            print(f"✗ {module}: error - {e}")
            import traceback
            traceback.print_exc()
    print()

def main():
    print("AI App Builder Backend Diagnostic")
    print("=" * 50)
    print()
    
    check_python_environment()
    check_virtual_environment()
    check_dependencies()
    check_environment_variables()
    check_imports()
    
    print("=== Diagnostic Complete ===")

if __name__ == "__main__":
    main()