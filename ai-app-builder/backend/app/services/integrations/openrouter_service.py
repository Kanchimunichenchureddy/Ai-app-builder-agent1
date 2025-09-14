from typing import Dict, Any
import httpx
import json
from app.core.config import settings

class OpenRouterService:
    """Service for OpenRouter API integration."""
    
    def __init__(self):
        self.api_key = settings.OPENROUTER_API_KEY
        self.base_url = "https://openrouter.ai/api/v1"  # Changed from api.openrouter.ai to openrouter.ai
        # Use a free model that doesn't require payment
        self.default_model = "mistralai/mistral-7b-instruct"  # Free model
        
        if self.api_key:
            print("OpenRouter API key is configured")
        
    async def generate_response(
        self, 
        system_prompt: str, 
        user_prompt: str, 
        model: str = None, 
        max_tokens: int = 4000, 
        temperature: float = 0.7
    ) -> str:
        """Generate response using OpenRouter."""
        if not self.api_key:
            error_message = "OpenRouter API key is not configured. Please set the OPENROUTER_API_KEY environment variable."
            print(error_message)
            # Return a fallback response instead of raising an exception
            return f"// Fallback response: {error_message}"
            
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost:3000",  # For OpenRouter tracking
            "X-Title": "AI App Builder"
        }
        
        data = {
            "model": model or self.default_model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "max_tokens": max_tokens,
            "temperature": temperature
        }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/chat/completions",
                    headers=headers,
                    json=data,
                    timeout=30.0  # Reduced timeout for better user experience
                )
                # Check for specific error responses
                if response.status_code == 401:
                    error_text = response.text
                    if "User not found" in error_text:
                        error_message = "OpenRouter API error: Invalid API key or account not found. Please check your API key at https://openrouter.ai/"
                        print(error_message)
                        # Return a fallback response instead of raising an exception
                        return f"// Fallback response: {error_message}"
                    else:
                        error_message = f"OpenRouter API error: Unauthorized (401). Response: {error_text}"
                        print(error_message)
                        # Return a fallback response instead of raising an exception
                        return f"// Fallback response: {error_message}"
                elif response.status_code == 402:
                    error_message = "OpenRouter API error: Payment required (402). Please check your account balance at https://openrouter.ai/"
                    print(error_message)
                    # Return a fallback response instead of raising an exception
                    return f"// Fallback response: {error_message}"
                elif response.status_code == 429:
                    error_message = "OpenRouter API error: Rate limit exceeded (429). Please try again later."
                    print(error_message)
                    # Return a fallback response instead of raising an exception
                    return f"// Fallback response: {error_message}"
                elif response.status_code >= 400:
                    error_message = f"OpenRouter API error: HTTP {response.status_code}. Response: {response.text}"
                    print(error_message)
                    # Return a fallback response instead of raising an exception
                    return f"// Fallback response: {error_message}"
                    
                response.raise_for_status()
                result = response.json()
                return result["choices"][0]["message"]["content"]
        except httpx.TimeoutException as e:
            error_message = f"OpenRouter API error: Request timeout. The AI service is taking too long to respond."
            print(error_message)
            # Return a fallback response instead of raising an exception
            return f"// Fallback response: {error_message}"
        except Exception as e:
            error_message = f"OpenRouter API error: {e}"
            print(error_message)
            # Add more detailed logging
            import traceback
            traceback.print_exc()
            # Return a fallback response instead of raising an exception
            return f"// Fallback response: {error_message}"
    
    async def generate_code(self, description: str, language: str, framework: str = None) -> str:
        """Generate code using OpenRouter."""
        system_prompt = f"""
        You are an expert {language} developer. Generate clean, production-ready code.
        {"Framework: " + framework if framework else ""}
        
        Requirements:
        - Follow best practices
        - Include proper error handling
        - Add comments for complex logic
        - Make code modular and reusable
        - Include necessary imports
        - Ensure code is self-contained and runnable
        - Include example usage when relevant
        - Add security considerations
        - Optimize for performance
        """
        
        user_prompt = f"Generate {language} code for: {description}"
        
        return await self.generate_response(system_prompt, user_prompt)
    
    def _fallback_response(self, prompt: str) -> str:
        """Fallback response when OpenRouter is not available."""
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
            "note": "Generated with fallback - OpenRouter API not configured"
        })