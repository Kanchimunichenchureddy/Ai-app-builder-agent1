import React, { useState } from 'react';
import styled, { keyframes } from 'styled-components';
import { 
  CreditCard, 
  Database, 
  Grid, 
  Bot, 
  CheckCircle, 
  AlertCircle, 
  Plus, 
  Settings,
  Zap,
  Link,
  Shield,
  Key,
  RefreshCw,
  Trash2,
  Edit3,
  Eye,
  EyeOff,
  // Adding more icons for enhanced UI
  Copy,
  Share2,
  Heart,
  ThumbsUp,
  ThumbsDown,
  Search,
  Filter,
  Grid as GridIcon,
  List,
  ExternalLink,
  Play,
  Square,
  Lock,
  Unlock,
  GitBranch,
  Server,
  HardDrive
} from 'lucide-react';

const pulse = keyframes`
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
`;

const slideIn = keyframes`
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
`;

const Header = styled.div`
  margin-bottom: 2rem;
  position: relative;
  z-index: 1;
`;

const Title = styled.h1`
  font-size: 2rem;
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 0.5rem;
`;

const Subtitle = styled.p`
  color: #64748b;
  font-size: 1.1rem;
`;

const Controls = styled.div`
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
  flex-wrap: wrap;
  
  @media (max-width: 768px) {
    flex-direction: column;
  }
`;

const SearchInput = styled.input`
  flex: 1;
  padding: 0.75rem 1rem;
  border: 1px solid #e2e8f0;
  border-radius: 0.75rem;
  font-size: 1rem;
  min-width: 250px;
  
  &:focus {
    outline: none;
    border-color: #667eea;
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
  }
  
  @media (max-width: 768px) {
    min-width: 100%;
  }
`;

const FilterButton = styled.button`
  background: #f1f5f9;
  border: none;
  padding: 0.75rem 1.25rem;
  border-radius: 0.75rem;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  color: #1e293b;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: all 0.2s ease;
  
  &:hover {
    background: #e2e8f0;
  }
  
  @media (max-width: 768px) {
    padding: 0.625rem 1rem;
  }
`;

const ViewToggle = styled.div`
  display: flex;
  background: #f1f5f9;
  border-radius: 0.75rem;
  overflow: hidden;
`;

const ViewButton = styled.button`
  background: ${props => props.active ? 'white' : 'transparent'};
  border: none;
  padding: 0.75rem 1.25rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-weight: ${props => props.active ? '500' : 'normal'};
  
  &:hover {
    background: ${props => props.active ? 'white' : '#e2e8f0'};
  }
  
  @media (max-width: 768px) {
    padding: 0.625rem 1rem;
    font-size: 0.9rem;
  }
`;

const IntegrationsGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
  position: relative;
  z-index: 1;
`;

const IntegrationCard = styled.div`
  background: white;
  border-radius: 1.25rem;
  padding: 1.5rem;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.08);
  border: 1px solid #e2e8f0;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
  
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
    background: linear-gradient(90deg, #667eea, #764ba2);
  }
  
  @media (max-width: 768px) {
    padding: 1.25rem;
  }
`;

const IntegrationHeader = styled.div`
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1.5rem;
`;

const IntegrationIcon = styled.div`
  width: 3.5rem;
  height: 3.5rem;
  border-radius: 1rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  animation: ${float} 3s ease-in-out infinite;
`;

const IntegrationInfo = styled.div`
  flex: 1;
`;

const IntegrationName = styled.h3`
  font-size: 1.25rem;
  font-weight: 600;
  color: #1e293b;
  margin: 0 0 0.25rem 0;
`;

const IntegrationDescription = styled.p`
  color: #64748b;
  font-size: 0.9rem;
  margin: 0;
`;

const IntegrationStatus = styled.div`
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.9rem;
  font-weight: 500;
  
  &.connected {
    color: #10b981;
  }
  
  &.disconnected {
    color: #ef4444;
  }
`;

const IntegrationActions = styled.div`
  display: flex;
  gap: 0.75rem;
  margin-top: 1.5rem;
  padding-top: 1.5rem;
  border-top: 1px solid #f1f5f9;
  
  @media (max-width: 768px) {
    flex-direction: column;
  }
`;

const ActionButton = styled.button`
  flex: 1;
  background: #f1f5f9;
  border: none;
  padding: 0.75rem;
  border-radius: 0.75rem;
  font-size: 0.9rem;
  font-weight: 500;
  cursor: pointer;
  color: #1e293b;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  transition: all 0.2s ease;
  
  &:hover {
    background: #e2e8f0;
  }
  
  &.primary {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
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
    background: #fee2e2;
    color: #ef4444;
    
    &:hover {
      background: #fecaca;
    }
  }
  
  @media (max-width: 768px) {
    padding: 0.625rem;
    font-size: 0.8rem;
  }
`;

const FormSection = styled.div`
  background: white;
  border-radius: 1.25rem;
  padding: 2rem;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.08);
  border: 1px solid #e2e8f0;
  margin-bottom: 2rem;
  animation: ${slideIn} 0.5s ease-out;
  position: relative;
  z-index: 1;
  
  @media (max-width: 768px) {
    padding: 1.5rem;
  }
`;

const SectionTitle = styled.h2`
  font-size: 1.5rem;
  font-weight: 600;
  color: #1e293b;
  margin-bottom: 1.5rem;
  display: flex;
  align-items: center;
  gap: 0.75rem;
`;

const Form = styled.form`
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
  
  @media (max-width: 768px) {
    grid-template-columns: 1fr;
  }
`;

const FormGroup = styled.div`
  grid-column: ${props => props.fullWidth ? '1 / -1' : 'auto'};
`;

const Label = styled.label`
  display: block;
  font-size: 0.9rem;
  font-weight: 500;
  color: #1e293b;
  margin-bottom: 0.5rem;
`;

const Input = styled.input`
  width: 100%;
  padding: 0.75rem 1rem;
  border: 1px solid #e2e8f0;
  border-radius: 0.75rem;
  font-size: 1rem;
  transition: all 0.2s ease;
  
  &:focus {
    outline: none;
    border-color: #667eea;
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
  }
  
  @media (max-width: 768px) {
    padding: 0.625rem 0.875rem;
    font-size: 0.9rem;
  }
`;

const InputWithIcon = styled.div`
  position: relative;
  
  input {
    padding-right: 3rem;
  }
  
  svg {
    position: absolute;
    right: 1rem;
    top: 50%;
    transform: translateY(-50%);
    color: #94a3b8;
    cursor: pointer;
  }
`;

const SubmitButton = styled.button`
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  padding: 1rem 2rem;
  border-radius: 0.75rem;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
  grid-column: 1 / -1;
  width: 100%;
  
  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
  }
  
  &:disabled {
    opacity: 0.7;
    cursor: not-allowed;
    transform: none;
  }
  
  @media (max-width: 768px) {
    padding: 0.875rem 1.5rem;
    font-size: 0.9rem;
  }
`;

const Tabs = styled.div`
  display: flex;
  gap: 0.5rem;
  margin-bottom: 2rem;
  border-bottom: 1px solid #e2e8f0;
  padding-bottom: 1rem;
  flex-wrap: wrap;
  
  @media (max-width: 768px) {
    overflow-x: auto;
    flex-wrap: nowrap;
  }
`;

const Tab = styled.button`
  background: ${props => props.active ? '#667eea' : 'transparent'};
  color: ${props => props.active ? 'white' : '#64748b'};
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 2rem;
  font-size: 0.9rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  white-space: nowrap;
  
  &:hover {
    background: ${props => props.active ? '#667eea' : '#f1f5f9'};
  }
  
  @media (max-width: 768px) {
    padding: 0.625rem 1.25rem;
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
  
  &.connected {
    background: #dcfce7;
    color: #16a34a;
  }
  
  &.disconnected {
    background: #fee2e2;
    color: #dc2626;
  }
  
  &.pending {
    background: #fef3c7;
    color: #d97706;
  }
`;

const LoadingSpinner = styled.div`
  display: inline-flex;
  animation: ${props => props.rotate && pulse} 1s linear infinite;
`;

function Integrations() {
  const [activeTab, setActiveTab] = useState('all');
  const [showApiKey, setShowApiKey] = useState(false);
  const [formData, setFormData] = useState({
    stripeSecretKey: '',
    googleClientId: '',
    googleClientSecret: '',
    deepseekApiKey: ''
  });
  const [searchTerm, setSearchTerm] = useState('');
  const [viewMode, setViewMode] = useState('grid');
  
  const integrations = [
    {
      id: 'stripe',
      name: 'Stripe Payments',
      description: 'Accept payments with Stripe',
      icon: <CreditCard size={24} />,
      connected: true,
      category: 'payment'
    },
    {
      id: 'google-drive',
      name: 'Google Drive',
      description: 'Access and manage Google Drive files',
      icon: <Database size={24} />,
      connected: false,
      category: 'storage'
    },
    {
      id: 'google-sheets',
      name: 'Google Sheets',
      description: 'Read and write Google Sheets data',
      icon: <GridIcon size={24} />,
      connected: true,
      category: 'data'
    },
    {
      id: 'deepseek',
      name: 'DeepSeek AI',
      description: 'Generate code with DeepSeek AI',
      icon: <Bot size={24} />,
      connected: false,
      category: 'ai'
    },
    {
      id: 'openai',
      name: 'OpenAI',
      description: 'Integrate with OpenAI GPT models',
      icon: <Bot size={24} />,
      connected: true,
      category: 'ai'
    },
    {
      id: 'github',
      name: 'GitHub',
      description: 'Connect with GitHub repositories',
      icon: <GitBranch size={24} />,
      connected: false,
      category: 'dev'
    }
  ];
  
  const filteredIntegrations = integrations.filter(integration => {
    const matchesSearch = integration.name.toLowerCase().includes(searchTerm.toLowerCase()) || 
                         integration.description.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesTab = activeTab === 'all' || integration.category === activeTab;
    return matchesSearch && matchesTab;
  });
  
  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };
  
  const handleSubmit = (e) => {
    e.preventDefault();
    // Handle form submission
    console.log('Form submitted:', formData);
    alert('API keys saved successfully!');
  };
  
  const handleConnect = (integrationId) => {
    // In a real implementation, this would initiate the OAuth flow
    console.log(`Connecting to ${integrationId}`);
    alert(`Connecting to ${integrationId}...`);
  };
  
  const handleDisconnect = (integrationId) => {
    if (window.confirm(`Are you sure you want to disconnect from ${integrationId}?`)) {
      // In a real implementation, this would disconnect the integration
      console.log(`Disconnecting from ${integrationId}`);
      alert(`Disconnected from ${integrationId}`);
    }
  };
  
  const handleTestConnection = (integrationId) => {
    // In a real implementation, this would test the connection
    console.log(`Testing connection to ${integrationId}`);
    alert(`Connection to ${integrationId} is working!`);
  };
  
  return (
    <Container>
      <Header>
        <Title>Integrations</Title>
        <Subtitle>Connect your favorite tools and services to enhance your workflow</Subtitle>
      </Header>
      
      <Controls>
        <SearchInput
          type="text"
          placeholder="Search integrations..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
        />
        <FilterButton>
          <Filter size={16} />
          Filter
        </FilterButton>
        <ViewToggle>
          <ViewButton 
            active={viewMode === 'grid'} 
            onClick={() => setViewMode('grid')}
          >
            <GridIcon size={16} />
            Grid
          </ViewButton>
          <ViewButton 
            active={viewMode === 'list'} 
            onClick={() => setViewMode('list')}
          >
            <List size={16} />
            List
          </ViewButton>
        </ViewToggle>
      </Controls>
      
      <Tabs>
        <Tab active={activeTab === 'all'} onClick={() => setActiveTab('all')}>All Integrations</Tab>
        <Tab active={activeTab === 'ai'} onClick={() => setActiveTab('ai')}>AI Services</Tab>
        <Tab active={activeTab === 'payment'} onClick={() => setActiveTab('payment')}>Payment</Tab>
        <Tab active={activeTab === 'storage'} onClick={() => setActiveTab('storage')}>Storage</Tab>
        <Tab active={activeTab === 'data'} onClick={() => setActiveTab('data')}>Data</Tab>
        <Tab active={activeTab === 'dev'} onClick={() => setActiveTab('dev')}>Developer</Tab>
      </Tabs>
      
      <IntegrationsGrid>
        {filteredIntegrations.map((integration) => (
          <IntegrationCard key={integration.id}>
            <IntegrationHeader>
              <IntegrationIcon>
                {integration.icon}
              </IntegrationIcon>
              <IntegrationInfo>
                <IntegrationName>{integration.name}</IntegrationName>
                <IntegrationDescription>{integration.description}</IntegrationDescription>
              </IntegrationInfo>
              <IntegrationStatus className={integration.connected ? 'connected' : 'disconnected'}>
                {integration.connected ? <CheckCircle size={16} /> : <AlertCircle size={16} />}
                {integration.connected ? 'Connected' : 'Not Connected'}
              </IntegrationStatus>
            </IntegrationHeader>
            
            <IntegrationActions>
              {integration.connected ? (
                <>
                  <ActionButton onClick={() => handleTestConnection(integration.id)}>
                    <Zap size={16} />
                    Test
                  </ActionButton>
                  <ActionButton 
                    className="danger" 
                    onClick={() => handleDisconnect(integration.id)}
                  >
                    <Trash2 size={16} />
                    Disconnect
                  </ActionButton>
                </>
              ) : (
                <>
                  <ActionButton 
                    className="primary" 
                    onClick={() => handleConnect(integration.id)}
                  >
                    <Link size={16} />
                    Connect
                  </ActionButton>
                  <ActionButton>
                    <Eye size={16} />
                    Preview
                  </ActionButton>
                </>
              )}
            </IntegrationActions>
          </IntegrationCard>
        ))}
      </IntegrationsGrid>
      
      <FormSection>
        <SectionTitle>
          <Settings size={24} />
          API Configuration
        </SectionTitle>
        
        <Form onSubmit={handleSubmit}>
          <FormGroup>
            <Label>Stripe Secret Key</Label>
            <InputWithIcon>
              <Input
                type={showApiKey ? "text" : "password"}
                name="stripeSecretKey"
                value={formData.stripeSecretKey}
                onChange={handleInputChange}
                placeholder="sk_live_..."
              />
              <button type="button" onClick={() => setShowApiKey(!showApiKey)}>
                {showApiKey ? <EyeOff size={16} /> : <Eye size={16} />}
              </button>
            </InputWithIcon>
          </FormGroup>
          
          <FormGroup>
            <Label>Google Client ID</Label>
            <Input
              type="text"
              name="googleClientId"
              value={formData.googleClientId}
              onChange={handleInputChange}
              placeholder="Your Google Client ID"
            />
          </FormGroup>
          
          <FormGroup>
            <Label>Google Client Secret</Label>
            <Input
              type="password"
              name="googleClientSecret"
              value={formData.googleClientSecret}
              onChange={handleInputChange}
              placeholder="Your Google Client Secret"
            />
          </FormGroup>
          
          <FormGroup>
            <Label>DeepSeek API Key</Label>
            <Input
              type="password"
              name="deepseekApiKey"
              value={formData.deepseekApiKey}
              onChange={handleInputChange}
              placeholder="Your DeepSeek API Key"
            />
          </FormGroup>
          
          <SubmitButton type="submit">
            <Zap size={16} />
            Save Configuration
          </SubmitButton>
        </Form>
      </FormSection>
    </Container>
  );
}

export default Integrations;