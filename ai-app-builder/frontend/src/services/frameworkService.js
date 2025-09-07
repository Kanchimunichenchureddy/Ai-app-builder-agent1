import api from './api';

class FrameworkService {
  // Get supported frameworks
  async getSupportedFrameworks() {
    try {
      const response = await api.get('/builder/frameworks');
      return response.data;
    } catch (error) {
      console.error('Error fetching frameworks:', error);
      throw error;
    }
  }

  // Get framework recommendations
  async getFrameworkRecommendations(analysis) {
    try {
      const response = await api.post('/builder/recommend-stack', {
        analysis
      });
      return response.data;
    } catch (error) {
      console.error('Error getting recommendations:', error);
      throw error;
    }
  }

  // Generate project with custom stack
  async generateProjectWithCustomStack(projectData) {
    try {
      const response = await api.post('/builder/generate-with-stack', projectData);
      return response.data;
    } catch (error) {
      console.error('Error generating project with custom stack:', error);
      throw error;
    }
  }

  // Get enhanced capabilities
  async getEnhancedCapabilities() {
    try {
      const response = await api.get('/builder/capabilities');
      return response.data;
    } catch (error) {
      console.error('Error fetching capabilities:', error);
      throw error;
    }
  }
}

export default new FrameworkService();