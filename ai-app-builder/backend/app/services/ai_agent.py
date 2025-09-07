from typing import Dict, List, Optional, Any
import json
import os
from pathlib import Path
import asyncio
from .integrations.openai_service import OpenAIService
from .integrations.gemini_service import GeminiService
from .integrations.stripe_service import StripeService
from .integrations.google_service import GoogleService
from .integrations.deepseek_service import DeepSeekService
from .code_generator import CodeGenerator
from .framework_generator import FrameworkGenerator
from .deployer import DeployerService
from ..core.config import settings

class AIAgentService:
    """
    Core AI Agent that can build unlimited applications.
    This is the brain of the AI App Builder.
    """
    
    def __init__(self):
        self.openai_service = OpenAIService()
        self.gemini_service = GeminiService()
        self.stripe_service = StripeService()
        self.google_service = GoogleService()
        self.deepseek_service = DeepSeekService()
        self.code_generator = CodeGenerator()
        self.framework_generator = FrameworkGenerator()
        self.deployer = DeployerService()
        
    async def analyze_request(self, user_request: str) -> Dict[str, Any]:
        """
        Analyze user request and determine what kind of application to build.
        """
        system_prompt = """
        You are an expert AI agent that analyzes user requests to build applications.
        Analyze the request and return a structured response with:
        1. Project type (web_app, mobile_app, dashboard, ecommerce, blog, crm, chat, api)
        2. Required features
        3. Technology recommendations
        4. Database schema needs
        5. API integrations needed
        6. Deployment strategy
        
        Return only valid JSON.
        """
        
        user_prompt = f"""
        User Request: {user_request}
        
        Analyze this request and provide a detailed project specification.
        """
        
        analysis = await self.openai_service.generate_response(
            system_prompt, user_prompt
        )
        
        try:
            return json.loads(analysis)
        except json.JSONDecodeError:
            # Fallback analysis
            return self._fallback_analysis(user_request)
    
    async def generate_project(self, analysis: Dict[str, Any], project_name: str, tech_stack: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        Generate complete project based on analysis.
        """
        # Use provided tech stack or defaults
        if tech_stack:
            selected_tech_stack = tech_stack
        else:
            selected_tech_stack = {
                "frontend": analysis.get("tech_stack", {}).get("frontend", "react"),
                "backend": analysis.get("tech_stack", {}).get("backend", "fastapi"),
                "database": analysis.get("tech_stack", {}).get("database", "mysql")
            }
        
        project_data = {
            "name": project_name,
            "type": analysis.get("project_type", "web_app"),
            "features": analysis.get("features", []),
            "tech_stack": selected_tech_stack,
            "files": {},
            "structure": {}
        }
        
        # Use advanced framework generator if non-default stack is specified
        if (selected_tech_stack["frontend"] != "react" or 
            selected_tech_stack["backend"] != "fastapi" or 
            selected_tech_stack["database"] != "mysql"):
            
            # Use advanced framework generator
            advanced_project = await self.framework_generator.generate_project_with_frameworks(
                selected_tech_stack["frontend"],
                selected_tech_stack["backend"],
                selected_tech_stack["database"],
                analysis,
                project_name
            )
            project_data.update(advanced_project)
        else:
            # Use default generation
            project_data["structure"] = await self._generate_project_structure(analysis)
            project_data["files"] = await self._generate_all_files(analysis, project_data["structure"])
        
        return project_data
    
    async def _generate_project_structure(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Generate project folder structure."""
        project_type = analysis.get("project_type", "web_app")
        
        base_structure = {
            "frontend": {
                "src": {
                    "components": {},
                    "pages": {},
                    "services": {},
                    "utils": {},
                    "styles": {}
                },
                "public": {}
            },
            "backend": {
                "app": {
                    "api": {},
                    "models": {},
                    "schemas": {},
                    "services": {},
                    "core": {}
                }
            },
            "database": {
                "migrations": {},
                "schemas": {}
            },
            "deployment": {}
        }
        
        # Customize structure based on project type
        if project_type == "ecommerce":
            base_structure["frontend"]["src"]["components"]["products"] = {}
            base_structure["frontend"]["src"]["components"]["cart"] = {}
            base_structure["frontend"]["src"]["components"]["checkout"] = {}
            base_structure["backend"]["app"]["services"]["payment"] = {}
            
        elif project_type == "dashboard":
            base_structure["frontend"]["src"]["components"]["charts"] = {}
            base_structure["frontend"]["src"]["components"]["widgets"] = {}
            
        elif project_type == "chat":
            base_structure["frontend"]["src"]["components"]["chat"] = {}
            base_structure["backend"]["app"]["services"]["websocket"] = {}
            
        return base_structure
    
    async def _generate_all_files(self, analysis: Dict[str, Any], structure: Dict[str, Any]) -> Dict[str, str]:
        """Generate all project files."""
        files = {}
        
        # Generate frontend files
        frontend_files = await self.code_generator.generate_react_app(analysis)
        files.update(frontend_files)
        
        # Generate backend files  
        backend_files = await self.code_generator.generate_fastapi_app(analysis)
        files.update(backend_files)
        
        # Generate database files
        database_files = await self.code_generator.generate_database_schema(analysis)
        files.update(database_files)
        
        # Generate deployment files
        deployment_files = await self.code_generator.generate_deployment_config(analysis)
        files.update(deployment_files)
        
        return files
    
    async def modify_project(self, project_id: int, modification_request: str) -> Dict[str, Any]:
        """
        Modify existing project based on user request.
        """
        system_prompt = """
        You are an expert AI agent that modifies existing applications.
        Analyze the modification request and determine:
        1. Which files need to be changed
        2. What specific changes to make
        3. Any new files that need to be created
        4. Dependencies that need to be updated
        
        Return only valid JSON with the changes.
        """
        
        user_prompt = f"""
        Modification Request: {modification_request}
        
        Provide specific file changes needed to implement this modification.
        """
        
        modification_plan = await self.openai_service.generate_response(
            system_prompt, user_prompt
        )
        
        try:
            changes = json.loads(modification_plan)
            return await self._apply_modifications(project_id, changes)
        except json.JSONDecodeError:
            return {"error": "Failed to parse modification plan"}
    
    async def _apply_modifications(self, project_id: int, changes: Dict[str, Any]) -> Dict[str, Any]:
        """Apply modifications to project."""
        # Implementation for applying changes to existing project
        return {
            "project_id": project_id,
            "changes_applied": changes,
            "status": "success"
        }
    
    def _fallback_analysis(self, user_request: str) -> Dict[str, Any]:
        """Fallback analysis when AI parsing fails."""
        # Simple keyword-based analysis
        request_lower = user_request.lower()
        
        if "ecommerce" in request_lower or "shop" in request_lower:
            project_type = "ecommerce"
        elif "dashboard" in request_lower or "analytics" in request_lower:
            project_type = "dashboard"
        elif "blog" in request_lower or "cms" in request_lower:
            project_type = "blog"
        elif "chat" in request_lower or "messaging" in request_lower:
            project_type = "chat"
        elif "crm" in request_lower or "customer" in request_lower:
            project_type = "crm"
        else:
            project_type = "web_app"
        
        return {
            "project_type": project_type,
            "features": ["user_authentication", "responsive_design"],
            "tech_stack": {
                "frontend": "react",
                "backend": "fastapi",
                "database": "mysql"
            },
            "complexity": "medium"
        }
    
    async def get_supported_frameworks(self) -> Dict[str, Any]:
        """Get all supported frameworks and configurations."""
        return self.framework_generator.get_supported_frameworks()
    
    async def generate_project_with_custom_stack(
        self, 
        analysis: Dict[str, Any], 
        project_name: str,
        frontend_framework: str,
        backend_framework: str,
        database: str
    ) -> Dict[str, Any]:
        """Generate project with custom technology stack."""
        return await self.framework_generator.generate_project_with_frameworks(
            frontend_framework,
            backend_framework,
            database,
            analysis,
            project_name
        )
    
    async def get_framework_recommendations(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Get framework recommendations based on project analysis."""
        project_type = analysis.get("project_type", "web_app")
        features = analysis.get("features", [])
        
        recommendations = {
            "primary": {
                "frontend": "react",
                "backend": "fastapi",
                "database": "mysql",
                "reason": "Default balanced stack for web applications"
            },
            "alternatives": []
        }
        
        # Mobile app recommendations
        if "mobile" in project_type or "mobile_app" in features:
            recommendations["alternatives"].append({
                "frontend": "react_native",
                "backend": "fastapi",
                "database": "mysql",
                "reason": "Cross-platform mobile development"
            })
            recommendations["alternatives"].append({
                "frontend": "flutter",
                "backend": "fastapi",
                "database": "postgresql",
                "reason": "High-performance native mobile apps"
            })
        
        # Enterprise app recommendations
        if "enterprise" in features or "large_scale" in features:
            recommendations["alternatives"].append({
                "frontend": "angular",
                "backend": "spring_boot",
                "database": "postgresql",
                "reason": "Enterprise-grade frameworks with strong typing"
            })
        
        # Real-time app recommendations
        if "real_time" in features or "chat" in project_type:
            recommendations["alternatives"].append({
                "frontend": "react",
                "backend": "express",
                "database": "mongodb",
                "reason": "Optimized for real-time applications"
            })
        
        # SSR/SEO focused recommendations
        if "seo" in features or "blog" in project_type:
            recommendations["primary"] = {
                "frontend": "nextjs",
                "backend": "fastapi",
                "database": "postgresql",
                "reason": "Server-side rendering for better SEO"
            }
        
        return recommendations
    
    async def get_project_templates(self) -> List[Dict[str, Any]]:
        """Get available project templates."""
        return [
            {
                "id": "dashboard",
                "name": "Dashboard Template",
                "description": "Analytics dashboard with charts and widgets",
                "features": ["authentication", "charts", "widgets", "responsive"],
                "tech_stack": ["react", "fastapi", "mysql"]
            },
            {
                "id": "ecommerce", 
                "name": "E-commerce Template",
                "description": "Complete online store with payments",
                "features": ["products", "cart", "checkout", "payments", "admin"],
                "tech_stack": ["react", "fastapi", "mysql", "stripe"]
            },
            {
                "id": "blog",
                "name": "Blog Template", 
                "description": "Content management system",
                "features": ["posts", "comments", "categories", "admin"],
                "tech_stack": ["react", "fastapi", "mysql"]
            },
            {
                "id": "chat",
                "name": "Chat App Template",
                "description": "Real-time messaging application",
                "features": ["real_time_chat", "rooms", "file_sharing"],
                "tech_stack": ["react", "fastapi", "mysql", "websockets"]
            },
            {
                "id": "crm",
                "name": "CRM Template",
                "description": "Customer relationship management",
                "features": ["contacts", "deals", "tasks", "analytics"],
                "tech_stack": ["react", "fastapi", "mysql"]
            }
        ]
    
    async def chat_with_user(self, message: str, context: Dict[str, Any] = None) -> str:
        """Chat with user to assist with application building."""
        system_prompt = """
        You are an expert AI assistant helping users build applications. 
        Provide helpful, concise responses about:
        1. Application architecture and design
        2. Code generation and best practices
        3. Technology stack recommendations
        4. Troubleshooting and debugging
        5. Deployment strategies
        
        Be friendly, professional, and focused on helping the user build their application.
        """
        
        user_prompt = f"""
        User Message: {message}
        
        Context: {json.dumps(context, indent=2) if context else "No additional context"}
        """
        
        response = await self.openai_service.generate_response(system_prompt, user_prompt)
        return response
    
    async def generate_code_from_description(self, description: str, context: Dict[str, Any] = None) -> str:
        """Generate code based on natural language description."""
        system_prompt = """
        You are an expert developer generating clean, modern code based on descriptions.
        Follow these guidelines:
        1. Use modern best practices and design patterns
        2. Include proper error handling
        3. Write clean, readable, well-commented code
        4. Follow the requested technology stack
        5. Include proper imports and dependencies
        
        Return only the generated code without explanations.
        """
        
        user_prompt = f"""
        Generate code for: {description}
        
        Context: {json.dumps(context, indent=2) if context else "No additional context"}
        
        Technology Stack: {context.get("tech_stack", "React + FastAPI + MySQL") if context else "React + FastAPI + MySQL"}
        """
        
        code = await self.openai_service.generate_response(system_prompt, user_prompt)
        return code
    
    async def suggest_next_steps(self, context: Dict[str, Any], history: List[Dict[str, Any]]) -> List[str]:
        """Suggest next steps for application development."""
        system_prompt = """
        You are an expert application development advisor.
        Based on the current context and conversation history, suggest 3-5 logical next steps.
        Each suggestion should be:
        1. Specific and actionable
        2. Relevant to the current project state
        3. Prioritized by importance
        4. Realistic and achievable
        
        Return only a JSON array of string suggestions.
        """
        
        user_prompt = f"""
        Current Context: {json.dumps(context, indent=2) if context else "No context provided"}
        
        Recent Conversation History:
        {json.dumps(history[-3:] if history else [], indent=2)}
        
        Suggest 3-5 next steps for the user's application development.
        """
        
        suggestions_json = await self.openai_service.generate_response(system_prompt, user_prompt)
        try:
            suggestions = json.loads(suggestions_json)
            return suggestions if isinstance(suggestions, list) else [suggestions]
        except:
            # Fallback to simple suggestions
            return [
                "Define your application's core features",
                "Choose the appropriate technology stack",
                "Create a basic project structure",
                "Implement user authentication",
                "Add database models for your data"
            ]
    
    async def explain_concept(self, concept: str, context: Dict[str, Any] = None) -> str:
        """Explain programming concepts or code."""
        system_prompt = """
        You are an expert software engineer explaining technical concepts.
        Provide clear, concise explanations that:
        1. Are easy to understand for developers of all levels
        2. Include practical examples when relevant
        3. Mention common use cases and best practices
        4. Highlight potential pitfalls or gotchas
        5. Use analogies when helpful
        
        Keep explanations focused and actionable.
        """
        
        user_prompt = f"""
        Explain this concept: {concept}
        
        Context: {json.dumps(context, indent=2) if context else "No additional context"}
        """
        
        explanation = await self.openai_service.generate_response(system_prompt, user_prompt)
        return explanation
    
    async def debug_code(self, code: str, error: str = "", context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Debug code issues."""
        system_prompt = """
        You are an expert code debugger.
        Analyze the provided code and error, then provide:
        1. Clear explanation of what's wrong
        2. Specific line numbers or code sections with issues
        3. Step-by-step fix instructions
        4. Improved code snippet
        5. Prevention tips for similar issues
        
        Be precise and actionable in your response.
        """
        
        user_prompt = f"""
        Debug this code:
        ```
        {code}
        ```
        
        Error: {error if error else "No error message provided"}
        
        Context: {json.dumps(context, indent=2) if context else "No additional context"}
        """
        
        debug_analysis = await self.openai_service.generate_response(system_prompt, user_prompt)
        return {
            "analysis": debug_analysis,
            "fixed_code": self._extract_code_from_response(debug_analysis),
            "issues_found": self._identify_issues(code, error)
        }
    
    async def optimize_code(self, code: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Optimize code for performance and best practices."""
        system_prompt = """
        You are an expert code optimizer.
        Analyze the provided code and suggest improvements for:
        1. Performance optimization
        2. Code readability and maintainability
        3. Best practices and design patterns
        4. Security considerations
        5. Error handling improvements
        
        Return a JSON object with optimized code and improvement suggestions.
        """
        
        user_prompt = f"""
        Optimize this code:
        ```
        {code}
        ```
        
        Context: {json.dumps(context, indent=2) if context else "No additional context"}
        """
        
        optimization_json = await self.openai_service.generate_response(system_prompt, user_prompt)
        try:
            optimization_result = json.loads(optimization_json)
            return optimization_result
        except:
            # Fallback response
            return {
                "optimized_code": code,
                "improvements": ["Code analysis completed"],
                "performance_gain": "0%"
            }
    
    def _extract_code_from_response(self, response: str) -> str:
        """Extract code from AI response."""
        # Simple extraction - in practice, this would be more sophisticated
        lines = response.split('\n')
        code_lines = []
        in_code_block = False
        
        for line in lines:
            if line.strip().startswith('```'):
                in_code_block = not in_code_block
                continue
            if in_code_block:
                code_lines.append(line)
        
        return '\n'.join(code_lines) if code_lines else response
    
    def _identify_issues(self, code: str, error: str) -> List[str]:
        """Identify potential issues in code."""
        # Simple issue identification - in practice, this would be more sophisticated
        issues = []
        
        if "undefined" in error.lower():
            issues.append("Variable or function not defined")
        if "syntax" in error.lower():
            issues.append("Syntax error in code")
        if "null" in error.lower() or "none" in error.lower():
            issues.append("Null pointer or undefined reference")
            
        return issues