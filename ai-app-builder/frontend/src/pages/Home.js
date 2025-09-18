import React from 'react';
import styled, { keyframes } from 'styled-components';
import { useNavigate } from 'react-router-dom';
import { 
  Sparkles, 
  Bot, 
  Code, 
  Database, 
  Cloud, 
  Rocket, 
  Zap, 
  Globe, 
  Smartphone, 
  ShoppingCart, 
  BarChart3, 
  MessageSquare,
  GitBranch,
  Server,
  HardDrive,
  MousePointerClick,
  Lightbulb,
  Wand2,
  // Adding more icons for enhanced UI
  Play,
  Eye,
  Download,
  Share2,
  Heart,
  ThumbsUp,
  Users,
  TrendingUp,
  Award,
  Star,
  CheckCircle,
  ArrowRight,
  Settings,
  FolderOpen
} from 'lucide-react';

const float = keyframes`
  0%, 100% { transform: translateY(0px); }
  50% { transform: translateY(-20px); }
`;

const pulse = keyframes`
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
`;

const gradient = keyframes`
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
`;

const slideIn = keyframes`
  from { opacity: 0; transform: translateY(30px); }
  to { opacity: 1; transform: translateY(0); }
`;

const Container = styled.div`
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

const HeroSection = styled.section`
  padding: 5rem 2rem;
  text-align: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  position: relative;
  overflow: hidden;
  z-index: 1;
  
  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: radial-gradient(circle at center, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0) 70%);
  }
  
  @media (max-width: 768px) {
    padding: 3rem 1rem;
  }
`;

const HeroContent = styled.div`
  max-width: 1200px;
  margin: 0 auto;
  position: relative;
  z-index: 2;
`;

const Title = styled.h1`
  font-size: 3.5rem;
  font-weight: 800;
  margin-bottom: 1.5rem;
  background: linear-gradient(45deg, #fff, #e2e8f0);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  
  @media (max-width: 768px) {
    font-size: 2.5rem;
  }
`;

const Subtitle = styled.p`
  font-size: 1.5rem;
  opacity: 0.9;
  max-width: 700px;
  margin: 0 auto 2rem;
  
  @media (max-width: 768px) {
    font-size: 1.2rem;
  }
`;

const CTAButton = styled.button`
  background: white;
  color: #667eea;
  border: none;
  padding: 1.25rem 2.5rem;
  font-size: 1.25rem;
  font-weight: 600;
  border-radius: 3rem;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
  display: inline-flex;
  align-items: center;
  gap: 0.75rem;
  margin: 0 0.5rem;
  
  &:hover {
    transform: translateY(-5px);
    box-shadow: 0 15px 35px rgba(0, 0, 0, 0.3);
  }
  
  @media (max-width: 768px) {
    padding: 1rem 2rem;
    font-size: 1.1rem;
    margin: 0.5rem;
  }
`;

const ButtonGroup = styled.div`
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  gap: 1rem;
  margin-top: 2rem;
  
  @media (max-width: 768px) {
    flex-direction: column;
    align-items: center;
  }
`;

const WorkflowSection = styled.section`
  padding: 5rem 2rem;
  max-width: 1400px;
  margin: 0 auto;
  position: relative;
  z-index: 1;
  
  @media (max-width: 768px) {
    padding: 3rem 1rem;
  }
`;

const SectionTitle = styled.h2`
  text-align: center;
  font-size: 2.5rem;
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 3rem;
  
  @media (max-width: 768px) {
    font-size: 2rem;
  }
`;

const WorkflowSteps = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
`;

const StepCard = styled.div`
  background: white;
  border-radius: 1.5rem;
  padding: 2rem;
  text-align: center;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
  border: 1px solid #e2e8f0;
  position: relative;
  overflow: hidden;
  animation: ${slideIn} 0.6s ease-out;
  
  &:hover {
    transform: translateY(-10px);
    box-shadow: 0 15px 40px rgba(102, 126, 234, 0.15);
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
    padding: 1.5rem;
  }
`;

const StepNumber = styled.div`
  width: 3rem;
  height: 3rem;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 1.25rem;
  margin: 0 auto 1.5rem;
`;

const StepTitle = styled.h3`
  font-size: 1.5rem;
  font-weight: 600;
  color: #1e293b;
  margin-bottom: 1rem;
`;

const StepDescription = styled.p`
  color: #64748b;
  font-size: 1.1rem;
  line-height: 1.6;
`;

const StepIcon = styled.div`
  width: 4rem;
  height: 4rem;
  border-radius: 1rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  margin: 0 auto 1.5rem;
  font-size: 2rem;
  animation: ${float} 3s ease-in-out infinite;
`;

const FeaturesSection = styled.section`
  padding: 5rem 2rem;
  background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
  color: white;
  text-align: center;
  position: relative;
  z-index: 1;
  
  @media (max-width: 768px) {
    padding: 3rem 1rem;
  }
`;

const FeaturesGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  max-width: 1400px;
  margin: 0 auto;
`;

const FeatureCard = styled.div`
  background: rgba(255, 255, 255, 0.05);
  border-radius: 1.5rem;
  padding: 2rem;
  text-align: center;
  transition: all 0.3s ease;
  border: 1px solid rgba(255, 255, 255, 0.1);
  
  &:hover {
    background: rgba(255, 255, 255, 0.1);
    transform: translateY(-5px);
  }
  
  @media (max-width: 768px) {
    padding: 1.5rem;
  }
`;

const FeatureIcon = styled.div`
  width: 5rem;
  height: 5rem;
  border-radius: 1.5rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  margin: 0 auto 1.5rem;
  font-size: 2rem;
  animation: ${float} 3s ease-in-out infinite;
`;

const FeatureTitle = styled.h3`
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 1rem;
`;

const FeatureDescription = styled.p`
  font-size: 1.1rem;
  line-height: 1.6;
  opacity: 0.8;
`;

const StatsSection = styled.section`
  padding: 5rem 2rem;
  background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
  color: white;
  text-align: center;
  position: relative;
  z-index: 1;
  
  @media (max-width: 768px) {
    padding: 3rem 1rem;
  }
`;

const StatsGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
  max-width: 1200px;
  margin: 0 auto;
`;

const StatItem = styled.div`
  padding: 2rem;
  animation: ${slideIn} 0.6s ease-out;
`;

const StatNumber = styled.div`
  font-size: 3rem;
  font-weight: 700;
  margin-bottom: 1rem;
  background: linear-gradient(45deg, #667eea, #764ba2);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  
  @media (max-width: 768px) {
    font-size: 2.5rem;
  }
`;

const StatLabel = styled.div`
  font-size: 1.25rem;
  opacity: 0.8;
  
  @media (max-width: 768px) {
    font-size: 1.1rem;
  }
`;

const TestimonialsSection = styled.section`
  padding: 5rem 2rem;
  max-width: 1400px;
  margin: 0 auto;
  position: relative;
  z-index: 1;
  
  @media (max-width: 768px) {
    padding: 3rem 1rem;
  }
`;

const TestimonialsGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 2rem;
`;

const TestimonialCard = styled.div`
  background: white;
  border-radius: 1.5rem;
  padding: 2rem;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.08);
  border: 1px solid #e2e8f0;
  position: relative;
  
  &::before {
    content: '"';
    position: absolute;
    top: 1rem;
    left: 1rem;
    font-size: 4rem;
    color: #667eea;
    opacity: 0.1;
    font-family: serif;
  }
  
  @media (max-width: 768px) {
    padding: 1.5rem;
  }
`;

const TestimonialContent = styled.p`
  font-size: 1.1rem;
  line-height: 1.6;
  color: #1e293b;
  margin-bottom: 1.5rem;
  position: relative;
  z-index: 1;
`;

const TestimonialAuthor = styled.div`
  display: flex;
  align-items: center;
  gap: 1rem;
`;

const AuthorAvatar = styled.div`
  width: 3rem;
  height: 3rem;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: 600;
`;

const AuthorInfo = styled.div`
  text-align: left;
`;

const AuthorName = styled.div`
  font-weight: 600;
  color: #1e293b;
`;

const AuthorRole = styled.div`
  font-size: 0.9rem;
  color: #64748b;
`;

const CTASection = styled.section`
  padding: 5rem 2rem;
  text-align: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  position: relative;
  overflow: hidden;
  z-index: 1;
  
  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: radial-gradient(circle at center, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0) 70%);
  }
  
  @media (max-width: 768px) {
    padding: 3rem 1rem;
  }
`;

const CTATitle = styled.h2`
  font-size: 2.5rem;
  font-weight: 700;
  margin-bottom: 1.5rem;
  
  @media (max-width: 768px) {
    font-size: 2rem;
  }
`;

const CTADescription = styled.p`
  font-size: 1.25rem;
  opacity: 0.9;
  max-width: 700px;
  margin: 0 auto 2rem;
  
  @media (max-width: 768px) {
    font-size: 1.1rem;
  }
`;

const CTABtn = styled.button`
  background: white;
  color: #667eea;
  border: none;
  padding: 1.25rem 2.5rem;
  font-size: 1.25rem;
  font-weight: 600;
  border-radius: 3rem;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
  display: inline-flex;
  align-items: center;
  gap: 0.75rem;
  margin: 0 0.5rem;
  
  &:hover {
    transform: translateY(-5px);
    box-shadow: 0 15px 35px rgba(0, 0, 0, 0.3);
  }
  
  @media (max-width: 768px) {
    padding: 1rem 2rem;
    font-size: 1.1rem;
    margin: 0.5rem;
  }
`;

const ButtonGroupCTA = styled.div`
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  gap: 1rem;
  margin-top: 2rem;
  
  @media (max-width: 768px) {
    flex-direction: column;
    align-items: center;
  }
`;

function Home() {
  const navigate = useNavigate();
  
  const workflowSteps = [
    {
      id: 1,
      title: 'Describe Your Idea',
      description: 'Simply tell us what kind of application you want to build in natural language.',
      icon: Lightbulb
    },
    {
      id: 2,
      title: 'Preview & Customize',
      description: 'See a preview of your application and customize the technology stack.',
      icon: Eye
    },
    {
      id: 3,
      title: 'Generate Code',
      description: 'Our AI generates complete, production-ready code for your application.',
      icon: Code
    },
    {
      id: 4,
      title: 'Deploy Instantly',
      description: 'Deploy your application to the cloud with a single click.',
      icon: Rocket
    }
  ];
  
  const features = [
    {
      title: 'AI-Powered Generation',
      description: 'Transform your ideas into fully functional applications using advanced AI.',
      icon: Sparkles
    },
    {
      title: 'Multiple Frameworks',
      description: 'Choose from React, Vue, Angular for frontend and FastAPI, Django, Express for backend.',
      icon: GitBranch
    },
    {
      title: 'Database Integration',
      description: 'Automatic database schema generation and integration with MySQL, PostgreSQL, MongoDB.',
      icon: Database
    },
    {
      title: 'One-Click Deployment',
      description: 'Deploy to AWS, Google Cloud, or Azure with a single click.',
      icon: Cloud
    },
    {
      title: 'Responsive Design',
      description: 'All generated applications are fully responsive and mobile-friendly.',
      icon: Smartphone
    },
    {
      title: 'Best Practices',
      description: 'Code follows industry best practices and security standards.',
      icon: Award
    }
  ];
  
  const testimonials = [
    {
      content: 'This tool saved me weeks of development time. I described my idea and had a fully functional app in minutes!',
      author: 'Sarah Johnson',
      role: 'Startup Founder'
    },
    {
      content: 'The AI-generated code quality is impressive. It follows best practices and is easy to customize.',
      author: 'Michael Chen',
      role: 'Senior Developer'
    },
    {
      content: 'As a non-technical founder, this tool helped me prototype my idea without hiring developers.',
      author: 'Emma Rodriguez',
      role: 'Product Manager'
    }
  ];
  
  const stats = [
    { number: '10,000+', label: 'Applications Built' },
    { number: '50+', label: 'Supported Technologies' },
    { number: '99.9%', label: 'Uptime' },
    { number: '24/7', label: 'Support' }
  ];
  
  const handleGetStarted = () => {
    navigate('/builder');
  };
  
  const handleViewProjects = () => {
    navigate('/projects');
  };
  
  const handleViewSettings = () => {
    navigate('/integrations'); // Using integrations as settings page
  };

  return (
    <Container>
      <HeroSection>
        <HeroContent>
          <Title>
            <Bot size={60} style={{ verticalAlign: 'middle', marginRight: '10px' }} />
            AI App Builder
            <Sparkles size={50} style={{ marginLeft: '10px', verticalAlign: 'middle' }} />
          </Title>
          <Subtitle>
            Transform your ideas into production-ready applications in minutes using natural language.
            No coding required.
          </Subtitle>
          <ButtonGroup>
            <CTAButton onClick={handleGetStarted}>
              <Play size={24} />
              Start Building Now
              <ArrowRight size={24} />
            </CTAButton>
            <CTAButton onClick={handleViewProjects} style={{ background: 'transparent', color: 'white', border: '2px solid white' }}>
              <FolderOpen size={24} />
              My Projects
            </CTAButton>
            <CTAButton onClick={handleViewSettings} style={{ background: 'transparent', color: 'white', border: '2px solid white' }}>
              <Settings size={24} />
              Settings
            </CTAButton>
          </ButtonGroup>
        </HeroContent>
      </HeroSection>
      
      <WorkflowSection>
        <SectionTitle>How It Works</SectionTitle>
        <WorkflowSteps>
          {workflowSteps.map((step, index) => (
            <StepCard key={step.id} style={{ animationDelay: `${index * 0.1}s` }}>
              <StepNumber>{step.id}</StepNumber>
              <StepIcon>
                <step.icon size={32} />
              </StepIcon>
              <StepTitle>{step.title}</StepTitle>
              <StepDescription>{step.description}</StepDescription>
            </StepCard>
          ))}
        </WorkflowSteps>
      </WorkflowSection>
      
      <FeaturesSection>
        <SectionTitle>Powerful Features</SectionTitle>
        <FeaturesGrid>
          {features.map((feature, index) => (
            <FeatureCard key={index} style={{ animationDelay: `${index * 0.1}s` }}>
              <FeatureIcon>
                <feature.icon size={32} />
              </FeatureIcon>
              <FeatureTitle>{feature.title}</FeatureTitle>
              <FeatureDescription>{feature.description}</FeatureDescription>
            </FeatureCard>
          ))}
        </FeaturesGrid>
      </FeaturesSection>
      
      <StatsSection>
        <StatsGrid>
          {stats.map((stat, index) => (
            <StatItem key={index} style={{ animationDelay: `${index * 0.1}s` }}>
              <StatNumber>{stat.number}</StatNumber>
              <StatLabel>{stat.label}</StatLabel>
            </StatItem>
          ))}
        </StatsGrid>
      </StatsSection>
      
      <TestimonialsSection>
        <SectionTitle>What Our Users Say</SectionTitle>
        <TestimonialsGrid>
          {testimonials.map((testimonial, index) => (
            <TestimonialCard key={index} style={{ animationDelay: `${index * 0.1}s` }}>
              <TestimonialContent>"{testimonial.content}"</TestimonialContent>
              <TestimonialAuthor>
                <AuthorAvatar>
                  {testimonial.author.charAt(0)}
                </AuthorAvatar>
                <AuthorInfo>
                  <AuthorName>{testimonial.author}</AuthorName>
                  <AuthorRole>{testimonial.role}</AuthorRole>
                </AuthorInfo>
              </TestimonialAuthor>
            </TestimonialCard>
          ))}
        </TestimonialsGrid>
      </TestimonialsSection>
      
      <CTASection>
        <CTATitle>Ready to Build Your Next Application?</CTATitle>
        <CTADescription>
          Join thousands of developers and entrepreneurs who are already using AI App Builder to bring their ideas to life.
        </CTADescription>
        <ButtonGroupCTA>
          <CTABtn onClick={handleGetStarted}>
            <Zap size={24} />
            Get Started Free
            <ArrowRight size={24} />
          </CTABtn>
          <CTABtn onClick={handleViewProjects} style={{ background: 'transparent', color: 'white', border: '2px solid white' }}>
            <FolderOpen size={24} />
            View My Projects
          </CTABtn>
        </ButtonGroupCTA>
      </CTASection>
    </Container>
  );
}

export default Home;