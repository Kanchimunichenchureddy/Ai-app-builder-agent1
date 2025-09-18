import os
import shutil
import threading
import time
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
import socketserver
import json
from typing import Dict, Any

class StaticFileServer:
    """
    Simple static file server for serving deployed frontend applications.
    This provides an alternative to Docker deployment for local development.
    """
    
    def __init__(self, static_dir: str = "static", port: int = 8080):
        self.static_dir = Path(static_dir)
        self.port = port
        self.servers = {}  # Keep track of running servers
        self.server_threads = {}  # Keep track of server threads
        
        # Ensure static directory exists
        self.static_dir.mkdir(exist_ok=True)
        
    def serve_project(self, project_id: int, project_name: str, build_path: str) -> Dict[str, Any]:
        """
        Serve a project's frontend build files.
        
        Args:
            project_id: The project ID
            project_name: The project name
            build_path: Path to the frontend build directory
            
        Returns:
            Dictionary with server information
        """
        try:
            # Create project directory in static folder
            project_dir = self.static_dir / f"project_{project_id}"
            project_dir.mkdir(exist_ok=True)
            
            # Copy build files to project directory
            if os.path.exists(build_path):
                # Clear existing files
                for item in project_dir.iterdir():
                    if item.is_file():
                        item.unlink()
                    elif item.is_dir():
                        shutil.rmtree(item)
                
                # Copy new files
                self._copytree(build_path, project_dir)
            
            # Start server for this project if not already running
            if project_id not in self.servers:
                # Find available port
                port = self._find_available_port(self.port + project_id)
                
                # Start server in a separate thread
                server_thread = threading.Thread(
                    target=self._start_server, 
                    args=(project_dir, port, project_id),
                    daemon=True
                )
                server_thread.start()
                
                # Store server info
                self.server_threads[project_id] = server_thread
                
                # Wait a moment for server to start
                time.sleep(1)
            
            # Return server information
            port = self.port + project_id
            return {
                "success": True,
                "url": f"http://localhost:{port}",
                "port": port,
                "project_id": project_id,
                "message": f"Project {project_name} is now available at http://localhost:{port}"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": f"Failed to serve project {project_name}: {str(e)}"
            }
    
    def _find_available_port(self, start_port: int) -> int:
        """Find an available port starting from start_port."""
        port = start_port
        while True:
            try:
                with socketserver.TCPServer(("", port), SimpleHTTPRequestHandler) as srv:
                    srv.server_close()
                return port
            except OSError:
                port += 1
                if port > start_port + 100:  # Don't search indefinitely
                    return start_port
    
    def _start_server(self, directory: Path, port: int, project_id: int):
        """Start HTTP server for a specific directory."""
        try:
            # Change to the directory we want to serve
            os.chdir(str(directory))
            
            # Create and start server
            handler = SimpleHTTPRequestHandler
            server = HTTPServer(("", port), handler)
            self.servers[project_id] = server
            
            print(f"Static file server started for project {project_id} on port {port}")
            print(f"Serving directory: {directory}")
            
            # Start serving
            server.serve_forever()
            
        except Exception as e:
            print(f"Error starting server for project {project_id}: {e}")
    
    def stop_server(self, project_id: int) -> Dict[str, Any]:
        """Stop server for a specific project."""
        try:
            if project_id in self.servers:
                server = self.servers[project_id]
                server.shutdown()
                server.server_close()
                del self.servers[project_id]
                
                if project_id in self.server_threads:
                    del self.server_threads[project_id]
            
            return {
                "success": True,
                "message": f"Server for project {project_id} stopped"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": f"Failed to stop server for project {project_id}: {str(e)}"
            }
    
    def get_server_info(self, project_id: int) -> Dict[str, Any]:
        """Get information about a project's server."""
        if project_id in self.servers:
            port = self.port + project_id
            return {
                "running": True,
                "url": f"http://localhost:{port}",
                "port": port,
                "project_id": project_id
            }
        else:
            return {
                "running": False,
                "project_id": project_id
            }
    
    def _copytree(self, src: str, dst: str):
        """Copy directory tree, handling existing files."""
        src_path = Path(src)
        dst_path = Path(dst)
        
        if not src_path.exists():
            return
            
        for item in src_path.iterdir():
            dst_item = dst_path / item.name
            if item.is_dir():
                dst_item.mkdir(exist_ok=True)
                self._copytree(str(item), str(dst_item))
            else:
                shutil.copy2(str(item), str(dst_item))

# Create a global instance
static_server = StaticFileServer()

if __name__ == "__main__":
    # Example usage
    print("Static File Server Service")
    print("This module should be imported and used by other services.")