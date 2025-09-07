from typing import Dict, Any, List
import json
from ..core.config import settings
import httpx

class OpenAIService:
    """Service for OpenAI API integration."""
    
    def __init__(self):
        self.api_key = settings.OPENAI_API_KEY
        self.base_url = "https://api.openai.com/v1"
        self.model = "gpt-4"
        
    async def generate_response(self, system_prompt: str, user_prompt: str) -> str:
        """Generate response using OpenAI."""
        if not self.api_key:
            return self._fallback_response(user_prompt)
            
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "max_tokens": 4000,
            "temperature": 0.7
        }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/chat/completions",
                    headers=headers,
                    json=data,
                    timeout=60.0
                )
                response.raise_for_status()
                result = response.json()
                return result["choices"][0]["message"]["content"]
        except Exception as e:
            print(f"OpenAI API error: {e}")
            return self._fallback_response(user_prompt)
    
    async def generate_code(self, description: str, language: str, framework: str = None) -> str:
        """Generate code using OpenAI."""
        system_prompt = f"""
        You are an expert {language} developer. Generate clean, production-ready code.
        {"Framework: " + framework if framework else ""}
        
        Requirements:
        - Follow best practices
        - Include proper error handling
        - Add comments for complex logic
        - Make code modular and reusable
        - Include necessary imports
        """
        
        user_prompt = f"Generate {language} code for: {description}"
        
        return await self.generate_response(system_prompt, user_prompt)
    
    def _fallback_response(self, prompt: str) -> str:
        """Fallback response when OpenAI is not available."""
        return json.dumps({
            "project_type": "web_app",
            "features": ["authentication", "responsive_design"],
            "tech_recommendations": {
                "frontend": "react",
                "backend": "fastapi",
                "database": "mysql"
            },
            "integrations": [],
            "deployment": "docker",
            "note": "Generated with fallback - OpenAI API not configured"
        })