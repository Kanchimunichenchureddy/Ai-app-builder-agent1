import React from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import styled from 'styled-components';
import { 
  Home, 
  Wrench, 
  BarChart3, 
  Rocket, 
  FolderOpen, 
  Settings,
  LogOut,
  Bot,
  MessageCircle,
  Plug
} from 'lucide-react';
import { useAuth } from '../../services/auth';

const SidebarContainer = styled.aside`
  width: 250px;
  background: #1e293b;
  color: white;
  height: 100vh;
  position: fixed;
  left: 0;
  top: 0;
  transform: translateX(${props => props.isOpen ? '0' : '-100%'});
  transition: transform 0.3s ease;
  z-index: 200;
  
  @media (min-width: 768px) {
    position: relative;
    transform: translateX(0);
    display: ${props => props.isOpen ? 'block' : 'none'};
  }
`;

const SidebarHeader = styled.div`
  padding: 1.5rem;
  border-bottom: 1px solid #334155;
  display: flex;
  align-items: center;
  gap: 0.75rem;
`;

const Logo = styled.div`
  width: 2.5rem;
  height: 2.5rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 0.75rem;
  display: flex;
  align-items: center;
  justify-content: center;
`;

const LogoText = styled.div`
  h1 {
    font-size: 1.125rem;
    font-weight: 700;
    margin: 0;
  }
  
  p {
    font-size: 0.75rem;
    opacity: 0.7;
    margin: 0;
  }
`;

const Navigation = styled.nav`
  padding: 1rem 0;
  flex: 1;
`;

const NavSection = styled.div`
  margin-bottom: 2rem;
`;

const SectionTitle = styled.h3`
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  opacity: 0.7;
  margin: 0 1.5rem 1rem;
`;

const NavList = styled.ul`
  list-style: none;
  margin: 0;
  padding: 0;
`;

const NavItem = styled.li`
  margin: 0;
`;

const NavLink = styled(Link)`
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 1.5rem;
  color: white;
  text-decoration: none;
  transition: all 0.2s ease;
  
  ${props => props.$isActive && `
    background: rgba(102, 126, 234, 0.2);
    border-right: 3px solid #667eea;
  `}
  
  &:hover {
    background: rgba(255, 255, 255, 0.1);
  }
`;

const NavIcon = styled.span`
  display: flex;
  align-items: center;
  justify-content: center;
  width: 1.25rem;
  height: 1.25rem;
`;

const NavText = styled.span`
  font-weight: 500;
`;

const SidebarFooter = styled.div`
  padding: 1.5rem;
  border-top: 1px solid #334155;
`;

const LogoutButton = styled.button`
  display: flex;
  align-items: center;
  gap: 0.75rem;
  width: 100%;
  padding: 0.75rem;
  background: none;
  border: none;
  color: white;
  cursor: pointer;
  border-radius: 0.5rem;
  transition: background 0.2s ease;
  
  &:hover {
    background: rgba(239, 68, 68, 0.2);
  }
`;

function Sidebar({ isOpen, onToggle }) {
  const location = useLocation();
  const navigate = useNavigate();
  const { logout } = useAuth();
  
  const mainNavItems = [
    { path: '/', label: 'Home', icon: Home },
    { path: '/builder', label: 'AI Builder', icon: Wrench },
    { path: '/dashboard', label: 'Dashboard', icon: BarChart3 },
    { path: '/deploy', label: 'Deploy', icon: Rocket },
    { path: '/ai-chat', label: 'AI Chat', icon: MessageCircle },
    { path: '/integrations', label: 'Integrations', icon: Plug },
  ];
  
  const projectNavItems = [
    { path: '/projects', label: 'My Projects', icon: FolderOpen },
    { path: '/settings', label: 'Settings', icon: Settings },
  ];
  
  const handleLogout = () => {
    logout();
    navigate('/login'); // Use React Router navigation for better state sync
  };
  
  return (
    <SidebarContainer isOpen={isOpen}>
      <SidebarHeader>
        <Logo>
          <Bot size={20} />
        </Logo>
        <LogoText>
          <h1>AI Builder</h1>
          <p>Unlimited Apps</p>
        </LogoText>
      </SidebarHeader>
      
      <Navigation>
        <NavSection>
          <SectionTitle>Main</SectionTitle>
          <NavList>
            {mainNavItems.map((item) => (
              <NavItem key={item.path}>
                <NavLink 
                  to={item.path} 
                  $isActive={location.pathname === item.path}
                >
                  <NavIcon>
                    <item.icon size={16} />
                  </NavIcon>
                  <NavText>{item.label}</NavText>
                </NavLink>
              </NavItem>
            ))}
          </NavList>
        </NavSection>
        
        <NavSection>
          <SectionTitle>Projects</SectionTitle>
          <NavList>
            {projectNavItems.map((item) => (
              <NavItem key={item.path}>
                <NavLink 
                  to={item.path} 
                  $isActive={location.pathname === item.path}
                >
                  <NavIcon>
                    <item.icon size={16} />
                  </NavIcon>
                  <NavText>{item.label}</NavText>
                </NavLink>
              </NavItem>
            ))}
          </NavList>
        </NavSection>
      </Navigation>
      
      <SidebarFooter>
        <LogoutButton onClick={handleLogout}>
          <LogOut size={16} />
          Logout
        </LogoutButton>
      </SidebarFooter>
    </SidebarContainer>
  );
}

export default Sidebar;