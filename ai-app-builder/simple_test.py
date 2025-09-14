import sys
import os

# Add the current directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from backend.app.services.code_generator import CodeGenerator
    print("✓ Successfully imported CodeGenerator")
    
    # Create an instance
    code_gen = CodeGenerator()
    print("✓ Successfully created CodeGenerator instance")
    
    # Test a simple method
    analysis = {
        "project_type": "web_app",
        "features": ["authentication"]
    }
    
    # Test if the methods exist
    if hasattr(code_gen, 'generate_react_app'):
        print("✓ generate_react_app method exists")
    else:
        print("✗ generate_react_app method missing")
        
    if hasattr(code_gen, 'generate_fastapi_app'):
        print("✓ generate_fastapi_app method exists")
    else:
        print("✗ generate_fastapi_app method missing")
        
    print("Import test completed successfully!")
    
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()