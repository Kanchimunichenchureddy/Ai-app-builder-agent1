from app.core.config import settings
import google.generativeai as genai
from typing import Dict, Any
import httpx
import json

class GeminiService:
    """Service for Google Gemini AI integration."""
    
    def __init__(self):
        self.api_key = settings.GEMINI_API_KEY
        self.base_url = "https://generativelanguage.googleapis.com/v1beta"
        # Use the correct model name for Gemini
        self.model = "gemini-1.5-pro-latest"
    
    async def generate_response(self, system_prompt: str, user_prompt: str) -> str:
        """Generate response using Gemini AI."""
        if not self.api_key:
            return self._fallback_response(user_prompt)
            
        combined_prompt = f"{system_prompt}\n\nUser Request: {user_prompt}"
        
        data = {
            "contents": [{
                "parts": [{
                    "text": combined_prompt
                }]
            }],
            "generationConfig": {
                "temperature": 0.7,
                "maxOutputTokens": 4000,
            }
        }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/models/{self.model}:generateContent?key={self.api_key}",
                    json=data,
                    timeout=60.0
                )
                response.raise_for_status()
                result = response.json()
                return result["candidates"][0]["content"]["parts"][0]["text"]
        except Exception as e:
            print(f"Gemini API error: {e}")
            return self._fallback_response(user_prompt)
    
    async def generate_code(self, description: str, language: str, framework: str = None) -> str:
        """Generate code using Gemini AI."""
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
        """Fallback response when Gemini is not available."""
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
            "note": "Generated with fallback - Gemini API not configured"
        })