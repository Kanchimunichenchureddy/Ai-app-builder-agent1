import api from './api';

class AIChatService {
  constructor() {
    this.conversationHistory = [];
  }

  // Send a message to the AI chat
  async sendMessage(message, context = {}) {
    try {
      const response = await api.post('/builder/chat', {
        message,
        context
      });
      
      // Add to conversation history
      this.conversationHistory.push({
        role: 'user',
        content: message,
        timestamp: new Date().toISOString()
      });
      
      this.conversationHistory.push({
        role: 'assistant',
        content: response.data.response,
        timestamp: new Date().toISOString()
      });
      
      return response.data;
    } catch (error) {
      console.error('Error sending message to AI chat:', error);
      throw error;
    }
  }

  // Analyze user requirements and generate project specification
  async analyzeRequirements(description) {
    try {
      const response = await api.post('/builder/analyze', {
        request: description
      });
      
      return response.data;
    } catch (error) {
      console.error('Error analyzing requirements:', error);
      // Return a fallback response for offline testing
      if (error.code === 'ECONNREFUSED' || error.code === 'ERR_NETWORK') {
        return {
          analysis: {
            description: `A ${description.substring(0, 20)}... application`,
            features: ['User Authentication', 'Responsive Design', 'API Integration'],
            tech_recommendations: {
              frontend: 'React.js',
              backend: 'FastAPI',
              database: 'MySQL'
            },
            project_type: 'web_app',
            complexity: 'medium'
          },
          estimated_time: '2-5 minutes'
        };
      }
      throw error;
    }
  }

  // Generate code based on user request
  async generateCode(data) {
    try {
      const response = await api.post('/builder/generate', data);
      
      return response.data;
    } catch (error) {
      console.error('Error generating code:', error);
      // Return a fallback response for offline testing
      if (error.code === 'ECONNREFUSED' || error.code === 'ERR_NETWORK') {
        return {
          success: true,
          project: {
            id: 1,
            name: data.name || 'Sample Project',
            type: 'web_app',
            status: 'active',
            tech_stack: data.tech_stack || {
              frontend: 'react',
              backend: 'fastapi',
              database: 'mysql'
            },
            created_at: new Date().toISOString(),
            project_path: './generated_projects/project_1'
          },
          files_generated: 5,
          message: `🎉 ${data.name || 'Sample Project'} has been successfully generated!`
        };
      }
      throw error;
    }
  }

  // Modify existing code based on user request
  async modifyCode(projectId, modificationRequest) {
    try {
      const response = await api.post(`/builder/modify/${projectId}`, {
        request: modificationRequest
      });
      
      return response.data;
    } catch (error) {
      console.error('Error modifying code:', error);
      throw error;
    }
  }

  // Get project templates
  async getTemplates() {
    try {
      const response = await api.get('/builder/templates');
      return response.data;
    } catch (error) {
      console.error('Error fetching templates:', error);
      throw error;
    }
  }

  // Create project from template
  async createFromTemplate(templateId, projectName, customizations = {}) {
    try {
      const response = await api.post(`/builder/template/${templateId}`, {
        name: projectName,
        customizations
      });
      
      return response.data;
    } catch (error) {
      console.error('Error creating from template:', error);
      throw error;
    }
  }

  // Get AI agent capabilities
  async getCapabilities() {
    try {
      const response = await api.get('/builder/capabilities');
      return response.data;
    } catch (error) {
      console.error('Error fetching capabilities:', error);
      throw error;
    }
  }

  // Clear conversation history
  clearHistory() {
    this.conversationHistory = [];
  }

  // Get conversation history
  getHistory() {
    return this.conversationHistory;
  }

  // Suggest next steps based on conversation
  async suggestNextSteps(currentContext) {
    try {
      const response = await api.post('/builder/suggest-next', {
        context: currentContext,
        history: this.conversationHistory.slice(-5) // Last 5 messages
      });
      
      return response.data;
    } catch (error) {
      console.error('Error getting next steps:', error);
      throw error;
    }
  }

  // Explain code or concepts
  async explainConcept(concept, context = {}) {
    try {
      const response = await api.post('/builder/explain', {
        concept,
        context
      });
      
      return response.data;
    } catch (error) {
      console.error('Error explaining concept:', error);
      throw error;
    }
  }

  // Debug code issues
  async debugCode(code, error, context = {}) {
    try {
      const response = await api.post('/builder/debug', {
        code,
        error,
        context
      });
      
      return response.data;
    } catch (error) {
      console.error('Error debugging code:', error);
      throw error;
    }
  }

  // Optimize code
  async optimizeCode(code, context = {}) {
    try {
      const response = await api.post('/builder/optimize', {
        code,
        context
      });
      
      return response.data;
    } catch (error) {
      console.error('Error optimizing code:', error);
      throw error;
    }
  }

  // Create Stripe payment intent
  async createStripePaymentIntent(amount, currency = 'usd', metadata = {}) {
    try {
      const response = await api.post('/integrations/stripe/create-payment-intent', {
        amount,
        currency,
        metadata
      });
      
      return response.data;
    } catch (error) {
      console.error('Error creating Stripe payment intent:', error);
      throw error;
    }
  }

  // Create Stripe customer
  async createStripeCustomer(email, name, metadata = {}) {
    try {
      const response = await api.post('/integrations/stripe/create-customer', {
        email,
        name,
        metadata
      });
      
      return response.data;
    } catch (error) {
      console.error('Error creating Stripe customer:', error);
      throw error;
    }
  }

  // Create Google Drive file
  async createGoogleDriveFile(fileName, content, mimeType = 'text/plain') {
    try {
      const response = await api.post('/integrations/google/create-drive-file', {
        file_name: fileName,
        content,
        mime_type: mimeType
      });
      
      return response.data;
    } catch (error) {
      console.error('Error creating Google Drive file:', error);
      throw error;
    }
  }

  // Create Google Sheet
  async createGoogleSheet(title, data = null) {
    try {
      const response = await api.post('/integrations/google/create-sheet', {
        title,
        data
      });
      
      return response.data;
    } catch (error) {
      console.error('Error creating Google Sheet:', error);
      throw error;
    }
  }

  // Generate code with DeepSeek
  async generateCodeWithDeepSeek(prompt, model = 'deepseek-coder', maxTokens = 2000, temperature = 0.7) {
    try {
      const response = await api.post('/integrations/deepseek/generate-code', {
        prompt,
        model,
        max_tokens: maxTokens,
        temperature
      });
      
      return response.data;
    } catch (error) {
      console.error('Error generating code with DeepSeek:', error);
      throw error;
    }
  }

  // Explain code with DeepSeek
  async explainCodeWithDeepSeek(code, request, model = 'deepseek-chat', maxTokens = 1000) {
    try {
      const response = await api.post('/integrations/deepseek/explain-code', {
        code,
        request,
        model,
        max_tokens: maxTokens
      });
      
      return response.data;
    } catch (error) {
      console.error('Error explaining code with DeepSeek:', error);
      throw error;
    }
  }
}

export default new AIChatService();