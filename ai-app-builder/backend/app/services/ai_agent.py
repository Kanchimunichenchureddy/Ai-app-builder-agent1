from typing import Dict, Any, List, Optional
import json
import os
from pathlib import Path
from app.core.config import settings
from app.services.integrations.openrouter_service import OpenRouterService
from app.services.code_generator import CodeGenerator  # Import the real CodeGenerator
from app.services.framework_generator import FrameworkGenerator  # Import the real FrameworkGenerator

class AIAgentService:
    """
    Core AI Agent that can build unlimited applications.
    This is the brain of the AI App Builder.
    """
    
    def __init__(self):
        # Remove other services and only use OpenRouter
        self.openrouter_service = OpenRouterService()
        # Initialize real components
        self.code_generator = CodeGenerator()
        self.framework_generator = FrameworkGenerator()
        # Conversation history for context
        self.conversation_history = {}
        # Set OpenRouter as the active service
        self.active_llm_service = "openrouter"
        # Enhanced capabilities
        self.capabilities = {
            "code_generation": True,
            "project_analysis": True,
            "debugging": True,
            "optimization": True,
            "explanation": True,
            "architecture_design": True,
            "security_review": True,
            "performance_analysis": True
        }
        # Add model selection preferences
        self.model_preferences = {
            "openrouter": "mistralai/mistral-7b-instruct"  # Using a free model
        }
        # Track if we've detected API issues
        self.openrouter_api_working = True
        print(f"AI agent initialized with LLM service: {self.active_llm_service}")
    
    def _determine_best_llm_service(self):
        """
        Determine the best available LLM service based on API key configuration.
        """
        # Check if OpenRouter API key is configured
        if settings.OPENROUTER_API_KEY:
            print("Using OpenRouter as the LLM service")
            return "openrouter"
        
        # Default fallback
        print("No API keys configured for any LLM service")
        return "openrouter"
    
    async def _generate_response_with_best_service(self, system_prompt: str, user_prompt: str, max_tokens: int = 4000) -> str:
        """
        Generate response using OpenRouter service with fallback to local generation.
        """
        try:
            if self.active_llm_service == "openrouter" and settings.OPENROUTER_API_KEY:
                # Use enhanced parameters for better responses
                print("Sending request to OpenRouter service...")
                response = await self.openrouter_service.generate_response(
                    system_prompt, 
                    user_prompt,
                    model=self.model_preferences.get("openrouter", "mistralai/mistral-7b-instruct"),
                    max_tokens=max_tokens,
                    temperature=0.7
                )
                # Check if we got a valid response (not a fallback)
                if not response.startswith("// Fallback") and "insufficient_quota" not in response and "Too Many Requests" not in response and "429" not in response and "User not found" not in response and "Request timeout" not in response:
                    return response
                else:
                    # Mark API as not working if we get specific errors
                    if "User not found" in response:
                        self.openrouter_api_working = False
                        error_message = "OpenRouter: Invalid API key or account not found"
                    elif "insufficient_quota" in response or "Too Many Requests" in response or "429" in response:
                        error_message = "OpenRouter: API quota exceeded or rate limit reached"
                    elif "Request timeout" in response:
                        error_message = "OpenRouter: Request timeout - service is taking too long to respond"
                    else:
                        error_message = "OpenRouter: Service unavailable"
                    
                    return self._generate_fallback_response(error_message)
                        
        except Exception as e:
            # Mark API as not working on exception
            self.openrouter_api_working = False
            error_message = f"OpenRouter: {str(e)}"
            return self._generate_fallback_response(error_message)
    
    def _generate_fallback_response(self, error_message: str) -> str:
        """
        Generate a fallback response when AI services are not available.
        """
        return f"""// Fallback response: AI service is currently unavailable.

Configuration Issues Detected:
  - {error_message}

Please resolve the following:
1. Check your OpenRouter API key and quota limits
2. Verify your internet connection
3. Visit https://openrouter.ai/ to check your account status
4. Follow the setup guide in OPENROUTER_SETUP.md

Using fallback mode - limited functionality available.

Fallback Response:
I'm unable to access the AI service at the moment. Here's some general guidance:

For application development:
1. Define clear project requirements and scope
2. Choose appropriate technologies for your needs
3. Plan your database structure early
4. Implement user authentication and security measures
5. Test your application thoroughly

For code generation:
1. Break down complex problems into smaller components
2. Follow established design patterns and best practices
3. Write clean, readable, and well-documented code
4. Include proper error handling
5. Consider performance and scalability from the start

If you need specific help, please try again later when the AI service is available."""
    
    async def chat_with_user(self, message: str, context: Dict[str, Any] = None) -> str:
        """
        Chat with the user and generate helpful responses.
        """
        system_prompt = """
        You are a helpful AI assistant that can provide guidance on software development,
        answer technical questions, and assist with coding tasks. Be concise and clear
        in your responses.
        """
        
        # Include context in the user prompt if available
        context_str = ""
        if context and context.get("history"):
            context_str = "\nConversation history:\n" + "\n".join(
                f"{msg['role']}: {msg['content']}" 
                for msg in context["history"][-5:]  # Include last 5 messages
            )
        
        user_prompt = f"{message}\n{context_str}"
        
        try:
            response = await self._generate_response_with_best_service(
                system_prompt,
                user_prompt,
                max_tokens=2000  # Shorter responses for chat
            )
            return response
        except Exception as e:
            print(f"Error in chat_with_user: {str(e)}")
            raise

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
        7. Security considerations
        8. Performance requirements
        9. Scalability needs
        10. Estimated complexity and development time
        
        Return only valid JSON.
        """
        
        user_prompt = f"""
        User Request: {user_request}
        
        Analyze this request and provide a detailed project specification.
        Include technical architecture, potential challenges, and best practices.
        """
        
        analysis = await self._generate_response_with_best_service(
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
            "structure": {},
            "documentation": {
                "setup_instructions": "Run npm install and python requirements.txt",
                "deployment_guide": "Use Docker for deployment",
                "api_documentation": "Available at /docs endpoint"
            }
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
                    "styles": {},
                    "hooks": {},
                    "contexts": {}
                },
                "public": {},
                "tests": {}
            },
            "backend": {
                "app": {
                    "api": {},
                    "models": {},
                    "schemas": {},
                    "services": {},
                    "core": {},
                    "utils": {}
                },
                "tests": {}
            },
            "database": {
                "migrations": {},
                "schemas": {}
            },
            "deployment": {},
            "docs": {}
        }
        
        # Customize structure based on project type
        if project_type == "ecommerce":
            base_structure["frontend"]["src"]["components"]["products"] = {}
            base_structure["frontend"]["src"]["components"]["cart"] = {}
            base_structure["frontend"]["src"]["components"]["checkout"] = {}
            base_structure["backend"]["app"]["services"]["payment"] = {}
            base_structure["backend"]["app"]["services"]["inventory"] = {}
            
        elif project_type == "dashboard":
            base_structure["frontend"]["src"]["components"]["charts"] = {}
            base_structure["frontend"]["src"]["components"]["widgets"] = {}
            base_structure["frontend"]["src"]["components"]["analytics"] = {}
            base_structure["backend"]["app"]["services"]["analytics"] = {}
            
        elif project_type == "chat":
            base_structure["frontend"]["src"]["components"]["chat"] = {}
            base_structure["backend"]["app"]["services"]["websocket"] = {}
            base_structure["backend"]["app"]["services"]["messaging"] = {}
            
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
        
        # Generate documentation files
        files["README.md"] = f"# {analysis.get('project_type', 'Web Application')}\n\n" + \
                           f"## Features\n" + \
                           "\n".join([f"- {feature}" for feature in analysis.get("features", [])]) + \
                           f"\n\n## Tech Stack\n" + \
                           f"- Frontend: {analysis.get('tech_stack', {}).get('frontend', 'React')}\n" + \
                           f"- Backend: {analysis.get('tech_stack', {}).get('backend', 'FastAPI')}\n" + \
                           f"- Database: {analysis.get('tech_stack', {}).get('database', 'MySQL')}\n"
        
        return files
    
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
            "complexity": "medium",
            "security_considerations": ["authentication", "input_validation"],
            "performance_requirements": "standard"
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
        # Get user ID from context
        user_id = context.get("user_id", "default") if context else "default"
        
        # Initialize conversation history for this user if not exists
        if user_id not in self.conversation_history:
            self.conversation_history[user_id] = []
        
        # Add current message to history
        self.conversation_history[user_id].append({"role": "user", "content": message})
        
        # Keep only the last 15 messages for context (increased from 10)
        if len(self.conversation_history[user_id]) > 15:
            self.conversation_history[user_id] = self.conversation_history[user_id][-15:]
        
        # Build conversation history string
        conversation_history = "\n".join([
            f"{msg['role'].capitalize()}: {msg['content']}" 
            for msg in self.conversation_history[user_id]
        ])
        
        # Get current date and time for context
        from datetime import datetime
        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        day_of_week = datetime.now().strftime("%A")
        
        # Get available capabilities
        capabilities_list = ", ".join([cap for cap, enabled in self.capabilities.items() if enabled])
        
        system_prompt = f"""
        You are an expert AI assistant helping users build applications. 
        Provide helpful, concise responses about:
        1. Application architecture and design
        2. Code generation and best practices
        3. Technology stack recommendations
        4. Troubleshooting and debugging
        5. Deployment strategies
        6. Project planning and management
        7. UI/UX design principles
        8. Security considerations
        9. Performance optimization
        10. Testing strategies
        11. Code review and quality assurance
        12. Documentation and maintenance
        
        Be friendly, professional, and focused on helping the user build their application.
        Always provide actionable advice and specific examples when relevant.
        If you don't know something, be honest and suggest alternatives or ways to find the information.
        
        Your Capabilities: {capabilities_list}
        Current Date and Time: {current_datetime} ({day_of_week})
        
        Previous conversation history:
        {conversation_history}
        """
        
        user_prompt = f"""
        User Message: {message}
        
        Context: {json.dumps(context, indent=2) if context else "No additional context"}
        
        Please provide a comprehensive response that directly addresses the user's question or request.
        Include specific examples, code snippets, or step-by-step instructions when appropriate.
        If this is a follow-up to a previous conversation, maintain context and build upon previous discussions.
        When providing technical information, include relevant data, statistics, or references to support your answers.
        """
        
        try:
            response = await self._generate_response_with_best_service(system_prompt, user_prompt)
            # Add AI response to history
            self.conversation_history[user_id].append({"role": "assistant", "content": response})
            return response
        except Exception as e:
            # Add error response to history
            error_response = f"I can help you with that! Here's some general guidance:\n\n" \
                   f"1. For application development, consider starting with a clear project scope\n" \
                   f"2. Choose appropriate technologies for your needs (React/Vue for frontend, FastAPI/Django for backend)\n" \
                   f"3. Plan your database structure early\n" \
                   f"4. Implement user authentication and security measures\n" \
                   f"5. Test your application thoroughly\n\n" \
                   f"If you'd like more specific advice, please provide more details about what you're trying to build!"
            self.conversation_history[user_id].append({"role": "assistant", "content": error_response})
            return error_response
    
    async def generate_code_from_description(self, description: str, context: Dict[str, Any] = None) -> str:
        """Generate code based on natural language description."""
        # Get current date and time for context
        from datetime import datetime
        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        day_of_week = datetime.now().strftime("%A")
        
        # Get technology stack from context or use defaults
        tech_stack = context.get("tech_stack", {"frontend": "React", "backend": "FastAPI", "database": "MySQL"}) if context else {"frontend": "React", "backend": "FastAPI", "database": "MySQL"}
        
        system_prompt = f"""
        You are an expert developer generating clean, modern code based on descriptions.
        Follow these guidelines:
        1. Use modern best practices and design patterns
        2. Include proper error handling
        3. Write clean, readable, well-commented code
        4. Follow the requested technology stack
        5. Include proper imports and dependencies
        6. Make code modular and reusable
        7. Include example usage when relevant
        8. Add security considerations
        9. Optimize for performance
        10. Include testing considerations
        11. Follow accessibility standards
        12. Include documentation comments
        
        Return only the generated code without explanations.
        
        Technology Stack: {tech_stack['frontend']} (Frontend), {tech_stack['backend']} (Backend), {tech_stack['database']} (Database)
        Current Date and Time: {current_datetime} ({day_of_week})
        """
        
        user_prompt = f"""
        Generate code for: {description}
        
        Context: {json.dumps(context, indent=2) if context else "No additional context"}
        
        Technology Stack: {context.get("tech_stack", "React + FastAPI + MySQL") if context else "React + FastAPI + MySQL"}
        
        Please generate complete, functional code that follows best practices.
        Include all necessary imports and make the code as self-contained as possible.
        Add comments to explain complex logic.
        When generating code, include relevant data structures, sample data, or example usage that demonstrates the functionality.
        """
        
        try:
            code = await self._generate_response_with_best_service(system_prompt, user_prompt)
            return code
        except Exception as e:
            # Fallback code generation
            return f"// Fallback code for: {description}\n" \
                   f"// Please implement your solution here\n" \
                   f"function exampleFunction() {{\n" \
                   f"  console.log('This is a placeholder for your implementation');\n" \
                   f"  // Add your code here\n" \
                   f"}}\n\n" \
                   f"// Example usage\n" \
                   f"exampleFunction();"
    
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
        5. Include estimated time investment
        6. Mention potential challenges
        7. Provide implementation guidance
        
        Return only a JSON array of string suggestions.
        """
        
        user_prompt = f"""
        Current Context: {json.dumps(context, indent=2) if context else "No context provided"}
        
        Recent Conversation History:
        {json.dumps(history[-5:] if history else [], indent=2)}
        
        Suggest 3-5 next steps for the user's application development.
        Make each suggestion actionable with clear steps.
        Include technical details and best practices.
        """
        
        try:
            suggestions_json = await self._generate_response_with_best_service(system_prompt, user_prompt)
            suggestions = json.loads(suggestions_json)
            return suggestions if isinstance(suggestions, list) else [suggestions]
        except:
            # Fallback to simple suggestions
            return [
                "Define your application's core features and user flows",
                "Choose the appropriate technology stack for your needs",
                "Create a basic project structure with folders and files",
                "Implement user authentication and security measures",
                "Add database models for your core data entities"
            ]
    
    async def explain_concept(self, concept: str, context: Dict[str, Any] = None) -> str:
        """Explain programming concepts or code."""
        # Get current date and time for context
        from datetime import datetime
        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        day_of_week = datetime.now().strftime("%A")
        
        system_prompt = f"""
        You are an expert software engineer explaining technical concepts.
        Provide clear, concise explanations that:
        1. Are easy to understand for developers of all levels
        2. Include practical examples when relevant
        3. Mention common use cases and best practices
        4. Highlight potential pitfalls or gotchas
        5. Use analogies when helpful
        6. Include code examples when appropriate
        7. Mention related concepts
        8. Provide learning resources
        9. Explain trade-offs and alternatives
        10. Include real-world applications
        11. Include relevant statistics, benchmarks, or data when applicable
        12. Reference industry standards and best practices
        
        Keep explanations focused and actionable.
        
        Current Date and Time: {current_datetime} ({day_of_week})
        """
        
        user_prompt = f"""
        Explain this concept: {concept}
        
        Context: {json.dumps(context, indent=2) if context else "No additional context"}
        
        Please provide a comprehensive explanation with examples.
        Include code snippets if relevant.
        Explain how this concept fits into the broader development landscape.
        When explaining, include relevant data, statistics, or references to support your answers.
        """
        
        try:
            explanation = await self._generate_response_with_best_service(system_prompt, user_prompt)
            return explanation
        except Exception as e:
            # Fallback explanation
            return f"Here's an explanation of {concept}:\n\n" \
                   f"{concept} is an important concept in software development. " \
                   f"Without more specific context, I can provide a general overview. " \
                   f"To get a more detailed explanation, please provide more information about what aspect of {concept} you'd like to understand."
    
    async def debug_code(self, code: str, error: str = "", context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Debug code issues."""
        # Get current date and time for context
        from datetime import datetime
        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        day_of_week = datetime.now().strftime("%A")
        
        system_prompt = f"""
        You are an expert code debugger.
        Analyze the provided code and error, then provide:
        1. Clear explanation of what's wrong
        2. Specific line numbers or code sections with issues
        3. Step-by-step fix instructions
        4. Improved code snippet
        5. Prevention tips for similar issues
        6. Best practices to avoid this type of error
        7. Alternative approaches if applicable
        8. Performance implications of the fix
        9. Common patterns that lead to this type of error
        10. Industry statistics on this type of bug
        
        Be precise and actionable in your response.
        
        Current Date and Time: {current_datetime} ({day_of_week})
        """
        
        user_prompt = f"""
        Debug this code:
        ```
        {code}
        ```
        
        Error: {error if error else "No error message provided"}
        
        Context: {json.dumps(context, indent=2) if context else "No additional context"}
        
        Please provide a detailed debugging analysis with specific fixes.
        Include the corrected code and explain why the changes were needed.
        When debugging, include relevant data, statistics, or references to support your analysis.
        """
        
        try:
            debug_analysis = await self._generate_response_with_best_service(system_prompt, user_prompt)
            return {
                "analysis": debug_analysis,
                "fixed_code": self._extract_code_from_response(debug_analysis),
                "issues_found": self._identify_issues(code, error)
            }
        except Exception as e:
            # Fallback debugging
            return {
                "analysis": f"Here's a general approach to debugging your code:\n\n" \
                           f"1. Check for syntax errors (missing brackets, semicolons, etc.)\n" \
                           f"2. Verify variable names and scope\n" \
                           f"3. Ensure all dependencies are properly imported\n" \
                           f"4. Look for type mismatches\n" \
                           f"5. Check function calls and parameters\n\n" \
                           f"If you're still having issues, please share more details about the specific error you're encountering.",
                "fixed_code": code,
                "issues_found": self._identify_issues(code, error)
            }
    
    async def optimize_code(self, code: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Optimize code for performance and best practices."""
        # Get current date and time for context
        from datetime import datetime
        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        day_of_week = datetime.now().strftime("%A")
        
        system_prompt = f"""
        You are an expert code optimizer.
        Analyze the provided code and suggest improvements for:
        1. Performance optimization
        2. Code readability and maintainability
        3. Best practices and design patterns
        4. Security considerations
        5. Error handling improvements
        6. Memory usage optimization
        7. Scalability improvements
        8. Testing considerations
        9. Documentation and comments
        10. Code reusability
        11. Industry benchmarks and performance metrics
        12. Statistical analysis of potential improvements
        
        Return a JSON object with optimized code and improvement suggestions.
        
        Current Date and Time: {current_datetime} ({day_of_week})
        """
        
        user_prompt = f"""
        Optimize this code:
        ```
        {code}
        ```
        
        Context: {json.dumps(context, indent=2) if context else "No additional context"}
        
        Please provide specific optimizations and improvements.
        Include explanations for each optimization and its benefits.
        When optimizing, include relevant data, statistics, or references to support your suggestions.
        """
        
        try:
            optimization_json = await self._generate_response_with_best_service(system_prompt, user_prompt)
            optimization_result = json.loads(optimization_json)
            return optimization_result
        except:
            # Fallback response
            return {
                "optimized_code": code,
                "improvements": [
                    "Review code for performance bottlenecks",
                    "Ensure proper error handling is implemented",
                    "Check for code duplication and refactor",
                    "Verify security best practices are followed",
                    "Add comprehensive comments and documentation"
                ],
                "performance_gain": "0%"
            }
    
    async def review_code_security(self, code: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Review code for security vulnerabilities."""
        # Get current date and time for context
        from datetime import datetime
        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        day_of_week = datetime.now().strftime("%A")
        
        system_prompt = f"""
        You are an expert security analyst.
        Analyze the provided code for security vulnerabilities and provide:
        1. List of identified security issues
        2. Severity rating for each issue
        3. Detailed explanation of each vulnerability
        4. Specific fix recommendations
        5. Best practices to prevent similar issues
        6. References to security standards (OWASP, etc.)
        7. Industry statistics on this type of vulnerability
        8. Real-world examples of exploits
        9. Cost of potential breaches
        10. Compliance considerations
        
        Focus on common vulnerabilities like:
        - SQL injection
        - Cross-site scripting (XSS)
        - Cross-site request forgery (CSRF)
        - Authentication issues
        - Authorization problems
        - Input validation flaws
        - Sensitive data exposure
        
        Current Date and Time: {current_datetime} ({day_of_week})
        """
        
        user_prompt = f"""
        Review this code for security vulnerabilities:
        ```
        {code}
        ```
        
        Context: {json.dumps(context, indent=2) if context else "No additional context"}
        
        Please provide a comprehensive security analysis.
        When reviewing, include relevant data, statistics, or references to support your analysis.
        """
        
        try:
            security_review = await self._generate_response_with_best_service(system_prompt, user_prompt)
            return {
                "review": security_review,
                "vulnerabilities_found": self._identify_security_issues(code)
            }
        except Exception as e:
            return {
                "review": "Security review failed. Please try again.",
                "vulnerabilities_found": []
            }
    
    async def analyze_project_architecture(self, project_description: str, tech_stack: Dict[str, str]) -> Dict[str, Any]:
        """Analyze and suggest improvements to project architecture."""
        # Get current date and time for context
        from datetime import datetime
        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        day_of_week = datetime.now().strftime("%A")
        
        system_prompt = f"""
        You are a senior software architect.
        Analyze the project description and technology stack, then provide:
        1. Architecture overview and components
        2. Strengths of the current approach
        3. Potential weaknesses or bottlenecks
        4. Scalability considerations
        5. Performance optimization suggestions
        6. Security architecture recommendations
        7. Deployment strategy
        8. Monitoring and logging approach
        9. Testing strategy
        10. Maintenance considerations
        11. Industry benchmarks and best practices
        12. Cost analysis and resource requirements
        
        Current Date and Time: {current_datetime} ({day_of_week})
        """
        
        user_prompt = f"""
        Analyze this project:
        
        Description: {project_description}
        Technology Stack: {json.dumps(tech_stack, indent=2)}
        
        Provide a comprehensive architecture analysis.
        When analyzing, include relevant data, statistics, or references to support your recommendations.
        """
        
        try:
            architecture_analysis = await self._generate_response_with_best_service(system_prompt, user_prompt)
            return {
                "analysis": architecture_analysis
            }
        except Exception as e:
            return {
                "analysis": "Architecture analysis failed. Please try again."
            }
    
    async def generate_documentation(self, project_data: Dict[str, Any]) -> str:
        """Generate comprehensive documentation for a project."""
        # Get current date and time for context
        from datetime import datetime
        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        day_of_week = datetime.now().strftime("%A")
        
        system_prompt = f"""
        You are a technical documentation expert.
        Create comprehensive documentation for the provided project data.
        Include:
        1. Project overview and goals
        2. Technology stack explanation
        3. Architecture diagram description
        4. Setup and installation instructions
        5. Configuration guide
        6. API documentation (if applicable)
        7. Database schema (if applicable)
        8. Deployment instructions
        9. Troubleshooting guide
        10. Contributing guidelines
        11. Performance benchmarks and metrics
        12. Security considerations and best practices
        
        Current Date and Time: {current_datetime} ({day_of_week})
        """
        
        user_prompt = f"""
        Generate documentation for this project:
        
        {json.dumps(project_data, indent=2)}
        
        Please provide comprehensive, well-structured documentation.
        When documenting, include relevant data, statistics, or references to support your explanations.
        """
        
        try:
            documentation = await self._generate_response_with_best_service(system_prompt, user_prompt, max_tokens=8000)
            return documentation
        except Exception as e:
            return f"Documentation generation failed: {str(e)}"
    
    async def suggest_improvements(self, project_data: Dict[str, Any], user_feedback: str = "") -> Dict[str, Any]:
        """Suggest improvements for an existing project."""
        # Get current date and time for context
        from datetime import datetime
        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        day_of_week = datetime.now().strftime("%A")
        
        system_prompt = f"""
        You are a senior software engineer and consultant.
        Analyze the project data and user feedback to suggest improvements.
        Focus on:
        1. Code quality and maintainability
        2. Performance optimizations
        3. Security enhancements
        4. User experience improvements
        5. Scalability considerations
        6. Best practices adoption
        7. Technology stack updates
        8. Testing strategy improvements
        9. Industry benchmarks and best practices
        10. Cost-benefit analysis of suggestions
        11. Implementation timeline and complexity
        12. Risk assessment and mitigation strategies
        
        Current Date and Time: {current_datetime} ({day_of_week})
        """
        
        user_prompt = f"""
        Suggest improvements for this project:
        
        Project Data:
        {json.dumps(project_data, indent=2)}
        
        User Feedback:
        {user_feedback if user_feedback else "No specific feedback provided"}
        
        Please provide actionable improvement suggestions.
        When suggesting improvements, include relevant data, statistics, or references to support your recommendations.
        """
        
        try:
            suggestions = await self._generate_response_with_best_service(system_prompt, user_prompt)
            return {
                "suggestions": suggestions
            }
        except Exception as e:
            return {
                "suggestions": f"Improvement suggestions failed: {str(e)}"
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
        if "timeout" in error.lower():
            issues.append("Potential performance or network issue")
        if "memory" in error.lower():
            issues.append("Memory allocation or usage issue")
            
        return issues
    
    def _identify_security_issues(self, code: str) -> List[str]:
        """Identify potential security issues in code."""
        security_issues = []
        
        # Simple security issue identification
        if "eval(" in code:
            security_issues.append("Use of eval() function - potential code injection")
        if "document.write" in code:
            security_issues.append("Use of document.write() - potential XSS vulnerability")
        if "password" in code.lower() and "hardcoded" in code.lower():
            security_issues.append("Hardcoded credentials detected")
            
        return security_issues
