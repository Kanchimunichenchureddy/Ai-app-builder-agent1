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
  Copy
} from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import toast from 'react-hot-toast';

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
  justify-content: between;
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
  justify-content: between;
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
  }
  
  .status-text {
    font-size: 0.875rem;
    font-weight: 500;
    
    &.active { color: #10b981; }
    &.building { color: #f59e0b; }
    &.error { color: #ef4444; }
    &.deployed { color: #3b82f6; }
  }
`;

const ProjectMeta = styled.div`
  display: flex;
  align-items: center;
  gap: 1rem;
  font-size: 0.875rem;
  color: #64748b;
`;

const ProjectActions = styled.div`
  padding: 1rem 1.5rem;
  background: #f8fafc;
  display: flex;
  gap: 0.5rem;
`;

const ActionButton = styled.button`
  flex: 1;
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
  }
`;

function Projects() {
  const navigate = useNavigate();
  const [projects, setProjects] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterStatus, setFilterStatus] = useState('all');
  const [loading, setLoading] = useState(true);

  // Mock project data - in real app, this would come from API
  useEffect(() => {
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
        url: 'https://my-store.vercel.app'
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
      },
      {
        id: 3,
        name: 'Blog Platform',
        type: 'blog',
        description: 'Content management system with rich editor and SEO optimization.',
        status: 'building',
        createdAt: '2024-01-20',
        lastModified: '2024-01-22',
        features: ['React', 'FastAPI', 'MySQL']
      },
      {
        id: 4,
        name: 'Chat Application',
        type: 'chat',
        description: 'Real-time messaging platform with file sharing and group chats.',
        status: 'error',
        createdAt: '2024-01-19',
        lastModified: '2024-01-21',
        features: ['React', 'FastAPI', 'MySQL', 'WebSocket']
      }
    ];

    setTimeout(() => {
      setProjects(mockProjects);
      setLoading(false);
    }, 1000);
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

  const handleCreateProject = () => {
    navigate('/builder');
  };

  const handleViewProject = (project) => {
    toast.success(`Opening ${project.name}`);
  };

  const handleEditProject = (project) => {
    toast.success(`Editing ${project.name}`);
  };

  const handleDeployProject = (project) => {
    navigate('/deploy', { state: { project } });
  };

  const handleDeleteProject = (project) => {
    if (window.confirm(`Are you sure you want to delete ${project.name}?`)) {
      setProjects(prev => prev.filter(p => p.id !== project.id));
      toast.success(`${project.name} deleted`);
    }
  };

  const getProjectIcon = (type) => {
    const icons = {
      ecommerce: <Cloud size={20} />,
      blog: <Edit3 size={20} />,
      chat: <MessageCircle size={20} />,
      productivity: <CheckCircle size={20} />,
      dashboard: <BarChart3 size={20} />
    };
    return icons[type] || <Folder size={20} />;
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
              "You haven't created any projects yet"
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
                
                <ProjectMeta>
                  <span>
                    <Calendar size={14} style={{ marginRight: '0.25rem' }} />
                    {new Date(project.createdAt).toLocaleDateString()}
                  </span>
                  <span>
                    <Clock size={14} style={{ marginRight: '0.25rem' }} />
                    {new Date(project.lastModified).toLocaleDateString()}
                  </span>
                </ProjectMeta>
              </ProjectHeader>
              
              <ProjectActions>
                <ActionButton 
                  className="primary"
                  onClick={() => handleViewProject(project)}
                >
                  <Eye size={14} />
                  View
                </ActionButton>
                <ActionButton onClick={() => handleEditProject(project)}>
                  <Edit3 size={14} />
                  Edit
                </ActionButton>
                <ActionButton onClick={() => handleDeployProject(project)}>
                  <Play size={14} />
                  Deploy
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