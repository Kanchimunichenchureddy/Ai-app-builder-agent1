import React from 'react';
import styled from 'styled-components';
import { Menu, User, Bell, Settings } from 'lucide-react';

const NavbarContainer = styled.nav`
  background: white;
  border-bottom: 1px solid #e2e8f0;
  padding: 1rem 1.5rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  position: sticky;
  top: 0;
  z-index: 100;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
`;

const LeftSection = styled.div`
  display: flex;
  align-items: center;
  gap: 1rem;
`;

const MenuButton = styled.button`
  background: none;
  border: none;
  padding: 0.5rem;
  border-radius: 0.5rem;
  cursor: pointer;
  color: #64748b;
  
  &:hover {
    background: #f1f5f9;
    color: #334155;
  }
  
  @media (min-width: 768px) {
    display: none;
  }
`;

const Title = styled.h1`
  font-size: 1.25rem;
  font-weight: 600;
  color: #1e293b;
`;

const RightSection = styled.div`
  display: flex;
  align-items: center;
  gap: 1rem;
`;

const IconButton = styled.button`
  background: none;
  border: none;
  padding: 0.5rem;
  border-radius: 0.5rem;
  cursor: pointer;
  color: #64748b;
  position: relative;
  
  &:hover {
    background: #f1f5f9;
    color: #334155;
  }
`;

const UserMenu = styled.div`
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.5rem;
  border-radius: 0.5rem;
  cursor: pointer;
  
  &:hover {
    background: #f1f5f9;
  }
`;

const UserAvatar = styled.div`
  width: 2rem;
  height: 2rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: 600;
  font-size: 0.875rem;
`;

const UserName = styled.span`
  font-weight: 500;
  color: #1e293b;
  display: none;
  
  @media (min-width: 640px) {
    display: block;
  }
`;

function Navbar({ onMenuClick }) {
  return (
    <NavbarContainer>
      <LeftSection>
        <MenuButton onClick={onMenuClick}>
          <Menu size={20} />
        </MenuButton>
        <Title>AI App Builder</Title>
      </LeftSection>
      
      <RightSection>
        <IconButton>
          <Bell size={20} />
        </IconButton>
        
        <IconButton>
          <Settings size={20} />
        </IconButton>
        
        <UserMenu>
          <UserAvatar>
            <User size={16} />
          </UserAvatar>
          <UserName>Demo User</UserName>
        </UserMenu>
      </RightSection>
    </NavbarContainer>
  );
}

export default Navbar;