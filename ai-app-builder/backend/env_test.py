import os
print("OPENROUTER_API_KEY in env:", "OPENROUTER_API_KEY" in os.environ)
print("API Key value:", os.environ.get("OPENROUTER_API_KEY", "Not found"))