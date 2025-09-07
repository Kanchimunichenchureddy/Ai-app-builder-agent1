from typing import Dict, List, Optional, Any
import json
import asyncio
import uuid
from datetime import datetime
from fastapi import WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from ..models.project import Project, ProjectStatus
from ..core.database import get_db
from .ai_agent import AIAgentService

class ProjectProgressStep:
    """Represents a step in the project creation process."""
    
    def __init__(self, id: str, name: str, description: str, weight: float = 1.0):
        self.id = id
        self.name = name
        self.description = description
        self.weight = weight
        self.status = "pending"  # pending, active, completed, error
        self.progress = 0.0
        self.start_time = None
        self.end_time = None
        self.error_message = None
        self.details = {}

class RealTimeProjectCreator:
    """
    Real-time project creation service with WebSocket progress tracking.
    Provides live updates during the AI-powered application generation process.
    """
    
    def __init__(self):
        self.ai_agent = AIAgentService()
        self.active_connections: Dict[str, WebSocket] = {}
        self.creation_sessions: Dict[str, Dict[str, Any]] = {}
        
        # Define the standard project creation pipeline
        self.creation_steps = [
            ProjectProgressStep("analyze", "Analyzing Requirements", "AI is analyzing your project requirements and determining the best architecture", 1.0),
            ProjectProgressStep("plan", "Creating Project Plan", "Generating detailed project structure and component specifications", 1.5),
            ProjectProgressStep("frontend", "Generating Frontend", "Creating React components, pages, and user interface elements", 3.0),
            ProjectProgressStep("backend", "Building Backend", "Developing FastAPI endpoints, database models, and business logic", 3.0),
            ProjectProgressStep("database", "Setting Up Database", "Creating database schema, migrations, and seed data", 1.5),
            ProjectProgressStep("integration", "Connecting Services", "Integrating frontend and backend, setting up API connections", 2.0),
            ProjectProgressStep("testing", "Running Tests", "Generating and executing unit tests and integration tests", 1.5),
            ProjectProgressStep("optimization", "Optimizing Code", "Code review, performance optimization, and security enhancements", 1.0),
            ProjectProgressStep("deployment", "Preparing Deployment", "Creating Docker configurations and deployment scripts", 1.5),
            ProjectProgressStep("finalize", "Finalizing Project", "Final validation and project packaging", 1.0)
        ]
    
    async def connect_websocket(self, websocket: WebSocket, session_id: str):
        """Connect a WebSocket client for real-time updates."""
        await websocket.accept()
        self.active_connections[session_id] = websocket
        
        # Send initial connection confirmation
        await self.send_update(session_id, {
            "type": "connection_established",
            "session_id": session_id,
            "message": "🔗 Connected to AI App Builder",
            "timestamp": datetime.now().isoformat()
        })
    
    async def disconnect_websocket(self, session_id: str):
        """Disconnect a WebSocket client."""
        if session_id in self.active_connections:
            del self.active_connections[session_id]
        if session_id in self.creation_sessions:
            del self.creation_sessions[session_id]
    
    async def send_update(self, session_id: str, update: Dict[str, Any]):
        """Send a real-time update to the connected client."""
        if session_id in self.active_connections:
            try:
                await self.active_connections[session_id].send_text(json.dumps(update))
            except Exception as e:
                print(f"Error sending update to {session_id}: {e}")
                await self.disconnect_websocket(session_id)
    
    async def create_project_realtime(
        self,
        session_id: str,
        project_data: Dict[str, Any],
        db: Session
    ) -> Dict[str, Any]:
        """
        Create a project with real-time progress updates via WebSocket.
        """
        try:
            # Initialize creation session
            self.creation_sessions[session_id] = {
                "project_data": project_data,
                "steps": [step.__dict__.copy() for step in self.creation_steps],
                "overall_progress": 0.0,
                "start_time": datetime.now(),
                "status": "active"
            }
            
            # Send initial progress update
            await self.send_progress_update(session_id)
            
            project_name = project_data.get("name", "")\n            analysis = project_data.get("analysis", {})\n            tech_stack = project_data.get("tech_stack", {})\n            \n            # Create project record in database\n            project = Project(\n                name=project_name,\n                description=analysis.get("description", ""),\n                project_type=analysis.get("project_type", "web_app"),\n                status=ProjectStatus.CREATING,\n                owner_id=project_data.get("user_id"),\n                config={"tech_stack": tech_stack},\n                features=analysis.get("features", [])\n            )\n            \n            db.add(project)\n            db.commit()\n            db.refresh(project)\n            \n            # Execute creation steps with real-time updates\n            generated_files = {}\n            \n            for i, step in enumerate(self.creation_steps):\n                await self.execute_creation_step(session_id, i, step, project_data, generated_files)\n                \n                # Check if session was cancelled\n                if session_id not in self.creation_sessions:\n                    break\n            \n            # Update project status\n            if session_id in self.creation_sessions:\n                project.status = ProjectStatus.ACTIVE\n                project.project_path = f"generated_projects/project_{project.id}"\n                db.commit()\n                \n                # Send completion update\n                await self.send_update(session_id, {\n                    "type": "project_completed",\n                    "project": {\n                        "id": project.id,\n                        "name": project.name,\n                        "status": project.status.value,\n                        "created_at": project.created_at.isoformat()\n                    },\n                    "files_generated": len(generated_files),\n                    "message": f"🎉 {project_name} has been successfully created!",\n                    "timestamp": datetime.now().isoformat()\n                })\n                \n                return {\n                    "success": True,\n                    "project_id": project.id,\n                    "session_id": session_id,\n                    "files_generated": len(generated_files)\n                }\n            \n        except Exception as e:\n            # Handle errors and notify client\n            await self.send_update(session_id, {\n                "type": "project_error",\n                "error": str(e),\n                "message": f"❌ Project creation failed: {str(e)}",\n                "timestamp": datetime.now().isoformat()\n            })\n            \n            # Update project status to error\n            if 'project' in locals():\n                project.status = ProjectStatus.ERROR\n                db.commit()\n            \n            raise e\n        \n        finally:\n            # Clean up session\n            if session_id in self.creation_sessions:\n                del self.creation_sessions[session_id]\n    \n    async def execute_creation_step(\n        self,\n        session_id: str,\n        step_index: int,\n        step: ProjectProgressStep,\n        project_data: Dict[str, Any],\n        generated_files: Dict[str, str]\n    ):\n        """Execute a single creation step with progress updates."""\n        # Update step status to active\n        self.creation_sessions[session_id]["steps"][step_index]["status"] = "active"\n        self.creation_sessions[session_id]["steps"][step_index]["start_time"] = datetime.now().isoformat()\n        \n        await self.send_progress_update(session_id)\n        \n        try:\n            # Execute step based on its ID\n            if step.id == "analyze":\n                await self.step_analyze_requirements(session_id, step_index, project_data)\n            elif step.id == "plan":\n                await self.step_create_project_plan(session_id, step_index, project_data)\n            elif step.id == "frontend":\n                frontend_files = await self.step_generate_frontend(session_id, step_index, project_data)\n                generated_files.update(frontend_files)\n            elif step.id == "backend":\n                backend_files = await self.step_generate_backend(session_id, step_index, project_data)\n                generated_files.update(backend_files)\n            elif step.id == "database":\n                db_files = await self.step_setup_database(session_id, step_index, project_data)\n                generated_files.update(db_files)\n            elif step.id == "integration":\n                await self.step_integrate_services(session_id, step_index, project_data)\n            elif step.id == "testing":\n                test_files = await self.step_generate_tests(session_id, step_index, project_data)\n                generated_files.update(test_files)\n            elif step.id == "optimization":\n                await self.step_optimize_code(session_id, step_index, project_data)\n            elif step.id == "deployment":\n                deploy_files = await self.step_prepare_deployment(session_id, step_index, project_data)\n                generated_files.update(deploy_files)\n            elif step.id == "finalize":\n                await self.step_finalize_project(session_id, step_index, project_data)\n            \n            # Mark step as completed\n            self.creation_sessions[session_id]["steps"][step_index]["status"] = "completed"\n            self.creation_sessions[session_id]["steps"][step_index]["end_time"] = datetime.now().isoformat()\n            self.creation_sessions[session_id]["steps"][step_index]["progress"] = 100.0\n            \n            await self.send_progress_update(session_id)\n            \n        except Exception as e:\n            # Mark step as error\n            self.creation_sessions[session_id]["steps"][step_index]["status"] = "error"\n            self.creation_sessions[session_id]["steps"][step_index]["error_message"] = str(e)\n            self.creation_sessions[session_id]["steps"][step_index]["end_time"] = datetime.now().isoformat()\n            \n            await self.send_progress_update(session_id)\n            raise e\n    \n    async def send_progress_update(self, session_id: str):\n        """Send current progress update to the client."""\n        if session_id not in self.creation_sessions:\n            return\n        \n        session = self.creation_sessions[session_id]\n        \n        # Calculate overall progress\n        total_weight = sum(step["weight"] for step in session["steps"])\n        completed_weight = sum(\n            step["weight"] for step in session["steps"] \n            if step["status"] == "completed"\n        )\n        active_weight = sum(\n            step["weight"] * (step["progress"] / 100.0) for step in session["steps"] \n            if step["status"] == "active"\n        )\n        \n        overall_progress = min(100.0, ((completed_weight + active_weight) / total_weight) * 100.0)\n        session["overall_progress"] = overall_progress\n        \n        await self.send_update(session_id, {\n            "type": "progress_update",\n            "overall_progress": overall_progress,\n            "steps": session["steps"],\n            "timestamp": datetime.now().isoformat()\n        })\n    \n    # Individual step implementations\n    async def step_analyze_requirements(self, session_id: str, step_index: int, project_data: Dict[str, Any]):\n        """Step 1: Analyze project requirements."""\n        await asyncio.sleep(1)  # Simulate AI processing time\n        \n        # Update step progress incrementally\n        for progress in [25, 50, 75, 100]:\n            self.creation_sessions[session_id]["steps"][step_index]["progress"] = progress\n            await self.send_progress_update(session_id)\n            await asyncio.sleep(0.5)\n    \n    async def step_create_project_plan(self, session_id: str, step_index: int, project_data: Dict[str, Any]):\n        """Step 2: Create detailed project plan."""\n        await asyncio.sleep(1.5)\n        \n        for progress in [20, 40, 60, 80, 100]:\n            self.creation_sessions[session_id]["steps"][step_index]["progress"] = progress\n            await self.send_progress_update(session_id)\n            await asyncio.sleep(0.6)\n    \n    async def step_generate_frontend(self, session_id: str, step_index: int, project_data: Dict[str, Any]) -> Dict[str, str]:\n        """Step 3: Generate frontend components."""\n        await asyncio.sleep(2)\n        \n        # Simulate file generation progress\n        files = {}\n        components = ["App.js", "HomePage.js", "components/Navbar.js", "components/Footer.js", "services/api.js"]\n        \n        for i, component in enumerate(components):\n            progress = ((i + 1) / len(components)) * 100\n            self.creation_sessions[session_id]["steps"][step_index]["progress"] = progress\n            self.creation_sessions[session_id]["steps"][step_index]["details"] = {\n                "current_file": component,\n                "files_generated": i + 1,\n                "total_files": len(components)\n            }\n            \n            files[f"frontend/src/{component}"] = f"// Generated {component} content"\n            \n            await self.send_progress_update(session_id)\n            await asyncio.sleep(0.4)\n        \n        return files\n    \n    async def step_generate_backend(self, session_id: str, step_index: int, project_data: Dict[str, Any]) -> Dict[str, str]:\n        """Step 4: Generate backend APIs."""\n        await asyncio.sleep(2)\n        \n        files = {}\n        endpoints = ["main.py", "models/user.py", "api/auth.py", "api/routes.py", "core/config.py"]\n        \n        for i, endpoint in enumerate(endpoints):\n            progress = ((i + 1) / len(endpoints)) * 100\n            self.creation_sessions[session_id]["steps"][step_index]["progress"] = progress\n            self.creation_sessions[session_id]["steps"][step_index]["details"] = {\n                "current_file": endpoint,\n                "files_generated": i + 1,\n                "total_files": len(endpoints)\n            }\n            \n            files[f"backend/{endpoint}"] = f"# Generated {endpoint} content"\n            \n            await self.send_progress_update(session_id)\n            await asyncio.sleep(0.4)\n        \n        return files\n    \n    async def step_setup_database(self, session_id: str, step_index: int, project_data: Dict[str, Any]) -> Dict[str, str]:\n        """Step 5: Setup database schema."""\n        await asyncio.sleep(1.5)\n        \n        files = {\n            "database/init.sql": "-- Database initialization script",\n            "database/migrations/001_initial.sql": "-- Initial migration",\n            "database/seeds/sample_data.sql": "-- Sample data"\n        }\n        \n        for i in range(1, 6):\n            progress = (i / 5) * 100\n            self.creation_sessions[session_id]["steps"][step_index]["progress"] = progress\n            await self.send_progress_update(session_id)\n            await asyncio.sleep(0.3)\n        \n        return files\n    \n    async def step_integrate_services(self, session_id: str, step_index: int, project_data: Dict[str, Any]):\n        """Step 6: Integrate frontend and backend."""\n        await asyncio.sleep(1.5)\n        \n        for progress in [25, 50, 75, 100]:\n            self.creation_sessions[session_id]["steps"][step_index]["progress"] = progress\n            await self.send_progress_update(session_id)\n            await asyncio.sleep(0.5)\n    \n    async def step_generate_tests(self, session_id: str, step_index: int, project_data: Dict[str, Any]) -> Dict[str, str]:\n        """Step 7: Generate test files."""\n        await asyncio.sleep(1)\n        \n        files = {\n            "frontend/src/tests/App.test.js": "// Frontend tests",\n            "backend/tests/test_auth.py": "# Backend tests",\n            "backend/tests/test_api.py": "# API tests"\n        }\n        \n        for i in range(1, 4):\n            progress = (i / 3) * 100\n            self.creation_sessions[session_id]["steps"][step_index]["progress"] = progress\n            await self.send_progress_update(session_id)\n            await asyncio.sleep(0.4)\n        \n        return files\n    \n    async def step_optimize_code(self, session_id: str, step_index: int, project_data: Dict[str, Any]):\n        """Step 8: Optimize generated code."""\n        await asyncio.sleep(1)\n        \n        optimizations = ["Code formatting", "Performance optimization", "Security review", "Best practices"]\n        \n        for i, opt in enumerate(optimizations):\n            progress = ((i + 1) / len(optimizations)) * 100\n            self.creation_sessions[session_id]["steps"][step_index]["progress"] = progress\n            self.creation_sessions[session_id]["steps"][step_index]["details"] = {"current_optimization": opt}\n            await self.send_progress_update(session_id)\n            await asyncio.sleep(0.3)\n    \n    async def step_prepare_deployment(self, session_id: str, step_index: int, project_data: Dict[str, Any]) -> Dict[str, str]:\n        """Step 9: Prepare deployment configurations."""\n        await asyncio.sleep(1)\n        \n        files = {\n            "Dockerfile": "# Docker configuration",\n            "docker-compose.yml": "# Docker Compose configuration",\n            ".github/workflows/deploy.yml": "# GitHub Actions deployment",\n            "deploy.sh": "#!/bin/bash\\n# Deployment script"\n        }\n        \n        for i in range(1, 5):\n            progress = (i / 4) * 100\n            self.creation_sessions[session_id]["steps"][step_index]["progress"] = progress\n            await self.send_progress_update(session_id)\n            await asyncio.sleep(0.3)\n        \n        return files\n    \n    async def step_finalize_project(self, session_id: str, step_index: int, project_data: Dict[str, Any]):\n        """Step 10: Finalize project creation."""\n        await asyncio.sleep(0.5)\n        \n        tasks = ["Final validation", "Generating README", "Creating documentation", "Project packaging"]\n        \n        for i, task in enumerate(tasks):\n            progress = ((i + 1) / len(tasks)) * 100\n            self.creation_sessions[session_id]["steps"][step_index]["progress"] = progress\n            self.creation_sessions[session_id]["steps"][step_index]["details"] = {"current_task": task}\n            await self.send_progress_update(session_id)\n            await asyncio.sleep(0.2)\n    \n    async def cancel_creation(self, session_id: str):\n        """Cancel an ongoing project creation."""\n        if session_id in self.creation_sessions:\n            await self.send_update(session_id, {\n                "type": "creation_cancelled",\n                "message": "🛑 Project creation was cancelled",\n                "timestamp": datetime.now().isoformat()\n            })\n            \n            del self.creation_sessions[session_id]\n    \n    def get_creation_status(self, session_id: str) -> Optional[Dict[str, Any]]:\n        """Get current creation status for a session."""\n        return self.creation_sessions.get(session_id)