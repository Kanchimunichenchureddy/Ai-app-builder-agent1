# AI App Builder - Deployment Instructions

## Overview
This document provides instructions on how to properly deploy your AI-generated applications and resolve the 404 error when clicking "View Demo" or "View Live Demo" buttons.

## Problem Resolution Summary
The 404 error has been resolved by implementing proper integration between the frontend and backend deployment systems. The issue was caused by using mock data with placeholder URLs instead of real deployment URLs.

## How to Deploy Your Applications

### Step 1: Create a Project
1. Navigate to the "My Projects" page
2. Click "New Project" to create an AI-generated application
3. Configure your project requirements using the AI builder

### Step 2: Deploy Your Application
1. Go to the "Deploy" page from the main navigation
2. Select a deployment platform:
   - **Docker**: For local deployment or cloud container deployment
   - **Vercel**: For frontend deployment with global CDN
   - **Netlify**: For static site deployment with continuous integration
   - **AWS**: For full cloud deployment on Amazon Web Services
   - **GCP**: For deployment on Google Cloud Platform
   - **Azure**: For deployment on Microsoft Azure

3. Click "Deploy to this Platform" to start the deployment process

### Step 3: View Your Live Application
1. After successful deployment, return to the "My Projects" page
2. You will see a "View Demo" button for deployed projects
3. Click the button to open your live application in a new tab

## Understanding the Deployment System

### Deployment Flow
1. **Project Creation**: AI generates full-stack application code
2. **Platform Selection**: Choose deployment target based on requirements
3. **Deployment Process**: System packages and deploys application
4. **URL Generation**: Real URLs are created and stored in database
5. **Demo Access**: Users can view live applications through "View Demo" buttons

### Supported Platforms
- **Docker**: Local containers with Nginx reverse proxy
- **Vercel**: Frontend hosting with serverless functions
- **Netlify**: Static site hosting with form handling
- **AWS**: Full cloud infrastructure with auto-scaling
- **GCP**: Google Cloud with Kubernetes integration
- **Azure**: Microsoft cloud with enterprise features

## Troubleshooting Common Issues

### 1. "View Demo" Button Not Appearing
**Cause**: Project hasn't been deployed yet
**Solution**: 
1. Go to the "Deploy" page
2. Select a deployment platform
3. Complete the deployment process
4. Return to "My Projects" page

### 2. 404 Error When Clicking Demo Links
**Cause**: Deployment failed or URL not properly generated
**Solution**:
1. Check deployment logs in the "Deploy" page
2. Retry deployment process
3. Verify platform credentials are configured

### 3. Deployment Process Fails
**Cause**: Missing platform credentials or tools
**Solution**:
1. Ensure required CLI tools are installed (Docker, Vercel CLI, etc.)
2. Configure platform credentials in backend environment variables
3. Check network connectivity to deployment platforms

## Required Environment Variables

For each platform, you need to configure the following environment variables in your backend [.env](file:///c%3A/Users/teja.kanchi/Desktop/AI%20co-developer/ai-app-builder/backend/.env.example#L1-L23) file:

### Docker
```env
# Docker requires no additional credentials
# Ensure Docker Desktop is installed and running
```

### Vercel
```env
VERCEL_TOKEN=your_vercel_token
```

### Netlify
```env
NETLIFY_AUTH_TOKEN=your_netlify_token
```

### AWS
```env
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_DEFAULT_REGION=us-east-1
```

### Google Cloud
```env
GOOGLE_APPLICATION_CREDENTIALS=path_to_service_account_key.json
```

### Azure
```env
AZURE_CLIENT_ID=your_client_id
AZURE_CLIENT_SECRET=your_client_secret
AZURE_TENANT_ID=your_tenant_id
```

## Testing Your Deployment

### 1. Verify Backend Services
```bash
# Check if backend is running
curl http://localhost:8000/health

# Check deployment endpoints
curl http://localhost:8000/api/deployment/platforms
```

### 2. Test Frontend Integration
1. Start the frontend development server
2. Navigate to "My Projects" page
3. Create a test project
4. Deploy the project using Docker (easiest for local testing)
5. Verify "View Demo" button appears and works

## Best Practices

### 1. Platform Selection
- **Development**: Use Docker for local testing
- **Static Sites**: Use Vercel or Netlify
- **Full Applications**: Use AWS, GCP, or Azure
- **Enterprise**: Use Azure for Microsoft integration

### 2. Security
- Never commit credentials to version control
- Use environment variables for sensitive data
- Regularly rotate API tokens
- Enable two-factor authentication on deployment platforms

### 3. Monitoring
- Check deployment logs regularly
- Monitor application performance
- Set up alerts for deployment failures
- Keep deployment tools updated

## Getting Help

If you continue to experience issues:

1. **Check the Console**: Open browser developer tools to see error messages
2. **Verify Services**: Ensure both frontend and backend services are running
3. **Review Logs**: Check deployment logs for specific error information
4. **Contact Support**: Refer to the main documentation for support contacts

## Conclusion

The deployment system is now fully functional. Users can create AI-generated applications and deploy them to various platforms with a single click. The 404 error has been resolved by implementing proper integration between frontend and backend systems, ensuring that demo URLs are only shown when valid deployments exist.