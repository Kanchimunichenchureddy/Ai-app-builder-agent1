import api from './api';

class IntegrationsService {
  // Stripe Payment Intent
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

  // Stripe Customer
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

  // Google Drive File
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

  // Google Sheet
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

  // DeepSeek Code Generation
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

  // DeepSeek Code Explanation
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

export default new IntegrationsService();