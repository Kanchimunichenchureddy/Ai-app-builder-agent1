from typing import Dict, Any, List, Optional
import httpx
import json
from ....core.config import settings

class DeepSeekService:
    """
    Service for handling DeepSeek API integrations.
    Supports code generation, explanation, and optimization using DeepSeek models.
    """
    
    def __init__(self):
        self.api_key = settings.DEEPSEEK_API_KEY
        self.base_url = "https://api.deepseek.com/v1"
        self.client = httpx.AsyncClient(
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            },
            timeout=30.0
        )
    
    async def generate_code(
        self,
        prompt: str,
        model: str = "deepseek-coder",
        max_tokens: int = 2000,
        temperature: float = 0.7
    ) -> Dict[str, Any]:
        """
        Generate code using DeepSeek AI.
        
        Args:
            prompt: The prompt for code generation
            model: The DeepSeek model to use
            max_tokens: Maximum number of tokens to generate
            temperature: Sampling temperature
            
        Returns:
            Dict containing generated code
        """
        try:
            payload = {
                "model": model,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "max_tokens": max_tokens,
                "temperature": temperature
            }
            
            response = await self.client.post(
                f"{self.base_url}/chat/completions",
                json=payload
            )
            
            if response.status_code == 200:
                result = response.json()
                return {
                    "success": True,
                    "code": result["choices"][0]["message"]["content"],
                    "model": result["model"],
                    "usage": result.get("usage", {})
                }
            else:
                return {
                    "success": False,
                    "error": f"API request failed with status {response.status_code}",
                    "error_type": "api_error"
                }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "error_type": "deepseek_api_error"
            }
    
    async def explain_code(
        self,
        code: str,
        explanation_request: str,
        model: str = "deepseek-chat",
        max_tokens: int = 1000
    ) -> Dict[str, Any]:
        """
        Explain code using DeepSeek AI.
        
        Args:
            code: The code to explain
            explanation_request: Specific explanation request
            model: The DeepSeek model to use
            max_tokens: Maximum number of tokens to generate
            
        Returns:
            Dict containing explanation
        """
        try:
            prompt = f"""
            Please explain the following code:
            
            ```code
            {code}
            ```
            
            Specific request: {explanation_request}
            
            Provide a clear, detailed explanation that would be helpful to developers.
            """
            
            payload = {
                "model": model,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "max_tokens": max_tokens,
                "temperature": 0.3
            }
            
            response = await self.client.post(
                f"{self.base_url}/chat/completions",
                json=payload
            )
            
            if response.status_code == 200:
                result = response.json()
                return {
                    "success": True,
                    "explanation": result["choices"][0]["message"]["content"],
                    "model": result["model"],
                    "usage": result.get("usage", {})
                }
            else:
                return {
                    "success": False,
                    "error": f"API request failed with status {response.status_code}",
                    "error_type": "api_error"
                }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "error_type": "deepseek_api_error"
            }
    
    async def debug_code(
        self,
        code: str,
        error_message: Optional[str] = None,
        model: str = "deepseek-chat",
        max_tokens: int = 1500
    ) -> Dict[str, Any]:
        """
        Debug code using DeepSeek AI.
        
        Args:
            code: The code to debug
            error_message: Error message if available
            model: The DeepSeek model to use
            max_tokens: Maximum number of tokens to generate
            
        Returns:
            Dict containing debug analysis
        """
        try:
            prompt = f"""
            Please debug the following code:
            
            ```code
            {code}
            ```
            
            {f"Error message: {error_message}" if error_message else "No error message provided"}
            
            Provide:
            1. Identification of issues
            2. Explanation of problems
            3. Fixed code
            4. Best practices to avoid similar issues
            """
            
            payload = {
                "model": model,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "max_tokens": max_tokens,
                "temperature": 0.3
            }
            
            response = await self.client.post(
                f"{self.base_url}/chat/completions",
                json=payload
            )
            
            if response.status_code == 200:
                result = response.json()
                return {
                    "success": True,
                    "debug_analysis": result["choices"][0]["message"]["content"],
                    "model": result["model"],
                    "usage": result.get("usage", {})
                }
            else:
                return {
                    "success": False,
                    "error": f"API request failed with status {response.status_code}",
                    "error_type": "api_error"
                }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "error_type": "deepseek_api_error"
            }
    
    async def optimize_code(
        self,
        code: str,
        optimization_goal: str = "performance",
        model: str = "deepseek-coder",
        max_tokens: int = 1500
    ) -> Dict[str, Any]:
        """
        Optimize code using DeepSeek AI.
        
        Args:
            code: The code to optimize
            optimization_goal: Goal for optimization (performance, readability, etc.)
            model: The DeepSeek model to use
            max_tokens: Maximum number of tokens to generate
            
        Returns:
            Dict containing optimized code and suggestions
        """
        try:
            prompt = f"""
            Please optimize the following code for {optimization_goal}:
            
            ```code
            {code}
            ```
            
            Provide:
            1. Optimized code
            2. Explanation of improvements
            3. Performance benefits
            4. Best practices applied
            """
            
            payload = {
                "model": model,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "max_tokens": max_tokens,
                "temperature": 0.3
            }
            
            response = await self.client.post(
                f"{self.base_url}/chat/completions",
                json=payload
            )
            
            if response.status_code == 200:
                result = response.json()
                return {
                    "success": True,
                    "optimized_code": result["choices"][0]["message"]["content"],
                    "model": result["model"],
                    "usage": result.get("usage", {})
                }
            else:
                return {
                    "success": False,
                    "error": f"API request failed with status {response.status_code}",
                    "error_type": "api_error"
                }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "error_type": "deepseek_api_error"
            }
    
    async def get_available_models(self) -> Dict[str, Any]:
        """
        Get available DeepSeek models.
        
        Returns:
            Dict containing available models
        """
        try:
            response = await self.client.get(f"{self.base_url}/models")
            
            if response.status_code == 200:
                result = response.json()
                return {
                    "success": True,
                    "models": result.get("data", [])
                }
            else:
                return {
                    "success": False,
                    "error": f"API request failed with status {response.status_code}",
                    "error_type": "api_error"
                }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "error_type": "deepseek_api_error"
            }