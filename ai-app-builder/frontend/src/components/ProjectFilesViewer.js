import React, { useState, useEffect } from 'react';
import styled from 'styled-components';
import { FileText, Folder, ChevronRight, ChevronDown, ExternalLink, Copy, Check } from 'lucide-react';
import api from '../services/api';

const Container = styled.div`
  display: flex;
  flex-direction: column;
  height: 100%;
  background: #ffffff;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  overflow: hidden;
`;

const Header = styled.div`
  padding: 1.5rem;
  border-bottom: 1px solid #e2e8f0;
  background: #f8fafc;
`;

const Title = styled.h3`
  margin: 0;
  font-size: 1.25rem;
  font-weight: 600;
  color: #1e293b;
  display: flex;
  align-items: center;
  gap: 0.75rem;
`;

const DemoSection = styled.div`
  margin-top: 1rem;
  padding: 1rem;
  background: #eff6ff;
  border-radius: 8px;
  border: 1px solid #dbeafe;
`;

const DemoButton = styled.a`
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
  color: white;
  text-decoration: none;
  border-radius: 8px;
  font-weight: 500;
  transition: all 0.2s ease;
  box-shadow: 0 4px 6px rgba(59, 130, 246, 0.2);
  
  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 8px rgba(59, 130, 246, 0.3);
  }
  
  &:active {
    transform: translateY(0);
  }
`;

const FilesTree = styled.div`
  flex: 1;
  overflow-y: auto;
  padding: 1rem;
`;

const TreeNode = styled.div`
  margin-bottom: 0.25rem;
`;

const TreeNodeLabel = styled.div`
  display: flex;
  align-items: center;
  padding: 0.5rem;
  border-radius: 6px;
  cursor: pointer;
  user-select: none;
  transition: background-color 0.15s ease;
  
  &:hover {
    background-color: #f1f5f9;
  }
  
  &.active {
    background-color: #dbeafe;
  }
`;

const TreeNodeIcon = styled.div`
  display: flex;
  align-items: center;
  margin-right: 0.5rem;
  color: #64748b;
`;

const TreeNodeName = styled.span`
  font-size: 0.95rem;
  color: #334155;
`;

const TreeNodeChildren = styled.div`
  margin-left: 1.5rem;
`;

const FileViewer = styled.div`
  flex: 1;
  display: flex;
  flex-direction: column;
  border-left: 1px solid #e2e8f0;
  background: #f8fafc;
`;

const FileHeader = styled.div`
  padding: 1rem 1.5rem;
  border-bottom: 1px solid #e2e8f0;
  background: #ffffff;
  display: flex;
  justify-content: space-between;
  align-items: center;
`;

const FileName = styled.h4`
  margin: 0;
  font-size: 1rem;
  font-weight: 500;
  color: #1e293b;
  display: flex;
  align-items: center;
  gap: 0.5rem;
`;

const CopyButton = styled.button`
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background: #e2e8f0;
  border: none;
  border-radius: 6px;
  font-size: 0.875rem;
  color: #475569;
  cursor: pointer;
  transition: all 0.15s ease;
  
  &:hover {
    background: #cbd5e1;
  }
`;

const FileContent = styled.pre`
  flex: 1;
  margin: 0;
  padding: 1.5rem;
  background: #ffffff;
  overflow: auto;
  font-family: 'Fira Code', 'Monaco', 'Consolas', monospace;
  font-size: 0.875rem;
  line-height: 1.5;
  color: #334155;
  white-space: pre-wrap;
`;

const SplitView = styled.div`
  display: flex;
  flex: 1;
  overflow: hidden;
`;

const FilesPanel = styled.div`
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  max-width: ${props => props.expanded ? '100%' : '400px'};
  transition: max-width 0.3s ease;
`;

const ToggleButton = styled.button`
  position: absolute;
  top: 50%;
  right: -12px;
  transform: translateY(-50%);
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: #ffffff;
  border: 1px solid #e2e8f0;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  z-index: 10;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  
  &:hover {
    background: #f1f5f9;
  }
`;

const NoFilesMessage = styled.div`
  padding: 2rem;
  text-align: center;
  color: #64748b;
`;

function ProjectFilesViewer({ project }) {
  const [files, setFiles] = useState({});
  const [selectedFile, setSelectedFile] = useState(null);
  const [copied, setCopied] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [expanded, setExpanded] = useState(false);
  const [deployments, setDeployments] = useState([]); // Add state for deployments

  useEffect(() => {
    if (project?.id) {
      fetchProjectFiles();
      fetchProjectDeployments(); // Fetch deployments when project loads
    }
  }, [project]);

  const fetchProjectFiles = async () => {
    try {
      setLoading(true);
      const response = await api.get(`/projects/${project.id}/files`);
      if (response.data.success) {
        setFiles(response.data.files);
      }
    } catch (err) {
      setError('Failed to load project files');
      console.error('Error fetching project files:', err);
    } finally {
      setLoading(false);
    }
  };

  // New function to fetch project deployments
  const fetchProjectDeployments = async () => {
    try {
      const response = await api.get(`/deployment/deployments/${project.id}`);
      if (response.data.success) {
        setDeployments(response.data.deployments);
      }
    } catch (err) {
      console.error('Error fetching project deployments:', err);
    }
  };

  const fetchFileContent = async (fileId) => {
    try {
      const response = await api.get(`/projects/${project.id}/file/${fileId}`);
      if (response.data.success) {
        setSelectedFile(response.data.file);
      }
    } catch (err) {
      console.error('Error fetching file content:', err);
    }
  };

  const copyToClipboard = () => {
    if (selectedFile?.content) {
      navigator.clipboard.writeText(selectedFile.content);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  const renderTree = (nodes, path = '') => {
    if (!nodes) return null;

    return Object.entries(nodes).map(([name, node]) => {
      const fullPath = path ? `${path}/${name}` : name;
      
      // Check if it's a file (has an id) or folder (object with children)
      if (node && typeof node === 'object' && 'id' in node) {
        // This is a file
        return (
          <TreeNode key={node.id}>
            <TreeNodeLabel 
              onClick={() => fetchFileContent(node.id)}
              className={selectedFile?.id === node.id ? 'active' : ''}
            >
              <TreeNodeIcon>
                <FileText size={16} />
              </TreeNodeIcon>
              <TreeNodeName>{name}</TreeNodeName>
            </TreeNodeLabel>
          </TreeNode>
        );
      } else {
        // This is a folder
        const [isOpen, setIsOpen] = useState(true);
        
        return (
          <TreeNode key={fullPath}>
            <TreeNodeLabel onClick={() => setIsOpen(!isOpen)}>
              <TreeNodeIcon>
                {isOpen ? <ChevronDown size={16} /> : <ChevronRight size={16} />}
              </TreeNodeIcon>
              <TreeNodeIcon>
                <Folder size={16} />
              </TreeNodeIcon>
              <TreeNodeName>{name}</TreeNodeName>
            </TreeNodeLabel>
            {isOpen && (
              <TreeNodeChildren>
                {renderTree(node, fullPath)}
              </TreeNodeChildren>
            )}
          </TreeNode>
        );
      }
    });
  };

  if (loading) {
    return (
      <Container>
        <Header>
          <Title>Project Files</Title>
        </Header>
        <div style={{ padding: '2rem', textAlign: 'center', color: '#64748b' }}>
          Loading files...
        </div>
      </Container>
    );
  }

  if (error) {
    return (
      <Container>
        <Header>
          <Title>Project Files</Title>
        </Header>
        <div style={{ padding: '2rem', textAlign: 'center', color: '#ef4444' }}>
          {error}
        </div>
      </Container>
    );
  }

  return (
    <Container>
      <Header>
        <Title>Project Files</Title>
        {/* Show View Demo button if there's a successful deployment */}
        {deployments.length > 0 && deployments.some(d => d.status === 'deployed') && (
          <DemoSection>
            <DemoButton 
              href={deployments.find(d => d.status === 'deployed')?.url} 
              target="_blank"
              rel="noopener noreferrer"
            >
              <ExternalLink size={16} />
              View Demo
            </DemoButton>
          </DemoSection>
        )}
        {/* Show deployment status if there are deployments */}
        {deployments.length > 0 && deployments.some(d => d.status !== 'deployed') && (
          <DemoSection>
            <div style={{ color: '#667eea', fontWeight: '500' }}>
              {deployments.some(d => d.status === 'building') ? 'Deploying...' : 'Deployment in progress'}
            </div>
          </DemoSection>
        )}
      </Header>
      
      <SplitView>
        <FilesPanel expanded={expanded}>
          <FilesTree>
            {Object.keys(files).length > 0 ? (
              renderTree(files)
            ) : (
              <NoFilesMessage>
                No files generated yet for this project.
              </NoFilesMessage>
            )}
          </FilesTree>
        </FilesPanel>
        
        {!expanded && selectedFile && (
          <FileViewer>
            <FileHeader>
              <FileName>
                <FileText size={16} />
                {selectedFile.name}
              </FileName>
              <CopyButton onClick={copyToClipboard}>
                {copied ? <Check size={16} /> : <Copy size={16} />}
                {copied ? 'Copied!' : 'Copy'}
              </CopyButton>
            </FileHeader>
            <FileContent>{selectedFile.content}</FileContent>
          </FileViewer>
        )}
      </SplitView>
    </Container>
  );
}

export default ProjectFilesViewer;