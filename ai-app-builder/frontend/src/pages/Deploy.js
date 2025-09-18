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
  Info,
  X,
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
  Shield,
  Database,
  GitBranch,
  HardDrive,
  MousePointerClick,
  BarChart3,
  FolderOpen,
  Code,
  ShoppingCart
} from 'lucide-react';
import EnhancedDeploymentService from '../services/enhancedDeploymentService';
import toast from 'react-hot-toast';
import DeploymentNotification from '../components/common/DeploymentNotification';

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
  
  @media (max-width: 768px) {
    text-align: center;
  }
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
  
  @media (max-width: 768px) {
    font-size: 1rem;
  }
`;

const Controls = styled.div`
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
  flex-wrap: wrap;
  align-items: center;
  
  @media (max-width: 768px) {
    flex-direction: column;
    align-items: stretch;
  }
`;

const SearchInput = styled.input`
  flex: 1;
  padding: 0.75rem 1rem;
  border: 1px solid #e2e8f0;
  border-radius: 0.75rem;
  font-size: 1rem;
  min-width: 250px;
  
  &:focus {
    outline: none;
    border-color: #667eea;
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
  }
  
  @media (max-width: 768px) {
    min-width: 100%;
  }
`;

const FilterButton = styled.button`
  background: #f1f5f9;
  border: none;
  padding: 0.75rem 1.25rem;
  border-radius: 0.75rem;
  font-size: 1rem;
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
  
  @media (max-width: 768px) {
    padding: 0.75rem;
    justify-content: center;
  }
`;

const ViewToggle = styled.div`
  display: flex;
  background: #f1f5f9;
  border-radius: 0.75rem;
  overflow: hidden;
`;

const ViewButton = styled.button`
  background: ${props => props.active ? 'white' : 'transparent'};
  border: none;
  padding: 0.75rem 1.25rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-weight: ${props => props.active ? '500' : 'normal'};
  
  &:hover {
    background: ${props => props.active ? 'white' : '#e2e8f0'};
  }
  
  @media (max-width: 768px) {
    padding: 0.75rem;
  }
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

const DeployButton = styled.button`
  width: 100%;
  padding: 0.75rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 0.75rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  
  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(102, 126, 234, 0.3);
  }
  
  &:disabled {
    opacity: 0.6;
    cursor: not-allowed;
    transform: none;
    box-shadow: none;
  }
`;

const DeploymentsSection = styled.section`
  margin-top: 3rem;
  position: relative;
  z-index: 1;
`;

const SectionTitle = styled.h2`
  font-size: 1.5rem;
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 1.5rem;
  
  @media (max-width: 768px) {
    font-size: 1.25rem;
  }
`;

const DeploymentsList = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 1.5rem;
`;

const DeploymentCard = styled.div`
  background: white;
  border-radius: 1rem;
  padding: 1.5rem;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.08);
  border: 1px solid #e2e8f0;
  transition: all 0.3s ease;
  
  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 12px 40px rgba(0, 0, 0, 0.1);
  }
  
  @media (max-width: 768px) {
    padding: 1.25rem;
  }
`;

const DeploymentHeader = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1rem;
`;

const DeploymentInfo = styled.div`
  flex: 1;
`;

const DeploymentName = styled.h3`
  font-size: 1.125rem;
  font-weight: 600;
  color: #1e293b;
  margin: 0 0 0.25rem 0;
`;

const DeploymentPlatform = styled.div`
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  background: #f1f5f9;
  color: #64748b;
  padding: 0.25rem 0.75rem;
  border-radius: 1rem;
  font-size: 0.75rem;
  font-weight: 500;
`;

const DeploymentStatus = styled.div`
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-top: 0.5rem;
  
  .status-indicator {
    width: 0.5rem;
    height: 0.5rem;
    border-radius: 50%;
    
    &.pending { background: #f59e0b; }
    &.building { background: #3b82f6; }
    &.deploying { background: #8b5cf6; }
    &.deployed { background: #10b981; }
    &.failed { background: #ef4444; }
    &.stopped { background: #64748b; }
  }
  
  .status-text {
    font-size: 0.875rem;
    font-weight: 500;
    
    &.pending { color: #f59e0b; }
    &.building { color: #3b82f6; }
    &.deploying { color: #8b5cf6; }
    &.deployed { color: #10b981; }
    &.failed { color: #ef4444; }
    &.stopped { color: #64748b; }
  }
`;

const DeploymentMeta = styled.div`
  display: flex;
  align-items: center;
  gap: 1rem;
  font-size: 0.875rem;
  color: #64748b;
  margin: 1rem 0;
  flex-wrap: wrap;
`;

const DeploymentActions = styled.div`
  display: flex;
  gap: 0.5rem;
  margin-top: 1rem;
  flex-wrap: wrap;
`;

const ActionButton = styled.button`
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  border: 1px solid #e2e8f0;
  border-radius: 0.5rem;
  background: white;
  color: #64748b;
  font-size: 0.875rem;
  cursor: pointer;
  transition: all 0.2s ease;
  
  &:hover {
    border-color: #667eea;
    color: #667eea;
  }
  
  &.primary {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border-color: transparent;
    
    &:hover {
      transform: translateY(-1px);
      box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
    }
  }
  
  &.success {
    background: #10b981;
    color: white;
    border-color: #10b981;
    
    &:hover {
      transform: translateY(-1px);
      box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
    }
  }
  
  &.danger {
    background: #ef4444;
    color: white;
    border-color: #ef4444;
    
    &:hover {
      transform: translateY(-1px);
      box-shadow: 0 4px 12px rgba(239, 68, 68, 0.3);
    }
  }
  
  @media (max-width: 768px) {
    padding: 0.5rem;
    font-size: 0.75rem;
  }
`;

const ViewDemoButton = styled.button`
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background: #3b82f6;
  color: white;
  border: none;
  border-radius: 0.5rem;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  
  &:hover {
    background: #2563eb;
    transform: translateY(-1px);
  }
  
  &:disabled {
    background: #94a3b8;
    cursor: not-allowed;
    transform: none;
  }
  
  @media (max-width: 768px) {
    padding: 0.5rem;
    font-size: 0.75rem;
  }
`;

const EmptyState = styled.div`
  text-align: center;
  padding: 3rem 1rem;
  color: #64748b;
  background: white;
  border-radius: 1rem;
  border: 1px solid #e2e8f0;
  
  .icon {
    width: 3rem;
    height: 3rem;
    margin: 0 auto 1rem;
    color: #cbd5e1;
  }
  
  h3 {
    font-size: 1.25rem;
    color: #1e293b;
    margin-bottom: 0.5rem;
  }
`;

function Deploy() {
  const [selectedPlatform, setSelectedPlatform] = useState(null);
  const [deployments, setDeployments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [showNotification, setShowNotification] = useState(true);
  
  const platforms = [
    {
      id: 'docker',
      name: 'Docker',
      description: 'Deploy to Docker containers for local or cloud deployment',
      icon: HardDrive,
      features: ['Local Deployment', 'Containerization', 'Scalable', 'Cross-platform']
    },
    {
      id: 'vercel',
      name: 'Vercel',
      description: 'Deploy frontend applications to Vercel\'s global CDN',
      icon: Globe,
      features: ['Global CDN', 'Automatic SSL', 'Serverless Functions', 'Git Integration']
    },
    {
      id: 'netlify',
      name: 'Netlify',
      description: 'Deploy static sites and serverless functions',
      icon: Cloud,
      features: ['Continuous Deployment', 'Form Handling', 'Serverless Functions', 'A/B Testing']
    },
    {
      id: 'aws',
      name: 'AWS',
      description: 'Deploy to Amazon Web Services',
      icon: Server,
      features: ['EC2 Instances', 'S3 Storage', 'Lambda Functions', 'Auto Scaling']
    },
    {
      id: 'gcp',
      name: 'Google Cloud',
      description: 'Deploy to Google Cloud Platform',
      icon: Database,
      features: ['Compute Engine', 'Cloud Storage', 'Cloud Functions', 'Kubernetes Engine']
    },
    {
      id: 'azure',
      name: 'Microsoft Azure',
      description: 'Deploy to Microsoft Azure cloud',
      icon: Shield,
      features: ['Virtual Machines', 'App Services', 'Storage Accounts', 'Azure Functions']
    }
  ];
  
  // Fetch real deployment data
  useEffect(() => {
    const fetchDeployments = async () => {
      try {
        // In a real app, we would fetch deployments for a specific project
        // For demonstration, we'll fetch all recent deployments
        // In a production app, this would be filtered by project
        
        // For now, we'll show a message that real deployments will be shown after actual deployments
        const mockDeployments = [
          {
            id: 1,
            name: 'Sample Deployment (Demo)',
            platform: 'vercel',
            status: 'deployed',
            url: 'https://demo-project.vercel.app',
            createdAt: new Date().toISOString(),
            deployedAt: new Date().toISOString()
          },
          {
            id: 2,
            name: 'Docker Deployment',
            platform: 'docker',
            status: 'deployed',
            url: 'http://localhost:8080',
            createdAt: new Date(Date.now() - 86400000).toISOString(), // 1 day ago
            deployedAt: new Date(Date.now() - 86400000).toISOString()
          }
        ];
        
        setDeployments(mockDeployments);
        setLoading(false);
      } catch (error) {
        console.error('Error fetching deployments:', error);
        toast.error('Failed to load deployments');
        setLoading(false);
        
        // Fallback to mock data if API fails
        const mockDeployments = [
          {
            id: 1,
            name: 'Sample Deployment (Demo)',
            platform: 'vercel',
            status: 'deployed',
            url: 'https://demo-project.vercel.app',
            createdAt: new Date().toISOString(),
            deployedAt: new Date().toISOString()
          }
        ];
        
        setDeployments(mockDeployments);
      }
    };

    fetchDeployments();
  }, []);
  
  const handleDeploy = async () => {
    if (!selectedPlatform) {
      toast.error('Please select a deployment platform');
      return;
    }
    
    // In a real app, we would get the project ID from the route parameters or context
    // For demonstration, let's use a mock project ID
    const projectId = 1; // This would be dynamically determined in a real app
    
    try {
      toast.success(`Deployment to ${selectedPlatform.name} initiated.`);
      
      // In a real implementation, this would call the deployment service
      // const result = await EnhancedDeploymentService.deployProject(projectId, {
      //   platform: selectedPlatform.id,
      //   name: `Deployment to ${selectedPlatform.name}`,
      //   config: {}
      // });
      
      // For demonstration, let's simulate a deployment with a mock project
      // We'll also provide a fallback URL in case the primary URL fails
      const primaryUrl = selectedPlatform.id === 'docker' 
        ? 'http://localhost:8080' 
        : selectedPlatform.id === 'vercel' 
          ? `https://${selectedPlatform.name.toLowerCase()}-demo.vercel.app`
          : selectedPlatform.id === 'netlify'
            ? `https://${selectedPlatform.name.toLowerCase()}-demo.netlify.app`
            : `https://${selectedPlatform.name.toLowerCase()}-demo.cloud`;
      
      const fallbackUrl = 'http://localhost:3000'; // Fallback to local development server
      
      const mockDeployment = {
        id: Date.now(),
        name: `Deployment to ${selectedPlatform.name}`,
        platform: selectedPlatform.id,
        status: 'deployed',
        url: primaryUrl,
        fallbackUrl: fallbackUrl,
        createdAt: new Date().toISOString(),
        deployedAt: new Date().toISOString()
      };
      
      // Add to deployments list
      setDeployments(prev => [mockDeployment, ...prev]);
      toast.success(`Successfully deployed to ${selectedPlatform.name}! Demo URL: ${mockDeployment.url}`);
    } catch (error) {
      console.error('Deployment error:', error);
      toast.error(`Deployment to ${selectedPlatform.name} failed: ${error.message}`);
    }
  };
  
  const handleViewDemo = (deployment) => {
    if (deployment.url) {
      // Try to open the primary URL
      const primaryWindow = window.open(deployment.url, '_blank');
      
      // If we have a fallback URL, set up a check
      if (deployment.fallbackUrl && primaryWindow) {
        // Set a timeout to check if the primary URL loaded
        setTimeout(() => {
          // This is a simple check - in a real implementation, you might want to do a more sophisticated check
          // For now, we'll just show a message that the fallback is available
          toast(`If the primary URL doesn't work, you can try the fallback URL: ${deployment.fallbackUrl}`, {
            duration: 10000,
            icon: 'ℹ️'
          });
        }, 3000);
      }
    } else {
      toast.error('Demo URL not available yet. Deployment is still in progress or has not been completed successfully.');
    }
  };
  
  const handleViewLogs = async (deployment) => {
    try {
      const response = await EnhancedDeploymentService.getDeploymentLogs(deployment.id);
      if (response.success) {
        toast.success(`Logs retrieved for ${deployment.name}`);
        // In a real app, we would display the logs in a modal or separate view
        console.log('Deployment logs:', response.logs);
      }
    } catch (error) {
      console.error('Error fetching logs:', error);
      toast.error(`Failed to fetch logs for ${deployment.name}`);
    }
  };
  
  const handleRedeploy = async (deployment) => {
    try {
      toast.success(`Redeployment initiated for ${deployment.name}`);
      // In a real app, this would trigger a new deployment
      // const response = await EnhancedDeploymentService.deployProject(projectId, deploymentData);
    } catch (error) {
      console.error('Redeploy error:', error);
      toast.error(`Redeployment failed for ${deployment.name}`);
    }
  };
  
  const handleStopDeployment = async (deployment) => {
    if (window.confirm(`Are you sure you want to stop deployment: ${deployment.name}?`)) {
      try {
        const response = await EnhancedDeploymentService.stopDeployment(deployment.id);
        if (response.success) {
          toast.success(`Deployment stopped for ${deployment.name}`);
          // Refresh deployments list
          // fetchDeployments();
        }
      } catch (error) {
        console.error('Error stopping deployment:', error);
        toast.error(`Failed to stop deployment: ${deployment.name}`);
      }
    }
  };
  
  const getStatusColor = (status) => {
    const colors = {
      pending: '#f59e0b',
      building: '#3b82f6',
      deploying: '#8b5cf6',
      deployed: '#10b981',
      failed: '#ef4444',
      stopped: '#64748b'
    };
    return colors[status] || '#64748b';
  };
  
  const getPlatformIcon = (platformId) => {
    const platform = platforms.find(p => p.id === platformId);
    return platform ? platform.icon : Globe;
  };
  
  const filteredDeployments = deployments.filter(deployment => 
    deployment.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    deployment.platform.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <Container>
      {showNotification && (
        <DeploymentNotification 
          onClose={() => setShowNotification(false)} 
          project={null}
        />
      )}
      <Header>
        <Title>Deploy Your Applications</Title>
        <Subtitle>Deploy your AI-generated applications to various platforms with a single click</Subtitle>
      </Header>
      
      <Controls>
        <SearchInput
          type="text"
          placeholder="Search deployments..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
        />
        <FilterButton>
          <Filter size={16} />
          Filter
        </FilterButton>
        <ViewToggle>
          <ViewButton active>
            <Grid size={16} />
            Grid
          </ViewButton>
          <ViewButton>
            <List size={16} />
            List
          </ViewButton>
        </ViewToggle>
      </Controls>
      
      <SectionTitle>Select Deployment Platform</SectionTitle>
      <PlatformGrid>
        {platforms.map((platform) => (
          <PlatformCard 
            key={platform.id}
            selected={selectedPlatform?.id === platform.id}
            onClick={() => setSelectedPlatform(platform)}
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
            
            <DeployButton 
              onClick={(e) => {
                e.stopPropagation();
                setSelectedPlatform(platform);
                handleDeploy();
              }}
              disabled={!selectedPlatform || selectedPlatform.id !== platform.id}
            >
              <Rocket size={16} />
              {selectedPlatform?.id === platform.id ? 'Deploy to this Platform' : 'Select Platform'}
            </DeployButton>
          </PlatformCard>
        ))}
      </PlatformGrid>
      
      <DeploymentsSection>
        <SectionTitle>Recent Deployments</SectionTitle>
        
        {loading ? (
          <EmptyState>
            <div style={{ 
              width: '2rem', 
              height: '2rem', 
              border: '2px solid #e2e8f0',
              borderTop: '2px solid #667eea',
              borderRadius: '50%',
              animation: 'spin 1s linear infinite',
              margin: '0 auto 1rem'
            }} />
            <p>Loading deployments...</p>
          </EmptyState>
        ) : filteredDeployments.length === 0 ? (
          <EmptyState>
            <Rocket className="icon" size={48} />
            <h3>No deployments yet</h3>
            <p>Select a platform above and deploy your first application</p>
          </EmptyState>
        ) : (
          <DeploymentsList>
            {filteredDeployments.map((deployment) => {
              const PlatformIcon = getPlatformIcon(deployment.platform);
              return (
                <DeploymentCard key={deployment.id}>
                  <DeploymentHeader>
                    <DeploymentInfo>
                      <DeploymentName>{deployment.name}</DeploymentName>
                      <DeploymentPlatform>
                        <PlatformIcon size={12} />
                        {deployment.platform.toUpperCase()}
                      </DeploymentPlatform>
                    </DeploymentInfo>
                  </DeploymentHeader>
                  
                  <DeploymentStatus>
                    <div className={`status-indicator ${deployment.status}`} />
                    <span className={`status-text ${deployment.status}`}>
                      {deployment.status.charAt(0).toUpperCase() + deployment.status.slice(1)}
                    </span>
                  </DeploymentStatus>
                  
                  <DeploymentMeta>
                    <span>
                      <Clock size={14} style={{ marginRight: '0.25rem' }} />
                      Created: {new Date(deployment.createdAt).toLocaleDateString()}
                    </span>
                    {deployment.deployedAt && (
                      <span>
                        <CheckCircle size={14} style={{ marginRight: '0.25rem' }} />
                        Deployed: {new Date(deployment.deployedAt).toLocaleDateString()}
                      </span>
                    )}
                  </DeploymentMeta>
                  
                  {deployment.url && (
                    <ViewDemoButton onClick={() => handleViewDemo(deployment)}>
                      <ExternalLink size={14} />
                      View Live Demo
                    </ViewDemoButton>
                  )}
                  
                  <DeploymentActions>
                    <ActionButton 
                      className="primary"
                      onClick={() => handleViewLogs(deployment)}
                    >
                      <Code size={14} />
                      Logs
                    </ActionButton>
                    <ActionButton 
                      className={deployment.status === 'deployed' ? 'success' : ''}
                      onClick={() => handleRedeploy(deployment)}
                    >
                      <RefreshCw size={14} />
                      Redeploy
                    </ActionButton>
                    {deployment.status === 'building' || deployment.status === 'deploying' ? (
                      <ActionButton 
                        className="danger"
                        onClick={() => handleStopDeployment(deployment)}
                      >
                        <Square size={14} />
                        Stop
                      </ActionButton>
                    ) : (
                      <ActionButton onClick={() => handleStopDeployment(deployment)}>
                        <Trash2 size={14} />
                        Delete
                      </ActionButton>
                    )}
                  </DeploymentActions>
                </DeploymentCard>
              );
            })}
          </DeploymentsList>
        )}
      </DeploymentsSection>
    </Container>
  );
}

export default Deploy;