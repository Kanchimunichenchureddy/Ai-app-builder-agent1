import os
import sys

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from app.core.config import settings
    print("OpenRouter API Key configured:", bool(settings.OPENROUTER_API_KEY))
    if settings.OPENROUTER_API_KEY:
        print("API Key length:", len(settings.OPENROUTER_API_KEY))
        print("API Key starts with:", settings.OPENROUTER_API_KEY[:10])
    else:
        print("No API Key found")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()