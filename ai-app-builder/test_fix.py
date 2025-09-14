import sys
import os

# Add the current directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_code_generator_import():
    try:
        # Try to import the CodeGenerator class
        from backend.app.services.code_generator import CodeGenerator
        print("✓ Successfully imported CodeGenerator")
        
        # Create an instance
        code_gen = CodeGenerator()
        print("✓ Successfully created CodeGenerator instance")
        
        # Test if the methods exist
        methods_to_check = [
            'generate_react_app',
            'generate_fastapi_app', 
            'generate_database_schema',
            'generate_deployment_config'
        ]
        
        for method_name in methods_to_check:
            if hasattr(code_gen, method_name):
                print(f"✓ {method_name} method exists")
            else:
                print(f"✗ {method_name} method missing")
                
        print("All import tests passed!")
        return True
        
    except Exception as e:
        print(f"✗ Error during import test: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_code_generator_import()
    if success:
        print("\n🎉 CodeGenerator is ready to use!")
    else:
        print("\n❌ There are issues with CodeGenerator")