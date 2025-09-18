# AI App Builder Deployment Guide

## Understanding the 404 Error

When you click "View Demo" or "View Live Demo" and see a 404 error, it's because the application hasn't been deployed yet. The URLs shown in the demo are just examples and don't point to real applications.

## How to Properly Deploy Your Applications

### 1. Create Your Project
1. Navigate to the AI Builder page
2. Describe your application idea in natural language
3. Customize the technology stack if needed
4. Generate your application code

### 2. Deploy Your Project
1. Go to "My Projects" page
2. Find your project in the list
3. Click the "Deploy" button in the project actions
4. This will take you to the Deployment page

### 3. Select a Deployment Platform
On the Deployment page, you can choose from several platforms:
- **Docker**: For local deployment or cloud container deployment
- **Vercel**: For frontend deployment with global CDN
- **Netlify**: For static site deployment
- **AWS**: For full cloud deployment
- **Google Cloud**: For Google Cloud Platform deployment
- **Azure**: For Microsoft Azure deployment

### 4. Configure Your Deployment
Each platform has specific configuration options:
- **Docker**: Port mapping, environment variables
- **Vercel/Netlify**: Build commands, output directories
- **Cloud Platforms (AWS/GCP/Azure)**: Region, instance types, scaling options

### 5. Initiate Deployment
1. Select your preferred platform
2. Configure any required settings
3. Click "Deploy to this Platform"
4. Monitor the deployment progress in the "Recent Deployments" section

### 6. View Your Live Application
Once deployment is complete and successful:
1. The deployment status will show as "Deployed"
2. A valid URL will be generated
3. Click "View Live Demo" to open your application

## Troubleshooting Deployment Issues

### Common Issues and Solutions

1. **Deployment Fails**
   - Check your platform credentials (API keys, tokens)
   - Verify your project builds correctly
   - Ensure you have sufficient resources/quota on the platform

2. **404 Error After Deployment**
   - Wait a few minutes for DNS propagation
   - Check deployment logs for errors
   - Verify the platform dashboard for any issues

3. **Application Not Working as Expected**
   - Check environment variables are correctly set
   - Verify database connections if applicable
   - Review platform-specific configuration

## Platform-Specific Requirements

### Docker Deployment
- Docker must be installed locally
- Port 3000 should be available

### Vercel Deployment
- Vercel account required
- Vercel CLI installed (`npm install -g vercel`)

### Netlify Deployment
- Netlify account required
- Netlify CLI installed (`npm install -g netlify-cli`)

### Cloud Platform Deployments (AWS/GCP/Azure)
- Valid account with billing setup
- Appropriate CLI tools installed
- Required API keys/credentials configured

## Best Practices

1. **Test Locally First**
   - Always test your application locally before deploying
   - Use the "View Code" option to review generated code

2. **Monitor Deployments**
   - Check deployment logs for any warnings or errors
   - Verify the application works after deployment

3. **Use Environment Variables**
   - Store sensitive information in environment variables
   - Don't hardcode API keys or credentials

4. **Handle Errors Gracefully**
   - Implement proper error handling in your applications
   - Use health checks where applicable

## Getting Help

If you continue to experience issues:
1. Check the deployment logs for specific error messages
2. Verify all platform requirements are met
3. Contact support with deployment ID and error details