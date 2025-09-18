import React, { useState, useEffect } from 'react';
import styled, { keyframes } from 'styled-components';
import { 
  Plus, 
  Search, 
  Filter, 
  MoreVertical, 
  Edit3, 
  Download, 
  Trash2, 
  Play, 
  Code, 
  Database, 
  Cloud, 
  Calendar,
  Clock,
  CheckCircle,
  AlertCircle,
  Folder,
  GitBranch,
  Settings,
  Eye,
  Copy,
  ExternalLink,
  Rocket,
  BarChart3,
  Globe,
  ShoppingCart,
  MessageSquare,
  X
} from 'lucide-react'; // Updated imports to fix caching issues
import { useNavigate } from 'react-router-dom';
import toast from 'react-hot-toast';
import ProjectsService from '../services/projectsService';
import EnhancedDeploymentService from '../services/enhancedDeploymentService';
import DeploymentNotification from '../components/common/DeploymentNotification';

const fadeIn = keyframes`
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
`;

const Container = styled.div`
  padding: 2rem;
  background: #f8fafc;
  min-height: 100vh;
`;

const Header = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  
  @media (max-width: 768px) {
    flex-direction: column;
    gap: 1rem;
    align-items: stretch;
  }
`;

const HeaderLeft = styled.div`
  flex: 1;
`;

const Title = styled.h1`
  font-size: 2.5rem;
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 0.5rem;
`;

const Subtitle = styled.p`
  color: #64748b;
  font-size: 1.125rem;
`;

const HeaderRight = styled.div`
  display: flex;
  gap: 1rem;
  align-items: center;
  
  @media (max-width: 768px) {
    flex-wrap: wrap;
  }
`;

const SearchBar = styled.div`
  position: relative;
  
  input {
    width: 300px;
    padding: 0.75rem 1rem 0.75rem 2.5rem;
    border: 1px solid #e2e8f0;
    border-radius: 0.75rem;
    font-size: 1rem;
    
    &:focus {
      outline: none;
      border-color: #667eea;
      box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    @media (max-width: 768px) {
      width: 100%;
    }
  }
  
  .search-icon {
    position: absolute;
    left: 0.75rem;
    top: 50%;
    transform: translateY(-50%);
    color: #64748b;
  }
`;

const FilterButton = styled.button`
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1rem;
  border: 1px solid #e2e8f0;
  border-radius: 0.75rem;
  background: white;
  color: #64748b;
  cursor: pointer;
  transition: all 0.2s ease;
  
  &:hover {
    border-color: #667eea;
    color: #667eea;
  }
  
  @media (max-width: 768px) {
    padding: 0.75rem;
  }
`;

const CreateButton = styled.button`
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 0.75rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  
  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(102, 126, 234, 0.3);
  }
  
  @media (max-width: 768px) {
    padding: 0.75rem 1rem;
    font-size: 0.9rem;
  }
`;

const StatsGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
`;

const StatCard = styled.div`
  background: white;
  border-radius: 1rem;
  padding: 1.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  border: 1px solid #e2e8f0;
  animation: ${fadeIn} 0.5s ease-out;
  
  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  }
`;

const StatNumber = styled.div`
  font-size: 2rem;
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 0.5rem;
`;

const StatLabel = styled.div`
  color: #64748b;
  font-size: 0.875rem;
`;

const ProjectsGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 1.5rem;
`;

const ProjectCard = styled.div`
  background: white;
  border-radius: 1rem;
  overflow: hidden;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  border: 1px solid #e2e8f0;
  transition: all 0.3s ease;
  animation: ${fadeIn} 0.5s ease-out;
  
  &:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
  }
`;

const ProjectHeader = styled.div`
  padding: 1.5rem;
  border-bottom: 1px solid #f1f5f9;
`;

const ProjectHeaderTop = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1rem;
`;

const ProjectIcon = styled.div`
  width: 3rem;
  height: 3rem;
  border-radius: 0.75rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  margin-right: 1rem;
`;

const ProjectInfo = styled.div`
  flex: 1;
`;

const ProjectName = styled.h3`
  font-size: 1.25rem;
  font-weight: 600;
  color: #1e293b;
  margin-bottom: 0.25rem;
`;

const ProjectType = styled.span`
  background: #f1f5f9;
  color: #64748b;
  padding: 0.25rem 0.5rem;
  border-radius: 0.375rem;
  font-size: 0.75rem;
  text-transform: uppercase;
  font-weight: 500;
`;

const ProjectMenu = styled.button`
  background: none;
  border: none;
  color: #64748b;
  cursor: pointer;
  padding: 0.25rem;
  border-radius: 0.375rem;
  
  &:hover {
    background: #f1f5f9;
  }
`;

const ProjectDescription = styled.p`
  color: #64748b;
  line-height: 1.5;
  margin-bottom: 1rem;
  min-height: 3rem;
`;

const ProjectStatus = styled.div`
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 1rem;
  
  .status-indicator {
    width: 0.5rem;
    height: 0.5rem;
    border-radius: 50%;
    
    &.active { background: #10b981; }
    &.building { background: #f59e0b; }
    &.error { background: #ef4444; }
    &.deployed { background: #3b82f6; }
    &.creating { background: #8b5cf6; }
  }
  
  .status-text {
    font-size: 0.875rem;
    font-weight: 500;
    
    &.active { color: #10b981; }
    &.building { color: #f59e0b; }
    &.error { color: #ef4444; }
    &.deployed { color: #3b82f6; }
    &.creating { color: #8b5cf6; }
  }
`;

const ProjectMeta = styled.div`
  display: flex;
  align-items: center;
  gap: 1rem;
  font-size: 0.875rem;
  color: #64748b;
  margin-bottom: 1rem;
  flex-wrap: wrap;
`;

const ProjectFeatures = styled.div`
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-bottom: 1rem;
`;

const FeatureTag = styled.span`
  background: #e0f2fe;
  color: #0369a1;
  padding: 0.25rem 0.5rem;
  border-radius: 0.375rem;
  font-size: 0.75rem;
  font-weight: 500;
`;

const ProjectActions = styled.div`
  padding: 1rem 1.5rem;
  background: #f8fafc;
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 0.5rem;
  
  @media (max-width: 768px) {
    grid-template-columns: repeat(2, 1fr);
  }
`;

const ActionButton = styled.button`
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.5rem;
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
  
  &.warning {
    background: #f59e0b;
    color: white;
    border-color: #f59e0b;
    
    &:hover {
      transform: translateY(-1px);
      box-shadow: 0 4px 12px rgba(245, 158, 11, 0.3);
    }
  }
`;

const EmptyState = styled.div`
  text-align: center;
  padding: 4rem 2rem;
  color: #64748b;
  
  .icon {
    width: 4rem;
    height: 4rem;
    margin: 0 auto 1rem;
    color: #cbd5e1;
  }
  
  h3 {
    font-size: 1.25rem;
    color: #1e293b;
    margin-bottom: 0.5rem;
  }
  
  p {
    margin-bottom: 2rem;
    max-width: 500px;
    margin-left: auto;
    margin-right: auto;
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
`;

function Projects() {
  const navigate = useNavigate();
  const [projects, setProjects] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterStatus, setFilterStatus] = useState('all');
  const [loading, setLoading] = useState(true);
  const [showNotification, setShowNotification] = useState(true);

  // Fetch real project data from API
  useEffect(() => {
    const fetchProjects = async () => {
      try {
        setLoading(true);
        const response = await ProjectsService.getProjects();
        
        // Transform projects to match expected format
        const transformedProjects = response.projects.map(project => ({
          id: project.id,
          name: project.name,
          type: project.type || project.project_type || 'dashboard',
          description: project.description,
          status: project.status || 'active',
          createdAt: project.created_at,
          lastModified: project.updated_at || project.created_at,
          features: project.features || [],
          // We'll fetch the deployment URL separately
          url: null
        }));
        
        // Fetch deployment URLs for deployed projects
        const projectsWithUrls = await Promise.all(
          transformedProjects.map(async (project) => {
            try {
              // Get deployments for this project
              const deploymentResponse = await EnhancedDeploymentService.getProjectDeployments(project.id);
              
              // Find the most recent deployed deployment
              const deployedDeployments = deploymentResponse.deployments.filter(d => d.status === 'deployed');
              if (deployedDeployments.length > 0) {
                // Sort by created date to get the most recent
                deployedDeployments.sort((a, b) => new Date(b.created_at) - new Date(a.created_at));
                project.url = deployedDeployments[0].url;
              }
              
              return project;
            } catch (error) {
              console.warn(`Failed to fetch deployments for project ${project.id}:`, error);
              return project;
            }
          })
        );
        
        setProjects(projectsWithUrls);
        setLoading(false);
      } catch (error) {
        console.error('Error fetching projects:', error);
        toast.error('Failed to load projects');
        setLoading(false);
        
        // Fallback to mock data if API fails
        const mockProjects = [
          {
            id: 1,
            name: 'E-commerce Dashboard',
            type: 'ecommerce',
            description: 'Complete online store with product management, orders, and analytics dashboard.',
            status: 'deployed',
            createdAt: '2024-01-15',
            lastModified: '2024-01-20',
            features: ['React', 'FastAPI', 'MySQL', 'Stripe'],
            url: null
          },
          {
            id: 2,
            name: 'Task Manager Pro',
            type: 'productivity',
            description: 'Team collaboration platform with real-time updates and project tracking.',
            status: 'active',
            createdAt: '2024-01-18',
            lastModified: '2024-01-22',
            features: ['React', 'FastAPI', 'MySQL', 'WebSocket']
          }
        ];
        
        setProjects(mockProjects);
      }
    };

    fetchProjects();
  }, []);

  const filteredProjects = projects.filter(project => {
    const matchesSearch = project.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         project.description.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesFilter = filterStatus === 'all' || project.status === filterStatus;
    return matchesSearch && matchesFilter;
  });

  const projectStats = {
    total: projects.length,
    active: projects.filter(p => p.status === 'active').length,
    deployed: projects.filter(p => p.status === 'deployed').length,
    building: projects.filter(p => p.status === 'building').length
  };

  // Update project stats with real data when available
  useEffect(() => {
    const fetchProjectStats = async () => {
      try {
        const response = await ProjectsService.getProjectStats();
        // We'll keep using the local calculation for now since it's working
      } catch (error) {
        console.warn('Failed to fetch project stats:', error);
      }
    };

    if (projects.length > 0) {
      fetchProjectStats();
    }
  }, [projects]);

  const handleCreateProject = () => {
    navigate('/builder');
  };

  const handleViewProject = (project) => {
    toast.success(`Opening ${project.name}`);
    // In a real app, this would navigate to the project details page
  };

  const handleEditProject = (project) => {
    toast.success(`Editing ${project.name}`);
    // In a real app, this would navigate to the project editor
  };

  const handleDeployProject = (project) => {
    navigate('/deploy', { state: { projectId: project.id } });
  };

  const handleDeleteProject = async (project) => {
    if (window.confirm(`Are you sure you want to delete ${project.name}?`)) {
      try {
        await ProjectsService.deleteProject(project.id);
        setProjects(prev => prev.filter(p => p.id !== project.id));
        toast.success(`${project.name} deleted successfully`);
      } catch (error) {
        console.error('Error deleting project:', error);
        toast.error(`Failed to delete ${project.name}`);
      }
    }
  };

  const handleViewCode = (project) => {
    toast.success(`Viewing code for ${project.name}`);
    // In a real app, this would open the code viewer
  };

  const handleViewDemo = (project) => {
    if (project.url) {
      window.open(project.url, '_blank');
    } else {
      toast.error('Demo URL not available for this project. Please deploy the project first to generate a live demo URL.');
      // Navigate to deploy page to encourage user to deploy
      navigate('/deploy', { state: { projectId: project.id } });
    }
  };

  const getProjectIcon = (type) => {
    // Using a switch statement to ensure all icons are properly referenced
    switch (type) {
      case 'ecommerce':
        return <ShoppingCart size={20} />;
      case 'blog':
        return <Edit3 size={20} />;
      case 'chat':
        return <MessageSquare size={20} />;
      case 'productivity':
        return <CheckCircle size={20} />;
      case 'dashboard':
        return <BarChart3 size={20} />;
      default:
        return <Folder size={20} />;
    }
  };

  const getStatusColor = (status) => {
    const colors = {
      active: '#10b981',
      building: '#f59e0b',
      error: '#ef4444',
      deployed: '#3b82f6',
      creating: '#8b5cf6'
    };
    return colors[status] || '#64748b';
  };

  if (loading) {
    return (
      <Container>
        <div style={{ textAlign: 'center', padding: '4rem' }}>
          <div style={{ 
            width: '3rem', 
            height: '3rem', 
            border: '3px solid #e2e8f0',
            borderTop: '3px solid #667eea',
            borderRadius: '50%',
            animation: 'spin 1s linear infinite',
            margin: '0 auto 1rem'
          }} />
          <p>Loading your projects...</p>
        </div>
      </Container>
    );
  }

  return (
    <Container>
      {showNotification && (
        <DeploymentNotification 
          onClose={() => setShowNotification(false)} 
          project={null}
        />
      )}
      <Header>
        <HeaderLeft>
          <Title>My Projects</Title>
          <Subtitle>Manage and deploy your AI-generated applications</Subtitle>
        </HeaderLeft>
        
        <HeaderRight>
          <SearchBar>
            <Search className="search-icon" size={20} />
            <input
              type="text"
              placeholder="Search projects..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
          </SearchBar>
          
          <FilterButton onClick={() => setFilterStatus(filterStatus === 'all' ? 'active' : 'all')}>
            <Filter size={16} />
            Filter
          </FilterButton>
          
          <CreateButton onClick={handleCreateProject}>
            <Plus size={16} />
            New Project
          </CreateButton>
        </HeaderRight>
      </Header>

      <StatsGrid>
        <StatCard>
          <StatNumber>{projectStats.total}</StatNumber>
          <StatLabel>Total Projects</StatLabel>
        </StatCard>
        <StatCard>
          <StatNumber>{projectStats.active}</StatNumber>
          <StatLabel>Active Projects</StatLabel>
        </StatCard>
        <StatCard>
          <StatNumber>{projectStats.deployed}</StatNumber>
          <StatLabel>Deployed</StatLabel>
        </StatCard>
        <StatCard>
          <StatNumber>{projectStats.building}</StatNumber>
          <StatLabel>Building</StatLabel>
        </StatCard>
      </StatsGrid>

      {filteredProjects.length === 0 ? (
        <EmptyState>
          <Folder className="icon" size={64} />
          <h3>No projects found</h3>
          <p>
            {searchTerm ? 
              `No projects match "${searchTerm}"` : 
              "You haven't created any projects yet. Start building your first AI-powered application today!"
            }
          </p>
          <CreateButton onClick={handleCreateProject}>
            <Plus size={16} />
            Create Your First Project
          </CreateButton>
        </EmptyState>
      ) : (
        <ProjectsGrid>
          {filteredProjects.map((project) => (
            <ProjectCard key={project.id}>
              <ProjectHeader>
                <ProjectHeaderTop>
                  <div style={{ display: 'flex', alignItems: 'flex-start' }}>
                    <ProjectIcon>
                      {getProjectIcon(project.type)}
                    </ProjectIcon>
                    <ProjectInfo>
                      <ProjectName>{project.name}</ProjectName>
                      <ProjectType>{project.type}</ProjectType>
                    </ProjectInfo>
                  </div>
                  <ProjectMenu>
                    <MoreVertical size={16} />
                  </ProjectMenu>
                </ProjectHeaderTop>
                
                <ProjectDescription>{project.description}</ProjectDescription>
                
                <ProjectStatus>
                  <div className={`status-indicator ${project.status}`} />
                  <span className={`status-text ${project.status}`}>
                    {project.status.charAt(0).toUpperCase() + project.status.slice(1)}
                  </span>
                </ProjectStatus>
                
                <ProjectFeatures>
                  {project.features && project.features.map((feature, index) => (
                    <FeatureTag key={index}>{feature}</FeatureTag>
                  ))}
                </ProjectFeatures>
                
                <ProjectMeta>
                  <span>
                    <Calendar size={14} style={{ marginRight: '0.25rem' }} />
                    Created: {new Date(project.createdAt).toLocaleDateString()}
                  </span>
                  <span>
                    <Clock size={14} style={{ marginRight: '0.25rem' }} />
                    Modified: {new Date(project.lastModified).toLocaleDateString()}
                  </span>
                </ProjectMeta>
                
                {project.url && (
                  <ViewDemoButton onClick={() => handleViewDemo(project)}>
                    <ExternalLink size={14} />
                    View Demo
                  </ViewDemoButton>
                )}
              </ProjectHeader>
              
              <ProjectActions>
                <ActionButton 
                  className="primary"
                  onClick={() => handleViewProject(project)}
                >
                  <Eye size={14} />
                  View
                </ActionButton>
                <ActionButton onClick={() => handleViewCode(project)}>
                  <Code size={14} />
                  Code
                </ActionButton>
                <ActionButton 
                  className={project.status === 'deployed' ? 'success' : 'warning'}
                  onClick={() => handleDeployProject(project)}
                >
                  <Rocket size={14} />
                  {project.status === 'deployed' ? 'Re-deploy' : 'Deploy'}
                </ActionButton>
                <ActionButton onClick={() => handleDeleteProject(project)}>
                  <Trash2 size={14} />
                  Delete
                </ActionButton>
              </ProjectActions>
            </ProjectCard>
          ))}
        </ProjectsGrid>
      )}
    </Container>
  );
}

export default Projects;