from typing import Dict, Any, List, Optional
from datetime import datetime
import asyncio
from fastapi import WebSocket
from sqlalchemy.orm import Session
from app.models.project import Project, ProjectStatus

class ProjectProgressStep:
    """Represents a step in the project creation process."""
    
    def __init__(self, id: str, name: str, description: str, weight: float = 1.0):
        self.id = id
        self.name = name
        self.description = description
        self.weight = weight

class RealTimeProjectCreator:
    """Manages real-time project creation with progress updates."""
    
    def __init__(self):
        # Define creation steps with weights for progress calculation
        self.creation_steps = [
            ProjectProgressStep("analyze", "Analyze Requirements", "Analyzing project requirements and specifications", 1.0),
            ProjectProgressStep("plan", "Create Project Plan", "Creating detailed project plan and architecture", 1.5),
            ProjectProgressStep("frontend", "Generate Frontend", "Generating frontend components and UI", 2.0),
            ProjectProgressStep("backend", "Generate Backend", "Generating backend APIs and services", 2.0),
            ProjectProgressStep("database", "Setup Database", "Setting up database schema and migrations", 1.5),
            ProjectProgressStep("integration", "Integrate Services", "Integrating frontend and backend services", 1.5),
            ProjectProgressStep("testing", "Generate Tests", "Generating test files and test suites", 1.0),
            ProjectProgressStep("optimization", "Optimize Code", "Optimizing generated code for performance", 1.0),
            ProjectProgressStep("deployment", "Prepare Deployment", "Preparing deployment configurations", 1.0),
            ProjectProgressStep("finalize", "Finalize Project", "Finalizing project creation and packaging", 0.5)
        ]
        
        # Store active creation sessions
        self.creation_sessions: Dict[str, Dict[str, Any]] = {}
    
    async def connect_websocket(self, websocket: WebSocket, session_id: str):
        """Connect a WebSocket to a creation session."""
        await websocket.accept()
        
        # Initialize session data
        self.creation_sessions[session_id] = {
            "websocket": websocket,
            "steps": [
                {
                    "id": step.id,
                    "name": step.name,
                    "description": step.description,
                    "status": "pending",
                    "progress": 0.0,
                    "weight": step.weight,
                    "start_time": None,
                    "end_time": None,
                    "error_message": None,
                    "details": {}
                }
                for step in self.creation_steps
            ],
            "overall_progress": 0.0,
            "start_time": datetime.now().isoformat()
        }
        
        # Send initial connection confirmation
        await self.send_update(session_id, {
            "type": "connected",
            "session_id": session_id,
            "message": "🚀 Connected to real-time project creation!",
            "timestamp": datetime.now().isoformat()
        })
    
    async def disconnect_websocket(self, session_id: str):
        """Disconnect a WebSocket from a creation session."""
        if session_id in self.creation_sessions:
            websocket = self.creation_sessions[session_id]["websocket"]
            try:
                await websocket.close()
            except:
                pass
            del self.creation_sessions[session_id]
    
    async def send_update(self, session_id: str, data: Dict[str, Any]):
        """Send an update to a connected client."""
        if session_id in self.creation_sessions:
            websocket = self.creation_sessions[session_id]["websocket"]
            try:
                await websocket.send_text(data)
            except:
                # If sending fails, disconnect the WebSocket
                await self.disconnect_websocket(session_id)
    
    async def create_project_realtime(self, session_id: str, project_data: Dict[str, Any], db: Session):
        """Create a project with real-time progress updates."""
        try:
            # Send initial status update
            await self.send_update(session_id, {
                "type": "project_started",
                "message": "🚀 Starting project creation...",
                "timestamp": datetime.now().isoformat()
            })
            
            await self.send_progress_update(session_id)
            
            project_name = project_data.get("name", "")
            analysis = project_data.get("analysis", {})
            tech_stack = project_data.get("tech_stack", {})
            
            # Create project record in database
            project = Project(
                name=project_name,
                description=analysis.get("description", ""),
                project_type=analysis.get("project_type", "web_app"),
                status=ProjectStatus.CREATING,
                owner_id=project_data.get("user_id"),
                config={"tech_stack": tech_stack},
                features=analysis.get("features", [])
            )
            
            db.add(project)
            db.commit()
            db.refresh(project)
            
            # Execute creation steps with real-time updates
            generated_files = {}
            
            for i, step in enumerate(self.creation_steps):
                await self.execute_creation_step(session_id, i, step, project_data, generated_files)
                
                # Check if session was cancelled
                if session_id not in self.creation_sessions:
                    break
            
            # Update project status
            if session_id in self.creation_sessions:
                project.status = ProjectStatus.ACTIVE
                project.project_path = f"generated_projects/project_{project.id}"
                db.commit()
                
                # Send completion update
                await self.send_update(session_id, {
                    "type": "project_completed",
                    "project": {
                        "id": project.id,
                        "name": project.name,
                        "status": project.status.value,
                        "created_at": project.created_at.isoformat()
                    },
                    "files_generated": len(generated_files),
                    "message": f"🎉 {project_name} has been successfully created!",
                    "timestamp": datetime.now().isoformat()
                })
                
                return {
                    "success": True,
                    "project_id": project.id,
                    "session_id": session_id,
                    "files_generated": len(generated_files)
                }
            
        except Exception as e:
            # Handle errors and notify client
            await self.send_update(session_id, {
                "type": "project_error",
                "error": str(e),
                "message": f"❌ Project creation failed: {str(e)}",
                "timestamp": datetime.now().isoformat()
            })
            
            # Update project status to error
            if 'project' in locals():
                project.status = ProjectStatus.ERROR
                db.commit()
            
            raise e
        
        finally:
            # Clean up session
            if session_id in self.creation_sessions:
                del self.creation_sessions[session_id]
    
    async def execute_creation_step(
        self,
        session_id: str,
        step_index: int,
        step: ProjectProgressStep,
        project_data: Dict[str, Any],
        generated_files: Dict[str, str]
    ):
        """Execute a single creation step with progress updates."""
        # Update step status to active
        self.creation_sessions[session_id]["steps"][step_index]["status"] = "active"
        self.creation_sessions[session_id]["steps"][step_index]["start_time"] = datetime.now().isoformat()
        
        await self.send_progress_update(session_id)
        
        try:
            # Execute step based on its ID
            if step.id == "analyze":
                await self.step_analyze_requirements(session_id, step_index, project_data)
            elif step.id == "plan":
                await self.step_create_project_plan(session_id, step_index, project_data)
            elif step.id == "frontend":
                frontend_files = await self.step_generate_frontend(session_id, step_index, project_data)
                generated_files.update(frontend_files)
            elif step.id == "backend":
                backend_files = await self.step_generate_backend(session_id, step_index, project_data)
                generated_files.update(backend_files)
            elif step.id == "database":
                db_files = await self.step_setup_database(session_id, step_index, project_data)
                generated_files.update(db_files)
            elif step.id == "integration":
                await self.step_integrate_services(session_id, step_index, project_data)
            elif step.id == "testing":
                test_files = await self.step_generate_tests(session_id, step_index, project_data)
                generated_files.update(test_files)
            elif step.id == "optimization":
                await self.step_optimize_code(session_id, step_index, project_data)
            elif step.id == "deployment":
                deploy_files = await self.step_prepare_deployment(session_id, step_index, project_data)
                generated_files.update(deploy_files)
            elif step.id == "finalize":
                await self.step_finalize_project(session_id, step_index, project_data)
            
            # Mark step as completed
            self.creation_sessions[session_id]["steps"][step_index]["status"] = "completed"
            self.creation_sessions[session_id]["steps"][step_index]["end_time"] = datetime.now().isoformat()
            self.creation_sessions[session_id]["steps"][step_index]["progress"] = 100.0
            
            await self.send_progress_update(session_id)
            
        except Exception as e:
            # Mark step as error
            self.creation_sessions[session_id]["steps"][step_index]["status"] = "error"
            self.creation_sessions[session_id]["steps"][step_index]["error_message"] = str(e)
            self.creation_sessions[session_id]["steps"][step_index]["end_time"] = datetime.now().isoformat()
            
            await self.send_progress_update(session_id)
            raise e
    
    async def send_progress_update(self, session_id: str):
        """Send current progress update to the client."""
        if session_id not in self.creation_sessions:
            return
        
        session = self.creation_sessions[session_id]
        
        # Calculate overall progress
        total_weight = sum(step["weight"] for step in session["steps"])
        completed_weight = sum(
            step["weight"] for step in session["steps"] 
            if step["status"] == "completed"
        )
        active_weight = sum(
            step["weight"] * (step["progress"] / 100.0) for step in session["steps"] 
            if step["status"] == "active"
        )
        
        overall_progress = min(100.0, ((completed_weight + active_weight) / total_weight) * 100.0)
        session["overall_progress"] = overall_progress
        
        await self.send_update(session_id, {
            "type": "progress_update",
            "overall_progress": overall_progress,
            "steps": session["steps"],
            "timestamp": datetime.now().isoformat()
        })
    
    # Individual step implementations
    async def step_analyze_requirements(self, session_id: str, step_index: int, project_data: Dict[str, Any]):
        """Step 1: Analyze project requirements."""
        await asyncio.sleep(1)  # Simulate AI processing time
        
        # Update step progress incrementally
        for progress in [25, 50, 75, 100]:
            self.creation_sessions[session_id]["steps"][step_index]["progress"] = progress
            await self.send_progress_update(session_id)
            await asyncio.sleep(0.5)
    
    async def step_create_project_plan(self, session_id: str, step_index: int, project_data: Dict[str, Any]):
        """Step 2: Create detailed project plan."""
        await asyncio.sleep(1.5)
        
        for progress in [20, 40, 60, 80, 100]:
            self.creation_sessions[session_id]["steps"][step_index]["progress"] = progress
            await self.send_progress_update(session_id)
            await asyncio.sleep(0.6)
    
    async def step_generate_frontend(self, session_id: str, step_index: int, project_data: Dict[str, Any]) -> Dict[str, str]:
        """Step 3: Generate frontend components."""
        await asyncio.sleep(2)
        
        # Simulate file generation progress
        files = {}
        components = ["App.js", "HomePage.js", "components/Navbar.js", "components/Footer.js", "services/api.js"]
        
        for i, component in enumerate(components):
            progress = ((i + 1) / len(components)) * 100
            self.creation_sessions[session_id]["steps"][step_index]["progress"] = progress
            self.creation_sessions[session_id]["steps"][step_index]["details"] = {
                "current_file": component,
                "files_generated": i + 1,
                "total_files": len(components)
            }
            
            files[f"frontend/src/{component}"] = f"// Generated {component} content"
            
            await self.send_progress_update(session_id)
            await asyncio.sleep(0.4)
        
        return files
    
    async def step_generate_backend(self, session_id: str, step_index: int, project_data: Dict[str, Any]) -> Dict[str, str]:
        """Step 4: Generate backend APIs."""
        await asyncio.sleep(2)
        
        files = {}
        endpoints = ["main.py", "models/user.py", "api/auth.py", "api/routes.py", "core/config.py"]
        
        for i, endpoint in enumerate(endpoints):
            progress = ((i + 1) / len(endpoints)) * 100
            self.creation_sessions[session_id]["steps"][step_index]["progress"] = progress
            self.creation_sessions[session_id]["steps"][step_index]["details"] = {
                "current_file": endpoint,
                "files_generated": i + 1,
                "total_files": len(endpoints)
            }
            
            files[f"backend/{endpoint}"] = f"# Generated {endpoint} content"
            
            await self.send_progress_update(session_id)
            await asyncio.sleep(0.4)
        
        return files
    
    async def step_setup_database(self, session_id: str, step_index: int, project_data: Dict[str, Any]) -> Dict[str, str]:
        """Step 5: Setup database schema."""
        await asyncio.sleep(1.5)
        
        files = {
            "database/init.sql": "-- Database initialization script",
            "database/migrations/001_initial.sql": "-- Initial migration",
            "database/seeds/sample_data.sql": "-- Sample data"
        }
        
        for i in range(1, 6):
            progress = (i / 5) * 100
            self.creation_sessions[session_id]["steps"][step_index]["progress"] = progress
            await self.send_progress_update(session_id)
            await asyncio.sleep(0.3)
        
        return files
    
    async def step_integrate_services(self, session_id: str, step_index: int, project_data: Dict[str, Any]):
        """Step 6: Integrate frontend and backend."""
        await asyncio.sleep(1.5)
        
        for progress in [25, 50, 75, 100]:
            self.creation_sessions[session_id]["steps"][step_index]["progress"] = progress
            await self.send_progress_update(session_id)
            await asyncio.sleep(0.5)
    
    async def step_generate_tests(self, session_id: str, step_index: int, project_data: Dict[str, Any]) -> Dict[str, str]:
        """Step 7: Generate test files."""
        await asyncio.sleep(1)
        
        files = {
            "frontend/src/tests/App.test.js": "// Frontend tests",
            "backend/tests/test_auth.py": "# Backend tests",
            "backend/tests/test_api.py": "# API tests"
        }
        
        for i in range(1, 4):
            progress = (i / 3) * 100
            self.creation_sessions[session_id]["steps"][step_index]["progress"] = progress
            await self.send_progress_update(session_id)
            await asyncio.sleep(0.4)
        
        return files
    
    async def step_optimize_code(self, session_id: str, step_index: int, project_data: Dict[str, Any]):
        """Step 8: Optimize generated code."""
        await asyncio.sleep(1)
        
        optimizations = ["Code formatting", "Performance optimization", "Security review", "Best practices"]
        
        for i, opt in enumerate(optimizations):
            progress = ((i + 1) / len(optimizations)) * 100
            self.creation_sessions[session_id]["steps"][step_index]["progress"] = progress
            self.creation_sessions[session_id]["steps"][step_index]["details"] = {"current_optimization": opt}
            await self.send_progress_update(session_id)
            await asyncio.sleep(0.3)
    
    async def step_prepare_deployment(self, session_id: str, step_index: int, project_data: Dict[str, Any]) -> Dict[str, str]:
        """Step 9: Prepare deployment configurations."""
        await asyncio.sleep(1)
        
        files = {
            "Dockerfile": "# Docker configuration",
            "docker-compose.yml": "# Docker Compose configuration",
            ".github/workflows/deploy.yml": "# GitHub Actions deployment",
            "deploy.sh": "#!/bin/bash\\n# Deployment script"
        }
        
        for i in range(1, 5):
            progress = (i / 4) * 100
            self.creation_sessions[session_id]["steps"][step_index]["progress"] = progress
            await self.send_progress_update(session_id)
            await asyncio.sleep(0.3)
        
        return files
    
    async def step_finalize_project(self, session_id: str, step_index: int, project_data: Dict[str, Any]):
        """Step 10: Finalize project creation."""
        await asyncio.sleep(0.5)
        
        tasks = ["Final validation", "Generating README", "Creating documentation", "Project packaging"]
        
        for i, task in enumerate(tasks):
            progress = ((i + 1) / len(tasks)) * 100
            self.creation_sessions[session_id]["steps"][step_index]["progress"] = progress
            self.creation_sessions[session_id]["steps"][step_index]["details"] = {"current_task": task}
            await self.send_progress_update(session_id)
            await asyncio.sleep(0.2)
    
    async def cancel_creation(self, session_id: str):
        """Cancel an ongoing project creation."""
        if session_id in self.creation_sessions:
            await self.send_update(session_id, {
                "type": "creation_cancelled",
                "message": "🛑 Project creation was cancelled",
                "timestamp": datetime.now().isoformat()
            })
            
            del self.creation_sessions[session_id]
    
    def get_creation_status(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get current creation status for a session."""
        return self.creation_sessions.get(session_id)
