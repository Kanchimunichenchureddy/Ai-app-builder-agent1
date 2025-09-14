import asyncio
import json
from backend.app.services.code_generator import CodeGenerator

async def test_code_generator():
    """Test the code generator to ensure it creates actual project files."""
    print("Testing CodeGenerator...")
    
    # Create an instance of the code generator
    code_generator = CodeGenerator()
    
    # Create a sample analysis
    analysis = {
        "project_type": "dashboard",
        "features": ["authentication", "charts", "widgets", "responsive_design"],
        "tech_stack": {
            "frontend": "react",
            "backend": "fastapi",
            "database": "mysql"
        },
        "description": "Analytics dashboard with charts and widgets"
    }
    
    print("Generating React app...")
    react_files = await code_generator.generate_react_app(analysis)
    print(f"Generated {len(react_files)} React files")
    
    print("Generating FastAPI app...")
    fastapi_files = await code_generator.generate_fastapi_app(analysis)
    print(f"Generated {len(fastapi_files)} FastAPI files")
    
    print("Generating database schema...")
    db_files = await code_generator.generate_database_schema(analysis)
    print(f"Generated {len(db_files)} database files")
    
    print("Generating deployment config...")
    deploy_files = await code_generator.generate_deployment_config(analysis)
    print(f"Generated {len(deploy_files)} deployment files")
    
    # Check if we have actual content, not just placeholders
    app_js_content = react_files.get("frontend/src/App.js", "")
    if app_js_content and not app_js_content.startswith("//") and len(app_js_content) > 100:
        print("✓ React App.js contains actual code")
    else:
        print("✗ React App.js contains placeholder code")
        print(f"Content: {app_js_content[:100]}...")
    
    main_py_content = fastapi_files.get("backend/app/main.py", "")
    if main_py_content and not main_py_content.startswith("#") and len(main_py_content) > 100:
        print("✓ FastAPI main.py contains actual code")
    else:
        print("✗ FastAPI main.py contains placeholder code")
        print(f"Content: {main_py_content[:100]}...")
    
    schema_sql_content = db_files.get("database/schema.sql", "")
    if schema_sql_content and not schema_sql_content.startswith("--") and len(schema_sql_content) > 100:
        print("✓ Database schema.sql contains actual code")
    else:
        print("✗ Database schema.sql contains placeholder code")
        print(f"Content: {schema_sql_content[:100]}...")
    
    dockerfile_content = deploy_files.get("Dockerfile", "")
    if dockerfile_content and not dockerfile_content.startswith("#") and len(dockerfile_content) > 50:
        print("✓ Dockerfile contains actual code")
    else:
        print("✗ Dockerfile contains placeholder code")
        print(f"Content: {dockerfile_content[:100]}...")
    
    # Print sample of generated files
    print("\nSample generated files:")
    print("=" * 50)
    
    if react_files:
        print("React App.js (first 500 chars):")
        print(app_js_content[:500] + ("..." if len(app_js_content) > 500 else ""))
        print()
    
    if fastapi_files:
        print("FastAPI main.py (first 500 chars):")
        print(main_py_content[:500] + ("..." if len(main_py_content) > 500 else ""))
        print()
    
    print("Test completed!")

if __name__ == "__main__":
    asyncio.run(test_code_generator())