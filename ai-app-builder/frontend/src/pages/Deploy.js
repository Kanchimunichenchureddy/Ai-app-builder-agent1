import React, { useState, useEffect } from 'react';
import styled, { keyframes } from 'styled-components';
import { 
  Rocket, 
  Cloud, 
  Server, 
  Globe, 
  CheckCircle, 
  AlertCircle, 
  Clock,
  ExternalLink,
  Play,
  Square,
  Zap,
  Settings,
  RefreshCw,
  Trash2,
  Eye,
  // Adding more icons for enhanced UI
  Plus,
  Edit3,
  Copy,
  Share2,
  Heart,
  ThumbsUp,
  ThumbsDown,
  Search,
  Filter,
  Grid,
  List,
  Monitor,
  Tablet,
  Smartphone as Mobile,
  Lock,
  Unlock,
  Key,
  Shield
} from 'lucide-react';

const pulse = keyframes`
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.7; transform: scale(1.05); }
`;

const slideIn = keyframes`
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
`;

const float = keyframes`
  0%, 100% { transform: translateY(0px); }
  50% { transform: translateY(-10px); }
`;

const shimmer = keyframes`
  0% { background-position: -200% 0; }
  100% { background-position: 200% 0; }
`;

const bounce = keyframes`
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-5px); }
`;

const Container = styled.div`
  padding: 2rem;
  background: linear-gradient(135deg, #f0f4f8 0%, #e6f7ff 100%);
  min-height: 100vh;
  position: relative;
  overflow: hidden;
  
  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: radial-gradient(circle at center, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0) 70%);
    z-index: 0;
  }
`;

const Header = styled.div`
  margin-bottom: 2rem;
  position: relative;
  z-index: 1;
`;

const Title = styled.h1`
  font-size: 2rem;
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 0.5rem;
`;

const Subtitle = styled.p`
  color: #64748b;
  font-size: 1.1rem;
`;

const PlatformGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
  position: relative;
  z-index: 1;
`;

const PlatformCard = styled.div`
  background: white;
  border-radius: 1rem;
  padding: 1.5rem;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.08);
  border: 2px solid ${props => props.selected ? '#667eea' : '#e2e8f0'};
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
  
  &:hover {
    border-color: #667eea;
    transform: translateY(-5px);
    box-shadow: 0 12px 40px rgba(102, 126, 234, 0.15);
  }
  
  ${props => props.selected && `
    &::before {
      content: '';
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      height: 4px;
      background: linear-gradient(90deg, #667eea, #764ba2);
    }
  `}
  
  @media (max-width: 768px) {
    padding: 1.25rem;
  }
`;

const PlatformHeader = styled.div`
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1rem;
`;

const PlatformIcon = styled.div`
  width: 3.5rem;
  height: 3.5rem;
  border-radius: 1rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 1.5rem;
  animation: ${float} 3s ease-in-out infinite;
`;

const PlatformInfo = styled.div`
  flex: 1;
`;

const PlatformName = styled.h3`
  font-size: 1.25rem;
  font-weight: 600;
  color: #1e293b;
  margin: 0;
`;

const PlatformDescription = styled.p`
  color: #64748b;
  font-size: 0.875rem;
  margin: 0;
`;

const FeatureList = styled.ul`
  list-style: none;
  margin: 0;
  padding: 0;
  margin-bottom: 1rem;
`;

const FeatureItem = styled.li`
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #64748b;
  font-size: 0.875rem;
  margin-bottom: 0.5rem;
  
  &:last-child {
    margin-bottom: 0;
  }
`;

const DeploymentSection = styled.div`
  background: white;
  border-radius: 1.25rem;
  padding: 2rem;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.08);
  border: 1px solid #e2e8f0;
  margin-bottom: 2rem;
  animation: ${slideIn} 0.5s ease-out;
  position: relative;
  z-index: 1;
  
  @media (max-width: 768px) {
    padding: 1.5rem;
  }
`;

const SectionTitle = styled.h2`
  font-size: 1.5rem;
  font-weight: 600;
  color: #1e293b;
  margin-bottom: 1.5rem;
  display: flex;
  align-items: center;
  gap: 0.75rem;
`;

const DeploymentList = styled.div`
  display: flex;
  flex-direction: column;
  gap: 1rem;
`;

const DeploymentItem = styled.div`
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1.25rem;
  background: #f8fafc;
  border-radius: 0.75rem;
  border: 1px solid #e2e8f0;
  transition: all 0.2s ease;
  
  &:hover {
    background: #f1f5f9;
    border-color: #c7d2fe;
  }
  
  @media (max-width: 768px) {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }
`;

const DeploymentInfo = styled.div`
  display: flex;
  align-items: center;
  gap: 1rem;
  
  @media (max-width: 768px) {
    width: 100%;
  }
`;

const StatusIcon = styled.div`
  width: 2.5rem;
  height: 2.5rem;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  
  &.success {
    background: #dcfce7;
    color: #16a34a;
  }
  
  &.pending {
    background: #fef3c7;
    color: #d97706;
  }
  
  &.failed {
    background: #fee2e2;
    color: #dc2626;
  }
  
  &.running {
    background: #dbeafe;
    color: #2563eb;
  }
`;

const DeploymentDetails = styled.div`
  @media (max-width: 768px) {
    width: 100%;
  }
`;

const DeploymentName = styled.h3`
  font-size: 1.1rem;
  font-weight: 600;
  color: #1e293b;
  margin: 0 0 0.25rem 0;
`;

const DeploymentMeta = styled.div`
  display: flex;
  gap: 1rem;
  font-size: 0.875rem;
  color: #64748b;
  
  @media (max-width: 768px) {
    flex-direction: column;
    gap: 0.25rem;
  }
`;

const DeploymentActions = styled.div`
  display: flex;
  gap: 0.75rem;
  
  @media (max-width: 768px) {
    width: 100%;
    justify-content: flex-end;
  }
`;

const ActionButton = styled.button`
  background: #f1f5f9;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 0.5rem;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  color: #1e293b;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: all 0.2s ease;
  
  &:hover {
    background: #e2e8f0;
  }
  
  &.primary {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    
    &:hover {
      opacity: 0.9;
    }
  }
  
  &.success {
    background: #10b981;
    color: white;
    
    &:hover {
      background: #059669;
    }
  }
  
  &.danger {
    background: #ef4444;
    color: white;
    
    &:hover {
      background: #dc2626;
    }
  }
  
  @media (max-width: 768px) {
    padding: 0.4rem 0.8rem;
    font-size: 0.8rem;
  }
`;

const FormSection = styled.div`
  background: white;
  border-radius: 1.25rem;
  padding: 2rem;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.08);
  border: 1px solid #e2e8f0;
  margin-bottom: 2rem;
  animation: ${slideIn} 0.5s ease-out;
  position: relative;
  z-index: 1;
  
  @media (max-width: 768px) {
    padding: 1.5rem;
  }
`;

const Form = styled.form`
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
  
  @media (max-width: 768px) {
    grid-template-columns: 1fr;
  }
`;

const FormGroup = styled.div`
  grid-column: ${props => props.fullWidth ? '1 / -1' : 'auto'};
`;

const Label = styled.label`
  display: block;
  font-size: 0.9rem;
  font-weight: 500;
  color: #1e293b;
  margin-bottom: 0.5rem;
`;

const Input = styled.input`
  width: 100%;
  padding: 0.75rem 1rem;
  border: 1px solid #e2e8f0;
  border-radius: 0.75rem;
  font-size: 1rem;
  transition: all 0.2s ease;
  
  &:focus {
    outline: none;
    border-color: #667eea;
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
  }
  
  @media (max-width: 768px) {
    padding: 0.625rem 0.875rem;
    font-size: 0.9rem;
  }
`;

const Select = styled.select`
  width: 100%;
  padding: 0.75rem 1rem;
  border: 1px solid #e2e8f0;
  border-radius: 0.75rem;
  font-size: 1rem;
  background: white;
  transition: all 0.2s ease;
  
  &:focus {
    outline: none;
    border-color: #667eea;
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
  }
  
  @media (max-width: 768px) {
    padding: 0.625rem 0.875rem;
    font-size: 0.9rem;
  }
`;

const TextArea = styled.textarea`
  width: 100%;
  padding: 0.75rem 1rem;
  border: 1px solid #e2e8f0;
  border-radius: 0.75rem;
  font-size: 1rem;
  font-family: inherit;
  min-height: 120px;
  resize: vertical;
  transition: all 0.2s ease;
  
  &:focus {
    outline: none;
    border-color: #667eea;
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
  }
  
  @media (max-width: 768px) {
    padding: 0.625rem 0.875rem;
    font-size: 0.9rem;
  }
`;

const SubmitButton = styled.button`
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  padding: 1rem 2rem;
  border-radius: 0.75rem;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
  grid-column: 1 / -1;
  width: 100%;
  
  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
  }
  
  &:disabled {
    opacity: 0.7;
    cursor: not-allowed;
    transform: none;
  }
  
  @media (max-width: 768px) {
    padding: 0.875rem 1.5rem;
    font-size: 0.9rem;
  }
`;

const LoadingSpinner = styled.div`
  display: inline-flex;
  animation: ${props => props.rotate && pulse} 1s linear infinite;
`;

const StatusIndicator = styled.div`
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.25rem 0.75rem;
  border-radius: 2rem;
  font-size: 0.875rem;
  font-weight: 500;
  
  &.success {
    background: #dcfce7;
    color: #16a34a;
  }
  
  &.pending {
    background: #fef3c7;
    color: #d97706;
  }
  
  &.failed {
    background: #fee2e2;
    color: #dc2626;
  }
  
  &.running {
    background: #dbeafe;
    color: #2563eb;
  }
`;

const ProjectSelector = styled.div`
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 2rem;
  padding: 1rem;
  background: white;
  border-radius: 0.75rem;
  border: 1px solid #e2e8f0;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
  
  @media (max-width: 768px) {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.75rem;
  }
`;

const SelectorLabel = styled.label`
  font-weight: 500;
  color: #1e293b;
  margin: 0;
`;

const Selector = styled.select`
  flex: 1;
  padding: 0.75rem 1rem;
  border: 1px solid #e2e8f0;
  border-radius: 0.75rem;
  font-size: 1rem;
  background: white;
  transition: all 0.2s ease;
  
  &:focus {
    outline: none;
    border-color: #667eea;
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
  }
  
  @media (max-width: 768px) {
    width: 100%;
  }
`;

function Deploy() {
  const [selectedPlatform, setSelectedPlatform] = useState(null);
  const [deployments, setDeployments] = useState([
    {
      id: 1,
      name: 'dashboard-app-prod',
      status: 'success',
      platform: 'AWS',
      url: 'https://dashboard-app.example.com',
      lastDeployed: '2023-06-15 14:30:00',
      region: 'us-west-2'
    },
    {
      id: 2,
      name: 'ecommerce-store-dev',
      status: 'running',
      platform: 'Google Cloud',
      url: 'https://ecommerce-dev.example.com',
      lastDeployed: '2023-06-14 09:15:00',
      region: 'us-central1'
    },
    {
      id: 3,
      name: 'blog-cms-staging',
      status: 'pending',
      platform: 'Azure',
      url: 'https://blog-staging.example.com',
      lastDeployed: '2023-06-13 16:45:00',
      region: 'East US'
    }
  ]);
  
  const [projects, setProjects] = useState([
    { id: 1, name: 'Analytics Dashboard', createdAt: '2023-06-10' },
    { id: 2, name: 'E-commerce Store', createdAt: '2023-06-12' },
    { id: 3, name: 'Blog CMS', createdAt: '2023-06-14' }
  ]);
  
  const [selectedProject, setSelectedProject] = useState(1);
  const [isDeploying, setIsDeploying] = useState(false);
  const [formData, setFormData] = useState({
    projectName: '',
    platform: 'aws',
    region: 'us-west-2',
    environment: 'production',
    domain: '',
    ssl: true
  });

  const platforms = [
    {
      id: 'aws',
      name: 'Amazon Web Services',
      description: 'Deploy to AWS with auto-scaling and load balancing',
      icon: Cloud,
      features: ['Auto Scaling', 'Load Balancer', 'CloudFront CDN', 'S3 Storage']
    },
    {
      id: 'gcp',
      name: 'Google Cloud Platform',
      description: 'Deploy to Google Cloud with Kubernetes and Firebase',
      icon: Server,
      features: ['Kubernetes Engine', 'Firebase Integration', 'Cloud Storage', 'Cloud SQL']
    },
    {
      id: 'azure',
      name: 'Microsoft Azure',
      description: 'Deploy to Azure with App Service and SQL Database',
      icon: Globe,
      features: ['App Service', 'SQL Database', 'Azure CDN', 'Storage Accounts']
    }
  ];

  const handlePlatformSelect = (platform) => {
    setSelectedPlatform(platform);
    setFormData(prev => ({
      ...prev,
      platform: platform.id
    }));
  };

  const handleInputChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
  };

  const handleDeploy = async (e) => {
    e.preventDefault();
    if (!selectedPlatform) {
      alert('Please select a deployment platform');
      return;
    }
    
    setIsDeploying(true);
    
    try {
      // Simulate deployment process
      setTimeout(() => {
        const newDeployment = {
          id: Date.now(),
          name: `${formData.projectName}-${formData.environment}`,
          status: 'running',
          platform: selectedPlatform.name,
          url: `https://${formData.projectName.replace(/\s+/g, '-').toLowerCase()}.example.com`,
          lastDeployed: new Date().toISOString(),
          region: formData.region
        };
        
        setDeployments(prev => [newDeployment, ...prev]);
        setIsDeploying(false);
        alert('Deployment started successfully!');
      }, 3000);
    } catch (error) {
      console.error('Deployment error:', error);
      setIsDeploying(false);
      alert('Deployment failed. Please try again.');
    }
  };

  const handleViewDeployment = (deployment) => {
    window.open(deployment.url, '_blank');
  };

  const handleStopDeployment = (deploymentId) => {
    setDeployments(prev => 
      prev.map(deployment => 
        deployment.id === deploymentId 
          ? { ...deployment, status: 'failed' } 
          : deployment
      )
    );
  };

  const handleRestartDeployment = (deploymentId) => {
    setDeployments(prev => 
      prev.map(deployment => 
        deployment.id === deploymentId 
          ? { ...deployment, status: 'running' } 
          : deployment
      )
    );
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'success':
        return <CheckCircle size={16} />;
      case 'failed':
        return <AlertCircle size={16} />;
      case 'pending':
        return <Clock size={16} />;
      case 'running':
        return <LoadingSpinner rotate><RefreshCw size={16} /></LoadingSpinner>;
      default:
        return <Clock size={16} />;
    }
  };

  const getStatusText = (status) => {
    switch (status) {
      case 'success':
        return 'Deployed';
      case 'failed':
        return 'Failed';
      case 'pending':
        return 'Pending';
      case 'running':
        return 'Deploying';
      default:
        return 'Unknown';
    }
  };

  return (
    <Container>
      <Header>
        <Title>
          <Rocket size={32} style={{ verticalAlign: 'middle', marginRight: '10px' }} />
          Deploy Applications
        </Title>
        <Subtitle>
          Deploy your generated applications to the cloud with a single click
        </Subtitle>
      </Header>
      
      <ProjectSelector>
        <SelectorLabel>Select Project:</SelectorLabel>
        <Selector 
          value={selectedProject} 
          onChange={(e) => setSelectedProject(Number(e.target.value))}
        >
          {projects.map(project => (
            <option key={project.id} value={project.id}>
              {project.name}
            </option>
          ))}
        </Selector>
      </ProjectSelector>
      
      <PlatformGrid>
        {platforms.map(platform => (
          <PlatformCard
            key={platform.id}
            selected={selectedPlatform?.id === platform.id}
            onClick={() => handlePlatformSelect(platform)}
          >
            <PlatformHeader>
              <PlatformIcon>
                <platform.icon size={24} />
              </PlatformIcon>
              <PlatformInfo>
                <PlatformName>{platform.name}</PlatformName>
                <PlatformDescription>{platform.description}</PlatformDescription>
              </PlatformInfo>
            </PlatformHeader>
            
            <FeatureList>
              {platform.features.map((feature, index) => (
                <FeatureItem key={index}>
                  <CheckCircle size={14} color="#10b981" />
                  {feature}
                </FeatureItem>
              ))}
            </FeatureList>
          </PlatformCard>
        ))}
      </PlatformGrid>
      
      {selectedPlatform && (
        <FormSection>
          <SectionTitle>
            <Settings size={24} />
            Deployment Configuration
          </SectionTitle>
          
          <Form onSubmit={handleDeploy}>
            <FormGroup>
              <Label>Project Name</Label>
              <Input
                type="text"
                name="projectName"
                value={formData.projectName}
                onChange={handleInputChange}
                placeholder="Enter project name"
                required
              />
            </FormGroup>
            
            <FormGroup>
              <Label>Environment</Label>
              <Select
                name="environment"
                value={formData.environment}
                onChange={handleInputChange}
              >
                <option value="development">Development</option>
                <option value="staging">Staging</option>
                <option value="production">Production</option>
              </Select>
            </FormGroup>
            
            <FormGroup>
              <Label>Region</Label>
              <Select
                name="region"
                value={formData.region}
                onChange={handleInputChange}
              >
                {selectedPlatform.id === 'aws' && (
                  <>
                    <option value="us-west-2">US West (Oregon)</option>
                    <option value="us-east-1">US East (N. Virginia)</option>
                    <option value="eu-west-1">EU (Ireland)</option>
                  </>
                )}
                {selectedPlatform.id === 'gcp' && (
                  <>
                    <option value="us-central1">US Central (Iowa)</option>
                    <option value="us-west1">US West (Oregon)</option>
                    <option value="europe-west1">Europe West (Belgium)</option>
                  </>
                )}
                {selectedPlatform.id === 'azure' && (
                  <>
                    <option value="East US">East US</option>
                    <option value="West US">West US</option>
                    <option value="North Europe">North Europe</option>
                  </>
                )}
              </Select>
            </FormGroup>
            
            <FormGroup>
              <Label>Custom Domain (Optional)</Label>
              <Input
                type="text"
                name="domain"
                value={formData.domain}
                onChange={handleInputChange}
                placeholder="yourapp.example.com"
              />
            </FormGroup>
            
            <FormGroup fullWidth>
              <Label>
                <input
                  type="checkbox"
                  name="ssl"
                  checked={formData.ssl}
                  onChange={handleInputChange}
                /> Enable SSL Certificate
              </Label>
            </FormGroup>
            
            <FormGroup fullWidth>
              <SubmitButton type="submit" disabled={isDeploying}>
                {isDeploying ? (
                  <>
                    <LoadingSpinner rotate>
                      <RefreshCw size={16} />
                    </LoadingSpinner>
                    Deploying...
                  </>
                ) : (
                  <>
                    <Rocket size={16} />
                    Deploy to {selectedPlatform.name}
                  </>
                )}
              </SubmitButton>
            </FormGroup>
          </Form>
        </FormSection>
      )}
      
      <DeploymentSection>
        <SectionTitle>
          <Server size={24} />
          Recent Deployments
        </SectionTitle>
        
        <DeploymentList>
          {deployments.map(deployment => (
            <DeploymentItem key={deployment.id}>
              <DeploymentInfo>
                <StatusIcon className={deployment.status}>
                  {getStatusIcon(deployment.status)}
                </StatusIcon>
                <DeploymentDetails>
                  <DeploymentName>{deployment.name}</DeploymentName>
                  <DeploymentMeta>
                    <span>{deployment.platform}</span>
                    <span>{deployment.region}</span>
                    <span>{new Date(deployment.lastDeployed).toLocaleString()}</span>
                  </DeploymentMeta>
                </DeploymentDetails>
              </DeploymentInfo>
              
              <DeploymentActions>
                <StatusIndicator className={deployment.status}>
                  {getStatusText(deployment.status)}
                </StatusIndicator>
                <ActionButton 
                  onClick={() => handleViewDeployment(deployment)}
                  className={deployment.status === 'success' ? 'success' : ''}
                  disabled={deployment.status !== 'success'}
                >
                  <ExternalLink size={16} />
                  View
                </ActionButton>
                {deployment.status === 'running' && (
                  <ActionButton 
                    onClick={() => handleStopDeployment(deployment.id)}
                    className="danger"
                  >
                    <Square size={16} />
                    Stop
                  </ActionButton>
                )}
                {deployment.status === 'failed' && (
                  <ActionButton 
                    onClick={() => handleRestartDeployment(deployment.id)}
                    className="primary"
                  >
                    <RefreshCw size={16} />
                    Retry
                  </ActionButton>
                )}
              </DeploymentActions>
            </DeploymentItem>
          ))}
        </DeploymentList>
      </DeploymentSection>
    </Container>
  );
}

export default Deploy;