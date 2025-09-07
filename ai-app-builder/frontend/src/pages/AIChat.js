import React, { useState, useRef, useEffect } from 'react';
import styled, { keyframes } from 'styled-components';
import { 
  Send, 
  Bot, 
  User, 
  Lightbulb, 
  Code, 
  Wrench, 
  Zap,
  Loader,
  Sparkles,
  MessageSquare,
  Terminal,
  Database,
  Globe,
  Smartphone,
  ShoppingCart,
  BarChart3,
  FileText,
  Cpu,
  Settings,
  Copy,
  ThumbsUp,
  ThumbsDown,
  RefreshCw,
  Trash2,
  Edit3,
  // Adding more icons for enhanced UI
  Plus,
  Eye,
  EyeOff,
  Share2,
  Heart,
  ExternalLink,
  Monitor,
  Tablet,
  Smartphone as Mobile,
  Search,
  Filter,
  Grid,
  List,
  ChevronLeft,
  ChevronRight,
  Menu,
  X,
  Check,
  AlertCircle,
  CheckCircle,
  Play,
  Download,
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
import aiChatService from '../services/aiChatService';
import { useNavigate } from 'react-router-dom';

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

const slideIn = keyframes`
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
`;

const float = keyframes`
  0%, 100% { transform: translateY(0px); }
  50% { transform: translateY(-5px); }
`;

const typing = keyframes`
  0% { width: 0; }
  100% { width: 100%; }
`;

const bounce = keyframes`
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-5px); }
`;

const shimmer = keyframes`
  0% { background-position: -200% 0; }
  100% { background-position: 200% 0; }
`;

// Additional animations for smoother experience
const fadeIn = keyframes`
  from { opacity: 0; }
  to { opacity: 1; }
`;

const slideUp = keyframes`
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
`;

const scaleIn = keyframes`
  from { opacity: 0; transform: scale(0.95); }
  to { opacity: 1; transform: scale(1); }
`;

const rotate = keyframes`
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
`;

const slideInLeft = keyframes`
  from { opacity: 0; transform: translateX(-20px); }
  to { opacity: 1; transform: translateX(0); }
`;

const Container = styled.div`
  display: flex;
  height: calc(100vh - 4rem);
  background: linear-gradient(135deg, #f0f4f8 0%, #e6f7ff 100%);
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
    flex-direction: column;
    height: auto;
    min-height: 100vh;
  }
  
  @media (max-width: 480px) {
    height: auto;
    min-height: 100vh;
  }
`;

const Sidebar = styled.div`
  width: 320px;
  background: ${theme.cardBackground};
  border-right: 1px solid ${theme.borderColor};
  padding: 1.5rem;
  overflow-y: auto;
  box-shadow: 2px 0 10px rgba(0, 0, 0, 0.05);
  z-index: 10;
  position: relative;
  height: calc(100vh - 4rem);
  
  @media (max-width: 768px) {
    position: absolute;
    left: ${props => props.isOpen ? '0' : '-100%'};
    transition: left 0.3s ease;
    width: 100%;
    height: calc(100vh - 4rem);
  }
  
  @media (max-width: 480px) {
    padding: 1rem;
    height: calc(100vh - 3rem);
  }
`;

const SidebarHeader = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  
  @media (max-width: 480px) {
    margin-bottom: 1rem;
  }
`;

const SidebarTitle = styled.h2`
  font-size: 1.25rem;
  font-weight: 600;
  color: ${theme.textColor};
  margin: 0;
  
  @media (max-width: 480px) {
    font-size: 1.1rem;
  }
`;

const CloseButton = styled.button`
  background: none;
  border: none;
  color: ${theme.secondaryTextColor};
  cursor: pointer;
  padding: 0.5rem;
  border-radius: 0.5rem;
  
  &:hover {
    background: #f1f5f9;
  }
  
  @media (min-width: 769px) {
    display: none;
  }
  
  @media (max-width: 480px) {
    padding: 0.25rem;
  }
`;

const NewChatButton = styled.button`
  width: 100%;
  background: ${theme.primaryGradient};
  color: white;
  border: none;
  padding: 0.875rem;
  border-radius: 0.75rem;
  font-weight: 500;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  margin-bottom: 1.5rem;
  transition: all 0.2s ease;
  
  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
  }
  
  @media (max-width: 480px) {
    padding: 0.75rem;
    font-size: 0.9rem;
  }
`;

const ChatHistory = styled.div`
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
`;

const ChatItem = styled.div`
  padding: 0.75rem 1rem;
  border-radius: 0.5rem;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 0.9rem;
  
  &:hover {
    background: #f1f5f9;
  }
  
  &.active {
    background: #e0e7ff;
    color: #4f46e5;
  }
  
  @media (max-width: 480px) {
    padding: 0.5rem 0.75rem;
    font-size: 0.85rem;
  }
`;

const MainContent = styled.div`
  flex: 1;
  display: flex;
  flex-direction: column;
  position: relative;
  z-index: 1;
  
  @media (max-width: 768px) {
    width: 100%;
  }
`;

const Header = styled.div`
  padding: 1.5rem;
  border-bottom: 1px solid ${theme.borderColor};
  background: ${theme.cardBackground};
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  display: flex;
  align-items: center;
  gap: 1rem;
  
  @media (max-width: 480px) {
    padding: 1rem;
  }
`;

const MenuButton = styled.button`
  background: none;
  border: none;
  color: ${theme.secondaryTextColor};
  cursor: pointer;
  padding: 0.5rem;
  border-radius: 0.5rem;
  
  &:hover {
    background: #f1f5f9;
  }
  
  @media (min-width: 769px) {
    display: none;
  }
  
  @media (max-width: 480px) {
    padding: 0.25rem;
  }
`;

const Title = styled.h1`
  font-size: 1.75rem;
  font-weight: 700;
  color: ${theme.textColor};
  margin: 0;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  
  @media (max-width: 768px) {
    font-size: 1.5rem;
  }
  
  @media (max-width: 480px) {
    font-size: 1.25rem;
  }
`;

const Subtitle = styled.p`
  color: ${theme.secondaryTextColor};
  font-size: 0.9rem;
  margin: 0.25rem 0 0 0;
  
  @media (max-width: 480px) {
    font-size: 0.8rem;
  }
`;

const ChatContainer = styled.div`
  flex: 1;
  overflow-y: auto;
  padding: 2rem;
  display: flex;
  flex-direction: column;
  background: linear-gradient(180deg, #ffffff 0%, #f8fafc 100%);
  gap: 2rem;
  
  &::-webkit-scrollbar {
    width: 8px;
  }
  
  &::-webkit-scrollbar-track {
    background: #f1f5f9;
  }
  
  &::-webkit-scrollbar-thumb {
    background: #c7d2fe;
    border-radius: 4px;
  }
  
  @media (max-width: 768px) {
    padding: 1.5rem;
    gap: 1.5rem;
  }
  
  @media (max-width: 480px) {
    padding: 1rem;
    gap: 1rem;
  }
`;

const Message = styled.div`
  display: flex;
  gap: 1.25rem;
  max-width: 900px;
  width: 100%;
  align-self: ${props => props.role === 'user' ? 'flex-end' : 'flex-start'};
  animation: ${slideIn} 0.4s ease-out;
  
  &.user {
    flex-direction: row-reverse;
    
    .message-content {
      background: ${theme.primaryGradient};
      color: white;
      border-radius: 1.5rem 0.5rem 1.5rem 1.5rem;
      box-shadow: 0 4px 15px rgba(102, 126, 234, 0.2);
    }
    
    .avatar {
      background: ${theme.primaryGradient};
      color: white;
      animation: ${float} 3s ease-in-out infinite;
    }
  }
  
  &.ai {
    .message-content {
      background: ${theme.cardBackground};
      border: 1px solid ${theme.borderColor};
      border-radius: 0.5rem 1.5rem 1.5rem 1.5rem;
      box-shadow: ${theme.boxShadow};
      animation: ${slideUp} 0.5s ease-out;
    }
    
    .avatar {
      background: #f1f5f9;
      color: ${theme.secondaryTextColor};
      animation: ${float} 4s ease-in-out infinite;
    }
  }
  
  @media (max-width: 768px) {
    max-width: 100%;
    padding: 0 1rem;
    gap: 1rem;
  }
  
  @media (max-width: 480px) {
    gap: 0.75rem;
  }
`;

const Avatar = styled.div`
  width: 3rem;
  height: 3rem;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  font-weight: 600;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  
  @media (max-width: 480px) {
    width: 2.5rem;
    height: 2.5rem;
  }
`;

const MessageContent = styled.div`
  max-width: 85%;
  padding: 1.25rem;
  line-height: 1.6;
  position: relative;
  
  pre {
    background: #1e293b;
    color: #f8fafc;
    padding: 1.25rem;
    border-radius: 0.75rem;
    overflow-x: auto;
    margin: 1rem 0;
    box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.2);
    font-family: 'Monaco', 'Consolas', monospace;
    font-size: 0.9rem;
  }
  
  code {
    background: #f1f5f9;
    padding: 0.25rem 0.5rem;
    border-radius: 0.375rem;
    font-family: 'Monaco', 'Consolas', monospace;
    font-size: 0.9rem;
  }
  
  p {
    margin: 0 0 1rem 0;
    
    &:last-child {
      margin-bottom: 0;
    }
  }
  
  @media (max-width: 768px) {
    padding: 1rem;
    max-width: 80%;
  }
  
  @media (max-width: 480px) {
    padding: 0.75rem;
    max-width: 75%;
    font-size: 0.9rem;
  }
`;

const MessageActions = styled.div`
  display: flex;
  gap: 0.5rem;
  margin-top: 0.75rem;
  padding-top: 0.75rem;
  border-top: 1px solid rgba(0, 0, 0, 0.05);
  
  @media (max-width: 480px) {
    gap: 0.25rem;
  }
`;

const ActionButton = styled.button`
  background: none;
  border: none;
  color: ${theme.secondaryTextColor};
  cursor: pointer;
  padding: 0.25rem;
  border-radius: 0.25rem;
  display: flex;
  align-items: center;
  gap: 0.25rem;
  font-size: 0.8rem;
  
  &:hover {
    background: #f1f5f9;
    color: ${theme.textColor};
  }
  
  @media (max-width: 480px) {
    padding: 0.125rem;
    font-size: 0.7rem;
  }
`;

const InputContainer = styled.div`
  padding: 1.5rem;
  border-top: 1px solid ${theme.borderColor};
  background: ${theme.cardBackground};
  
  @media (max-width: 480px) {
    padding: 1rem;
  }
`;

const InputWrapper = styled.div`
  display: flex;
  gap: 0.75rem;
  max-width: 900px;
  margin: 0 auto;
  
  @media (max-width: 768px) {
    gap: 0.5rem;
  }
  
  @media (max-width: 480px) {
    gap: 0.25rem;
  }
`;

const Input = styled.textarea`
  flex: 1;
  padding: 1rem 1.25rem;
  border: 1px solid ${theme.borderColor};
  border-radius: 1.5rem;
  font-size: 1rem;
  font-family: inherit;
  resize: none;
  min-height: 60px;
  max-height: 200px;
  transition: all 0.2s ease;
  
  &:focus {
    outline: none;
    border-color: #667eea;
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
  }
  
  @media (max-width: 768px) {
    padding: 0.875rem 1rem;
    font-size: 0.9rem;
  }
  
  @media (max-width: 480px) {
    padding: 0.75rem 0.875rem;
    font-size: 0.85rem;
  }
`;

const SendButton = styled.button`
  background: ${theme.primaryGradient};
  color: white;
  border: none;
  width: 50px;
  height: 50px;
  border-radius: 50%;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  align-self: flex-end;
  transition: all 0.2s ease;
  flex-shrink: 0;
  
  &:hover:not(:disabled) {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
  }
  
  &:disabled {
    opacity: 0.5;
    cursor: not-allowed;
    transform: none;
  }
  
  @media (max-width: 480px) {
    width: 40px;
    height: 40px;
  }
`;

const QuickSuggestions = styled.div`
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
  margin-top: 1rem;
  padding: 0 1rem;
  max-width: 900px;
  margin: 1rem auto 0;
  
  @media (max-width: 768px) {
    gap: 0.5rem;
  }
  
  @media (max-width: 480px) {
    gap: 0.25rem;
    padding: 0 0.5rem;
  }
`;

const SuggestionButton = styled.button`
  background: ${theme.cardBackground};
  border: 1px solid ${theme.borderColor};
  padding: 0.5rem 1rem;
  border-radius: 2rem;
  font-size: 0.875rem;
  cursor: pointer;
  transition: all 0.2s ease;
  
  &:hover {
    border-color: #667eea;
    background: #f8fafc;
  }
  
  @media (max-width: 480px) {
    padding: 0.25rem 0.75rem;
    font-size: 0.8rem;
  }
`;

const TypingIndicator = styled.div`
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 1rem 1.5rem;
  background: ${theme.cardBackground};
  border: 1px solid ${theme.borderColor};
  border-radius: 1.5rem;
  align-self: flex-start;
  max-width: 200px;
  box-shadow: ${theme.boxShadow};
  
  @media (max-width: 480px) {
    padding: 0.75rem 1rem;
    max-width: 150px;
  }
`;

const TypingDot = styled.div`
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: ${theme.secondaryTextColor};
  animation: ${pulse} 1.5s infinite;
  
  &:nth-child(1) {
    animation-delay: 0s;
  }
  
  &:nth-child(2) {
    animation-delay: 0.5s;
  }
  
  &:nth-child(3) {
    animation-delay: 1s;
  }
  
  @media (max-width: 480px) {
    width: 6px;
    height: 6px;
  }
`;

// Enhanced AI Response Components
const ProjectSuggestionCard = styled.div`
  background: ${theme.secondaryGradient};
  border: 1px solid #bae6fd;
  border-radius: 0.75rem;
  padding: 1.5rem;
  margin: 1rem 0;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  animation: ${scaleIn} 0.3s ease-out;
  transition: all 0.3s ease;
  
  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1);
  }
  
  @media (max-width: 768px) {
    padding: 1.25rem;
  }
  
  @media (max-width: 480px) {
    padding: 1rem;
  }
`;

const ProjectSuggestionHeader = styled.div`
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 1rem;
`;

const ProjectSuggestionTitle = styled.h3`
  font-size: 1.25rem;
  font-weight: 600;
  color: #0369a1;
  margin: 0;
  
  @media (max-width: 480px) {
    font-size: 1.1rem;
  }
`;

const ProjectDetailsGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  margin-bottom: 1.5rem;
  
  @media (max-width: 480px) {
    grid-template-columns: 1fr;
    gap: 0.75rem;
  }
`;

const ProjectDetailItem = styled.div`
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
`;

const ProjectDetailLabel = styled.span`
  font-size: 0.875rem;
  color: ${theme.secondaryTextColor};
  font-weight: 500;
`;

const ProjectDetailValue = styled.span`
  font-size: 1rem;
  font-weight: 600;
  color: #0369a1;
  
  @media (max-width: 480px) {
    font-size: 0.9rem;
  }
`;

const ProjectActionsContainer = styled.div`
  display: flex;
  gap: 1rem;
  margin-top: 1rem;
  flex-wrap: wrap;
  
  @media (max-width: 480px) {
    flex-direction: column;
    gap: 0.5rem;
  }
`;

const ProjectActionButton = styled.button`
  background: linear-gradient(135deg, #0ea5e9 0%, #0284c7 100%);
  color: white;
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
    box-shadow: 0 4px 12px rgba(14, 165, 233, 0.3);
  }
  
  &.secondary {
    background: #f1f5f9;
    color: ${theme.textColor};
    
    &:hover {
      background: #e2e8f0;
      transform: translateY(-2px);
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    }
  }
  
  @media (max-width: 480px) {
    padding: 0.5rem 1rem;
    font-size: 0.9rem;
    width: 100%;
    justify-content: center;
  }
`;

const ErrorMessage = styled.div`
  background: #fee2e2;
  border: 1px solid #fecaca;
  color: #dc2626;
  padding: 1rem;
  border-radius: 0.75rem;
  margin: 1rem 0;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  
  @media (max-width: 480px) {
    padding: 0.75rem;
    font-size: 0.9rem;
  }
`;

const SuccessMessage = styled.div`
  background: #dcfce7;
  border: 1px solid #bbf7d0;
  color: #16a34a;
  padding: 1rem;
  border-radius: 0.75rem;
  margin: 1rem 0;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  
  @media (max-width: 480px) {
    padding: 0.75rem;
    font-size: 0.9rem;
  }
`;

// AI Studio-like Analysis Card
const AnalysisCard = styled.div`
  background: ${theme.secondaryGradient};
  border: 1px solid #bae6fd;
  border-radius: 0.75rem;
  padding: 1.5rem;
  margin: 1rem 0;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  animation: ${scaleIn} 0.3s ease-out;
  transition: all 0.3s ease;
  
  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1);
  }
  
  @media (max-width: 768px) {
    padding: 1.25rem;
  }
  
  @media (max-width: 480px) {
    padding: 1rem;
  }
`;

const AnalysisHeader = styled.div`
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 1rem;
`;

const AnalysisTitle = styled.h3`
  font-size: 1.25rem;
  font-weight: 600;
  color: #0369a1;
  margin: 0;
  
  @media (max-width: 480px) {
    font-size: 1.1rem;
  }
`;

const AnalysisGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  margin-bottom: 1.5rem;
  
  @media (max-width: 480px) {
    grid-template-columns: 1fr;
    gap: 0.75rem;
  }
`;

const AnalysisItem = styled.div`
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
`;

const AnalysisLabel = styled.span`
  font-size: 0.875rem;
  color: ${theme.secondaryTextColor};
  font-weight: 500;
`;

const AnalysisValue = styled.span`
  font-size: 1rem;
  font-weight: 600;
  color: #0369a1;
  
  @media (max-width: 480px) {
    font-size: 0.9rem;
  }
`;

const FeaturesList = styled.ul`
  margin: 1rem 0;
  padding-left: 1.5rem;
  
  @media (max-width: 480px) {
    padding-left: 1rem;
  }
`;

const FeatureItem = styled.li`
  margin-bottom: 0.5rem;
  color: #0369a1;
  
  @media (max-width: 480px) {
    font-size: 0.9rem;
  }
`;

const TechStackGrid = styled.div`
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-top: 0.5rem;
`;

const TechTag = styled.span`
  background: #dbeafe;
  color: #1d4ed8;
  padding: 0.25rem 0.75rem;
  border-radius: 2rem;
  font-size: 0.8rem;
  font-weight: 500;
  
  @media (max-width: 480px) {
    padding: 0.2rem 0.6rem;
    font-size: 0.75rem;
  }
`;

// Project Generation Components
const ProjectGenerationCard = styled.div`
  background: ${theme.successGradient};
  border: 1px solid #bbf7d0;
  border-radius: 0.75rem;
  padding: 1.5rem;
  margin: 1rem 0;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  animation: ${scaleIn} 0.3s ease-out;
  transition: all 0.3s ease;
  
  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1);
  }
  
  @media (max-width: 768px) {
    padding: 1.25rem;
  }
  
  @media (max-width: 480px) {
    padding: 1rem;
  }
`;

const ProjectGenerationHeader = styled.div`
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 1rem;
`;

const ProjectGenerationTitle = styled.h3`
  font-size: 1.25rem;
  font-weight: 600;
  color: #15803d;
  margin: 0;
  
  @media (max-width: 480px) {
    font-size: 1.1rem;
  }
`;

const ProjectGenerationActions = styled.div`
  display: flex;
  gap: 1rem;
  margin-top: 1rem;
  flex-wrap: wrap;
  
  @media (max-width: 480px) {
    flex-direction: column;
    gap: 0.5rem;
  }
`;

const ProjectGenerationButton = styled.button`
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  color: white;
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
    box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
  }
  
  &.secondary {
    background: #f1f5f9;
    color: ${theme.textColor};
    
    &:hover {
      background: #e2e8f0;
      transform: translateY(-2px);
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    }
  }
  
  @media (max-width: 480px) {
    padding: 0.5rem 1rem;
    font-size: 0.9rem;
    width: 100%;
    justify-content: center;
  }
`;

function AIChat() {
  const navigate = useNavigate();
  const [messages, setMessages] = useState([
    {
      id: 1,
      role: 'ai',
      content: 'Hello! I\'m your AI assistant. How can I help you build your next application today?',
      timestamp: new Date()
    }
  ]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [chatHistory, setChatHistory] = useState([
    { id: 1, title: 'New Chat', timestamp: new Date() }
  ]);
  const [activeChat, setActiveChat] = useState(1);
  const chatContainerRef = useRef(null);
  const textareaRef = useRef(null);

  useEffect(() => {
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight;
    }
  }, [messages]);

  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = `${Math.min(textareaRef.current.scrollHeight, 200)}px`;
    }
  }, [inputValue]);

  const quickSuggestions = [
    "Create a dashboard with charts and analytics",
    "Build an e-commerce store with payment integration",
    "Make a blog with CMS and user authentication",
    "Develop a real-time chat application",
    "Design a CRM system with customer management",
    "Generate a task management app with team collaboration",
    "Create a social media platform with posts and likes",
    "Build an inventory management system for warehouses"
  ];

  const handleSendMessage = async () => {
    if (!inputValue.trim() || isLoading) return;

    const userMessage = {
      id: Date.now(),
      role: 'user',
      content: inputValue,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      // Check if the user is asking to generate a project
      if (inputValue.toLowerCase().includes('generate') || 
          inputValue.toLowerCase().includes('create') || 
          inputValue.toLowerCase().includes('build') ||
          inputValue.toLowerCase().includes('make') ||
          inputValue.toLowerCase().includes('develop')) {
        // Analyze the request and provide project generation options
        const analysisResponse = await aiChatService.analyzeRequirements(inputValue);
        
        const analysis = analysisResponse.analysis;
        
        // Create a detailed analysis card like Google AI Studio
        const analysisCard = (
          <AnalysisCard>
            <AnalysisHeader>
              <Sparkles size={20} color="#0369a1" />
              <AnalysisTitle>Project Analysis</AnalysisTitle>
            </AnalysisHeader>
            
            <AnalysisGrid>
              <AnalysisItem>
                <AnalysisLabel>Project Type</AnalysisLabel>
                <AnalysisValue>{analysis.project_type || 'Web Application'}</AnalysisValue>
              </AnalysisItem>
              
              <AnalysisItem>
                <AnalysisLabel>Complexity</AnalysisLabel>
                <AnalysisValue>{analysis.complexity || 'Medium'}</AnalysisValue>
              </AnalysisItem>
              
              <AnalysisItem>
                <AnalysisLabel>Estimated Time</AnalysisLabel>
                <AnalysisValue>{analysisResponse.estimated_time || '2-5 minutes'}</AnalysisValue>
              </AnalysisItem>
            </AnalysisGrid>
            
            <h4>Tech Stack Recommendation:</h4>
            <TechStackGrid>
              <TechTag>Frontend: {analysis.tech_recommendations?.frontend || 'React'}</TechTag>
              <TechTag>Backend: {analysis.tech_recommendations?.backend || 'FastAPI'}</TechTag>
              <TechTag>Database: {analysis.tech_recommendations?.database || 'MySQL'}</TechTag>
            </TechStackGrid>
            
            <h4>Key Features:</h4>
            <FeaturesList>
              {(analysis.features || ['User Authentication', 'Responsive Design', 'API Integration']).map((feature, index) => (
                <FeatureItem key={index}>{feature}</FeatureItem>
              ))}
            </FeaturesList>
            
            <ProjectGenerationActions>
              <ProjectGenerationButton onClick={() => handleGenerateProject(inputValue, analysis)}>
                <Play size={16} />
                Generate Project
              </ProjectGenerationButton>
              <ProjectGenerationButton className="secondary" onClick={() => handleAskForModifications(analysisResponse)}>
                <Edit3 size={16} />
                Modify Requirements
              </ProjectGenerationButton>
            </ProjectGenerationActions>
          </AnalysisCard>
        );
        
        const aiResponse = {
          id: Date.now() + 1,
          role: 'ai',
          content: analysisCard,
          timestamp: new Date(),
          type: 'analysis'
        };
        
        setMessages(prev => [...prev, aiResponse]);
        setIsLoading(false);
        return;
      }
      
      // Use the actual AI service for regular chat
      const response = await aiChatService.sendMessage(inputValue, {
        history: messages.slice(-5) // Send last 5 messages as context
      });
      
      const aiResponse = {
        id: Date.now() + 1,
        role: 'ai',
        content: response.response || 'I understand your request. How can I help you build your application?',
        timestamp: new Date()
      };
      
      setMessages(prev => [...prev, aiResponse]);
      setIsLoading(false);
    } catch (error) {
      console.error('Error sending message:', error);
      const errorMessage = {
        id: Date.now() + 1,
        role: 'ai',
        content: (
          <ErrorMessage>
            <AlertCircle size={20} />
            Sorry, I encountered an error processing your request. Please try again.
          </ErrorMessage>
        ),
        timestamp: new Date(),
        type: 'error'
      };
      setMessages(prev => [...prev, errorMessage]);
      setIsLoading(false);
    }
  };

  const handleAskForModifications = (analysisResponse) => {
    const modificationPrompt = `I'd like to modify the project requirements. Here's what I'd like to change:
    
1. Different tech stack preferences
2. Additional features
3. Specific design requirements

Please ask me questions to better understand my needs.`;
    
    setInputValue(modificationPrompt);
    textareaRef.current?.focus();
  };

  const handleGenerateProject = async (projectDescription, analysis) => {
    setIsLoading(true);
    
    try {
      // Show a project generation card
      const generationCard = (
        <ProjectGenerationCard>
          <ProjectGenerationHeader>
            <Zap size={20} color="#15803d" />
            <ProjectGenerationTitle>Generating Your Project</ProjectGenerationTitle>
          </ProjectGenerationHeader>
          
          <p>Creating your {analysis.project_type || 'application'} with the following specifications:</p>
          
          <AnalysisGrid>
            <AnalysisItem>
              <AnalysisLabel>Name</AnalysisLabel>
              <AnalysisValue>{projectDescription.substring(0, 30) + (projectDescription.length > 30 ? '...' : '')}</AnalysisValue>
            </AnalysisItem>
            
            <AnalysisItem>
              <AnalysisLabel>Tech Stack</AnalysisLabel>
              <AnalysisValue>
                {analysis.tech_recommendations?.frontend || 'React'} + 
                {analysis.tech_recommendations?.backend || 'FastAPI'} + 
                {analysis.tech_recommendations?.database || 'MySQL'}
              </AnalysisValue>
            </AnalysisItem>
          </AnalysisGrid>
          
          <p>This will take just a moment. Once complete, you'll be able to view the code and demo.</p>
          
          <ProjectGenerationActions>
            <ProjectGenerationButton onClick={() => navigate('/builder')}>
              <ExternalLink size={16} />
              View in Builder
            </ProjectGenerationButton>
          </ProjectGenerationActions>
        </ProjectGenerationCard>
      );
      
      const generationMessage = {
        id: Date.now() + 1,
        role: 'ai',
        content: generationCard,
        timestamp: new Date(),
        type: 'generation'
      };
      
      setMessages(prev => [...prev, generationMessage]);
      
      // Navigate to the builder page after a short delay
      setTimeout(() => {
        navigate('/builder', { 
          state: { 
            userPrompt: projectDescription,
            projectAnalysis: analysis
          }
        });
      }, 3000);
    } catch (error) {
      console.error('Error generating project:', error);
      const errorMessage = {
        id: Date.now() + 1,
        role: 'ai',
        content: (
          <ErrorMessage>
            <AlertCircle size={20} />
            Sorry, I encountered an error generating your project. Please try again.
          </ErrorMessage>
        ),
        timestamp: new Date(),
        type: 'error'
      };
      setMessages(prev => [...prev, errorMessage]);
      setIsLoading(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const handleNewChat = () => {
    const newChat = {
      id: Date.now(),
      title: 'New Chat',
      timestamp: new Date()
    };
    setChatHistory(prev => [newChat, ...prev]);
    setActiveChat(newChat.id);
    setMessages([
      {
        id: 1,
        role: 'ai',
        content: 'Hello! I\'m your AI assistant. How can I help you build your next application today?',
        timestamp: new Date()
      }
    ]);
  };

  const handleSuggestionClick = (suggestion) => {
    setInputValue(suggestion);
    textareaRef.current?.focus();
  };

  const handleCopyMessage = (content) => {
    // If content is a React element, we need to extract the text
    let textToCopy = content;
    if (typeof content === 'object' && content.props) {
      // This is a React element, extract text content
      textToCopy = content.props.children || '';
    }
    navigator.clipboard.writeText(textToCopy);
    // In a real implementation, you would show a toast notification
  };

  const handleLikeMessage = (messageId) => {
    // In a real implementation, you would send feedback to the backend
    console.log(`Message ${messageId} liked`);
  };

  const handleRegenerateResponse = async (messageId) => {
    // Find the last user message before this AI response
    const messageIndex = messages.findIndex(msg => msg.id === messageId);
    if (messageIndex > 0) {
      const userMessage = messages[messageIndex - 1];
      if (userMessage.role === 'user') {
        // Remove the current AI response and regenerate
        setMessages(prev => prev.slice(0, messageIndex));
        
        // Simulate typing delay
        setTimeout(() => {
          setIsLoading(true);
          
          // Use the actual AI service
          aiChatService.sendMessage(userMessage.content, {
            history: messages.slice(0, messageIndex - 1).slice(-5)
          }).then(response => {
            const aiResponse = {
              id: Date.now(),
              role: 'ai',
              content: response.response || 'I understand your request. How can I help you build your application?',
              timestamp: new Date()
            };
            setMessages(prev => [...prev, aiResponse]);
            setIsLoading(false);
          }).catch(error => {
            console.error('Error regenerating response:', error);
            const errorMessage = {
              id: Date.now(),
              role: 'ai',
              content: (
                <ErrorMessage>
                  <AlertCircle size={20} />
                  Sorry, I encountered an error regenerating the response. Please try again.
                </ErrorMessage>
              ),
              timestamp: new Date(),
              type: 'error'
            };
            setMessages(prev => [...prev, errorMessage]);
            setIsLoading(false);
          });
        }, 500);
      }
    }
  };

  const handleDislikeMessage = (messageId) => {
    // In a real implementation, you would send feedback to the backend
    console.log(`Message ${messageId} disliked`);
  };

  return (
    <Container>
      <Sidebar isOpen={sidebarOpen}>
        <SidebarHeader>
          <SidebarTitle>Chat History</SidebarTitle>
          <CloseButton onClick={() => setSidebarOpen(false)}>
            <X size={20} />
          </CloseButton>
        </SidebarHeader>
        
        <NewChatButton onClick={handleNewChat}>
          <Plus size={16} />
          New Chat
        </NewChatButton>
        
        <ChatHistory>
          {chatHistory.map(chat => (
            <ChatItem 
              key={chat.id} 
              className={chat.id === activeChat ? 'active' : ''}
              onClick={() => setActiveChat(chat.id)}
            >
              <MessageSquare size={16} />
              <span>{chat.title}</span>
            </ChatItem>
          ))}
        </ChatHistory>
      </Sidebar>
      
      <MainContent>
        <Header>
          <MenuButton onClick={() => setSidebarOpen(true)}>
            <Menu size={20} />
          </MenuButton>
          <div>
            <Title>
              <Bot size={24} />
              AI Chat Assistant
            </Title>
            <Subtitle>Ask me anything about building applications</Subtitle>
          </div>
        </Header>
        
        <ChatContainer ref={chatContainerRef}>
          {messages.map(message => (
            <Message key={message.id} role={message.role}>
              <Avatar className="avatar">
                {message.role === 'user' ? <User size={20} /> : <Bot size={20} />}
              </Avatar>
              <MessageContent>
                {typeof message.content === 'string' ? (
                  <div dangerouslySetInnerHTML={{ __html: message.content.replace(/\n/g, '<br />') }} />
                ) : (
                  message.content
                )}
                {message.role === 'ai' && message.type !== 'error' && message.type !== 'success' && (
                  <MessageActions>
                    <ActionButton onClick={() => handleCopyMessage(message.content)}>
                      <Copy size={14} />
                      Copy
                    </ActionButton>
                    <ActionButton onClick={() => handleLikeMessage(message.id)}>
                      <ThumbsUp size={14} />
                      Helpful
                    </ActionButton>
                    <ActionButton onClick={() => handleDislikeMessage(message.id)}>
                      <ThumbsDown size={14} />
                      Not Helpful
                    </ActionButton>
                    <ActionButton onClick={() => handleRegenerateResponse(message.id)}>
                      <RefreshCw size={14} />
                      Regenerate
                    </ActionButton>
                  </MessageActions>
                )}
              </MessageContent>
            </Message>
          ))}
          
          {isLoading && (
            <Message role="ai">
              <Avatar className="avatar">
                <Bot size={20} />
              </Avatar>
              <TypingIndicator>
                <TypingDot />
                <TypingDot />
                <TypingDot />
              </TypingIndicator>
            </Message>
          )}
        </ChatContainer>
        
        <QuickSuggestions>
          {quickSuggestions.map((suggestion, index) => (
            <SuggestionButton 
              key={index} 
              onClick={() => handleSuggestionClick(suggestion)}
            >
              {suggestion}
            </SuggestionButton>
          ))}
        </QuickSuggestions>
        
        <InputContainer>
          <InputWrapper>
            <Input
              ref={textareaRef}
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Message AI assistant... (Press Enter to send, Shift+Enter for new line)"
              disabled={isLoading}
            />
            <SendButton 
              onClick={handleSendMessage} 
              disabled={!inputValue.trim() || isLoading}
            >
              {isLoading ? <Loader size={20} /> : <Send size={20} />}
            </SendButton>
          </InputWrapper>
        </InputContainer>
      </MainContent>
    </Container>
  );
}

export default AIChat;