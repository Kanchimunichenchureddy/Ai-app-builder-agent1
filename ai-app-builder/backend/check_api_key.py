import os
import sys

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from app.core.config import settings
    print("✅ OpenRouter API Key configured:", bool(settings.OPENROUTER_API_KEY))
    if settings.OPENROUTER_API_KEY:
        print("🔑 API Key length:", len(settings.OPENROUTER_API_KEY))
        print("🔑 API Key starts with:", settings.OPENROUTER_API_KEY[:15] + "...")
        # Let's also check the exact value to make sure there are no hidden characters
        print("🔑 Full API Key (first 20 chars):", repr(settings.OPENROUTER_API_KEY[:20]))
    else:
        print("❌ No API Key found")
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()