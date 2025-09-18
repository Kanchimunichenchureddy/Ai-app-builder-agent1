import React, { useState } from 'react';
import styled, { keyframes } from 'styled-components';
import { 
  User, 
  Key, 
  Bell, 
  Palette, 
  Globe, 
  Shield, 
  Database, 
  Cloud, 
  CreditCard,
  Save,
  Eye,
  EyeOff,
  Edit3,
  Trash2,
  Plus,
  CheckCircle,
  XCircle,
  AlertCircle,
  Info,
  ExternalLink
} from 'lucide-react';
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
  margin-bottom: 2rem;
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

const Tabs = styled.div`
  display: flex;
  border-bottom: 1px solid #e2e8f0;
  margin-bottom: 2rem;
  overflow-x: auto;
  
  @media (max-width: 768px) {
    flex-wrap: wrap;
  }
`;

const Tab = styled.button`
  padding: 1rem 1.5rem;
  background: none;
  border: none;
  color: ${props => props.active ? '#667eea' : '#64748b'};
  font-weight: ${props => props.active ? '600' : 'normal'};
  border-bottom: 3px solid ${props => props.active ? '#667eea' : 'transparent'};
  cursor: pointer;
  transition: all 0.2s ease;
  white-space: nowrap;
  
  &:hover {
    color: #667eea;
  }
  
  @media (max-width: 768px) {
    padding: 0.75rem 1rem;
    font-size: 0.9rem;
  }
`;

const Section = styled.div`
  background: white;
  border-radius: 1rem;
  padding: 2rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  border: 1px solid #e2e8f0;
  margin-bottom: 2rem;
  animation: ${fadeIn} 0.5s ease-out;
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

const SectionDescription = styled.p`
  color: #64748b;
  margin-bottom: 1.5rem;
`;

const Form = styled.form`
  display: grid;
  gap: 1.5rem;
`;

const FormGroup = styled.div`
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
`;

const Label = styled.label`
  font-weight: 500;
  color: #1e293b;
`;

const Input = styled.input`
  padding: 0.75rem 1rem;
  border: 1px solid #e2e8f0;
  border-radius: 0.5rem;
  font-size: 1rem;
  
  &:focus {
    outline: none;
    border-color: #667eea;
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
  }
`;

const Select = styled.select`
  padding: 0.75rem 1rem;
  border: 1px solid #e2e8f0;
  border-radius: 0.5rem;
  font-size: 1rem;
  background: white;
  
  &:focus {
    outline: none;
    border-color: #667eea;
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
  }
`;

const TextArea = styled.textarea`
  padding: 0.75rem 1rem;
  border: 1px solid #e2e8f0;
  border-radius: 0.5rem;
  font-size: 1rem;
  min-height: 120px;
  resize: vertical;
  
  &:focus {
    outline: none;
    border-color: #667eea;
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
  }
`;

const Button = styled.button`
  padding: 0.75rem 1.5rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 0.5rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  
  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(102, 126, 234, 0.3);
  }
  
  &:disabled {
    opacity: 0.6;
    cursor: not-allowed;
    transform: none;
    box-shadow: none;
  }
  
  &.secondary {
    background: #f1f5f9;
    color: #1e293b;
    
    &:hover {
      background: #e2e8f0;
      transform: translateY(-1px);
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
    }
  }
  
  &.danger {
    background: #ef4444;
    
    &:hover {
      background: #dc2626;
      box-shadow: 0 6px 20px rgba(239, 68, 68, 0.3);
    }
  }
`;

const Toggle = styled.label`
  position: relative;
  display: inline-block;
  width: 50px;
  height: 24px;
`;

const ToggleInput = styled.input`
  opacity: 0;
  width: 0;
  height: 0;
`;

const ToggleSlider = styled.span`
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #cbd5e1;
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
  
  ${ToggleInput}:checked + & {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  }
  
  ${ToggleInput}:checked + &:before {
    transform: translateX(26px);
  }
`;

const ToggleContainer = styled.div`
  display: flex;
  align-items: center;
  gap: 0.75rem;
`;

const CardGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
  margin-top: 1rem;
`;

const Card = styled.div`
  background: white;
  border-radius: 0.75rem;
  padding: 1.5rem;
  border: 1px solid #e2e8f0;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  
  &:hover {
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  }
`;

const CardHeader = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1rem;
`;

const CardTitle = styled.h3`
  font-size: 1.1rem;
  font-weight: 600;
  color: #1e293b;
  margin: 0;
`;

const CardActions = styled.div`
  display: flex;
  gap: 0.5rem;
`;

const IconButton = styled.button`
  background: none;
  border: none;
  color: #64748b;
  cursor: pointer;
  padding: 0.25rem;
  border-radius: 0.25rem;
  
  &:hover {
    background: #f1f5f9;
    color: #1e293b;
  }
`;

const CardContent = styled.div`
  color: #64748b;
  font-size: 0.9rem;
  line-height: 1.5;
`;

const NotificationItem = styled.div`
  display: flex;
  align-items: flex-start;
  gap: 1rem;
  padding: 1rem;
  border-radius: 0.5rem;
  background: #f8fafc;
  margin-bottom: 1rem;
  
  &:last-child {
    margin-bottom: 0;
  }
`;

const NotificationIcon = styled.div`
  flex-shrink: 0;
  width: 2rem;
  height: 2rem;
  border-radius: 50%;
  background: ${props => {
    if (props.type === 'success') return '#dcfce7';
    if (props.type === 'error') return '#fee2e2';
    if (props.type === 'warning') return '#fef3c7';
    return '#ede9fe';
  }};
  display: flex;
  align-items: center;
  justify-content: center;
  
  ${Info} {
    color: ${props => {
      if (props.type === 'success') return '#10b981';
      if (props.type === 'error') return '#ef4444';
      if (props.type === 'warning') return '#f59e0b';
      return '#8b5cf6';
    }};
  }
`;

const NotificationContent = styled.div`
  flex: 1;
`;

const NotificationTitle = styled.h4`
  font-weight: 600;
  color: #1e293b;
  margin: 0 0 0.25rem 0;
`;

const NotificationDescription = styled.p`
  color: #64748b;
  margin: 0;
  font-size: 0.9rem;
`;

const NotificationTime = styled.div`
  font-size: 0.8rem;
  color: #94a3b8;
  margin-top: 0.25rem;
`;

function Settings() {
  const [activeTab, setActiveTab] = useState('profile');
  const [showPassword, setShowPassword] = useState(false);
  const [formData, setFormData] = useState({
    fullName: 'John Doe',
    email: 'john.doe@example.com',
    currentPassword: '',
    newPassword: '',
    confirmPassword: '',
    language: 'en',
    theme: 'light',
    notifications: {
      email: true,
      push: true,
      sms: false
    }
  });

  const handleInputChange = (e) => {
    const { name, value, type, checked } = e.target;
    
    if (name.startsWith('notifications.')) {
      const notificationType = name.split('.')[1];
      setFormData(prev => ({
        ...prev,
        notifications: {
          ...prev.notifications,
          [notificationType]: checked
        }
      }));
    } else {
      setFormData(prev => ({
        ...prev,
        [name]: type === 'checkbox' ? checked : value
      }));
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    toast.success('Settings saved successfully!');
  };

  const handleDeleteAccount = () => {
    if (window.confirm('Are you sure you want to delete your account? This action cannot be undone.')) {
      toast.success('Account deletion requested. Check your email for confirmation.');
    }
  };

  const renderProfileSettings = () => (
    <Section>
      <SectionTitle>
        <User size={24} />
        Profile Information
      </SectionTitle>
      <SectionDescription>
        Update your personal information and account details
      </SectionDescription>
      
      <Form onSubmit={handleSubmit}>
        <FormGroup>
          <Label htmlFor="fullName">Full Name</Label>
          <Input
            type="text"
            id="fullName"
            name="fullName"
            value={formData.fullName}
            onChange={handleInputChange}
          />
        </FormGroup>
        
        <FormGroup>
          <Label htmlFor="email">Email Address</Label>
          <Input
            type="email"
            id="email"
            name="email"
            value={formData.email}
            onChange={handleInputChange}
          />
        </FormGroup>
        
        <Button type="submit">
          <Save size={16} />
          Save Changes
        </Button>
      </Form>
    </Section>
  );

  const renderSecuritySettings = () => (
    <Section>
      <SectionTitle>
        <Key size={24} />
        Security
      </SectionTitle>
      <SectionDescription>
        Manage your password and security settings
      </SectionDescription>
      
      <Form onSubmit={handleSubmit}>
        <FormGroup>
          <Label htmlFor="currentPassword">Current Password</Label>
          <div style={{ position: 'relative' }}>
            <Input
              type={showPassword ? "text" : "password"}
              id="currentPassword"
              name="currentPassword"
              value={formData.currentPassword}
              onChange={handleInputChange}
            />
            <IconButton
              type="button"
              style={{ position: 'absolute', right: '10px', top: '50%', transform: 'translateY(-50%)' }}
              onClick={() => setShowPassword(!showPassword)}
            >
              {showPassword ? <EyeOff size={16} /> : <Eye size={16} />}
            </IconButton>
          </div>
        </FormGroup>
        
        <FormGroup>
          <Label htmlFor="newPassword">New Password</Label>
          <Input
            type={showPassword ? "text" : "password"}
            id="newPassword"
            name="newPassword"
            value={formData.newPassword}
            onChange={handleInputChange}
          />
        </FormGroup>
        
        <FormGroup>
          <Label htmlFor="confirmPassword">Confirm New Password</Label>
          <Input
            type={showPassword ? "text" : "password"}
            id="confirmPassword"
            name="confirmPassword"
            value={formData.confirmPassword}
            onChange={handleInputChange}
          />
        </FormGroup>
        
        <Button type="submit">
          <Save size={16} />
          Update Password
        </Button>
      </Form>
      
      <Section style={{ marginTop: '2rem' }}>
        <SectionTitle>
          <Shield size={24} />
          Account Security
        </SectionTitle>
        <SectionDescription>
          Manage your account security settings
        </SectionDescription>
        
        <CardGrid>
          <Card>
            <CardHeader>
              <CardTitle>Two-Factor Authentication</CardTitle>
              <CardActions>
                <Button className="secondary" size="sm">
                  <Edit3 size={14} />
                  Enable
                </Button>
              </CardActions>
            </CardHeader>
            <CardContent>
              Add an extra layer of security to your account by requiring a code in addition to your password.
            </CardContent>
          </Card>
          
          <Card>
            <CardHeader>
              <CardTitle>Login History</CardTitle>
              <CardActions>
                <Button className="secondary" size="sm">
                  <ExternalLink size={14} />
                  View
                </Button>
              </CardActions>
            </CardHeader>
            <CardContent>
              View and manage your recent login activity and connected devices.
            </CardContent>
          </Card>
        </CardGrid>
        
        <div style={{ marginTop: '2rem' }}>
          <Button className="danger" onClick={handleDeleteAccount}>
            <Trash2 size={16} />
            Delete Account
          </Button>
        </div>
      </Section>
    </Section>
  );

  const renderPreferencesSettings = () => (
    <Section>
      <SectionTitle>
        <Palette size={24} />
        Preferences
      </SectionTitle>
      <SectionDescription>
        Customize your experience and preferences
      </SectionDescription>
      
      <Form onSubmit={handleSubmit}>
        <FormGroup>
          <Label htmlFor="language">Language</Label>
          <Select
            id="language"
            name="language"
            value={formData.language}
            onChange={handleInputChange}
          >
            <option value="en">English</option>
            <option value="es">Spanish</option>
            <option value="fr">French</option>
            <option value="de">German</option>
          </Select>
        </FormGroup>
        
        <FormGroup>
          <Label htmlFor="theme">Theme</Label>
          <Select
            id="theme"
            name="theme"
            value={formData.theme}
            onChange={handleInputChange}
          >
            <option value="light">Light</option>
            <option value="dark">Dark</option>
            <option value="system">System Default</option>
          </Select>
        </FormGroup>
        
        <Button type="submit">
          <Save size={16} />
          Save Preferences
        </Button>
      </Form>
    </Section>
  );

  const renderNotificationsSettings = () => (
    <Section>
      <SectionTitle>
        <Bell size={24} />
        Notifications
      </SectionTitle>
      <SectionDescription>
        Manage how you receive notifications
      </SectionDescription>
      
      <Form onSubmit={handleSubmit}>
        <FormGroup>
          <ToggleContainer>
            <Toggle>
              <ToggleInput
                type="checkbox"
                name="notifications.email"
                checked={formData.notifications.email}
                onChange={handleInputChange}
              />
              <ToggleSlider />
            </Toggle>
            <Label>Email Notifications</Label>
          </ToggleContainer>
        </FormGroup>
        
        <FormGroup>
          <ToggleContainer>
            <Toggle>
              <ToggleInput
                type="checkbox"
                name="notifications.push"
                checked={formData.notifications.push}
                onChange={handleInputChange}
              />
              <ToggleSlider />
            </Toggle>
            <Label>Push Notifications</Label>
          </ToggleContainer>
        </FormGroup>
        
        <FormGroup>
          <ToggleContainer>
            <Toggle>
              <ToggleInput
                type="checkbox"
                name="notifications.sms"
                checked={formData.notifications.sms}
                onChange={handleInputChange}
              />
              <ToggleSlider />
            </Toggle>
            <Label>SMS Notifications</Label>
          </ToggleContainer>
        </FormGroup>
        
        <Button type="submit">
          <Save size={16} />
          Save Notification Settings
        </Button>
      </Form>
      
      <Section style={{ marginTop: '2rem' }}>
        <SectionTitle>
          <Bell size={24} />
          Recent Notifications
        </SectionTitle>
        
        <div>
          <NotificationItem>
            <NotificationIcon type="success">
              <Info size={16} />
            </NotificationIcon>
            <NotificationContent>
              <NotificationTitle>Deployment Successful</NotificationTitle>
              <NotificationDescription>
                Your "E-commerce Dashboard" application has been successfully deployed to Vercel.
              </NotificationDescription>
              <NotificationTime>2 hours ago</NotificationTime>
            </NotificationContent>
          </NotificationItem>
          
          <NotificationItem>
            <NotificationIcon type="warning">
              <Info size={16} />
            </NotificationIcon>
            <NotificationContent>
              <NotificationTitle>Maintenance Scheduled</NotificationTitle>
              <NotificationDescription>
                System maintenance scheduled for tomorrow at 2:00 AM UTC. Expect brief downtime.
              </NotificationDescription>
              <NotificationTime>1 day ago</NotificationTime>
            </NotificationContent>
          </NotificationItem>
          
          <NotificationItem>
            <NotificationIcon type="info">
              <Info size={16} />
            </NotificationIcon>
            <NotificationContent>
              <NotificationTitle>New Feature Available</NotificationTitle>
              <NotificationDescription>
                We've added support for deploying to Google Cloud Platform. Try it out now!
              </NotificationDescription>
              <NotificationTime>3 days ago</NotificationTime>
            </NotificationContent>
          </NotificationItem>
        </div>
      </Section>
    </Section>
  );

  const renderIntegrationsSettings = () => (
    <Section>
      <SectionTitle>
        <Cloud size={24} />
        Integrations
      </SectionTitle>
      <SectionDescription>
        Connect your account with third-party services
      </SectionDescription>
      
      <CardGrid>
        <Card>
          <CardHeader>
            <CardTitle>GitHub</CardTitle>
            <CardActions>
              <Button className="secondary" size="sm">
                Connect
              </Button>
            </CardActions>
          </CardHeader>
          <CardContent>
            Connect your GitHub account to automatically deploy changes from your repositories.
          </CardContent>
        </Card>
        
        <Card>
          <CardHeader>
            <CardTitle>Slack</CardTitle>
            <CardActions>
              <Button className="secondary" size="sm">
                Connect
              </Button>
            </CardActions>
          </CardHeader>
          <CardContent>
            Receive deployment notifications and updates directly in your Slack channels.
          </CardContent>
        </Card>
        
        <Card>
          <CardHeader>
            <CardTitle>Google Cloud</CardTitle>
            <CardActions>
              <Button className="secondary" size="sm">
                Connect
              </Button>
            </CardActions>
          </CardHeader>
          <CardContent>
            Deploy your applications directly to Google Cloud Platform with one click.
          </CardContent>
        </Card>
        
        <Card>
          <CardHeader>
            <CardTitle>AWS</CardTitle>
            <CardActions>
              <Button className="secondary" size="sm">
                Connect
              </Button>
            </CardActions>
          </CardHeader>
          <CardContent>
            Deploy your applications to Amazon Web Services with our integrated deployment tools.
          </CardContent>
        </Card>
      </CardGrid>
    </Section>
  );

  const tabs = [
    { id: 'profile', label: 'Profile', icon: User },
    { id: 'security', label: 'Security', icon: Key },
    { id: 'preferences', label: 'Preferences', icon: Palette },
    { id: 'notifications', label: 'Notifications', icon: Bell },
    { id: 'integrations', label: 'Integrations', icon: Cloud }
  ];

  const renderActiveTab = () => {
    switch (activeTab) {
      case 'profile':
        return renderProfileSettings();
      case 'security':
        return renderSecuritySettings();
      case 'preferences':
        return renderPreferencesSettings();
      case 'notifications':
        return renderNotificationsSettings();
      case 'integrations':
        return renderIntegrationsSettings();
      default:
        return renderProfileSettings();
    }
  };

  return (
    <Container>
      <Header>
        <Title>Settings</Title>
        <Subtitle>Manage your account settings and preferences</Subtitle>
      </Header>
      
      <Tabs>
        {tabs.map((tab) => (
          <Tab
            key={tab.id}
            active={activeTab === tab.id}
            onClick={() => setActiveTab(tab.id)}
          >
            <tab.icon size={16} style={{ marginRight: '0.5rem' }} />
            {tab.label}
          </Tab>
        ))}
      </Tabs>
      
      {renderActiveTab()}
    </Container>
  );
}

export default Settings;