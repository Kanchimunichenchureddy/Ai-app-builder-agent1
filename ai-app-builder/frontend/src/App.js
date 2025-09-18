import React, { useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from 'react-query';
import { Toaster } from 'react-hot-toast';
import styled, { createGlobalStyle } from 'styled-components';

// Components
import Navbar from './components/common/Navbar';
import Sidebar from './components/common/Sidebar';

// Pages
import Home from './pages/Home';
import Builder from './pages/Builder';
import Dashboard from './pages/Dashboard';
import Deploy from './pages/Deploy';
import Login from './pages/Login';
import Register from './pages/Register';
import AIChat from './pages/AIChat';
import Integrations from './pages/Integrations';
import Projects from './pages/Projects';
import Settings from './pages/Settings';

// Services
import { AuthProvider, useAuth } from './services/auth';

// Global Styles
const GlobalStyle = createGlobalStyle`
  * {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
  }

  body {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
    background: #f8fafc;
    color: #1a202c;
    line-height: 1.6;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
  }

  #loading {
    display: none;
  }
  
  ::-webkit-scrollbar {
    width: 8px;
    height: 8px;
  }
  
  ::-webkit-scrollbar-track {
    background: #f1f5f9;
  }
  
  ::-webkit-scrollbar-thumb {
    background: #c7d2fe;
    border-radius: 4px;
  }
  
  ::-webkit-scrollbar-thumb:hover {
    background: #a5b4fc;
  }
  
  // Enhanced focus styles for accessibility
  *:focus {
    outline: 2px solid #667eea;
    outline-offset: 2px;
  }
  
  // Smooth transitions
  * {
    transition: background-color 0.3s ease, border-color 0.3s ease, color 0.3s ease;
  }
`;

const AppContainer = styled.div`
  display: flex;
  min-height: 100vh;
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
`;

const MainContent = styled.main`
  flex: 1;
  display: flex;
  flex-direction: column;
  transition: margin-left 0.3s ease;
  margin-left: ${props => props.sidebarOpen ? '250px' : '0'};
  position: relative;
  z-index: 1;
  
  @media (max-width: 768px) {
    margin-left: 0;
  }
`;

const ContentArea = styled.div`
  flex: 1;
  padding: 20px;
  background: linear-gradient(180deg, #ffffff 0%, #f8fafc 100%);
  min-height: calc(100vh - 80px);
  
  @media (max-width: 768px) {
    padding: 15px;
  }
`;

// Create a client
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: 1,
      refetchOnWindowFocus: false,
    },
  },
});

function AppContent() {
  const { user, loading } = useAuth();
  const [sidebarOpen, setSidebarOpen] = React.useState(true);

  useEffect(() => {
    // Hide loading screen
    const loadingElement = document.getElementById('loading');
    if (loadingElement) {
      loadingElement.style.display = 'none';
    }
  }, []);

  if (loading) {
    return (
      <div style={{ 
        display: 'flex', 
        justifyContent: 'center', 
        alignItems: 'center', 
        height: '100vh',
        background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
      }}>
        <div style={{
          width: '60px',
          height: '60px',
          border: '4px solid rgba(255, 255, 255, 0.3)',
          borderRadius: '50%',
          borderTopColor: 'white',
          animation: 'spin 1s ease-in-out infinite'
        }} />
      </div>
    );
  }

  if (!user) {
    return (
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="*" element={<Login />} />
      </Routes>
    );
  }

  return (
    <AppContainer>
      <Sidebar isOpen={sidebarOpen} onToggle={() => setSidebarOpen(!sidebarOpen)} />
      <MainContent sidebarOpen={sidebarOpen}>
        <Navbar onMenuClick={() => setSidebarOpen(!sidebarOpen)} />
        <ContentArea>
          <Routes>
            <Route path="/" element={<Home />} />
            {/* AI Builder route - accepts state from AI Chat */}
            <Route path="/builder" element={<Builder />} />
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/deploy" element={<Deploy />} />
            {/* AI Chat route - can navigate to Builder with context */}
            <Route path="/ai-chat" element={<AIChat />} />
            <Route path="/integrations" element={<Integrations />} />
            <Route path="/projects" element={<Projects />} />
            <Route path="/settings" element={<Settings />} />
            <Route path="*" element={<Home />} />
          </Routes>
        </ContentArea>
      </MainContent>
    </AppContainer>
  );
}

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <AuthProvider>
        <Router>
          <GlobalStyle />
          <AppContent />
          <Toaster 
            position="top-right"
            toastOptions={{
              duration: 4000,
              style: {
                background: '#363636',
                color: '#fff',
                borderRadius: '12px',
                padding: '16px 20px',
                boxShadow: '0 4px 12px rgba(0, 0, 0, 0.15)'
              },
              success: {
                style: {
                  background: 'linear-gradient(135deg, #10b981 0%, #059669 100%)',
                },
              },
              error: {
                style: {
                  background: 'linear-gradient(135deg, #ef4444 0%, #dc2626 100%)',
                },
              },
              warning: {
                style: {
                  background: 'linear-gradient(135deg, #f59e0b 0%, #d97706 100%)',
                },
              },
              info: {
                style: {
                  background: 'linear-gradient(135deg, #3b82f6 0%, #2563eb 100%)',
                },
              }
            }}
          />
        </Router>
      </AuthProvider>
    </QueryClientProvider>
  );
}

export default App;