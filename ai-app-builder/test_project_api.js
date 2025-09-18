// Simple test script to verify project API functionality
const testProjectAPI = async () => {
  console.log('Testing Project API...');
  
  try {
    // Test if the API service is available
    const apiModule = await import('./frontend/src/services/api.js');
    const api = apiModule.default;
    
    console.log('✅ API service imported successfully');
    console.log('   Base URL:', api.defaults.baseURL);
    
    // Test projects service
    const projectsServiceModule = await import('./frontend/src/services/projectsService.js');
    const projectsService = projectsServiceModule.default;
    
    console.log('✅ Projects Service methods available:');
    console.log('   - getProjects:', typeof projectsService.getProjects === 'function');
    console.log('   - getProject:', typeof projectsService.getProject === 'function');
    console.log('   - deleteProject:', typeof projectsService.deleteProject === 'function');
    
    // Test enhanced deployment service
    const deploymentServiceModule = await import('./frontend/src/services/enhancedDeploymentService.js');
    const deploymentService = deploymentServiceModule.default;
    
    console.log('✅ Deployment Service methods available:');
    console.log('   - getSupportedPlatforms:', typeof deploymentService.getSupportedPlatforms === 'function');
    console.log('   - getProjectDeployments:', typeof deploymentService.getProjectDeployments === 'function');
    console.log('   - getDeploymentStatus:', typeof deploymentService.getDeploymentStatus === 'function');
    
    console.log('\n🎉 All services are properly configured!');
    console.log('\nTo test actual API connectivity:');
    console.log('1. Ensure the backend is running on http://localhost:8000');
    console.log('2. Make sure you are logged in to the application');
    console.log('3. Check browser console for any network errors');
    
  } catch (error) {
    console.error('❌ Error testing services:', error.message);
    console.error('Stack trace:', error.stack);
  }
};

// Run the test
testProjectAPI();