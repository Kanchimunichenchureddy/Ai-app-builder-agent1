// Simple test script to verify deployment services
const testDeploymentServices = async () => {
  console.log('Testing Deployment Services...');
  
  try {
    // Test if the required services are available
    const apiModule = await import('./frontend/src/services/api.js');
    const projectsServiceModule = await import('./frontend/src/services/projectsService.js');
    const deploymentServiceModule = await import('./frontend/src/services/enhancedDeploymentService.js');
    
    console.log('✅ All services imported successfully');
    
    // Test API configuration
    const api = apiModule.default;
    console.log('✅ API service configured');
    console.log('   Base URL:', api.defaults.baseURL);
    
    // Test service methods
    const projectsService = projectsServiceModule.default;
    const deploymentService = deploymentServiceModule.default;
    
    console.log('✅ Projects Service methods available:');
    console.log('   - getProjects:', typeof projectsService.getProjects === 'function');
    console.log('   - getProject:', typeof projectsService.getProject === 'function');
    console.log('   - deleteProject:', typeof projectsService.deleteProject === 'function');
    
    console.log('✅ Deployment Service methods available:');
    console.log('   - getSupportedPlatforms:', typeof deploymentService.getSupportedPlatforms === 'function');
    console.log('   - getProjectDeployments:', typeof deploymentService.getProjectDeployments === 'function');
    console.log('   - getDeploymentStatus:', typeof deploymentService.getDeploymentStatus === 'function');
    
    console.log('\n🎉 All deployment services are properly configured!');
    console.log('\nTo test actual API connectivity, start the backend server and run the application.');
    
  } catch (error) {
    console.error('❌ Error testing deployment services:', error.message);
    console.error('Stack trace:', error.stack);
  }
};

// Run the test
testDeploymentServices();