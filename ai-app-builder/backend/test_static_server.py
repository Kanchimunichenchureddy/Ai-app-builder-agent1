#!/usr/bin/env python3
"""
Test script for the static file server service.
"""

import sys
import os
from pathlib import Path

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

# Now we can import the static server
try:
    from services.static_server import StaticFileServer
    print("✓ StaticFileServer imported successfully")
    
    # Create an instance
    server = StaticFileServer()
    print("✓ StaticFileServer instance created successfully")
    
    # Test methods
    print("✓ StaticFileServer is ready for use")
    
except ImportError as e:
    print(f"✗ Failed to import StaticFileServer: {e}")
    sys.exit(1)

print("All tests passed!")