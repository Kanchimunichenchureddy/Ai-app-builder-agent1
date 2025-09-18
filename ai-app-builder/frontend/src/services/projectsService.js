import api from './api';

class ProjectsService {
  // Get all projects for the current user
  async getProjects(skip = 0, limit = 20, statusFilter = null, typeFilter = null) {
    try {
      const params = { skip, limit };
      if (statusFilter) params.status_filter = statusFilter;
      if (typeFilter) params.type_filter = typeFilter;
      
      const response = await api.get('/projects/', { params });
      return response.data;
    } catch (error) {
      console.error('Error fetching projects:', error);
      throw error;
    }
  }

  // Get a specific project by ID
  async getProject(projectId) {
    try {
      const response = await api.get(`/projects/${projectId}`);
      return response.data;
    } catch (error) {
      console.error('Error fetching project:', error);
      throw error;
    }
  }

  // Update a project
  async updateProject(projectId, updateData) {
    try {
      const response = await api.put(`/projects/${projectId}`, updateData);
      return response.data;
    } catch (error) {
      console.error('Error updating project:', error);
      throw error;
    }
  }

  // Delete a project
  async deleteProject(projectId) {
    try {
      const response = await api.delete(`/projects/${projectId}`);
      return response.data;
    } catch (error) {
      console.error('Error deleting project:', error);
      throw error;
    }
  }

  // Get project files
  async getProjectFiles(projectId) {
    try {
      const response = await api.get(`/projects/${projectId}/files`);
      return response.data;
    } catch (error) {
      console.error('Error fetching project files:', error);
      throw error;
    }
  }

  // Get project file content
  async getProjectFileContent(projectId, fileId) {
    try {
      const response = await api.get(`/projects/${projectId}/file/${fileId}`);
      return response.data;
    } catch (error) {
      console.error('Error fetching project file content:', error);
      throw error;
    }
  }

  // Get project statistics
  async getProjectStats() {
    try {
      const response = await api.get('/projects/stats/overview');
      return response.data;
    } catch (error) {
      console.error('Error fetching project stats:', error);
      throw error;
    }
  }
}

export default new ProjectsService();