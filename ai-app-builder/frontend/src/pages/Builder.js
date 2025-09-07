import React, { useState, useRef, useEffect } from 'react';
import styled, { keyframes } from 'styled-components';
import { 
  Sparkles, 
  Bot, 
  Zap, 
  Code, 
  Database, 
  Cloud, 
  Rocket, 
  ArrowRight,
  Send,
  Loader,
  CheckCircle,
  AlertCircle,
  Download,
  Play,
  Settings,
  MessageSquare,
  Layout,
  Palette,
  Layers,
  Globe,
  Smartphone,
  ShoppingCart,
  BarChart3,
  MessageCircle,
  Users,
  FileText,
  Cog,
  ChevronDown,
  Star,
  Cpu,
  Clock,
  Wifi,
  Lightbulb,
  Wand2,
  GitBranch,
  Server,
  HardDrive,
  MousePointerClick,
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
  ExternalLink,
  Monitor,
  Tablet,
  Smartphone as Mobile,
  Search,
  Filter,
  Grid,
  List,
  RefreshCw,
  Check,
  X,
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
import { useLocation, useNavigate } from 'react-router-dom';
import toast from 'react-hot-toast';
import frameworkService from '../services/frameworkService';
import templateService from '../services/templateService';
import realtimeProjectService from '../services/realtimeProjectService';
import aiChatService from '../services/aiChatService';
import api from '../services/api';
import '../test-api.js'; // Test API connection

// Consistent color palette and styling across all components
const theme = {
  primaryGradient: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
  secondaryGradient: 'linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%)',
  successGradient: 'linear-gradient(135deg, #10b981 0%, #059669 100%)',
  cardBackground: 'white',
  borderColor: '#e2e8f0',
  boxShadow: '0 4px 15px rgba(0, 0, 0, 0.05)',
  borderRadius: '1rem',
  textColor: '#1e293b',
  secondaryTextColor: '#64748b'
};

// Enhanced animations
const pulse = keyframes`
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.7; transform: scale(1.05); }
`;

const slideUp = keyframes`
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
`;

const rotate = keyframes`
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
`;

const fadeInUp = keyframes`
  from { opacity: 0; transform: translateY(30px); }
  to { opacity: 1; transform: translateY(0); }
`;

const typing = keyframes`
  from { width: 0; }
  to { width: 100%; }
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

// Additional animations for smoother experience
const fadeIn = keyframes`
  from { opacity: 0; }
  to { opacity: 1; }
`;

const scaleIn = keyframes`
  from { opacity: 0; transform: scale(0.95); }
  to { opacity: 1; transform: scale(1); }
`;

const slideInLeft = keyframes`
  from { opacity: 0; transform: translateX(-20px); }
  to { opacity: 1; transform: translateX(0); }
`;

const slideInRight = keyframes`
  from { opacity: 0; transform: translateX(20px); }
  to { opacity: 1; transform: translateX(0); }
`;

// Enhanced container with gradient background
const Container = styled.div`
  min-height: 100vh;
  background: linear-gradient(135deg, #f0f4f8 0%, #e6f7ff 100%);
  padding: 2rem;
  position: relative;
  overflow: hidden;
  
  &::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0) 70%);
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
  background: ${theme.primaryGradient};
  color: white;
  padding: 3rem 2rem;
  text-align: center;
  border-radius: 1.5rem;
  margin-bottom: 2rem;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
  position: relative;
  overflow: hidden;
  z-index: 1;
  
  &::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0) 70%);
    animation: ${rotate} 20s linear infinite;
  }
  
  @media (max-width: 768px) {
    padding: 2rem 1rem;
    border-radius: 1rem;
  }
  
  @media (max-width: 480px) {
    padding: 1.5rem 0.75rem;
    margin-bottom: 1rem;
  }
`;

const Title = styled.h1`
  font-size: 3rem;
  font-weight: 800;
  margin-bottom: 1rem;
  background: linear-gradient(45deg, #fff, #e2e8f0);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  position: relative;
  z-index: 2;
  
  @media (max-width: 768px) {
    font-size: 2.2rem;
  }
  
  @media (max-width: 480px) {
    font-size: 1.8rem;
  }
`;

const Subtitle = styled.p`
  font-size: 1.25rem;
  opacity: 0.9;
  max-width: 700px;
  margin: 0 auto 1.5rem;
  position: relative;
  z-index: 2;
  
  @media (max-width: 768px) {
    font-size: 1rem;
  }
  
  @media (max-width: 480px) {
    font-size: 0.9rem;
  }
`;

const FeatureHighlights = styled.div`
  display: flex;
  justify-content: center;
  gap: 2rem;
  margin-top: 1.5rem;
  flex-wrap: wrap;
  position: relative;
  z-index: 2;
  
  @media (max-width: 768px) {
    gap: 1rem;
  }
  
  @media (max-width: 480px) {
    gap: 0.5rem;
  }
`;

const FeatureItem = styled.div`
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.9rem;
  opacity: 0.9;
  
  @media (max-width: 480px) {
    font-size: 0.8rem;
  }
`;

// Main layout
const MainContent = styled.div`
  display: flex;
  gap: 2rem;
  position: relative;
  z-index: 1;
  
  @media (max-width: 1024px) {
    flex-direction: column;
  }
  
  @media (max-width: 768px) {
    gap: 1rem;
  }
  
  @media (max-width: 480px) {
    gap: 0.5rem;
  }
`;

const BuilderSection = styled.div`
  flex: 1;
`;

const Sidebar = styled.div`
  width: 350px;
  background: ${theme.cardBackground};
  border-radius: ${theme.borderRadius};
  padding: 1.5rem;
  box-shadow: ${theme.boxShadow};
  border: 1px solid ${theme.borderColor};
  height: fit-content;
  
  @media (max-width: 1024px) {
    width: 100%;
  }
  
  @media (max-width: 768px) {
    padding: 1rem;
  }
  
  @media (max-width: 480px) {
    padding: 0.75rem;
  }
`;

const SectionTitle = styled.h2`
  font-size: 1.25rem;
  font-weight: 600;
  color: ${theme.textColor};
  margin: 0 0 1.5rem 0;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  
  @media (max-width: 480px) {
    font-size: 1.1rem;
  }
`;

// Enhanced prompt input section
const PromptSection = styled.div`
  background: ${theme.cardBackground};
  border-radius: ${theme.borderRadius};
  padding: 1.5rem;
  margin-bottom: 2rem;
  border: 1px solid ${theme.borderColor};
  box-shadow: ${theme.boxShadow};
  animation: ${fadeInUp} 0.5s ease-out;
  
  @media (max-width: 768px) {
    padding: 1.25rem;
  }
  
  @media (max-width: 480px) {
    padding: 1rem;
    margin-bottom: 1rem;
  }
`;

const PromptHeader = styled.div`
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 1rem;
  
  @media (max-width: 480px) {
    gap: 0.5rem;
  }
`;

const PromptTitle = styled.h3`
  font-size: 1.25rem;
  font-weight: 600;
  color: ${theme.textColor};
  margin: 0;
  
  @media (max-width: 480px) {
    font-size: 1.1rem;
  }
`;

const PromptInput = styled.textarea`
  width: 100%;
  min-height: 120px;
  padding: 1.25rem;
  border: 1px solid ${theme.borderColor};
  border-radius: 0.75rem;
  font-size: 1rem;
  font-family: inherit;
  resize: vertical;
  transition: all 0.2s ease;
  
  &:focus {
    outline: none;
    border-color: #667eea;
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
  }
  
  @media (max-width: 768px) {
    padding: 1rem;
    font-size: 0.9rem;
  }
  
  @media (max-width: 480px) {
    padding: 0.75rem;
    font-size: 0.85rem;
    min-height: 100px;
  }
`;

const PromptActions = styled.div`
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 1rem;
  
  @media (max-width: 480px) {
    gap: 0.5rem;
    flex-direction: column;
  }
`;

const SecondaryButton = styled.button`
  background: #f1f5f9;
  border: none;
  padding: 0.875rem 1.5rem;
  border-radius: 0.75rem;
  font-size: 1rem;
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
  
  &:disabled {
    opacity: 0.7;
    cursor: not-allowed;
  }
  
  @media (max-width: 768px) {
    padding: 0.75rem 1.25rem;
    font-size: 0.9rem;
  }
  
  @media (max-width: 480px) {
    padding: 0.5rem 1rem;
    font-size: 0.85rem;
  }
`;

const ActionButton = styled.button`
  background: ${theme.primaryGradient};
  color: white;
  border: none;
  padding: 0.875rem 1.5rem;
  border-radius: 0.75rem;
  font-weight: 500;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: all 0.2s ease;
  
  &:hover:not(:disabled) {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
  }
  
  &:disabled {
    opacity: 0.7;
    cursor: not-allowed;
    transform: none;
  }
  
  @media (max-width: 768px) {
    padding: 0.75rem 1.25rem;
    font-size: 0.9rem;
  }
  
  @media (max-width: 480px) {
    padding: 0.5rem 1rem;
    font-size: 0.85rem;
  }
`;

// Preview section
const PreviewSection = styled.div`
  background: ${theme.cardBackground};
  border-radius: ${theme.borderRadius};
  padding: 1.5rem;
  margin-top: 2rem;
  border: 1px solid ${theme.borderColor};
  box-shadow: ${theme.boxShadow};
  animation: ${fadeInUp} 0.5s ease-out;
  
  @media (max-width: 768px) {
    padding: 1.25rem;
  }
  
  @media (max-width: 480px) {
    padding: 1rem;
  }
`;

const PreviewHeader = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  
  @media (max-width: 480px) {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
  }
`;

const PreviewTitle = styled.h3`
  font-size: 1.25rem;
  font-weight: 600;
  color: ${theme.textColor};
  margin: 0;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  
  @media (max-width: 480px) {
    font-size: 1.1rem;
  }
`;

const PreviewActions = styled.div`
  display: flex;
  gap: 0.75rem;
  
  @media (max-width: 480px) {
    width: 100%;
    justify-content: flex-end;
  }
`;

const PreviewButton = styled.button`
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
  
  @media (max-width: 480px) {
    padding: 0.4rem 0.8rem;
    font-size: 0.8rem;
  }
`;

const PreviewContent = styled.div`
  background: #f8fafc;
  border-radius: 0.75rem;
  padding: 1.5rem;
  min-height: 200px;
  border: 1px dashed #cbd5e1;
  
  @media (max-width: 768px) {
    padding: 1.25rem;
  }
  
  @media (max-width: 480px) {
    padding: 1rem;
  }
`;

const ProjectInfo = styled.div`
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-top: 1.5rem;
  
  @media (max-width: 480px) {
    gap: 0.75rem;
  }
`;

const InfoRow = styled.div`
  display: flex;
  justify-content: space-between;
  padding: 0.75rem 0;
  border-bottom: 1px solid #f1f5f9;
  
  &:last-child {
    border-bottom: none;
  }
  
  @media (max-width: 480px) {
    flex-direction: column;
    gap: 0.25rem;
  }
`;

const InfoLabel = styled.span`
  font-weight: 500;
  color: ${theme.textColor};
  
  @media (max-width: 480px) {
    font-size: 0.9rem;
  }
`;

const InfoValue = styled.span`
  color: ${theme.secondaryTextColor};
  display: flex;
  align-items: center;
  gap: 0.5rem;
  
  @media (max-width: 480px) {
    font-size: 0.9rem;
  }
`;

// Progress tracking
const ProgressCard = styled.div`
  background: ${theme.cardBackground};
  border-radius: ${theme.borderRadius};
  padding: 1.5rem;
  box-shadow: ${theme.boxShadow};
  border: 1px solid ${theme.borderColor};
  
  @media (max-width: 768px) {
    padding: 1.25rem;
  }
  
  @media (max-width: 480px) {
    padding: 1rem;
  }
`;

const ProgressStep = styled.div`
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem 0;
  border-bottom: 1px solid #f1f5f9;
  animation: ${slideInLeft} 0.3s ease-out;
  
  &:last-child {
    border-bottom: none;
  }
  
  &.completed {
    .step-icon {
      background: #10b981;
      color: white;
      animation: ${pulse} 2s infinite;
    }
  }
  
  &.active {
    .step-icon {
      background: #667eea;
      color: white;
      animation: ${pulse} 2s infinite;
    }
  }
  
  &.pending {
    .step-icon {
      background: #e2e8f0;
      color: #94a3b8;
    }
  }
  
  @media (max-width: 480px) {
    padding: 0.75rem 0;
  }
`;

const StepIcon = styled.div`
  width: 2rem;
  height: 2rem;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  flex-shrink: 0;
`;

// Demo Preview Components
const DemoPreview = styled.div`
  position: relative;
  border-radius: 0.75rem;
  overflow: hidden;
  margin-top: 1.5rem;
  border: 1px solid ${theme.borderColor};
  box-shadow: ${theme.boxShadow};
  background: #f8fafc;
  min-height: 300px;
  display: flex;
  flex-direction: column;
  animation: ${fadeInUp} 0.5s ease-out;
  
  @media (max-width: 768px) {
    min-height: 250px;
  }
  
  @media (max-width: 480px) {
    min-height: 200px;
  }
`;

const DemoHeader = styled.div`
  background: ${theme.primaryGradient};
  color: white;
  padding: 1rem 1.5rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  
  @media (max-width: 480px) {
    padding: 0.75rem 1rem;
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
  }
`;

const DemoTitle = styled.h3`
  font-size: 1.1rem;
  font-weight: 600;
  margin: 0;
  
  @media (max-width: 480px) {
    font-size: 1rem;
  }
`;

const DemoActions = styled.div`
  display: flex;
  gap: 0.5rem;
  
  @media (max-width: 480px) {
    width: 100%;
    justify-content: flex-end;
  }
`;

const DemoActionButton = styled.button`
  background: rgba(255, 255, 255, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.3);
  color: white;
  padding: 0.25rem 0.75rem;
  border-radius: 0.375rem;
  font-size: 0.8rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.25rem;
  transition: all 0.2s ease;
  
  &:hover {
    background: rgba(255, 255, 255, 0.3);
  }
  
  @media (max-width: 480px) {
    padding: 0.2rem 0.6rem;
    font-size: 0.75rem;
  }
`;

const DemoContent = styled.div`
  flex: 1;
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
  
  @media (max-width: 768px) {
    padding: 1.25rem;
  }
  
  @media (max-width: 480px) {
    padding: 1rem;
    gap: 0.75rem;
  }
`;

const DemoPlaceholder = styled.div`
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #94a3b8;
  font-size: 1rem;
  text-align: center;
  padding: 2rem;
  
  @media (max-width: 480px) {
    font-size: 0.9rem;
    padding: 1rem;
  }
`;

const DemoImage = styled.div`
  width: 100%;
  height: 200px;
  background: ${theme.primaryGradient};
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: 600;
  position: relative;
  border-radius: 0.5rem;
  margin-bottom: 1rem;
  
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
  
  @media (max-width: 768px) {
    height: 150px;
  }
  
  @media (max-width: 480px) {
    height: 120px;
  }
`;

// Code Preview Modal
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
  max-width: 1200px;
  max-height: 90vh;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.2);
  
  @media (max-width: 768px) {
    width: 95%;
    max-height: 85vh;
  }
  
  @media (max-width: 480px) {
    width: 98%;
    max-height: 80vh;
  }
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
  overflow: hidden;
  display: flex;
  
  @media (max-width: 768px) {
    flex-direction: column;
  }
`;

const FileTabs = styled.div`
  width: 250px;
  border-right: 1px solid ${theme.borderColor};
  overflow-y: auto;
  background: #f8fafc;
  
  @media (max-width: 768px) {
    width: 100%;
    border-right: none;
    border-bottom: 1px solid ${theme.borderColor};
    max-height: 200px;
  }
`;

const TabList = styled.div`
  display: flex;
  flex-direction: column;
`;

const Tab = styled.button`
  padding: 1rem;
  text-align: left;
  border: none;
  background: ${props => props.active ? 'white' : 'transparent'};
  border-left: 3px solid ${props => props.active ? '#667eea' : 'transparent'};
  cursor: pointer;
  font-size: 0.9rem;
  color: ${theme.textColor};
  transition: all 0.2s ease;
  
  &:hover {
    background: ${props => props.active ? 'white' : '#f1f5f9'};
  }
  
  @media (max-width: 480px) {
    padding: 0.75rem;
    font-size: 0.85rem;
  }
`;

const FileContent = styled.div`
  flex: 1;
  overflow-y: auto;
  padding: 1.5rem;
  background: #1e293b;
  color: #f8fafc;
  font-family: 'Monaco', 'Consolas', monospace;
  font-size: 0.9rem;
  line-height: 1.5;
  white-space: pre-wrap;
  overflow-x: auto;
  
  @media (max-width: 480px) {
    padding: 1rem;
    font-size: 0.8rem;
  }
`;

const CopyButton = styled.button`
  position: absolute;
  top: 1rem;
  right: 1rem;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 0.5rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: all 0.2s ease;
  
  &:hover {
    background: rgba(255, 255, 255, 0.2);
  }
  
  @media (max-width: 480px) {
    padding: 0.4rem 0.8rem;
    font-size: 0.85rem;
  }
`;

const CompletionSection = styled.div`
  background: ${theme.successGradient};
  border-radius: ${theme.borderRadius};
  padding: 2rem;
  margin-top: 2rem;
  color: white;
  text-align: center;
  box-shadow: 0 4px 15px rgba(16, 185, 129, 0.3);
  animation: ${fadeInUp} 0.5s ease-out;
  
  @media (max-width: 768px) {
    padding: 1.5rem;
  }
  
  @media (max-width: 480px) {
    padding: 1rem;
  }
`;

const CompletionTitle = styled.h3`
  font-size: 1.5rem;
  font-weight: 700;
  margin-bottom: 1rem;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
  
  @media (max-width: 480px) {
    font-size: 1.25rem;
  }
`;

const CompletionMessage = styled.p`
  font-size: 1.1rem;
  margin-bottom: 1.5rem;
  opacity: 0.9;
  
  @media (max-width: 480px) {
    font-size: 1rem;
  }
`;

const CompletionActions = styled.div`
  display: flex;
  justify-content: center;
  gap: 1rem;
  flex-wrap: wrap;
  
  @media (max-width: 480px) {
    flex-direction: column;
    gap: 0.5rem;
  }
`;

const CompletionButton = styled.button`
  background: rgba(255, 255, 255, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.3);
  color: white;
  padding: 0.875rem 1.5rem;
  border-radius: 0.75rem;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: all 0.2s ease;
  
  &:hover {
    background: rgba(255, 255, 255, 0.3);
    transform: translateY(-2px);
  }
  
  @media (max-width: 480px) {
    padding: 0.6rem 1rem;
    font-size: 0.9rem;
    width: 100%;
    justify-content: center;
  }
`;

// Error message styling
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
  animation: ${fadeInUp} 0.3s ease-out;
  
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
  margin: 1.5rem 0;
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

function Builder() {
  const navigate = useNavigate();
  const location = useLocation();
  const [selectedTemplate, setSelectedTemplate] = useState(null);
  const [chatMessages, setChatMessages] = useState([
    {
      type: 'ai',
      content: '👋 Hi! I\'m your AI App Builder assistant. Describe what application you want to build, or choose a template to get started!'
    }
  ]);
  const [inputMessage, setInputMessage] = useState('');
  const [isGenerating, setIsGenerating] = useState(false);
  const [currentProject, setCurrentProject] = useState(null);
  const [buildSteps, setBuildSteps] = useState([
    { id: 1, name: 'Analyze Requirements', status: 'pending' },
    { id: 2, name: 'Generate Code', status: 'pending' },
    { id: 3, name: 'Setup Database', status: 'pending' },
    { id: 4, name: 'Configure APIs', status: 'pending' },
    { id: 5, name: 'Ready to Deploy', status: 'pending' }
  ]);
  
  // New state for enhanced workflow
  const [userPrompt, setUserPrompt] = useState(location.state?.userPrompt || '');
  const [projectPreview, setProjectPreview] = useState(null);
  const [isPreviewLoading, setIsPreviewLoading] = useState(false);
  const [isProjectComplete, setIsProjectComplete] = useState(false);
  const [showCodePreview, setShowCodePreview] = useState(false);
  const [generatedCode, setGeneratedCode] = useState(null);
  const [selectedFile, setSelectedFile] = useState(null);
  const [supportedFrameworks, setSupportedFrameworks] = useState([]);
  const [selectedFramework, setSelectedFramework] = useState({
    frontend: 'react',
    backend: 'fastapi',
    database: 'mysql'
  });
  const [showAdvancedOptions, setShowAdvancedOptions] = useState(false);
  const [error, setError] = useState(null);
  const [projectAnalysis, setProjectAnalysis] = useState(location.state?.projectAnalysis || null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  
  // Load supported frameworks on component mount
  useEffect(() => {
    const loadFrameworks = async () => {
      try {
        const response = await frameworkService.getSupportedFrameworks();
        setSupportedFrameworks(response.frameworks);
      } catch (error) {
        console.error('Failed to load frameworks:', error);
        // Set default frameworks if API fails
        setSupportedFrameworks({
          frontend: ['react', 'nextjs', 'vue', 'angular'],
          backend: ['fastapi', 'express', 'nestjs', 'django'],
          database: ['mysql', 'postgresql', 'mongodb']
        });
      }
    };
    
    loadFrameworks();
    
    // Cleanup WebSocket connection on unmount
    return () => {
      if (realtimeProjectService.getIsConnected()) {
        realtimeProjectService.disconnect();
      }
    };
  }, []);

  const templates = [
    {
      id: 'dashboard',
      name: 'Analytics Dashboard',
      description: 'Business intelligence dashboard with charts, KPIs, and real-time data visualization',
      icon: BarChart3,
      features: ['Charts & Graphs', 'Real-time Data', 'User Management', 'Export Reports']
    },
    {
      id: 'ecommerce',
      name: 'E-commerce Store',
      description: 'Complete online store with product management, cart, and payment processing',
      icon: ShoppingCart,
      features: ['Product Catalog', 'Shopping Cart', 'Payment Gateway', 'Order Management']
    },
    {
      id: 'blog',
      name: 'Blog & CMS',
      description: 'Content management system with rich editor, comments, and SEO optimization',
      icon: FileText,
      features: ['Rich Text Editor', 'Comment System', 'SEO Tools', 'Media Management']
    },
    {
      id: 'chat',
      name: 'Chat Application',
      description: 'Real-time messaging platform with rooms, file sharing, and notifications',
      icon: MessageCircle,
      features: ['Real-time Chat', 'File Sharing', 'Chat Rooms', 'Push Notifications']
    },
    {
      id: 'crm',
      name: 'CRM System',
      description: 'Customer relationship management with contacts, deals, and sales pipeline',
      icon: Users,
      features: ['Contact Management', 'Sales Pipeline', 'Task Tracking', 'Reports']
    },
    {
      id: 'saas',
      name: 'SaaS Platform',
      description: 'Multi-tenant SaaS application with subscriptions and user management',
      icon: Cloud,
      features: ['Multi-tenancy', 'Subscription Billing', 'API Management', 'Analytics']
    }
  ];

  const examplePrompts = [
    "Build a task management app with team collaboration",
    "Create a social media platform with posts and likes",
    "Build an inventory management system for warehouses",
    "Create a booking system for appointments",
    "Build a learning management system for courses",
    "Create a fitness tracking app with workout plans",
    "Build a recipe sharing platform with meal planning",
    "Create a podcast app with audio streaming",
    "Build a job board with application tracking",
    "Create a crowdfunding platform for creative projects"
  ];

  const extractAppType = (message) => {
    const lowerMessage = message.toLowerCase();
    if (lowerMessage.includes('dashboard') || lowerMessage.includes('analytics')) return 'Analytics Dashboard';
    if (lowerMessage.includes('ecommerce') || lowerMessage.includes('store')) return 'E-commerce Store';
    if (lowerMessage.includes('blog') || lowerMessage.includes('cms')) return 'Blog & CMS';
    if (lowerMessage.includes('chat')) return 'Chat Application';
    if (lowerMessage.includes('crm')) return 'CRM System';
    if (lowerMessage.includes('saas')) return 'SaaS Platform';
    return 'Custom Application';
  };

  const handleAnalyzeProject = async () => {
    if (!userPrompt.trim()) {
      toast.error('Please describe your project first');
      return;
    }

    setIsAnalyzing(true);
    setError(null);
    
    try {
      // Analyze the request using AI agent
      const response = await aiChatService.analyzeRequirements(userPrompt);
      
      const analysis = response.analysis;
      
      // Set the analysis result
      setProjectAnalysis(analysis);
      setIsAnalyzing(false);
      toast.success('Project analysis completed successfully!');
    } catch (error) {
      console.error('Error analyzing project:', error);
      setError('Failed to analyze project. Please try again.');
      setIsAnalyzing(false);
    }
  };

  const handlePreviewProject = async () => {
    if (!userPrompt.trim()) {
      toast.error('Please describe your project first');
      return;
    }

    setIsPreviewLoading(true);
    setError(null);
    
    try {
      // Analyze the request using AI agent
      const response = await aiChatService.analyzeRequirements(userPrompt);
      
      const analysis = response.analysis;
      
      // Create project preview
      const preview = {
        name: userPrompt.substring(0, 30) + (userPrompt.length > 30 ? '...' : ''),
        description: analysis.description || `A ${extractAppType(userPrompt)} application with modern design and functionality`,
        features: analysis.features || [
          'User Authentication',
          'Responsive Design',
          'API Integration',
          'Database Management'
        ],
        techStack: {
          frontend: analysis.tech_recommendations?.frontend || 'React.js',
          backend: analysis.tech_recommendations?.backend || 'FastAPI',
          database: analysis.tech_recommendations?.database || 'MySQL'
        },
        estimatedTime: response.estimated_time || '2-5 minutes',
        complexity: response.complexity || 'medium'
      };
      
      setProjectPreview(preview);
      setIsPreviewLoading(false);
      toast.success('Project preview generated successfully!');
    } catch (error) {
      console.error('Error generating preview:', error);
      setError('Failed to generate project preview. Please try again.');
      setIsPreviewLoading(false);
    }
  };

  const handleCreateProject = async () => {
    if (!userPrompt.trim()) {
      toast.error('Please describe your project first');
      return;
    }

    setIsGenerating(true);
    setError(null);
    setBuildSteps(prev => prev.map(step => ({ ...step, status: 'pending' })));
    
    try {
      // First, analyze the request if we don't have analysis yet
      let analysis = projectAnalysis;
      if (!analysis) {
        const analysisResponse = await aiChatService.analyzeRequirements(userPrompt);
        analysis = analysisResponse.analysis;
        setProjectAnalysis(analysis);
      }
      
      // Update progress: Analyze Requirements
      setBuildSteps(prev => prev.map((step, index) => 
        index === 0 ? { ...step, status: 'completed' } : step
      ));
      
      // Generate the project
      const projectResponse = await aiChatService.generateCode({
        name: userPrompt.substring(0, 30) + (userPrompt.length > 30 ? '...' : ''),
        request: userPrompt,
        analysis: analysis,
        tech_stack: selectedFramework
      });
      
      // Update progress: Generate Code
      setBuildSteps(prev => prev.map((step, index) => 
        index <= 1 ? { ...step, status: 'completed' } : step
      ));
      
      // For demo purposes, we'll simulate a project creation
      const projectData = {
        name: userPrompt.substring(0, 30) + (userPrompt.length > 30 ? '...' : ''),
        type: analysis.project_type || 'web_app',
        status: 'active',
        tech_stack: selectedFramework,
        created_at: new Date().toISOString()
      };
      
      // Simulate database setup and API configuration
      setTimeout(() => {
        // Update progress: Setup Database & Configure APIs
        setBuildSteps(prev => prev.map((step, index) => 
          index <= 3 ? { ...step, status: 'completed' } : step
        ));
        
        // Project creation completed
        setIsProjectComplete(true);
        setIsGenerating(false);
        setCurrentProject(projectData);
        
        // Set generated code for preview
        setGeneratedCode({
          files: {
            'README.md': `# ${projectData.name}\n\nThis project was generated by AI App Builder.\n\n## Tech Stack\n- Frontend: ${selectedFramework.frontend}\n- Backend: ${selectedFramework.backend}\n- Database: ${selectedFramework.database}\n\n## Getting Started\n1. Install dependencies\n2. Configure environment variables\n3. Run the application`,
            'package.json': `{\n  "name": "${projectData.name.toLowerCase().replace(/\s+/g, '-')}",\n  "version": "1.0.0",\n  "description": "${projectData.name} - Generated by AI App Builder",\n  "scripts": {\n    "start": "node server.js"\n  }\n}`,
            'src/App.js': `import React from 'react';\n\nfunction App() {\n  return (\n    <div className="App">\n      <h1>${projectData.name}</h1>\n      <p>Your ${extractAppType(userPrompt)} application</p>\n    </div>\n  );\n}\n\nexport default App;`,
            'src/index.js': `import React from 'react';\nimport ReactDOM from 'react-dom';\nimport App from './App';\n\nReactDOM.render(<App />, document.getElementById('root'));`,
            'src/styles.css': `body {\n  margin: 0;\n  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',\n    'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',\n    sans-serif;\n  -webkit-font-smoothing: antialiased;\n  -moz-osx-font-smoothing: grayscale;\n}`
          }
        });
        
        // Update progress: Ready to Deploy
        setBuildSteps(prev => prev.map((step, index) => 
          index <= 4 ? { ...step, status: 'completed' } : step
        ));
        
        toast.success('Project created successfully!');
      }, 2000);
      
    } catch (error) {
      console.error('Error creating project:', error);
      setError('Failed to create project: ' + (error.response?.data?.detail || error.message));
      setIsGenerating(false);
      
      // Update progress to show error
      setBuildSteps(prev => prev.map(step => ({ ...step, status: 'pending' })));
    }
  };

  const handleViewCode = () => {
    if (generatedCode && Object.keys(generatedCode.files).length > 0) {
      setShowCodePreview(true);
      // Set first file as selected by default
      const firstFile = Object.keys(generatedCode.files)[0];
      setSelectedFile(firstFile);
    } else {
      toast.error('No code available to view');
    }
  };

  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text);
    toast.success('Copied to clipboard!');
  };

  const startBuildProcess = (message) => {
    setUserPrompt(message);
    // In a real implementation, this would trigger the actual build process
    setTimeout(() => {
      setIsProjectComplete(true);
      setGeneratedCode({
        files: {
          'App.js': `import React from 'react';\n\nfunction App() {\n  return (\n    <div className="App">\n      <h1>${extractAppType(message)}</h1>\n      <p>Your ${extractAppType(message)} application</p>\n    </div>\n  );\n}\n\nexport default App;`,
          'index.js': `import React from 'react';\nimport ReactDOM from 'react-dom';\nimport App from './App';\n\nReactDOM.render(<App />, document.getElementById('root'));`,
          'styles.css': `body {\n  margin: 0;\n  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',\n    'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',\n    sans-serif;\n  -webkit-font-smoothing: antialiased;\n  -moz-osx-font-smoothing: grayscale;\n}`
        }
      });
    }, 3000);
  };

  const handleViewDemo = () => {
    // In a real implementation, this would open a preview of the generated application
    toast.success('Demo preview would open in a new window');
  };

  const handleDownloadProject = () => {
    // In a real implementation, this would download the generated project files
    toast.success('Project download would start');
  };

  return (
    <Container>
      <Header>
        <Title>AI App Builder</Title>
        <Subtitle>Describe your idea, preview the plan, and generate a complete application in minutes</Subtitle>
        <FeatureHighlights>
          <FeatureItem>
            <Sparkles size={16} />
            <span>AI-Powered Generation</span>
          </FeatureItem>
          <FeatureItem>
            <Zap size={16} />
            <span>Real-time Preview</span>
          </FeatureItem>
          <FeatureItem>
            <Code size={16} />
            <span>Production-ready Code</span>
          </FeatureItem>
        </FeatureHighlights>
      </Header>
      
      <MainContent>
        <div>
          <BuilderSection>
            <SectionTitle>
              <Wand2 size={24} />
              Describe Your Project
            </SectionTitle>
            
            {error && (
              <ErrorMessage>
                <AlertCircle size={20} />
                {error}
              </ErrorMessage>
            )}
            
            <PromptSection>
              <PromptHeader>
                <Lightbulb size={20} />
                <PromptTitle>What would you like to build?</PromptTitle>
              </PromptHeader>
              <PromptInput
                value={userPrompt}
                onChange={(e) => setUserPrompt(e.target.value)}
                placeholder="Describe your application idea... (e.g., 'Create a task management app with team collaboration')"
              />
              <PromptActions>
                <SecondaryButton onClick={handleAnalyzeProject} disabled={isAnalyzing || !userPrompt.trim()}>
                  {isAnalyzing ? (
                    <>
                      <Loader size={16} />
                      Analyzing...
                    </>
                  ) : (
                    <>
                      <Zap size={16} />
                      Analyze Project
                    </>
                  )}
                </SecondaryButton>
                <SecondaryButton onClick={handlePreviewProject} disabled={isPreviewLoading || !userPrompt.trim()}>
                  {isPreviewLoading ? (
                    <>
                      <Loader size={16} />
                      Generating Preview...
                    </>
                  ) : (
                    <>
                      <Eye size={16} />
                      Preview Project
                    </>
                  )}
                </SecondaryButton>
                <ActionButton onClick={handleCreateProject} disabled={isGenerating || !userPrompt.trim()}>
                  {isGenerating ? (
                    <>
                      <Loader size={16} />
                      Creating Project...
                    </>
                  ) : (
                    <>
                      <Play size={16} />
                      Create Project
                    </>
                  )}
                </ActionButton>
              </PromptActions>
            </PromptSection>
            
            {projectAnalysis && (
              <AnalysisCard>
                <AnalysisHeader>
                  <Sparkles size={20} color="#0369a1" />
                  <AnalysisTitle>Project Analysis</AnalysisTitle>
                </AnalysisHeader>
                
                <AnalysisGrid>
                  <AnalysisItem>
                    <AnalysisLabel>Project Type</AnalysisLabel>
                    <AnalysisValue>{projectAnalysis.project_type || 'Web Application'}</AnalysisValue>
                  </AnalysisItem>
                  
                  <AnalysisItem>
                    <AnalysisLabel>Complexity</AnalysisLabel>
                    <AnalysisValue>{projectAnalysis.complexity || 'Medium'}</AnalysisValue>
                  </AnalysisItem>
                  
                  <AnalysisItem>
                    <AnalysisLabel>Estimated Time</AnalysisLabel>
                    <AnalysisValue>{projectAnalysis.estimated_time || '2-5 minutes'}</AnalysisValue>
                  </AnalysisItem>
                </AnalysisGrid>
                
                <h4>Tech Stack Recommendation:</h4>
                <TechStackGrid>
                  <TechTag>Frontend: {projectAnalysis.tech_recommendations?.frontend || 'React'}</TechTag>
                  <TechTag>Backend: {projectAnalysis.tech_recommendations?.backend || 'FastAPI'}</TechTag>
                  <TechTag>Database: {projectAnalysis.tech_recommendations?.database || 'MySQL'}</TechTag>
                </TechStackGrid>
                
                <h4>Key Features:</h4>
                <FeaturesList>
                  {(projectAnalysis.features || ['User Authentication', 'Responsive Design', 'API Integration']).map((feature, index) => (
                    <FeatureItem key={index}>{feature}</FeatureItem>
                  ))}
                </FeaturesList>
              </AnalysisCard>
            )}
            
            {projectPreview && (
              <PreviewSection>
                <PreviewHeader>
                  <PreviewTitle>
                    <Eye size={20} />
                    Project Preview
                  </PreviewTitle>
                  <PreviewActions>
                    <PreviewButton onClick={() => setProjectPreview(null)}>
                      <Trash2 size={16} />
                      Clear
                    </PreviewButton>
                  </PreviewActions>
                </PreviewHeader>
                <PreviewContent>
                  <h3>{projectPreview.name}</h3>
                  <p>{projectPreview.description}</p>
                  
                  <ProjectInfo>
                    <InfoRow>
                      <InfoLabel>Features:</InfoLabel>
                      <InfoValue>{projectPreview.features.join(', ')}</InfoValue>
                    </InfoRow>
                    <InfoRow>
                      <InfoLabel>Tech Stack:</InfoLabel>
                      <InfoValue>
                        {projectPreview.techStack.frontend} + {projectPreview.techStack.backend} + {projectPreview.techStack.database}
                      </InfoValue>
                    </InfoRow>
                    <InfoRow>
                      <InfoLabel>Estimated Time:</InfoLabel>
                      <InfoValue>{projectPreview.estimatedTime}</InfoValue>
                    </InfoRow>
                    <InfoRow>
                      <InfoLabel>Complexity:</InfoLabel>
                      <InfoValue>{projectPreview.complexity}</InfoValue>
                    </InfoRow>
                  </ProjectInfo>
                </PreviewContent>
              </PreviewSection>
            )}
            
            {isProjectComplete && (
              <CompletionSection>
                <CompletionTitle>
                  <CheckCircle size={24} />
                  Project Created Successfully!
                </CompletionTitle>
                <CompletionMessage>
                  Your {currentProject?.name || 'application'} has been generated and is ready to use.
                </CompletionMessage>
                <CompletionActions>
                  <CompletionButton onClick={handleViewCode}>
                    <Code size={16} />
                    View Generated Code
                  </CompletionButton>
                  <CompletionButton onClick={handleViewDemo}>
                    <ExternalLink size={16} />
                    View Demo
                  </CompletionButton>
                  <CompletionButton onClick={handleDownloadProject}>
                    <Download size={16} />
                    Download Project
                  </CompletionButton>
                  <CompletionButton onClick={() => navigate('/dashboard')}>
                    <Layout size={16} />
                    Go to Dashboard
                  </CompletionButton>
                </CompletionActions>
              </CompletionSection>
            )}
            
            {generatedCode && (
              <DemoPreview>
                <DemoHeader>
                  <DemoTitle>Application Demo Preview</DemoTitle>
                  <DemoActions>
                    <DemoActionButton onClick={handleViewDemo}>
                      <ExternalLink size={16} />
                      Open Full Demo
                    </DemoActionButton>
                    <DemoActionButton onClick={handleDownloadProject}>
                      <Download size={16} />
                      Download
                    </DemoActionButton>
                  </DemoActions>
                </DemoHeader>
                <DemoContent>
                  <DemoImage>
                    <Globe size={40} />
                  </DemoImage>
                  <p>This is a preview of your generated application. The full demo would show your complete application with all features.</p>
                  <p>Tech Stack: {selectedFramework.frontend} + {selectedFramework.backend} + {selectedFramework.database}</p>
                </DemoContent>
              </DemoPreview>
            )}
          </BuilderSection>
        </div>
        
        <Sidebar>
          <ProgressCard>
            <SectionTitle>
              <Cpu size={20} />
              Creation Progress
            </SectionTitle>
            {buildSteps.map((step) => (
              <ProgressStep key={step.id} className={step.status}>
                <StepIcon className={step.status}>
                  {step.status === 'completed' ? <Check size={16} /> : step.id}
                </StepIcon>
                <div>
                  <div style={{ fontWeight: step.status === 'active' ? '600' : 'normal' }}>
                    {step.name}
                  </div>
                </div>
              </ProgressStep>
            ))}
          </ProgressCard>
        </Sidebar>
      </MainContent>
      
      {showCodePreview && generatedCode && (
        <ModalOverlay onClick={() => setShowCodePreview(false)}>
          <ModalContent onClick={(e) => e.stopPropagation()}>
            <ModalHeader>
              <ModalTitle>Generated Code</ModalTitle>
              <CloseButton onClick={() => setShowCodePreview(false)}>
                <X size={20} />
              </CloseButton>
            </ModalHeader>
            <ModalBody>
              <FileTabs>
                <TabList>
                  {Object.keys(generatedCode.files).map((fileName) => (
                    <Tab
                      key={fileName}
                      active={selectedFile === fileName}
                      onClick={() => setSelectedFile(fileName)}
                    >
                      {fileName}
                    </Tab>
                  ))}
                </TabList>
              </FileTabs>
              <div style={{ position: 'relative', flex: 1, overflow: 'hidden' }}>
                <CopyButton onClick={() => copyToClipboard(generatedCode.files[selectedFile])}>
                  <Copy size={16} />
                  Copy
                </CopyButton>
                <FileContent>
                  {generatedCode.files[selectedFile]}
                </FileContent>
              </div>
            </ModalBody>
          </ModalContent>
        </ModalOverlay>
      )}
    </Container>
  );
}

export default Builder;