import React, { useState, useEffect } from 'react';
import styled, { keyframes } from 'styled-components';
import { 
  BarChart3, 
  Users, 
  Code, 
  Database, 
  Cloud, 
  Rocket, 
  AlertCircle, 
  CheckCircle, 
  Clock, 
  Zap,
  TrendingUp,
  DollarSign,
  GitBranch,
  Server,
  HardDrive,
  MessageSquare,
  // Adding more icons for enhanced UI
  Plus,
  Eye,
  EyeOff,
  Trash2,
  Copy,
  Share2,
  Heart,
  ThumbsUp,
  ThumbsDown,
  Search,
  Filter,
  Grid,
  List,
  ExternalLink,
  Play,
  Square,
  RefreshCw,
  Settings,
  Edit3,
  Image,
  Monitor,
  Smartphone,
  Tablet,
  Globe,
  Download,
  Link,
  X,
  Star,
  // Additional icons for AI Studio-like experience
  FileCode,
  FileText as FileDocument,
  ImageIcon,
  Video,
  Music,
  Calendar,
  MapPin,
  Mail,
  Phone,
  Link as LinkIcon
} from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import AIDashboard from '../components/dashboard/AIDashboard';

// Consistent color palette and styling across all components
const theme = {
  primaryGradient: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
  secondaryGradient: 'linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%)',
  successGradient: 'linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%)',
  cardBackground: 'white',
  borderColor: '#e2e8f0',
  boxShadow: '0 4px 15px rgba(0, 0, 0, 0.05)',
  borderRadius: '1rem',
  textColor: '#1e293b',
  secondaryTextColor: '#64748b'
};

// Enhanced animations
const pulse = keyframes`
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
`;

const fadeIn = keyframes`
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
`;

const float = keyframes`
  0%, 100% { transform: translateY(0px); }
  50% { transform: translateY(-5px); }
`;

const shimmer = keyframes`
  0% { background-position: -200% 0; }
  100% { background-position: 200% 0; }
`;

// Additional animations for smoother experience
const scaleIn = keyframes`
  from { opacity: 0; transform: scale(0.95); }
  to { opacity: 1; transform: scale(1); }
`;

const slideInUp = keyframes`
  from { opacity: 0; transform: translateY(30px); }
  to { opacity: 1; transform: translateY(0); }
`;

const slideInLeft = keyframes`
  from { opacity: 0; transform: translateX(-20px); }
  to { opacity: 1; transform: translateX(0); }
`;

const slideInRight = keyframes`
  from { opacity: 0; transform: translateX(20px); }
  to { opacity: 1; transform: translateX(0); }
`;

// Container with responsive design
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
  
  @media (max-width: 768px) {
    padding: 1rem;
  }
  
  @media (max-width: 480px) {
    padding: 0.5rem;
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
  color: ${theme.textColor};
  margin-bottom: 0.5rem;
  
  @media (max-width: 768px) {
    font-size: 1.75rem;
  }
  
  @media (max-width: 480px) {
    font-size: 1.5rem;
  }
`;

const Subtitle = styled.p`
  color: ${theme.secondaryTextColor};
  font-size: 1.1rem;
  
  @media (max-width: 480px) {
    font-size: 0.9rem;
  }
`;

const StatsGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
  position: relative;
  z-index: 1;
  
  @media (max-width: 768px) {
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 1rem;
  }
  
  @media (max-width: 480px) {
    grid-template-columns: 1fr;
  }
`;

const StatCard = styled.div`
  background: ${theme.cardBackground};
  border-radius: ${theme.borderRadius};
  padding: 1.5rem;
  box-shadow: ${theme.boxShadow};
  border: 1px solid ${theme.borderColor};
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
  animation: ${fadeIn} 0.5s ease-out;
  
  &:hover {
    transform: translateY(-5px);
    box-shadow: 0 12px 40px rgba(0, 0, 0, 0.12);
  }
  
  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 4px;
    background: ${theme.primaryGradient};
  }
  
  @media (max-width: 768px) {
    padding: 1.25rem;
  }
  
  @media (max-width: 480px) {
    padding: 1rem;
  }
`;

const StatHeader = styled.div`
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1rem;
`;

const StatIcon = styled.div`
  width: 3.5rem;
  height: 3.5rem;
  border-radius: 1rem;
  background: ${theme.primaryGradient};
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  animation: ${float} 3s ease-in-out infinite;
`;

const StatTitle = styled.h3`
  font-size: 1rem;
  font-weight: 500;
  color: ${theme.secondaryTextColor};
  margin: 0;
`;

const StatValue = styled.div`
  font-size: 2rem;
  font-weight: 700;
  color: ${theme.textColor};
  margin-bottom: 0.5rem;
  
  @media (max-width: 480px) {
    font-size: 1.75rem;
  }
`;

const StatChange = styled.div`
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.9rem;
  font-weight: 500;
  
  &.positive {
    color: #10b981;
  }
  
  &.negative {
    color: #ef4444;
  }
  
  @media (max-width: 480px) {
    font-size: 0.8rem;
  }
`;

const Section = styled.div`
  background: ${theme.cardBackground};
  border-radius: ${theme.borderRadius};
  padding: 2rem;
  box-shadow: ${theme.boxShadow};
  border: 1px solid ${theme.borderColor};
  margin-bottom: 2rem;
  animation: ${fadeIn} 0.5s ease-out;
  position: relative;
  z-index: 1;
  
  @media (max-width: 768px) {
    padding: 1.5rem;
  }
  
  @media (max-width: 480px) {
    padding: 1rem;
  }
`;

const SectionHeader = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  
  @media (max-width: 768px) {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }
  
  @media (max-width: 480px) {
    margin-bottom: 1rem;
  }
`;

const SectionTitle = styled.h2`
  font-size: 1.5rem;
  font-weight: 600;
  color: ${theme.textColor};
  margin: 0;
  
  @media (max-width: 768px) {
    font-size: 1.25rem;
  }
  
  @media (max-width: 480px) {
    font-size: 1.1rem;
  }
`;

const ViewAllButton = styled.button`
  background: #f1f5f9;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 0.5rem;
  font-size: 0.9rem;
  font-weight: 500;
  cursor: pointer;
  color: ${theme.textColor};
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  
  &:hover {
    background: #e2e8f0;
  }
  
  @media (max-width: 768px) {
    align-self: flex-end;
  }
  
  @media (max-width: 480px) {
    padding: 0.4rem 0.8rem;
    font-size: 0.8rem;
  }
`;

const Controls = styled.div`
  display: flex;
  gap: 1rem;
  align-items: center;
  
  @media (max-width: 768px) {
    width: 100%;
    justify-content: space-between;
  }
  
  @media (max-width: 480px) {
    flex-direction: column;
    align-items: stretch;
    gap: 0.5rem;
  }
`;

const SearchInput = styled.input`
  padding: 0.5rem 1rem;
  border: 1px solid ${theme.borderColor};
  border-radius: 0.5rem;
  font-size: 0.9rem;
  
  &:focus {
    outline: none;
    border-color: #667eea;
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
  }
  
  @media (max-width: 768px) {
    flex: 1;
  }
  
  @media (max-width: 480px) {
    padding: 0.4rem 0.8rem;
    font-size: 0.85rem;
  }
`;

const FilterButton = styled.button`
  background: #f1f5f9;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 0.5rem;
  font-size: 0.9rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  
  &:hover {
    background: #e2e8f0;
  }
  
  @media (max-width: 480px) {
    padding: 0.4rem 0.8rem;
    font-size: 0.85rem;
  }
`;

const ViewToggle = styled.div`
  display: flex;
  background: #f1f5f9;
  border-radius: 0.5rem;
  overflow: hidden;
`;

const ViewButton = styled.button`
  background: ${props => props.active ? 'white' : 'transparent'};
  border: none;
  padding: 0.5rem 1rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-weight: ${props => props.active ? '500' : 'normal'};
  
  &:hover {
    background: ${props => props.active ? 'white' : '#e2e8f0'};
  }
  
  @media (max-width: 480px) {
    padding: 0.4rem 0.8rem;
    font-size: 0.85rem;
  }
`;

const ProjectList = styled.div`
  display: flex;
  flex-direction: column;
  gap: 1rem;
`;

const ProjectGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 1.5rem;
  margin-top: 1rem;
  
  @media (max-width: 768px) {
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 1rem;
  }
  
  @media (max-width: 480px) {
    grid-template-columns: 1fr;
  }
`;

const ProjectCard = styled.div`
  background: ${theme.cardBackground};
  border-radius: ${theme.borderRadius};
  padding: 1.5rem;
  box-shadow: ${theme.boxShadow};
  border: 1px solid ${theme.borderColor};
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
  animation: ${slideInUp} 0.5s ease-out;
  
  &:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 25px rgba(102, 126, 234, 0.15);
    border-color: #667eea;
  }
  
  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 4px;
    background: ${theme.primaryGradient};
  }
  
  @media (max-width: 480px) {
    padding: 1.25rem;
  }
`;

const ProjectHeader = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1rem;
`;

const ProjectTitle = styled.h3`
  font-size: 1.25rem;
  font-weight: 600;
  color: ${theme.textColor};
  margin: 0;
  
  @media (max-width: 480px) {
    font-size: 1.1rem;
  }
`;

const ProjectFramework = styled.div`
  background: #f1f5f9;
  color: ${theme.secondaryTextColor};
  padding: 0.25rem 0.75rem;
  border-radius: 2rem;
  font-size: 0.8rem;
  font-weight: 500;
  margin-top: 0.5rem;
  display: inline-block;
`;

const ProjectDetails = styled.div`
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  margin-bottom: 1.5rem;
`;

const ProjectDetail = styled.div`
  display: flex;
  justify-content: space-between;
  font-size: 0.9rem;
  
  .label {
    color: ${theme.secondaryTextColor};
  }
  
  .value {
    color: ${theme.textColor};
    font-weight: 500;
  }
  
  @media (max-width: 480px) {
    font-size: 0.85rem;
  }
`;

const ProjectActionsGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 0.75rem;
  margin-top: 1rem;
  
  @media (max-width: 480px) {
    grid-template-columns: 1fr;
    gap: 0.5rem;
  }
`;

const ProjectItem = styled.div`
  display: flex;
  align-items: center;
  padding: 1.25rem;
  border-radius: 0.75rem;
  border: 1px solid ${theme.borderColor};
  transition: all 0.2s ease;
  animation: ${fadeIn} 0.3s ease-out;
  
  &:hover {
    background: #f8fafc;
    border-color: #c7d2fe;
  }
  
  @media (max-width: 768px) {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }
  
  @media (max-width: 480px) {
    padding: 1rem;
  }
`;

const ProjectIcon = styled.div`
  width: 3rem;
  height: 3rem;
  border-radius: 0.75rem;
  background: #f1f5f9;
  display: flex;
  align-items: center;
  justify-content: center;
  color: ${theme.secondaryTextColor};
  margin-right: 1rem;
  
  @media (max-width: 768px) {
    margin-right: 0;
  }
  
  @media (max-width: 480px) {
    width: 2.5rem;
    height: 2.5rem;
  }
`;

const ProjectInfo = styled.div`
  flex: 1;
  
  @media (max-width: 768px) {
    width: 100%;
  }
`;

const ProjectName = styled.h3`
  font-size: 1.1rem;
  font-weight: 600;
  color: ${theme.textColor};
  margin: 0 0 0.25rem 0;
  
  @media (max-width: 480px) {
    font-size: 1rem;
  }
`;

const ProjectMeta = styled.div`
  display: flex;
  gap: 1rem;
  font-size: 0.875rem;
  color: ${theme.secondaryTextColor};
  
  @media (max-width: 768px) {
    flex-direction: column;
    gap: 0.25rem;
  }
  
  @media (max-width: 480px) {
    font-size: 0.8rem;
  }
`;

const ProjectActions = styled.div`
  display: flex;
  gap: 0.75rem;
  
  @media (max-width: 768px) {
    width: 100%;
    justify-content: flex-end;
  }
  
  @media (max-width: 480px) {
    gap: 0.5rem;
    flex-wrap: wrap;
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
  color: ${theme.textColor};
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: all 0.2s ease;
  
  &:hover {
    background: #e2e8f0;
  }
  
  &.primary {
    background: ${theme.primaryGradient};
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
  
  @media (max-width: 480px) {
    padding: 0.4rem 0.8rem;
    font-size: 0.8rem;
  }
`;

const StatusIndicator = styled.div`
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.25rem 0.75rem;
  border-radius: 2rem;
  font-size: 0.875rem;
  font-weight: 500;
  
  &.completed {
    background: #dcfce7;
    color: #16a34a;
  }
  
  &.in-progress {
    background: #fef3c7;
    color: #d97706;
  }
  
  &.failed {
    background: #fee2e2;
    color: #dc2626;
  }
  
  @media (max-width: 480px) {
    font-size: 0.8rem;
    padding: 0.2rem 0.6rem;
  }
`;

const QuickActions = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1rem;
  margin-top: 1.5rem;
  
  @media (max-width: 768px) {
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  }
  
  @media (max-width: 480px) {
    grid-template-columns: 1fr;
  }
`;

const ActionCard = styled.div`
  background: ${theme.cardBackground};
  border-radius: ${theme.borderRadius};
  padding: 1.5rem;
  box-shadow: ${theme.boxShadow};
  border: 1px solid ${theme.borderColor};
  cursor: pointer;
  transition: all 0.3s ease;
  text-align: center;
  animation: ${scaleIn} 0.3s ease-out;
  
  &:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 25px rgba(102, 126, 234, 0.15);
    border-color: #667eea;
  }
  
  @media (max-width: 768px) {
    padding: 1.25rem;
  }
  
  @media (max-width: 480px) {
    padding: 1rem;
  }
`;

const ActionIcon = styled.div`
  width: 3rem;
  height: 3rem;
  border-radius: 0.75rem;
  background: ${theme.primaryGradient};
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  margin: 0 auto 1rem;
  font-size: 1.5rem;
`;

const ActionTitle = styled.h3`
  font-size: 1.1rem;
  font-weight: 600;
  color: ${theme.textColor};
  margin: 0 0 0.5rem 0;
  
  @media (max-width: 480px) {
    font-size: 1rem;
  }
`;

const ActionDescription = styled.p`
  color: ${theme.secondaryTextColor};
  font-size: 0.9rem;
  margin: 0;
  
  @media (max-width: 480px) {
    font-size: 0.85rem;
  }
`;

// Enhanced Demo Preview Components
const DemoPreview = styled.div`
  position: relative;
  border-radius: 0.75rem;
  overflow: hidden;
  margin-top: 1rem;
  border: 1px solid ${theme.borderColor};
  box-shadow: ${theme.boxShadow};
  background: #f8fafc;
  height: 200px;
  display: flex;
  flex-direction: column;
`;

const DemoImage = styled.div`
  width: 100%;
  height: 100%;
  background: ${theme.primaryGradient};
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: 600;
  position: relative;
  
  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><rect x="10" y="20" width="80" height="10" fill="rgba(255,255,255,0.2)"/><rect x="10" y="40" width="60" height="10" fill="rgba(255,255,255,0.2)"/><rect x="10" y="60" width="70" height="10" fill="rgba(255,255,255,0.2)"/></svg>');
    background-size: cover;
  }
`;

const DemoOverlay = styled.div`
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.3s ease;
  
  ${ProjectCard}:hover & {
    opacity: 1;
  }
`;

const DemoActions = styled.div`
  display: flex;
  gap: 1rem;
`;

const DemoButton = styled.button`
  background: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 0.5rem;
  font-weight: 500;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: all 0.2s ease;
  
  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  }
  
  @media (max-width: 480px) {
    padding: 0.5rem 1rem;
    font-size: 0.9rem;
  }
`;

const TechStack = styled.div`
  display: flex;
  gap: 0.5rem;
  margin-top: 0.5rem;
  flex-wrap: wrap;
`;

const TechTag = styled.span`
  background: #e0e7ff;
  color: #4f46e5;
  padding: 0.25rem 0.75rem;
  border-radius: 2rem;
  font-size: 0.75rem;
  font-weight: 500;
`;

const FeaturesList = styled.div`
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-top: 0.5rem;
`;

const FeatureTag = styled.span`
  background: #dcfce7;
  color: #16a34a;
  padding: 0.25rem 0.75rem;
  border-radius: 2rem;
  font-size: 0.75rem;
  font-weight: 500;
`;

// Project Detail Modal with enhanced styling
const ModalOverlay = styled.div`
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 1rem;
`;

const ModalContent = styled.div`
  background: ${theme.cardBackground};
  border-radius: ${theme.borderRadius};
  width: 90%;
  max-width: 900px;
  max-height: 90vh;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.2);
`;

const ModalHeader = styled.div`
  padding: 1.5rem;
  border-bottom: 1px solid ${theme.borderColor};
  display: flex;
  justify-content: space-between;
  align-items: center;
  
  @media (max-width: 480px) {
    padding: 1rem;
  }
`;

const ModalTitle = styled.h2`
  font-size: 1.5rem;
  font-weight: 600;
  color: ${theme.textColor};
  margin: 0;
  
  @media (max-width: 480px) {
    font-size: 1.25rem;
  }
`;

const CloseButton = styled.button`
  background: none;
  border: none;
  color: ${theme.secondaryTextColor};
  cursor: pointer;
  padding: 0.5rem;
  border-radius: 0.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  
  &:hover {
    background: #f1f5f9;
  }
  
  @media (max-width: 480px) {
    padding: 0.25rem;
  }
`;

const ModalBody = styled.div`
  flex: 1;
  overflow-y: auto;
  padding: 1.5rem;
  
  @media (max-width: 480px) {
    padding: 1rem;
  }
`;

const ModalActions = styled.div`
  padding: 1.5rem;
  border-top: 1px solid ${theme.borderColor};
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  
  @media (max-width: 480px) {
    padding: 1rem;
    flex-direction: column;
    gap: 0.5rem;
  }
`;

// Enhanced Project Details Section
const ProjectDetailsSection = styled.div`
  margin-bottom: 1.5rem;
`;

const ProjectDetailsTitle = styled.h3`
  font-size: 1.25rem;
  font-weight: 600;
  color: ${theme.textColor};
  margin: 0 0 1rem 0;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  
  @media (max-width: 480px) {
    font-size: 1.1rem;
  }
`;

const ProjectDetailsGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1rem;
  
  @media (max-width: 480px) {
    grid-template-columns: 1fr;
  }
`;

const ProjectDetailCard = styled.div`
  background: #f8fafc;
  border-radius: 0.75rem;
  padding: 1rem;
  border: 1px solid ${theme.borderColor};
`;

const ProjectDetailLabel = styled.div`
  font-size: 0.875rem;
  color: ${theme.secondaryTextColor};
  margin-bottom: 0.25rem;
  
  @media (max-width: 480px) {
    font-size: 0.8rem;
  }
`;

const ProjectDetailValue = styled.div`
  font-size: 1rem;
  font-weight: 500;
  color: ${theme.textColor};
  
  @media (max-width: 480px) {
    font-size: 0.9rem;
  }
`;

// Enhanced Demo Preview in Modal
const ModalDemoPreview = styled.div`
  background: #f8fafc;
  border-radius: 0.75rem;
  padding: 1.5rem;
  margin: 1.5rem 0;
  border: 1px solid ${theme.borderColor};
  text-align: center;
`;

const ModalDemoImage = styled.div`
  width: 100%;
  height: 300px;
  background: ${theme.primaryGradient};
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: 600;
  border-radius: 0.5rem;
  margin-bottom: 1rem;
  position: relative;
  
  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><rect x="10" y="20" width="80" height="10" fill="rgba(255,255,255,0.2)"/><rect x="10" y="40" width="60" height="10" fill="rgba(255,255,255,0.2)"/><rect x="10" y="60" width="70" height="10" fill="rgba(255,255,255,0.2)"/></svg>');
    background-size: cover;
  }
  
  @media (max-width: 480px) {
    height: 200px;
  }
`;

function Dashboard() {
  const navigate = useNavigate();
  const [projects, setProjects] = useState([
    {
      id: 1,
      name: 'Analytics Dashboard',
      status: 'completed',
      createdAt: '2023-06-15',
      lastModified: '2023-06-18',
      framework: 'React + FastAPI',
      deployed: true,
      techStack: {
        frontend: 'React',
        backend: 'FastAPI',
        database: 'MySQL'
      },
      features: ['Charts & Graphs', 'Real-time Data', 'User Management'],
      previewUrl: 'https://dashboard-demo.example.com'
    },
    {
      id: 2,
      name: 'E-commerce Store',
      status: 'in-progress',
      createdAt: '2023-06-10',
      lastModified: '2023-06-17',
      framework: 'Vue + Express',
      deployed: false,
      techStack: {
        frontend: 'Vue.js',
        backend: 'Express.js',
        database: 'PostgreSQL'
      },
      features: ['Product Catalog', 'Shopping Cart', 'Payment Gateway'],
      previewUrl: null
    },
    {
      id: 3,
      name: 'Blog CMS',
      status: 'completed',
      createdAt: '2023-06-05',
      lastModified: '2023-06-12',
      framework: 'Angular + Django',
      deployed: true,
      techStack: {
        frontend: 'Angular',
        backend: 'Django',
        database: 'SQLite'
      },
      features: ['Rich Text Editor', 'SEO Tools', 'Media Management'],
      previewUrl: 'https://blog-demo.example.com'
    },
    {
      id: 4,
      name: 'Chat Application',
      status: 'failed',
      createdAt: '2023-06-01',
      lastModified: '2023-06-15',
      framework: 'React + NestJS',
      deployed: false,
      techStack: {
        frontend: 'React',
        backend: 'NestJS',
        database: 'MongoDB'
      },
      features: ['Real-time Chat', 'File Sharing', 'Push Notifications'],
      previewUrl: null
    }
  ]);
  
  const [stats, setStats] = useState({
    totalProjects: 12,
    activeProjects: 8,
    completedProjects: 9,
    totalDeployments: 15
  });
  
  const [searchTerm, setSearchTerm] = useState('');
  const [viewMode, setViewMode] = useState('grid');
  const [filterStatus, setFilterStatus] = useState('all');
  const [selectedProject, setSelectedProject] = useState(null);
  const [showProjectModal, setShowProjectModal] = useState(false);

  const filteredProjects = projects.filter(project => {
    const matchesSearch = project.name.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesFilter = filterStatus === 'all' || project.status === filterStatus;
    return matchesSearch && matchesFilter;
  });

  const handleCreateNew = () => {
    navigate('/builder');
  };

  const handleViewDemo = (project) => {
    if (project.previewUrl) {
      window.open(project.previewUrl, '_blank');
    } else {
      // In a real implementation, this would show a preview modal or message
      alert('Demo not available for this project yet.');
    }
  };

  const handleViewProject = (project) => {
    setSelectedProject(project);
    setShowProjectModal(true);
  };

  const handleDeployProject = (projectId) => {
    navigate('/deploy');
  };

  const handleDeleteProject = (projectId) => {
    if (window.confirm('Are you sure you want to delete this project?')) {
      setProjects(prev => prev.filter(project => project.id !== projectId));
    }
  };

  const handleEditProject = (projectId) => {
    // In a real implementation, this would navigate to the project edit page
    console.log(`Editing project ${projectId}`);
  };

  const handleGenerateProject = () => {
    navigate('/builder');
  };

  const getStatusText = (status) => {
    switch (status) {
      case 'completed':
        return 'Completed';
      case 'in-progress':
        return 'In Progress';
      case 'failed':
        return 'Failed';
      default:
        return 'Unknown';
    }
  };

  const quickActions = [
    {
      title: 'New Project',
      description: 'Create a new application from scratch',
      icon: Plus,
      action: handleCreateNew
    },
    {
      title: 'AI Chat',
      description: 'Chat with AI to build applications',
      icon: MessageSquare,
      action: () => navigate('/ai-chat')
    },
    {
      title: 'Deploy',
      description: 'Deploy your applications to the cloud',
      icon: Rocket,
      action: () => navigate('/deploy')
    },
    {
      title: 'Integrations',
      description: 'Connect third-party services',
      icon: GitBranch,
      action: () => navigate('/integrations')
    }
  ];

  return (
    <Container>
      <Header>
        <Title>Dashboard</Title>
        <Subtitle>Welcome back! Here's what's happening with your projects.</Subtitle>
      </Header>
      
      <StatsGrid>
        <StatCard>
          <StatHeader>
            <StatTitle>Total Projects</StatTitle>
            <StatIcon>
              <Code size={20} />
            </StatIcon>
          </StatHeader>
          <StatValue>{stats.totalProjects}</StatValue>
          <StatChange className="positive">
            <TrendingUp size={16} />
            12% from last month
          </StatChange>
        </StatCard>
        
        <StatCard>
          <StatHeader>
            <StatTitle>Active Projects</StatTitle>
            <StatIcon>
              <Zap size={20} />
            </StatIcon>
          </StatHeader>
          <StatValue>{stats.activeProjects}</StatValue>
          <StatChange className="positive">
            <TrendingUp size={16} />
            5% from last month
          </StatChange>
        </StatCard>
        
        <StatCard>
          <StatHeader>
            <StatTitle>Completed</StatTitle>
            <StatIcon>
              <CheckCircle size={20} />
            </StatIcon>
          </StatHeader>
          <StatValue>{stats.completedProjects}</StatValue>
          <StatChange className="positive">
            <TrendingUp size={16} />
            8% from last month
          </StatChange>
        </StatCard>
        
        <StatCard>
          <StatHeader>
            <StatTitle>Deployments</StatTitle>
            <StatIcon>
              <Rocket size={20} />
            </StatIcon>
          </StatHeader>
          <StatValue>{stats.totalDeployments}</StatValue>
          <StatChange className="positive">
            <TrendingUp size={16} />
            15% from last month
          </StatChange>
        </StatCard>
      </StatsGrid>
      
      <Section>
        <SectionHeader>
          <SectionTitle>Quick Actions</SectionTitle>
        </SectionHeader>
        
        <QuickActions>
          {quickActions.map((action, index) => (
            <ActionCard key={index} onClick={action.action}>
              <ActionIcon>
                <action.icon size={24} />
              </ActionIcon>
              <ActionTitle>{action.title}</ActionTitle>
              <ActionDescription>{action.description}</ActionDescription>
            </ActionCard>
          ))}
        </QuickActions>
      </Section>
      
      <Section>
        <SectionHeader>
          <SectionTitle>AI-Powered Analytics</SectionTitle>
        </SectionHeader>
        <AIDashboard />
      </Section>
      
      <Section>
        <SectionHeader>
          <SectionTitle>Your Projects</SectionTitle>
          <Controls>
            <SearchInput
              type="text"
              placeholder="Search projects..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
            <FilterButton onClick={() => setFilterStatus(filterStatus === 'all' ? 'completed' : 'all')}>
              <Filter size={16} />
              {filterStatus === 'all' ? 'Show Completed' : 'Show All'}
            </FilterButton>
            <ViewToggle>
              <ViewButton 
                active={viewMode === 'list'} 
                onClick={() => setViewMode('list')}
              >
                <List size={16} />
                List
              </ViewButton>
              <ViewButton 
                active={viewMode === 'grid'} 
                onClick={() => setViewMode('grid')}
              >
                <Grid size={16} />
                Grid
              </ViewButton>
            </ViewToggle>
            <ViewAllButton onClick={handleCreateNew}>
              <Plus size={16} />
              New Project
            </ViewAllButton>
          </Controls>
        </SectionHeader>
        
        {viewMode === 'list' ? (
          <ProjectList>
            {filteredProjects.map(project => (
              <ProjectItem key={project.id}>
                <ProjectIcon>
                  <Code size={20} />
                </ProjectIcon>
                <ProjectInfo>
                  <ProjectName>{project.name}</ProjectName>
                  <ProjectMeta>
                    <span>{project.framework}</span>
                    <span>Created: {project.createdAt}</span>
                    <span>Modified: {project.lastModified}</span>
                  </ProjectMeta>
                </ProjectInfo>
                <ProjectActions>
                  <StatusIndicator className={project.status}>
                    {getStatusText(project.status)}
                  </StatusIndicator>
                  <ActionButton onClick={() => handleViewProject(project)}>
                    <Eye size={16} />
                    View
                  </ActionButton>
                  {project.previewUrl && (
                    <ActionButton 
                      className="success" 
                      onClick={() => handleViewDemo(project)}
                    >
                      <ExternalLink size={16} />
                      Demo
                    </ActionButton>
                  )}
                  {!project.deployed && (
                    <ActionButton 
                      className="primary" 
                      onClick={() => handleDeployProject(project.id)}
                    >
                      <Rocket size={16} />
                      Deploy
                    </ActionButton>
                  )}
                  <ActionButton onClick={() => handleEditProject(project.id)}>
                    <Edit3 size={16} />
                    Edit
                  </ActionButton>
                  <ActionButton 
                    className="danger" 
                    onClick={() => handleDeleteProject(project.id)}
                  >
                    <Trash2 size={16} />
                    Delete
                  </ActionButton>
                </ProjectActions>
              </ProjectItem>
            ))}
          </ProjectList>
        ) : (
          <ProjectGrid>
            {filteredProjects.map(project => (
              <ProjectCard key={project.id}>
                <ProjectHeader>
                  <div>
                    <ProjectTitle>{project.name}</ProjectTitle>
                    <ProjectFramework>{project.framework}</ProjectFramework>
                  </div>
                  <StatusIndicator className={project.status}>
                    {getStatusText(project.status)}
                  </StatusIndicator>
                </ProjectHeader>
                
                <ProjectDetails>
                  <ProjectDetail>
                    <span className="label">Created</span>
                    <span className="value">{project.createdAt}</span>
                  </ProjectDetail>
                  <ProjectDetail>
                    <span className="label">Last Modified</span>
                    <span className="value">{project.lastModified}</span>
                  </ProjectDetail>
                  <ProjectDetail>
                    <span className="label">Features</span>
                    <span className="value">{project.features.join(', ')}</span>
                  </ProjectDetail>
                  <ProjectDetail>
                    <span className="label">Tech Stack</span>
                    <span className="value">
                      {project.techStack.frontend} + {project.techStack.backend} + {project.techStack.database}
                    </span>
                  </ProjectDetail>
                </ProjectDetails>
                
                <TechStack>
                  {Object.values(project.techStack).map((tech, index) => (
                    <TechTag key={index}>{tech}</TechTag>
                  ))}
                </TechStack>
                
                <FeaturesList>
                  {project.features.slice(0, 3).map((feature, index) => (
                    <FeatureTag key={index}>{feature}</FeatureTag>
                  ))}
                  {project.features.length > 3 && (
                    <FeatureTag>+{project.features.length - 3} more</FeatureTag>
                  )}
                </FeaturesList>
                
                {project.previewUrl && (
                  <DemoPreview>
                    <DemoImage>
                      <Globe size={40} />
                    </DemoImage>
                    <DemoOverlay>
                      <DemoActions>
                        <DemoButton onClick={() => handleViewDemo(project)}>
                          <ExternalLink size={16} />
                          View Demo
                        </DemoButton>
                      </DemoActions>
                    </DemoOverlay>
                  </DemoPreview>
                )}
                
                <ProjectActionsGrid>
                  <ActionButton onClick={() => handleViewProject(project)}>
                    <Eye size={16} />
                    View
                  </ActionButton>
                  {project.previewUrl ? (
                    <ActionButton 
                      className="success" 
                      onClick={() => handleViewDemo(project)}
                    >
                      <ExternalLink size={16} />
                      Demo
                    </ActionButton>
                  ) : (
                    <ActionButton disabled>
                      <ExternalLink size={16} />
                      No Demo
                    </ActionButton>
                  )}
                  {!project.deployed && (
                    <ActionButton 
                      className="primary" 
                      onClick={() => handleDeployProject(project.id)}
                    >
                      <Rocket size={16} />
                      Deploy
                    </ActionButton>
                  )}
                  <ActionButton 
                    className="danger" 
                    onClick={() => handleDeleteProject(project.id)}
                  >
                    <Trash2 size={16} />
                    Delete
                  </ActionButton>
                </ProjectActionsGrid>
              </ProjectCard>
            ))}
          </ProjectGrid>
        )}
      </Section>
      
      {showProjectModal && selectedProject && (
        <ModalOverlay onClick={() => setShowProjectModal(false)}>
          <ModalContent onClick={(e) => e.stopPropagation()}>
            <ModalHeader>
              <ModalTitle>{selectedProject.name}</ModalTitle>
              <CloseButton onClick={() => setShowProjectModal(false)}>
                <X size={20} />
              </CloseButton>
            </ModalHeader>
            <ModalBody>
              <ProjectDetailsSection>
                <ProjectDetailsTitle>
                  <FileDocument size={20} />
                  Project Details
                </ProjectDetailsTitle>
                <ProjectDetailsGrid>
                  <ProjectDetailCard>
                    <ProjectDetailLabel>Status</ProjectDetailLabel>
                    <ProjectDetailValue>
                      <StatusIndicator className={selectedProject.status}>
                        {getStatusText(selectedProject.status)}
                      </StatusIndicator>
                    </ProjectDetailValue>
                  </ProjectDetailCard>
                  
                  <ProjectDetailCard>
                    <ProjectDetailLabel>Framework</ProjectDetailLabel>
                    <ProjectDetailValue>{selectedProject.framework}</ProjectDetailValue>
                  </ProjectDetailCard>
                  
                  <ProjectDetailCard>
                    <ProjectDetailLabel>Created</ProjectDetailLabel>
                    <ProjectDetailValue>{selectedProject.createdAt}</ProjectDetailValue>
                  </ProjectDetailCard>
                  
                  <ProjectDetailCard>
                    <ProjectDetailLabel>Last Modified</ProjectDetailLabel>
                    <ProjectDetailValue>{selectedProject.lastModified}</ProjectDetailValue>
                  </ProjectDetailCard>
                </ProjectDetailsGrid>
              </ProjectDetailsSection>
              
              <ProjectDetailsSection>
                <ProjectDetailsTitle>
                  <Code size={20} />
                  Tech Stack
                </ProjectDetailsTitle>
                <TechStack>
                  {Object.values(selectedProject.techStack).map((tech, index) => (
                    <TechTag key={index}>{tech}</TechTag>
                  ))}
                </TechStack>
              </ProjectDetailsSection>
              
              <ProjectDetailsSection>
                <ProjectDetailsTitle>
                  <Star size={20} />
                  Features
                </ProjectDetailsTitle>
                <FeaturesList>
                  {selectedProject.features.map((feature, index) => (
                    <FeatureTag key={index}>{feature}</FeatureTag>
                  ))}
                </FeaturesList>
              </ProjectDetailsSection>
              
              <ProjectDetailsSection>
                <ProjectDetailsTitle>
                  <Monitor size={20} />
                  Application Preview
                </ProjectDetailsTitle>
                {selectedProject.previewUrl ? (
                  <ModalDemoPreview>
                    <ModalDemoImage>
                      <Globe size={60} />
                    </ModalDemoImage>
                    <p>This is a preview of your generated application. The full demo shows your complete application with all features.</p>
                    <p>Tech Stack: {selectedProject.techStack.frontend} + {selectedProject.techStack.backend} + {selectedProject.techStack.database}</p>
                  </ModalDemoPreview>
                ) : (
                  <ModalDemoPreview>
                    <ModalDemoImage>
                      <ImageIcon size={60} />
                    </ModalDemoImage>
                    <p>Demo not available for this project yet. Generate a project to see a live preview.</p>
                    <ActionButton 
                      className="primary" 
                      onClick={() => {
                        setShowProjectModal(false);
                        navigate('/builder');
                      }}
                      style={{ marginTop: '1rem' }}
                    >
                      <Plus size={16} />
                      Create New Project
                    </ActionButton>
                  </ModalDemoPreview>
                )}
              </ProjectDetailsSection>
            </ModalBody>
            <ModalActions>
              <ActionButton onClick={() => setShowProjectModal(false)}>
                <X size={16} />
                Close
              </ActionButton>
              {selectedProject.previewUrl && (
                <ActionButton 
                  className="success" 
                  onClick={() => handleViewDemo(selectedProject)}
                >
                  <ExternalLink size={16} />
                  View Demo
                </ActionButton>
              )}
              <ActionButton 
                className="primary" 
                onClick={() => {
                  setShowProjectModal(false);
                  handleEditProject(selectedProject.id);
                }}
              >
                <Edit3 size={16} />
                Edit Project
              </ActionButton>
            </ModalActions>
          </ModalContent>
        </ModalOverlay>
      )}
    </Container>
  );
}

export default Dashboard;