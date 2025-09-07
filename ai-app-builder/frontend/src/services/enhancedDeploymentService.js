import api from './api';

class EnhancedDeploymentService {
  // Get supported deployment platforms
  async getSupportedPlatforms() {
    try {
      const response = await api.get('/deployment/platforms');
      return response.data;
    } catch (error) {
      console.error('Error fetching platforms:', error);
      throw error;
    }
  }

  // Deploy project to a specific platform
  async deployProject(projectId, deploymentData) {
    try {
      const response = await api.post(`/deployment/deploy/${projectId}`, deploymentData);
      return response.data;
    } catch (error) {
      console.error('Error deploying project:', error);
      throw error;
    }
  }

  // Get all deployments for a project
  async getProjectDeployments(projectId) {
    try {
      const response = await api.get(`/deployment/deployments/${projectId}`);
      return response.data;
    } catch (error) {
      console.error('Error fetching deployments:', error);
      throw error;
    }
  }

  // Get deployment status
  async getDeploymentStatus(deploymentId) {
    try {
      const response = await api.get(`/deployment/deployment/${deploymentId}/status`);
      return response.data;
    } catch (error) {
      console.error('Error fetching deployment status:', error);
      throw error;
    }
  }

  // Stop a deployment
  async stopDeployment(deploymentId) {
    try {
      const response = await api.post(`/deployment/deployment/${deploymentId}/stop`);
      return response.data;
    } catch (error) {
      console.error('Error stopping deployment:', error);
      throw error;
    }
  }

  // Delete a deployment
  async deleteDeployment(deploymentId) {
    try {
      const response = await api.delete(`/deployment/deployment/${deploymentId}`);
      return response.data;
    } catch (error) {
      console.error('Error deleting deployment:', error);
      throw error;
    }
  }

  // Get deployment logs
  async getDeploymentLogs(deploymentId) {
    try {
      // This would be implemented if we had a logs endpoint
      // For now, we'll return the deployment status which includes logs
      const response = await api.get(`/deployment/deployment/${deploymentId}/status`);
      return {
        success: true,
        logs: response.data.deployment?.deployment_logs || ''
      };
    } catch (error) {
      console.error('Error fetching deployment logs:', error);
      throw error;
    }
  }

  // Get platform-specific configuration options
  getPlatformConfigOptions(platform) {
    const configOptions = {
      aws: {
        region: 'us-east-1',
        instanceType: 't3.micro',
        autoScaling: true,
        loadBalancer: true
      },
      gcp: {
        region: 'us-central1',
        machineType: 'e2-micro',
        preemptible: false,
        autoscaling: true
      },
      azure: {
        region: 'East US',
        vmSize: 'Standard_B1s',
        autoScaling: true,
        loadBalancer: true
      },
      docker: {
        portMapping: '3000:3000',
        environment: {},
        volumes: []
      },
      vercel: {
        buildCommand: 'npm run build',
        outputDirectory: 'build',
        environment: {}
      },
      netlify: {
        buildCommand: 'npm run build',
        publishDirectory: 'build',
        functionsDirectory: 'functions'
      }
    };

    return configOptions[platform] || {};
  }

  // Validate deployment configuration
  validateDeploymentConfig(platform, config) {
    const requiredFields = {
      aws: ['region', 'instanceType'],
      gcp: ['region', 'machineType'],
      azure: ['region', 'vmSize'],
      docker: [],
      vercel: ['buildCommand'],
      netlify: ['buildCommand']
    };

    const required = requiredFields[platform] || [];
    const missing = required.filter(field => !config[field]);

    if (missing.length > 0) {
      return {
        valid: false,
        missingFields: missing
      };
    }

    return {
      valid: true,
      missingFields: []
    };
  }
}

export default new EnhancedDeploymentService();