import React from 'react';
import styled from 'styled-components';
import { Info, ExternalLink, Rocket } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

const NotificationContainer = styled.div`
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 1rem;
  border-radius: 0.75rem;
  margin: 1rem 0;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
`;

const NotificationHeader = styled.div`
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 0.5rem;
`;

const NotificationTitle = styled.h3`
  margin: 0;
  font-size: 1.1rem;
  font-weight: 600;
`;

const NotificationContent = styled.p`
  margin: 0.5rem 0;
  font-size: 0.95rem;
  line-height: 1.5;
`;

const NotificationActions = styled.div`
  display: flex;
  gap: 0.75rem;
  margin-top: 1rem;
  flex-wrap: wrap;
`;

const ActionButton = styled.button`
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background: rgba(255, 255, 255, 0.2);
  color: white;
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 0.5rem;
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 0.9rem;
  
  &:hover {
    background: rgba(255, 255, 255, 0.3);
    transform: translateY(-1px);
  }
`;

const CloseButton = styled.button`
  background: none;
  border: none;
  color: rgba(255, 255, 255, 0.7);
  cursor: pointer;
  padding: 0.25rem;
  margin-left: auto;
  font-size: 1.2rem;
  
  &:hover {
    color: white;
  }
`;

const NotificationHeaderContainer = styled.div`
  display: flex;
  align-items: center;
`;

function DeploymentNotification({ onClose, project }) {
  const navigate = useNavigate();

  const handleDeploy = () => {
    if (project) {
      navigate('/deploy', { state: { projectId: project.id } });
    } else {
      navigate('/deploy');
    }
  };

  const handleViewGuide = () => {
    // In a real app, this would open the deployment guide
    alert('Deployment guide would open here. Please refer to the DEPLOYMENT_GUIDE.md file for detailed instructions.');
  };

  return (
    <NotificationContainer>
      <NotificationHeaderContainer>
        <NotificationHeader>
          <Info size={20} />
          <NotificationTitle>Deployment Information</NotificationTitle>
        </NotificationHeader>
        <CloseButton onClick={onClose}>×</CloseButton>
      </NotificationHeaderContainer>
      
      <NotificationContent>
        The demo URLs shown are examples. To view your actual application, you need to deploy it first.
        After deployment, a real URL will be generated that you can use to view your live application.
      </NotificationContent>
      
      <NotificationActions>
        <ActionButton onClick={handleDeploy}>
          <Rocket size={16} />
          Deploy Project
        </ActionButton>
        <ActionButton onClick={handleViewGuide}>
          <ExternalLink size={16} />
          View Deployment Guide
        </ActionButton>
      </NotificationActions>
    </NotificationContainer>
  );
}

export default DeploymentNotification;