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
  Link as LinkIcon,
  // New icons for enhanced features
  Moon,
  Sun,
  Volume2,
  Mic,
  Download as DownloadIcon,
  BookOpen,
  Paperclip,
  // New icons for enhanced features
  VolumeX,
  Speech,
  Shield,
  Building,
  GitBranch,
  Cpu as CpuIcon,
  HardDrive,
  Lock,
  Unlock,
  Key,
  Bug,
  Rocket,
  Target,
  TrendingUp,
  Award,
  Star,
  Users,
  Clock,
  Calendar as CalendarIcon,
  // Additional icons for project management
  Folder,
  Layout,
  Eye as EyeIcon
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

// Additional animations for smoother experience
const slideUp = keyframes`
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
`;

const scaleIn = keyframes`
  from { opacity: 0; transform: scale(0.95); }
  to { opacity: 1; transform: scale(1); }
`;

// Theme management
const getThemeColors = (isDarkMode) => ({
  background: isDarkMode ? '#0f172a' : '#f0f4f8',
  containerBackground: isDarkMode ? '#1e293b' : '#ffffff',
  cardBackground: isDarkMode ? '#334155' : '#ffffff',
  textColor: isDarkMode ? '#f1f5f9' : '#1e293b',
  secondaryTextColor: isDarkMode ? '#94a3b8' : '#64748b',
  borderColor: isDarkMode ? '#475569' : '#e2e8f0',
  userMessageBg: isDarkMode ? '#4f46e5' : '#667eea',
  aiMessageBg: isDarkMode ? '#334155' : '#ffffff',
  inputBg: isDarkMode ? '#1e293b' : '#ffffff',
  buttonBg: isDarkMode ? '#4f46e5' : '#667eea',
  buttonHoverBg: isDarkMode ? '#6366f1' : '#7c8cff',
  successBg: isDarkMode ? '#166534' : '#dcfce7',
  warningBg: isDarkMode ? '#854d0e' : '#fef9c3',
  errorBg: isDarkMode ? '#7f1d1d' : '#fee2e2'
});

// Styled components with dark mode support
const Container = styled.div`
  display: flex;
  height: calc(100vh - 4rem);
  background: ${props => getThemeColors(props.isDarkMode).background};
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
  width: 280px; /* Reduced from 320px to 280px to reduce left spacing */
  background: ${props => getThemeColors(props.isDarkMode).cardBackground};
  border-right: 1px solid ${props => getThemeColors(props.isDarkMode).borderColor};
  padding: 1rem; /* Reduced from 1.5rem to 1rem */
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
    padding: 0.75rem; /* Reduced from 1rem */
    height: calc(100vh - 3rem);
  }
`;

const SidebarHeader = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem; /* Reduced from 1.5rem to 1rem */
  
  @media (max-width: 480px) {
    margin-bottom: 0.75rem; /* Reduced from 1rem */
  }
`;

const SidebarTitle = styled.h2`
  font-size: 1.1rem; /* Reduced from 1.25rem to 1.1rem */
  font-weight: 600;
  color: ${props => getThemeColors(props.isDarkMode).textColor};
  margin: 0;
  
  @media (max-width: 480px) {
    font-size: 1rem; /* Reduced from 1.1rem */
  }
`;

const CloseButton = styled.button`
  background: none;
  border: none;
  color: ${props => getThemeColors(props.isDarkMode).secondaryTextColor};
  cursor: pointer;
  padding: 0.5rem;
  border-radius: 0.5rem;
  
  &:hover {
    background: ${props => props.isDarkMode ? '#475569' : '#f1f5f9'};
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
  padding: 0.75rem; /* Reduced from 0.875rem to 0.75rem */
  border-radius: 0.75rem;
  font-weight: 500;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  margin-bottom: 1rem; /* Reduced from 1.5rem to 1rem */
  transition: all 0.2s ease;
  
  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
  }
  
  @media (max-width: 480px) {
    padding: 0.625rem; /* Reduced from 0.75rem */
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
  color: ${props => getThemeColors(props.isDarkMode).textColor};
  background: ${props => props.isActive ? (props.isDarkMode ? '#475569' : '#e0e7ff') : 'transparent'};
  
  &:hover {
    background: ${props => props.isDarkMode ? '#475569' : '#f1f5f9'};
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
  width: calc(100% - 280px); /* Explicitly set width to fill remaining space */
  
  @media (max-width: 768px) {
    width: 100%;
  }
`;

const Header = styled.div`
  padding: 1rem; /* Reduced from 1.5rem to 1rem */
  border-bottom: 1px solid ${props => getThemeColors(props.isDarkMode).borderColor};
  background: ${props => getThemeColors(props.isDarkMode).cardBackground};
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  display: flex;
  align-items: center;
  gap: 0.75rem; /* Reduced from 1rem to 0.75rem */
  
  @media (max-width: 480px) {
    padding: 0.75rem; /* Reduced from 1rem */
  }
`;

const MenuButton = styled.button`
  background: none;
  border: none;
  color: ${props => getThemeColors(props.isDarkMode).secondaryTextColor};
  cursor: pointer;
  padding: 0.5rem;
  border-radius: 0.5rem;
  
  &:hover {
    background: ${props => props.isDarkMode ? '#475569' : '#f1f5f9'};
  }
  
  @media (min-width: 769px) {
    display: none;
  }
  
  @media (max-width: 480px) {
    padding: 0.25rem;
  }
`;

const Title = styled.h1`
  font-size: 1.5rem; /* Reduced from 1.75rem to 1.5rem */
  font-weight: 700;
  color: ${props => getThemeColors(props.isDarkMode).textColor};
  margin: 0;
  display: flex;
  align-items: center;
  gap: 0.5rem; /* Reduced from 0.75rem to 0.5rem */
  
  @media (max-width: 768px) {
    font-size: 1.35rem; /* Reduced from 1.5rem */
  }
  
  @media (max-width: 480px) {
    font-size: 1.25rem; /* Reduced from 1.25rem */
  }
`;

const Subtitle = styled.p`
  color: ${props => getThemeColors(props.isDarkMode).secondaryTextColor};
  font-size: 0.85rem; /* Reduced from 0.9rem to 0.85rem */
  margin: 0.125rem 0 0 0; /* Reduced from 0.25rem */
  
  @media (max-width: 480px) {
    font-size: 0.75rem; /* Reduced from 0.8rem */
  }
`;

const ThemeToggle = styled.button`
  background: none;
  border: none;
  color: ${props => getThemeColors(props.isDarkMode).secondaryTextColor};
  cursor: pointer;
  padding: 0.5rem;
  border-radius: 0.5rem;
  margin-left: auto;
  
  &:hover {
    background: ${props => props.isDarkMode ? '#475569' : '#f1f5f9'};
  }
`;

const ChatContainer = styled.div`
  flex: 1;
  overflow-y: auto;
  padding: 1rem; /* Reduced from 1.5rem to 1rem */
  display: flex;
  flex-direction: column;
  background: ${props => getThemeColors(props.isDarkMode).containerBackground};
  gap: 1.25rem; /* Reduced from 1.5rem to 1.25rem */
  
  &::-webkit-scrollbar {
    width: 8px;
  }
  
  &::-webkit-scrollbar-track {
    background: ${props => props.isDarkMode ? '#1e293b' : '#f1f5f9'};
  }
  
  &::-webkit-scrollbar-thumb {
    background: ${props => props.isDarkMode ? '#64748b' : '#c7d2fe'};
    border-radius: 4px;
  }
  
  @media (max-width: 768px) {
    padding: 0.875rem; /* Reduced from 1rem */
    gap: 1rem;
  }
  
  @media (max-width: 480px) {
    padding: 0.75rem; /* Reduced from 0.75rem */
    gap: 0.875rem;
  }
`;

const Message = styled.div`
  display: flex;
  gap: 1rem; /* Reduced from 1.25rem to 1rem */
  max-width: 100%; /* Changed from 900px to 100% to use full width */
  width: 100%;
  align-self: ${props => props.role === 'user' ? 'flex-end' : 'flex-start'};
  animation: ${slideIn} 0.4s ease-out;
  
  &.user {
    flex-direction: row-reverse;
    
    .message-content {
      background: ${props => props.isDarkMode ? '#4f46e5' : '#667eea'};
      color: white;
      border-radius: 1.5rem 0.5rem 1.5rem 1.5rem;
      box-shadow: 0 4px 15px rgba(102, 126, 234, 0.2);
    }
    
    .avatar {
      background: ${props => props.isDarkMode ? '#4f46e5' : '#667eea'};
      color: white;
      animation: ${float} 3s ease-in-out infinite;
    }
  }
  
  &.ai {
    .message-content {
      background: ${props => props.isDarkMode ? '#334155' : '#ffffff'};
      border: 1px solid ${props => getThemeColors(props.isDarkMode).borderColor};
      color: ${props => props.isDarkMode ? '#f1f5f9' : '#1e293b'};
      border-radius: 0.5rem 1.5rem 1.5rem 1.5rem;
      box-shadow: ${props => props.isDarkMode ? '0 4px 6px rgba(0, 0, 0, 0.3)' : '0 4px 15px rgba(0, 0, 0, 0.05)'};
      animation: ${slideUp} 0.5s ease-out;
    }
    
    .avatar {
      background: ${props => props.isDarkMode ? '#475569' : '#f1f5f9'};
      color: ${props => props.isDarkMode ? '#94a3b8' : '#64748b'};
      animation: ${float} 4s ease-in-out infinite;
    }
  }
  
  @media (max-width: 768px) {
    max-width: 100%;
    padding: 0 0.75rem; /* Reduced from 1rem */
    gap: 0.75rem; /* Reduced from 1rem */
  }
  
  @media (max-width: 480px) {
    gap: 0.5rem; /* Reduced from 0.75rem */
    padding: 0 0.5rem;
  }
`;

const Avatar = styled.div`
  width: 2.5rem; /* Reduced from 3rem to 2.5rem */
  height: 2.5rem; /* Reduced from 3rem to 2.5rem */
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  font-weight: 600;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  
  @media (max-width: 480px) {
    width: 2.25rem; /* Reduced from 2.5rem */
    height: 2.25rem; /* Reduced from 2.5rem */
  }
`;

const MessageContent = styled.div`
  flex: 1; /* Allow content to expand */
  padding: 1rem;
  line-height: 1.6;
  position: relative;
  word-wrap: break-word; /* Ensure long words break properly */
  overflow-wrap: break-word; /* Ensure content wraps correctly */
  
  pre {
    background: ${props => props.isDarkMode ? '#1e293b' : '#1e293b'};
    color: ${props => props.isDarkMode ? '#f8fafc' : '#f8fafc'};
    padding: 1rem;
    border-radius: 0.75rem;
    overflow-x: auto;
    margin: 1rem 0;
    box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.2);
    font-family: 'Monaco', 'Consolas', monospace;
    font-size: 0.9rem;
    max-width: 100%; /* Ensure pre doesn't overflow */
  }
  
  code {
    background: ${props => props.isDarkMode ? '#475569' : '#f1f5f9'};
    color: ${props => props.isDarkMode ? '#f1f5f9' : '#1e293b'};
    padding: 0.25rem 0.5rem;
    border-radius: 0.375rem;
    font-family: 'Monaco', 'Consolas', monospace;
    font-size: 0.9rem;
    word-break: break-word; /* Ensure code breaks properly */
  }
  
  p {
    margin: 0 0 1rem 0;
    
    &:last-child {
      margin-bottom: 0;
    }
  }
  
  ul, ol {
    padding-left: 1.5rem;
    margin: 1rem 0;
  }
  
  li {
    margin-bottom: 0.5rem;
  }
  
  h1, h2, h3, h4, h5, h6 {
    margin: 1.5rem 0 1rem 0;
    color: ${props => props.isDarkMode ? '#38bdf8' : '#0369a1'};
  }
  
  h1 {
    font-size: 1.75rem;
  }
  
  h2 {
    font-size: 1.5rem;
  }
  
  h3 {
    font-size: 1.25rem;
  }
  
  a {
    color: #667eea;
    text-decoration: none;
    
    &:hover {
      text-decoration: underline;
    }
  }
  
  blockquote {
    border-left: 4px solid ${props => props.isDarkMode ? '#475569' : '#cbd5e1'};
    padding-left: 1rem;
    margin: 1rem 0;
    color: ${props => props.isDarkMode ? '#94a3b8' : '#64748b'};
  }
  
  table {
    width: 100%;
    border-collapse: collapse;
    margin: 1rem 0;
    display: block; /* Allow table to scroll horizontally */
    overflow-x: auto;
    white-space: nowrap;
  }
  
  th, td {
    padding: 0.75rem;
    text-align: left;
    border-bottom: 1px solid ${props => props.isDarkMode ? '#475569' : '#e2e8f0'};
  }
  
  th {
    background: ${props => props.isDarkMode ? '#334155' : '#f1f5f9'};
    font-weight: 600;
  }
  
  @media (max-width: 768px) {
    padding: 0.875rem;
  }
  
  @media (max-width: 480px) {
    padding: 0.75rem;
    font-size: 0.9rem;
  }
`;

const MessageActions = styled.div`
  display: flex;
  gap: 0.5rem;
  margin-top: 0.75rem;
  padding-top: 0.75rem;
  border-top: 1px solid ${props => props.isDarkMode ? 'rgba(255, 255, 255, 0.1)' : 'rgba(0, 0, 0, 0.05)'};
  
  @media (max-width: 480px) {
    gap: 0.25rem;
  }
`;

const ActionButton = styled.button`
  background: none;
  border: none;
  color: ${props => getThemeColors(props.isDarkMode).secondaryTextColor};
  cursor: pointer;
  padding: 0.25rem;
  border-radius: 0.25rem;
  display: flex;
  align-items: center;
  gap: 0.25rem;
  font-size: 0.8rem;
  
  &:hover {
    background: ${props => props.isDarkMode ? '#475569' : '#f1f5f9'};
    color: ${props => props.isDarkMode ? '#f1f5f9' : '#1e293b'};
  }
  
  @media (max-width: 480px) {
    padding: 0.125rem;
    font-size: 0.7rem;
  }
`;

const InputContainer = styled.div`
  padding: 1rem; /* Reduced from 1.5rem to 1rem */
  border-top: 1px solid ${props => getThemeColors(props.isDarkMode).borderColor};
  background: ${props => getThemeColors(props.isDarkMode).cardBackground};
  
  @media (max-width: 480px) {
    padding: 0.75rem; /* Reduced from 1rem */
  }
`;

const InputWrapper = styled.div`
  display: flex;
  gap: 0.5rem; /* Reduced from 0.75rem to 0.5rem */
  max-width: 100%; /* Changed from 900px to 100% */
  margin: 0 auto;
  position: relative;
  
  @media (max-width: 768px) {
    gap: 0.5rem;
  }
  
  @media (max-width: 480px) {
    gap: 0.25rem;
  }
`;

const Input = styled.textarea`
  flex: 1;
  padding: 0.875rem 3rem 0.875rem 1rem; /* Adjusted padding */
  border: 1px solid ${props => getThemeColors(props.isDarkMode).borderColor};
  border-radius: 1.5rem;
  font-size: 1rem;
  font-family: inherit;
  resize: none;
  min-height: 50px; /* Reduced from 60px to 50px */
  max-height: 200px;
  transition: all 0.2s ease;
  background: ${props => getThemeColors(props.isDarkMode).inputBg};
  color: ${props => getThemeColors(props.isDarkMode).textColor};
  
  &:focus {
    outline: none;
    border-color: #667eea;
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
  }
  
  @media (max-width: 768px) {
    padding: 0.75rem 2.5rem 0.75rem 0.875rem; /* Adjusted padding */
    font-size: 0.9rem;
  }
  
  @media (max-width: 480px) {
    padding: 0.625rem 2rem 0.625rem 0.75rem; /* Adjusted padding */
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
  position: absolute;
  right: 10px;
  bottom: 5px;
  
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
    right: 5px;
  }
`;

const VoiceButton = styled.button`
  background: ${props => props.isDarkMode ? '#475569' : '#f1f5f9'};
  color: ${props => getThemeColors(props.isDarkMode).secondaryTextColor};
  border: none;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  align-self: flex-end;
  transition: all 0.2s ease;
  flex-shrink: 0;
  position: absolute;
  right: 65px;
  bottom: 10px;
  
  &:hover {
    background: ${props => props.isDarkMode ? '#64748b' : '#e2e8f0'};
    color: ${props => props.isDarkMode ? '#f1f5f9' : '#1e293b'};
  }
  
  @media (max-width: 480px) {
    width: 35px;
    height: 35px;
    right: 50px;
  }
`;

const QuickSuggestions = styled.div`
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem; /* Reduced from 0.75rem to 0.5rem */
  margin-top: 1rem;
  padding: 0 0.75rem; /* Reduced from 1rem */
  max-width: 100%; /* Changed from 900px to 100% */
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
  background: ${props => getThemeColors(props.isDarkMode).cardBackground};
  border: 1px solid ${props => getThemeColors(props.isDarkMode).borderColor};
  padding: 0.5rem 1rem;
  border-radius: 2rem;
  font-size: 0.875rem;
  cursor: pointer;
  transition: all 0.2s ease;
  color: ${props => getThemeColors(props.isDarkMode).textColor};
  
  &:hover {
    border-color: #667eea;
    background: ${props => props.isDarkMode ? '#475569' : '#f8fafc'};
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
  background: ${props => getThemeColors(props.isDarkMode).aiMessageBg};
  border: 1px solid ${props => getThemeColors(props.isDarkMode).borderColor};
  border-radius: 1.5rem;
  align-self: flex-start;
  max-width: 200px;
  box-shadow: ${props => props.isDarkMode ? '0 4px 6px rgba(0, 0, 0, 0.3)' : '0 4px 15px rgba(0, 0, 0, 0.05)'};
  
  @media (max-width: 480px) {
    padding: 0.75rem 1rem;
    max-width: 150px;
  }
`;

const TypingDot = styled.div`
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: ${props => getThemeColors(props.isDarkMode).secondaryTextColor};
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
  background: ${props => props.isDarkMode ? '#1e293b' : '#f0f9ff'};
  border: 1px solid ${props => props.isDarkMode ? '#475569' : '#bae6fd'};
  border-radius: 0.75rem;
  padding: 1.5rem;
  margin: 1rem 0;
  box-shadow: ${props => props.isDarkMode ? '0 4px 6px rgba(0, 0, 0, 0.3)' : '0 4px 6px rgba(0, 0, 0, 0.05)'};
  animation: ${scaleIn} 0.3s ease-out;
  transition: all 0.3s ease;
  color: ${props => props.isDarkMode ? '#f1f5f9' : '#0369a1'};
  
  &:hover {
    transform: translateY(-2px);
    box-shadow: ${props => props.isDarkMode ? '0 6px 12px rgba(0, 0, 0, 0.4)' : '0 6px 12px rgba(0, 0, 0, 0.1)'};
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
  color: ${props => props.isDarkMode ? '#38bdf8' : '#0369a1'};
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
  color: ${props => getThemeColors(props.isDarkMode).secondaryTextColor};
  font-weight: 500;
`;

const ProjectDetailValue = styled.span`
  font-size: 1rem;
  font-weight: 600;
  color: ${props => props.isDarkMode ? '#38bdf8' : '#0369a1'};
  
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
    background: ${props => props.isDarkMode ? '#475569' : '#f1f5f9'};
    color: ${props => props.isDarkMode ? '#f1f5f9' : '#1e293b'};
    
    &:hover {
      background: ${props => props.isDarkMode ? '#64748b' : '#e2e8f0'};
      transform: translateY(-2px);
      box-shadow: ${props => props.isDarkMode ? '0 4px 12px rgba(0, 0, 0, 0.2)' : '0 4px 12px rgba(0, 0, 0, 0.1)'};
    }
  }
  
  @media (max-width: 480px) {
    padding: 0.5rem 1rem;
    font-size: 0.9rem;
    width: 100%;
    justify-content: center;
  }
`;

// Enhanced Analysis Card with better styling
const AnalysisCard = styled.div`
  background: ${props => props.isDarkMode ? '#1e293b' : '#f0f9ff'};
  border: 1px solid ${props => props.isDarkMode ? '#475569' : '#bae6fd'};
  border-radius: 0.75rem;
  padding: 1.5rem;
  margin: 1rem 0;
  box-shadow: ${props => props.isDarkMode ? '0 4px 6px rgba(0, 0, 0, 0.3)' : '0 4px 6px rgba(0, 0, 0, 0.05)'};
  animation: ${scaleIn} 0.3s ease-out;
  transition: all 0.3s ease;
  color: ${props => props.isDarkMode ? '#f1f5f9' : '#0369a1'};
  
  &:hover {
    transform: translateY(-2px);
    box-shadow: ${props => props.isDarkMode ? '0 6px 12px rgba(0, 0, 0, 0.4)' : '0 6px 12px rgba(0, 0, 0, 0.1)'};
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
  color: ${props => props.isDarkMode ? '#38bdf8' : '#0369a1'};
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
  color: ${props => getThemeColors(props.isDarkMode).secondaryTextColor};
  font-weight: 500;
`;

const AnalysisValue = styled.span`
  font-size: 1rem;
  font-weight: 600;
  color: ${props => props.isDarkMode ? '#38bdf8' : '#0369a1'};
  
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
  color: ${props => props.isDarkMode ? '#38bdf8' : '#0369a1'};
  
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
  background: ${props => props.isDarkMode ? '#0c4a6e' : '#dbeafe'};
  color: ${props => props.isDarkMode ? '#bae6fd' : '#1d4ed8'};
  padding: 0.25rem 0.75rem;
  border-radius: 2rem;
  font-size: 0.8rem;
  font-weight: 500;
  
  @media (max-width: 480px) {
    padding: 0.2rem 0.6rem;
    font-size: 0.75rem;
  }
`;

// Documentation display component
const DocumentationCard = styled.div`
  background: ${props => props.isDarkMode ? '#1e293b' : '#f0f9ff'};
  border: 1px solid ${props => props.isDarkMode ? '#475569' : '#bae6fd'};
  border-radius: 0.75rem;
  padding: 1.5rem;
  margin: 1rem 0;
  box-shadow: ${props => props.isDarkMode ? '0 4px 6px rgba(0, 0, 0, 0.3)' : '0 4px 6px rgba(0, 0, 0, 0.05)'};
  animation: ${scaleIn} 0.3s ease-out;
  transition: all 0.3s ease;
  color: ${props => props.isDarkMode ? '#f1f5f9' : '#0369a1'};
  
  h1, h2, h3, h4, h5, h6 {
    color: ${props => props.isDarkMode ? '#38bdf8' : '#0369a1'};
    margin-top: 1.5rem;
    margin-bottom: 1rem;
  }
  
  pre {
    background: ${props => props.isDarkMode ? '#0f172a' : '#1e293b'};
    color: ${props => props.isDarkMode ? '#f8fafc' : '#f8fafc'};
    padding: 1rem;
    border-radius: 0.5rem;
    overflow-x: auto;
    margin: 1rem 0;
  }
  
  code {
    background: ${props => props.isDarkMode ? '#475569' : '#f1f5f9'};
    color: ${props => props.isDarkMode ? '#f1f5f9' : '#1e293b'};
    padding: 0.2rem 0.4rem;
    border-radius: 0.25rem;
    font-family: 'Monaco', 'Consolas', monospace;
    font-size: 0.85rem;
  }
  
  ul, ol {
    padding-left: 1.5rem;
    margin: 1rem 0;
  }
  
  li {
    margin-bottom: 0.5rem;
  }
  
  &:hover {
    transform: translateY(-2px);
    box-shadow: ${props => props.isDarkMode ? '0 6px 12px rgba(0, 0, 0, 0.4)' : '0 6px 12px rgba(0, 0, 0, 0.1)'};
  }
  
  @media (max-width: 768px) {
    padding: 1.25rem;
  }
  
  @media (max-width: 480px) {
    padding: 1rem;
  }
`;

const DocumentationHeader = styled.div`
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 1rem;
`;

const DocumentationTitle = styled.h3`
  font-size: 1.25rem;
  font-weight: 600;
  color: ${props => props.isDarkMode ? '#38bdf8' : '#0369a1'};
  margin: 0;
  
  @media (max-width: 480px) {
    font-size: 1.1rem;
  }
`;

// Improvement suggestions component
const SuggestionsCard = styled.div`
  background: ${props => props.isDarkMode ? '#14532d' : '#f0fdf4'};
  border: 1px solid ${props => props.isDarkMode ? '#166534' : '#bbf7d0'};
  border-radius: 0.75rem;
  padding: 1.5rem;
  margin: 1rem 0;
  box-shadow: ${props => props.isDarkMode ? '0 4px 6px rgba(0, 0, 0, 0.3)' : '0 4px 6px rgba(0, 0, 0, 0.05)'};
  animation: ${scaleIn} 0.3s ease-out;
  transition: all 0.3s ease;
  color: ${props => props.isDarkMode ? '#bbf7d0' : '#15803d'};
  
  h1, h2, h3, h4, h5, h6 {
    color: ${props => props.isDarkMode ? '#4ade80' : '#15803d'};
    margin-top: 1.5rem;
    margin-bottom: 1rem;
  }
  
  ul, ol {
    padding-left: 1.5rem;
    margin: 1rem 0;
  }
  
  li {
    margin-bottom: 0.5rem;
  }
  
  &:hover {
    transform: translateY(-2px);
    box-shadow: ${props => props.isDarkMode ? '0 6px 12px rgba(0, 0, 0, 0.4)' : '0 6px 12px rgba(0, 0, 0, 0.1)'};
  }
  
  @media (max-width: 768px) {
    padding: 1.25rem;
  }
  
  @media (max-width: 480px) {
    padding: 1rem;
  }
`;

const SuggestionsHeader = styled.div`
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 1rem;
`;

const SuggestionsTitle = styled.h3`
  font-size: 1.25rem;
  font-weight: 600;
  color: ${props => props.isDarkMode ? '#4ade80' : '#15803d'};
  margin: 0;
  
  @media (max-width: 480px) {
    font-size: 1.1rem;
  }
`;

const ErrorMessage = styled.div`
  background: ${props => props.isDarkMode ? '#7f1d1d' : '#fee2e2'};
  border: 1px solid ${props => props.isDarkMode ? '#b91c1c' : '#fecaca'};
  color: ${props => props.isDarkMode ? '#fecaca' : '#dc2626'};
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
  background: ${props => props.isDarkMode ? '#14532d' : '#dcfce7'};
  border: 1px solid ${props => props.isDarkMode ? '#166534' : '#bbf7d0'};
  color: ${props => props.isDarkMode ? '#bbf7d0' : '#16a34a'};
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

// Project Generation Components
const ProjectGenerationCard = styled.div`
  background: ${props => props.isDarkMode ? '#14532d' : '#f0fdf4'};
  border: 1px solid ${props => props.isDarkMode ? '#166534' : '#bbf7d0'};
  border-radius: 0.75rem;
  padding: 1.5rem;
  margin: 1rem 0;
  box-shadow: ${props => props.isDarkMode ? '0 4px 6px rgba(0, 0, 0, 0.3)' : '0 4px 6px rgba(0, 0, 0, 0.05)'};
  animation: ${scaleIn} 0.3s ease-out;
  transition: all 0.3s ease;
  color: ${props => props.isDarkMode ? '#bbf7d0' : '#15803d'};
  
  &:hover {
    transform: translateY(-2px);
    box-shadow: ${props => props.isDarkMode ? '0 6px 12px rgba(0, 0, 0, 0.4)' : '0 6px 12px rgba(0, 0, 0, 0.1)'};
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
  color: ${props => props.isDarkMode ? '#4ade80' : '#15803d'};
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
    background: ${props => props.isDarkMode ? '#475569' : '#f1f5f9'};
    color: ${props => props.isDarkMode ? '#f1f5f9' : '#1e293b'};
    
    &:hover {
      background: ${props => props.isDarkMode ? '#64748b' : '#e2e8f0'};
      transform: translateY(-2px);
      box-shadow: ${props => props.isDarkMode ? '0 4px 12px rgba(0, 0, 0, 0.2)' : '0 4px 12px rgba(0, 0, 0, 0.1)'};
    }
  }
  
  @media (max-width: 480px) {
    padding: 0.5rem 1rem;
    font-size: 0.9rem;
    width: 100%;
    justify-content: center;
  }
`;

// Export options modal
const Modal = styled.div`
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
`;

const ModalContent = styled.div`
  background: ${props => getThemeColors(props.isDarkMode).cardBackground};
  border-radius: 0.75rem;
  padding: 2rem;
  max-width: 500px;
  width: 90%;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
  
  @media (max-width: 480px) {
    padding: 1.5rem;
  }
`;

const ModalHeader = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
`;

const ModalTitle = styled.h3`
  font-size: 1.5rem;
  font-weight: 600;
  color: ${props => getThemeColors(props.isDarkMode).textColor};
  margin: 0;
`;

const CloseModalButton = styled.button`
  background: none;
  border: none;
  color: ${props => getThemeColors(props.isDarkMode).secondaryTextColor};
  cursor: pointer;
  padding: 0.5rem;
  border-radius: 0.5rem;
  
  &:hover {
    background: ${props => props.isDarkMode ? '#475569' : '#f1f5f9'};
  }
`;

const ExportOptions = styled.div`
  display: flex;
  flex-direction: column;
  gap: 1rem;
`;

const ExportOption = styled.button`
  background: ${props => props.isDarkMode ? '#475569' : '#f1f5f9'};
  border: 1px solid ${props => getThemeColors(props.isDarkMode).borderColor};
  padding: 1rem;
  border-radius: 0.5rem;
  display: flex;
  align-items: center;
  gap: 1rem;
  cursor: pointer;
  transition: all 0.2s ease;
  color: ${props => getThemeColors(props.isDarkMode).textColor};
  
  &:hover {
    background: ${props => props.isDarkMode ? '#64748b' : '#e2e8f0'};
    border-color: #667eea;
  }
`;

// Text-to-speech button
const TTSButton = styled.button`
  background: none;
  border: none;
  color: ${props => getThemeColors(props.isDarkMode).secondaryTextColor};
  cursor: pointer;
  padding: 0.25rem;
  border-radius: 0.25rem;
  display: flex;
  align-items: center;
  gap: 0.25rem;
  font-size: 0.8rem;
  
  &:hover {
    background: ${props => props.isDarkMode ? '#475569' : '#f1f5f9'};
    color: ${props => props.isDarkMode ? '#f1f5f9' : '#1e293b'};
  }
  
  @media (max-width: 480px) {
    padding: 0.125rem;
    font-size: 0.7rem;
  }
`;

// Advanced features panel
const FeaturesPanel = styled.div`
  position: fixed;
  right: 0;
  top: 0;
  height: 100vh;
  width: 300px;
  background: ${props => getThemeColors(props.isDarkMode).cardBackground};
  border-left: 1px solid ${props => getThemeColors(props.isDarkMode).borderColor};
  padding: 1.5rem;
  box-shadow: -2px 0 10px rgba(0, 0, 0, 0.05);
  z-index: 100;
  transform: ${props => props.isOpen ? 'translateX(0)' : 'translateX(100%)'};
  transition: transform 0.3s ease;
  
  @media (max-width: 768px) {
    width: 100%;
  }
`;

const FeaturesHeader = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
`;

const FeaturesTitle = styled.h3`
  font-size: 1.25rem;
  font-weight: 600;
  color: ${props => getThemeColors(props.isDarkMode).textColor};
  margin: 0;
`;

const FeatureCategory = styled.div`
  margin-bottom: 1.5rem;
`;

const FeatureCategoryTitle = styled.h4`
  font-size: 1rem;
  font-weight: 600;
  color: ${props => getThemeColors(props.isDarkMode).textColor};
  margin: 0 0 0.75rem 0;
  display: flex;
  align-items: center;
  gap: 0.5rem;
`;

const FeatureItemButton = styled.button`
  width: 100%;
  background: none;
  border: none;
  padding: 0.75rem;
  border-radius: 0.5rem;
  text-align: left;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  color: ${props => getThemeColors(props.isDarkMode).textColor};
  transition: all 0.2s ease;
  
  &:hover {
    background: ${props => props.isDarkMode ? '#475569' : '#f1f5f9'};
  }
`;

// Toggle features panel button
const ToggleFeaturesButton = styled.button`
  position: fixed;
  right: 1rem;
  bottom: 1rem;
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
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
  z-index: 99;
  
  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 15px rgba(102, 126, 234, 0.4);
  }
  
  @media (max-width: 480px) {
    width: 45px;
    height: 45px;
    right: 0.75rem;
  }
`;

// Settings panel
const SettingsPanel = styled.div`
  position: fixed;
  right: 0;
  top: 0;
  height: 100vh;
  width: 300px;
  background: ${props => getThemeColors(props.isDarkMode).cardBackground};
  border-left: 1px solid ${props => getThemeColors(props.isDarkMode).borderColor};
  padding: 1.5rem;
  box-shadow: -2px 0 10px rgba(0, 0, 0, 0.05);
  z-index: 100;
  transform: ${props => props.isOpen ? 'translateX(0)' : 'translateX(100%)'};
  transition: transform 0.3s ease;
  
  @media (max-width: 768px) {
    width: 100%;
  }
`;

const SettingsHeader = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
`;

const SettingsTitle = styled.h3`
  font-size: 1.25rem;
  font-weight: 600;
  color: ${props => getThemeColors(props.isDarkMode).textColor};
  margin: 0;
`;

const SettingsGroup = styled.div`
  margin-bottom: 1.5rem;
`;

const SettingsGroupTitle = styled.h4`
  font-size: 1rem;
  font-weight: 600;
  color: ${props => getThemeColors(props.isDarkMode).textColor};
  margin: 0 0 0.75rem 0;
`;

const SettingsOption = styled.div`
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.75rem 0;
  border-bottom: 1px solid ${props => getThemeColors(props.isDarkMode).borderColor};
`;

const SettingsLabel = styled.label`
  font-size: 0.9rem;
  color: ${props => getThemeColors(props.isDarkMode).textColor};
`;

const SettingsToggle = styled.label`
  position: relative;
  display: inline-block;
  width: 50px;
  height: 24px;
`;

const SettingsToggleInput = styled.input`
  opacity: 0;
  width: 0;
  height: 0;
`;

const SettingsToggleSlider = styled.span`
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: ${props => props.isDarkMode ? '#475569' : '#cbd5e1'};
  transition: .4s;
  border-radius: 24px;
  
  &:before {
    position: absolute;
    content: "";
    height: 16px;
    width: 16px;
    left: 4px;
    bottom: 4px;
    background-color: white;
    transition: .4s;
    border-radius: 50%;
  }
  
  ${SettingsToggleInput}:checked + & {
    background-color: #667eea;
  }
  
  ${SettingsToggleInput}:checked + &:before {
    transform: translateX(26px);
  }
`;

// Toggle settings panel button
const ToggleSettingsButton = styled.button`
  position: fixed;
  right: 70px;
  bottom: 1rem;
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
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
  z-index: 99;
  
  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 15px rgba(102, 126, 234, 0.4);
  }
  
  @media (max-width: 480px) {
    width: 45px;
    height: 45px;
    right: 60px;
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
  const [isDarkMode, setIsDarkMode] = useState(false);
  const [showExportModal, setShowExportModal] = useState(false);
  const [isListening, setIsListening] = useState(false);
  const [isSpeaking, setIsSpeaking] = useState(false);
  const [showFeaturesPanel, setShowFeaturesPanel] = useState(false);
  const [showSettingsPanel, setShowSettingsPanel] = useState(false);
  const chatContainerRef = useRef(null);
  const textareaRef = useRef(null);
  const recognitionRef = useRef(null);
  const speechSynthesisRef = useRef(null);

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

  // Initialize speech recognition
  useEffect(() => {
    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
      const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
      recognitionRef.current = new SpeechRecognition();
      recognitionRef.current.continuous = false;
      recognitionRef.current.interimResults = false;
      recognitionRef.current.lang = 'en-US';
      
      recognitionRef.current.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        setInputValue(prev => prev + transcript);
        setIsListening(false);
      };
      
      recognitionRef.current.onerror = (event) => {
        console.error('Speech recognition error', event.error);
        setIsListening(false);
      };
      
      recognitionRef.current.onend = () => {
        setIsListening(false);
      };
    }
    
    // Initialize speech synthesis
    if ('speechSynthesis' in window) {
      speechSynthesisRef.current = window.speechSynthesis;
    }
  }, []);

  const quickSuggestions = [
    "Build a task management app",
    "Create an e-commerce website",
    "Make a blog with CMS",
    "Develop a chat application",
    "Design a dashboard analytics",
    // Added new suggestion for builder integration
    "Take this conversation to the Builder"
  ];

  const advancedFeatures = [
    {
      category: "Code Assistance",
      icon: <Code size={16} />,
      features: [
        { name: "Generate Code", icon: <FileCode size={16} />, action: "generateCode" },
        { name: "Debug Code", icon: <Bug size={16} />, action: "debugCode" },
        { name: "Optimize Code", icon: <TrendingUp size={16} />, action: "optimizeCode" },
        { name: "Security Review", icon: <Shield size={16} />, action: "securityReview" }
      ]
    },
    {
      category: "Project Planning",
      icon: <Building size={16} />,
      features: [
        { name: "Architecture Analysis", icon: <Building size={16} />, action: "architectureAnalysis" },
        { name: "Technology Stack", icon: <CpuIcon size={16} />, action: "techStack" },
        { name: "Project Timeline", icon: <Clock size={16} />, action: "timeline" },
        { name: "Resource Planning", icon: <Users size={16} />, action: "resources" }
      ]
    },
    {
      category: "Learning",
      icon: <BookOpen size={16} />,
      features: [
        { name: "Concept Explanation", icon: <Lightbulb size={16} />, action: "explainConcept" },
        { name: "Best Practices", icon: <Award size={16} />, action: "bestPractices" },
        { name: "Code Examples", icon: <FileCode size={16} />, action: "codeExamples" },
        { name: "Framework Guide", icon: <GitBranch size={16} />, action: "frameworkGuide" }
      ]
    },
    {
      category: "Project Management",
      icon: <Folder size={16} />,
      features: [
        { name: "Project Templates", icon: <Layout size={16} />, action: "projectTemplates" },
        { name: "Documentation", icon: <FileText size={16} />, action: "generateDocumentation" },
        { name: "Improvement Suggestions", icon: <TrendingUp size={16} />, action: "improvementSuggestions" },
        { name: "Code Review", icon: <Eye size={16} />, action: "codeReview" }
      ]
    }
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
      // Check for specific commands
      const lowerInput = inputValue.toLowerCase();
      
      // Handle documentation request
      if (lowerInput.includes('documentation') || lowerInput.includes('document') || lowerInput.includes('docs')) {
        // Generate documentation for a sample project
        const sampleProjectData = {
          name: "Sample Project",
          type: "web_app",
          tech_stack: {
            frontend: "React",
            backend: "FastAPI",
            database: "MySQL"
          },
          features: ["User Authentication", "Responsive Design", "API Integration"]
        };
        
        const docResponse = await aiChatService.generateDocumentation(sampleProjectData);
        
        const documentationCard = (
          <DocumentationCard isDarkMode={isDarkMode}>
            <DocumentationHeader>
              <FileText size={20} color={isDarkMode ? "#38bdf8" : "#0369a1"} />
              <DocumentationTitle isDarkMode={isDarkMode}>Project Documentation</DocumentationTitle>
            </DocumentationHeader>
            <div dangerouslySetInnerHTML={{ __html: docResponse.documentation.replace(/\n/g, '<br />') }} />
          </DocumentationCard>
        );
        
        const aiResponse = {
          id: Date.now() + 1,
          role: 'ai',
          content: documentationCard,
          timestamp: new Date(),
          type: 'documentation'
        };
        
        setMessages(prev => [...prev, aiResponse]);
        setIsLoading(false);
        return;
      }
      
      // Handle improvement suggestions request
      if (lowerInput.includes('improve') || lowerInput.includes('enhance') || lowerInput.includes('optimize')) {
        // Generate suggestions for a sample project
        const sampleProjectData = {
          name: "Sample Project",
          type: "web_app",
          tech_stack: {
            frontend: "React",
            backend: "FastAPI",
            database: "MySQL"
          },
          features: ["User Authentication", "Responsive Design", "API Integration"]
        };
        
        const suggestionsResponse = await aiChatService.suggestImprovements(sampleProjectData, inputValue);
        
        const suggestionsCard = (
          <SuggestionsCard isDarkMode={isDarkMode}>
            <SuggestionsHeader>
              <Lightbulb size={20} color={isDarkMode ? "#4ade80" : "#15803d"} />
              <SuggestionsTitle isDarkMode={isDarkMode}>Improvement Suggestions</SuggestionsTitle>
            </SuggestionsHeader>
            <div dangerouslySetInnerHTML={{ __html: suggestionsResponse.suggestions.replace(/\n/g, '<br />') }} />
          </SuggestionsCard>
        );
        
        const aiResponse = {
          id: Date.now() + 1,
          role: 'ai',
          content: suggestionsCard,
          timestamp: new Date(),
          type: 'suggestions'
        };
        
        setMessages(prev => [...prev, aiResponse]);
        setIsLoading(false);
        return;
      }
      
      // Handle project generation requests
      if (lowerInput.includes('generate') || 
          lowerInput.includes('create') || 
          lowerInput.includes('build') ||
          lowerInput.includes('make') ||
          lowerInput.includes('develop') ||
          lowerInput.includes('project') ||
          lowerInput.includes('app') ||
          lowerInput.includes('application')) {
        // Analyze the request and provide project generation options
        const analysisResponse = await aiChatService.analyzeRequirements(inputValue);
        
        const analysis = analysisResponse.analysis || analysisResponse;
        
        // Create a detailed analysis card like Google AI Studio
        const analysisCard = (
          <AnalysisCard isDarkMode={isDarkMode}>
            <AnalysisHeader>
              <Sparkles size={20} color={isDarkMode ? "#38bdf8" : "#0369a1"} />
              <AnalysisTitle isDarkMode={isDarkMode}>Project Analysis</AnalysisTitle>
            </AnalysisHeader>
            
            <AnalysisGrid>
              <AnalysisItem>
                <AnalysisLabel isDarkMode={isDarkMode}>Project Type</AnalysisLabel>
                <AnalysisValue isDarkMode={isDarkMode}>{analysis.project_type || 'Web Application'}</AnalysisValue>
              </AnalysisItem>
              
              <AnalysisItem>
                <AnalysisLabel isDarkMode={isDarkMode}>Complexity</AnalysisLabel>
                <AnalysisValue isDarkMode={isDarkMode}>{analysis.complexity || 'Medium'}</AnalysisValue>
              </AnalysisItem>
              
              <AnalysisItem>
                <AnalysisLabel isDarkMode={isDarkMode}>Estimated Time</AnalysisLabel>
                <AnalysisValue isDarkMode={isDarkMode}>{analysisResponse.estimated_time || '2-5 minutes'}</AnalysisValue>
              </AnalysisItem>
            </AnalysisGrid>
            
            <h4>Tech Stack Recommendation:</h4>
            <TechStackGrid>
              <TechTag isDarkMode={isDarkMode}>Frontend: {analysis.tech_recommendations?.frontend || 'React'}</TechTag>
              <TechTag isDarkMode={isDarkMode}>Backend: {analysis.tech_recommendations?.backend || 'FastAPI'}</TechTag>
              <TechTag isDarkMode={isDarkMode}>Database: {analysis.tech_recommendations?.database || 'MySQL'}</TechTag>
            </TechStackGrid>
            
            <h4>Key Features:</h4>
            <FeaturesList>
              {(analysis.features || ['User Authentication', 'Responsive Design', 'API Integration']).map((feature, index) => (
                <FeatureItem key={index} isDarkMode={isDarkMode}>{feature}</FeatureItem>
              ))}
            </FeaturesList>
            
            <ProjectActionsContainer>
              <ProjectActionButton onClick={() => handleGenerateProject(inputValue, analysis)}>
                <Play size={16} />
                Generate Project
              </ProjectActionButton>
              <ProjectActionButton className="secondary" onClick={() => handleAskForModifications(analysisResponse)}>
                <Edit3 size={16} />
                Modify Requirements
              </ProjectActionButton>
            </ProjectActionsContainer>
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
        history: messages.slice(-10) // Send last 10 messages as context
      });
      
      // Handle both success and error responses
      let aiContent;
      if (response.success === false) {
        // Handle error response
        aiContent = (
          <ErrorMessage isDarkMode={isDarkMode}>
            <AlertCircle size={16} />
            <div>
              <strong>AI Service Error</strong>
              <p>{response.response}</p>
            </div>
          </ErrorMessage>
        );
      } else if (response.response && response.response.includes('All AI services are currently unavailable')) {
        // Handle fallback response with specific guidance
        aiContent = (
          <ErrorMessage isDarkMode={isDarkMode}>
            <AlertCircle size={16} />
            <div>
              <strong>AI Services Unavailable</strong>
              <p>We're currently unable to connect to any AI services. This could be due to:</p>
              <ul style={{ marginTop: '10px', paddingLeft: '20px', marginBottom: '10px' }}>
                <li>API quota limits being exceeded</li>
                <li>Required payment methods not configured</li>
                <li>Temporary service outages</li>
              </ul>
              <p>To resolve this issue:</p>
              <ol style={{ paddingLeft: '20px', marginBottom: '10px' }}>
                <li><strong>OpenAI:</strong> Upgrade your account or wait for quota reset</li>
                <li><strong>Gemini:</strong> Check your API key and quota limits</li>
                <li><strong>DeepSeek:</strong> Add payment method to your account</li>
              </ol>
              <p>You can still use basic functionality while we work on resolving this issue.</p>
            </div>
          </ErrorMessage>
        );
      } else {
        // Handle normal response
        aiContent = response.response;
      }
      
      const aiResponse = {
        id: Date.now() + 1,
        role: 'ai',
        content: aiContent,
        timestamp: new Date()
      };
      
      setMessages(prev => [...prev, aiResponse]);
      setIsLoading(false);
    } catch (error) {
      console.error('Error sending message:', error);
      
      const aiResponse = {
        id: Date.now() + 1,
        role: 'ai',
        content: (
          <ErrorMessage isDarkMode={isDarkMode}>
            <AlertCircle size={16} />
            <div>
              <strong>Connection Error</strong>
              <p>Failed to connect to the AI service. Please check your internet connection and try again.</p>
            </div>
          </ErrorMessage>
        ),
        timestamp: new Date()
      };
      
      setMessages(prev => [...prev, aiResponse]);
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
        <ProjectGenerationCard isDarkMode={isDarkMode}>
          <ProjectGenerationHeader>
            <Zap size={20} color={isDarkMode ? "#4ade80" : "#15803d"} />
            <ProjectGenerationTitle isDarkMode={isDarkMode}>Generating Your Project</ProjectGenerationTitle>
          </ProjectGenerationHeader>
          
          <p>Creating your {analysis.project_type || 'application'} with the following specifications:</p>
          
          <AnalysisGrid>
            <AnalysisItem>
              <AnalysisLabel isDarkMode={isDarkMode}>Name</AnalysisLabel>
              <AnalysisValue isDarkMode={isDarkMode}>{projectDescription.substring(0, 30) + (projectDescription.length > 30 ? '...' : '')}</AnalysisValue>
            </AnalysisItem>
            
            <AnalysisItem>
              <AnalysisLabel isDarkMode={isDarkMode}>Tech Stack</AnalysisLabel>
              <AnalysisValue isDarkMode={isDarkMode}>
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
          <ErrorMessage isDarkMode={isDarkMode}>
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
    aiChatService.clearHistory();
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
            // Handle both success and error responses
            let aiContent;
            if (response.success === false) {
              // Handle error response
              aiContent = (
                <ErrorMessage isDarkMode={isDarkMode}>
                  <AlertCircle size={20} />
                  {response.response}
                </ErrorMessage>
              );
            } else {
              // Handle success response
              aiContent = response.response || 'I understand your request. How can I help you build your application?';
            }
            
            const aiResponse = {
              id: Date.now(),
              role: 'ai',
              content: aiContent,
              timestamp: new Date(),
              type: response.success === false ? 'error' : 'message'
            };
            setMessages(prev => [...prev, aiResponse]);
            setIsLoading(false);
          }).catch(error => {
            console.error('Error regenerating response:', error);
            const errorMessage = {
              id: Date.now(),
              role: 'ai',
              content: (
                <ErrorMessage isDarkMode={isDarkMode}>
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

  const toggleDarkMode = () => {
    setIsDarkMode(prev => !prev);
  };

  const toggleVoiceInput = () => {
    if (!recognitionRef.current) return;
    
    if (isListening) {
      recognitionRef.current.stop();
      setIsListening(false);
    } else {
      recognitionRef.current.start();
      setIsListening(true);
    }
  };

  const toggleTextToSpeech = (content) => {
    if (!speechSynthesisRef.current) return;
    
    if (isSpeaking) {
      speechSynthesisRef.current.cancel();
      setIsSpeaking(false);
    } else {
      // If content is a React element, we need to extract the text
      let textToSpeak = content;
      if (typeof content === 'object' && content.props) {
        // This is a React element, extract text content
        textToSpeak = content.props.children || '';
      }
      
      const utterance = new SpeechSynthesisUtterance(textToSpeak);
      utterance.onend = () => setIsSpeaking(false);
      speechSynthesisRef.current.speak(utterance);
      setIsSpeaking(true);
    }
  };

  // Export chat history to different formats
  const exportChatHistory = (format) => {
    const chatText = messages
      .filter(msg => msg.role === 'user' || msg.role === 'ai')
      .map(msg => `${msg.role.toUpperCase()}: ${typeof msg.content === 'string' ? msg.content : 'Content not available for export'}`)
      .join('\n\n');
    
    const blob = new Blob([chatText], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `chat-history.${format}`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  const handleFeatureClick = (feature) => {
    switch (feature.action) {
      case 'generateCode':
        setInputValue("Generate a React component that displays a list of users with their avatars and names");
        break;
      case 'debugCode':
        setInputValue("Debug this JavaScript code that's not working as expected");
        break;
      case 'optimizeCode':
        setInputValue("Optimize this Python function for better performance");
        break;
      case 'securityReview':
        setInputValue("Review this code for security vulnerabilities");
        break;
      case 'architectureAnalysis':
        setInputValue("Analyze the architecture for a real-time chat application");
        break;
      case 'explainConcept':
        setInputValue("Explain how React hooks work");
        break;
      case 'projectTemplates':
        setInputValue("Show me available project templates");
        break;
      case 'generateDocumentation':
        setInputValue("Generate documentation for a web application");
        break;
      case 'improvementSuggestions':
        setInputValue("Suggest improvements for a React application");
        break;
      case 'codeReview':
        setInputValue("Review this code for best practices and improvements");
        break;
      default:
        setInputValue(`I need help with ${feature.name.toLowerCase()}`);
    }
    setShowFeaturesPanel(false);
    textareaRef.current?.focus();
  };

  return (
    <Container isDarkMode={isDarkMode}>
      <Sidebar isDarkMode={isDarkMode} isOpen={sidebarOpen}>
        <SidebarHeader isDarkMode={isDarkMode}>
          <SidebarTitle isDarkMode={isDarkMode}>Chat History</SidebarTitle>
          <CloseButton isDarkMode={isDarkMode} onClick={() => setSidebarOpen(false)}>
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
              isActive={chat.id === activeChat}
              isDarkMode={isDarkMode}
              onClick={() => setActiveChat(chat.id)}
            >
              <MessageSquare size={16} />
              <span>{chat.title}</span>
            </ChatItem>
          ))}
        </ChatHistory>
      </Sidebar>
      
      <MainContent>
        <Header isDarkMode={isDarkMode}>
          <MenuButton isDarkMode={isDarkMode} onClick={() => setSidebarOpen(true)}>
            <Menu size={20} />
          </MenuButton>
          <div>
            <Title isDarkMode={isDarkMode}>
              <Bot size={24} />
              AI Chat Assistant
            </Title>
            <Subtitle isDarkMode={isDarkMode}>Ask me anything about building applications</Subtitle>
          </div>
          <ThemeToggle isDarkMode={isDarkMode} onClick={toggleDarkMode}>
            {isDarkMode ? <Sun size={20} /> : <Moon size={20} />}
          </ThemeToggle>
          <button onClick={() => setShowExportModal(true)}>
            <DownloadIcon size={20} />
          </button>
        </Header>
        
        <ChatContainer ref={chatContainerRef} isDarkMode={isDarkMode}>
          {messages.map(message => (
            <Message key={message.id} role={message.role} isDarkMode={isDarkMode}>
              <Avatar className="avatar">
                {message.role === 'user' ? <User size={20} /> : <Bot size={20} />}
              </Avatar>
              <MessageContent isDarkMode={isDarkMode}>
                {typeof message.content === 'string' ? (
                  <div dangerouslySetInnerHTML={{ __html: message.content.replace(/\n/g, '<br />') }} />
                ) : (
                  message.content
                )}
                {message.role === 'ai' && message.type !== 'error' && message.type !== 'success' && (
                  <MessageActions isDarkMode={isDarkMode}>
                    <ActionButton isDarkMode={isDarkMode} onClick={() => handleCopyMessage(message.content)}>
                      <Copy size={14} />
                      Copy
                    </ActionButton>
                    <ActionButton isDarkMode={isDarkMode} onClick={() => handleLikeMessage(message.id)}>
                      <ThumbsUp size={14} />
                      Helpful
                    </ActionButton>
                    <ActionButton isDarkMode={isDarkMode} onClick={() => handleDislikeMessage(message.id)}>
                      <ThumbsDown size={14} />
                      Not Helpful
                    </ActionButton>
                    <ActionButton isDarkMode={isDarkMode} onClick={() => handleRegenerateResponse(message.id)}>
                      <RefreshCw size={14} />
                      Regenerate
                    </ActionButton>
                    <TTSButton isDarkMode={isDarkMode} onClick={() => toggleTextToSpeech(message.content)}>
                      {isSpeaking ? <VolumeX size={14} /> : <Speech size={14} />}
                      {isSpeaking ? 'Stop' : 'Listen'}
                    </TTSButton>
                    {/* Added new button to send conversation to Builder */}
                    <ActionButton 
                      isDarkMode={isDarkMode} 
                      onClick={() => {
                        navigate('/builder', { 
                          state: { 
                            userPrompt: message.content,
                            chatHistory: messages
                          }
                        });
                      }}
                    >
                      <Play size={14} />
                      Build Project
                    </ActionButton>
                  </MessageActions>
                )}
              </MessageContent>
            </Message>
          ))}
          
          {isLoading && (
            <Message role="ai" isDarkMode={isDarkMode}>
              <Avatar className="avatar">
                <Bot size={20} />
              </Avatar>
              <TypingIndicator isDarkMode={isDarkMode}>
                <TypingDot />
                <TypingDot />
                <TypingDot />
                <span>AI is thinking...</span>
              </TypingIndicator>
            </Message>
          )}
        </ChatContainer>
        
        <QuickSuggestions>
          {quickSuggestions.map((suggestion, index) => (
            <SuggestionButton 
              key={index} 
              isDarkMode={isDarkMode}
              onClick={() => handleSuggestionClick(suggestion)}
            >
              {suggestion}
            </SuggestionButton>
          ))}
        </QuickSuggestions>
        
        <InputContainer isDarkMode={isDarkMode}>
          <InputWrapper>
            <Input
              ref={textareaRef}
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Message AI assistant... (Press Enter to send, Shift+Enter for new line)"
              disabled={isLoading}
              isDarkMode={isDarkMode}
            />
            <VoiceButton 
              isDarkMode={isDarkMode}
              onClick={toggleVoiceInput}
              style={{ backgroundColor: isListening ? '#ef4444' : '' }}
            >
              <Mic size={16} />
            </VoiceButton>
            <SendButton 
              onClick={handleSendMessage} 
              disabled={!inputValue.trim() || isLoading}
            >
              {isLoading ? <Loader size={20} /> : <Send size={20} />}
            </SendButton>
          </InputWrapper>
        </InputContainer>
      </MainContent>
      
      {showExportModal && (
        <Modal>
          <ModalContent isDarkMode={isDarkMode}>
            <ModalHeader>
              <ModalTitle isDarkMode={isDarkMode}>Export Chat History</ModalTitle>
              <CloseModalButton isDarkMode={isDarkMode} onClick={() => setShowExportModal(false)}>
                <X size={20} />
              </CloseModalButton>
            </ModalHeader>
            <ExportOptions>
              <ExportOption isDarkMode={isDarkMode} onClick={() => {
                exportChatHistory('txt');
                setShowExportModal(false);
              }}>
                <FileText size={20} />
                Export as Text
              </ExportOption>
              <ExportOption isDarkMode={isDarkMode} onClick={() => {
                exportChatHistory('md');
                setShowExportModal(false);
              }}>
                <BookOpen size={20} />
                Export as Markdown
              </ExportOption>
              <ExportOption isDarkMode={isDarkMode} onClick={() => {
                exportChatHistory('pdf');
                setShowExportModal(false);
              }}>
                <FileDocument size={20} />
                Export as PDF
              </ExportOption>
            </ExportOptions>
          </ModalContent>
        </Modal>
      )}
      
      <FeaturesPanel isDarkMode={isDarkMode} isOpen={showFeaturesPanel}>
        <FeaturesHeader>
          <FeaturesTitle isDarkMode={isDarkMode}>Advanced Features</FeaturesTitle>
          <CloseModalButton isDarkMode={isDarkMode} onClick={() => setShowFeaturesPanel(false)}>
            <X size={20} />
          </CloseModalButton>
        </FeaturesHeader>
        
        {advancedFeatures.map((category, index) => (
          <FeatureCategory key={index}>
            <FeatureCategoryTitle isDarkMode={isDarkMode}>
              {category.icon}
              {category.category}
            </FeatureCategoryTitle>
            {category.features.map((feature, featureIndex) => (
              <FeatureItemButton 
                key={featureIndex} 
                isDarkMode={isDarkMode}
                onClick={() => handleFeatureClick(feature)}
              >
                {feature.icon}
                {feature.name}
              </FeatureItemButton>
            ))}
          </FeatureCategory>
        ))}
      </FeaturesPanel>
      
      <SettingsPanel isDarkMode={isDarkMode} isOpen={showSettingsPanel}>
        <SettingsHeader>
          <SettingsTitle isDarkMode={isDarkMode}>Settings</SettingsTitle>
          <CloseModalButton isDarkMode={isDarkMode} onClick={() => setShowSettingsPanel(false)}>
            <X size={20} />
          </CloseModalButton>
        </SettingsHeader>
        
        <SettingsGroup>
          <SettingsGroupTitle isDarkMode={isDarkMode}>Appearance</SettingsGroupTitle>
          <SettingsOption>
            <SettingsLabel isDarkMode={isDarkMode}>Dark Mode</SettingsLabel>
            <SettingsToggle isDarkMode={isDarkMode}>
              <SettingsToggleInput 
                type="checkbox" 
                checked={isDarkMode}
                onChange={toggleDarkMode}
              />
              <SettingsToggleSlider isDarkMode={isDarkMode} />
            </SettingsToggle>
          </SettingsOption>
        </SettingsGroup>
        
        <SettingsGroup>
          <SettingsGroupTitle isDarkMode={isDarkMode}>AI Assistant</SettingsGroupTitle>
          <SettingsOption>
            <SettingsLabel isDarkMode={isDarkMode}>Voice Input</SettingsLabel>
            <SettingsToggle isDarkMode={isDarkMode}>
              <SettingsToggleInput 
                type="checkbox" 
                checked={isListening}
                onChange={toggleVoiceInput}
              />
              <SettingsToggleSlider isDarkMode={isDarkMode} />
            </SettingsToggle>
          </SettingsOption>
          <SettingsOption>
            <SettingsLabel isDarkMode={isDarkMode}>Text-to-Speech</SettingsLabel>
            <SettingsToggle isDarkMode={isDarkMode}>
              <SettingsToggleInput 
                type="checkbox" 
                checked={isSpeaking}
                onChange={() => toggleTextToSpeech(messages[messages.length - 1]?.content || '')}
              />
              <SettingsToggleSlider isDarkMode={isDarkMode} />
            </SettingsToggle>
          </SettingsOption>
        </SettingsGroup>
        
        <SettingsGroup>
          <SettingsGroupTitle isDarkMode={isDarkMode}>Chat History</SettingsGroupTitle>
          <SettingsOption>
            <SettingsLabel isDarkMode={isDarkMode}>Auto-save Chats</SettingsLabel>
            <SettingsToggle isDarkMode={isDarkMode}>
              <SettingsToggleInput type="checkbox" defaultChecked />
              <SettingsToggleSlider isDarkMode={isDarkMode} />
            </SettingsToggle>
          </SettingsOption>
        </SettingsGroup>
      </SettingsPanel>
      
      <ToggleFeaturesButton onClick={() => setShowFeaturesPanel(!showFeaturesPanel)}>
        {showFeaturesPanel ? <X size={20} /> : <Star size={20} />}
      </ToggleFeaturesButton>
      
      <ToggleSettingsButton onClick={() => setShowSettingsPanel(!showSettingsPanel)}>
        <Settings size={20} />
      </ToggleSettingsButton>
    </Container>
  );
}

export default AIChat;