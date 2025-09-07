import api from './api';

class RealTimeProjectService {
  constructor() {
    this.socket = null;
    this.sessionId = null;
    this.isConnected = false;
    this.listeners = {};
  }

  // Create a new real-time session
  async createSession() {
    try {
      const response = await api.post('/realtime/create-session');
      this.sessionId = response.data.session_id;
      return response.data;
    } catch (error) {
      console.error('Failed to create real-time session:', error);
      throw error;
    }
  }

  // Connect to WebSocket for real-time updates
  async connectWebSocket(onProgress, onComplete, onError) {
    if (!this.sessionId) {
      throw new Error('No session ID available. Create a session first.');
    }

    // Store listeners
    this.listeners.onProgress = onProgress;
    this.listeners.onComplete = onComplete;
    this.listeners.onError = onError;

    // Create WebSocket connection
    const wsUrl = `ws://localhost:8000/api/realtime/ws/project-creation/${this.sessionId}`;
    this.socket = new WebSocket(wsUrl);

    // Set up event handlers
    this.socket.onopen = () => {
      this.isConnected = true;
      console.log('WebSocket connected for real-time project creation');
      
      // Send authentication token
      const token = localStorage.getItem('token');
      if (token) {
        this.sendMessage({
          type: 'authenticate',
          token: token
        });
      }
    };

    this.socket.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        this.handleWebSocketMessage(data);
      } catch (error) {
        console.error('Error parsing WebSocket message:', error);
      }
    };

    this.socket.onclose = () => {
      this.isConnected = false;
      console.log('WebSocket disconnected');
    };

    this.socket.onerror = (error) => {
      console.error('WebSocket error:', error);
      if (this.listeners.onError) {
        this.listeners.onError('WebSocket connection error');
      }
    };
  }

  // Handle incoming WebSocket messages
  handleWebSocketMessage(data) {
    switch (data.type) {
      case 'connection_established':
        console.log('Connected to real-time project creation:', data.message);
        break;

      case 'authenticated':
        console.log('Authenticated:', data.message);
        break;

      case 'progress_update':
        if (this.listeners.onProgress) {
          this.listeners.onProgress(data);
        }
        break;

      case 'project_completed':
        if (this.listeners.onComplete) {
          this.listeners.onComplete(data);
        }
        break;

      case 'project_error':
      case 'creation_error':
      case 'auth_error':
        if (this.listeners.onError) {
          this.listeners.onError(data.message || 'An error occurred during project creation');
        }
        break;

      case 'creation_cancelled':
        if (this.listeners.onError) {
          this.listeners.onError('Project creation was cancelled');
        }
        break;

      case 'pong':
        // Keep-alive response
        break;

      default:
        console.log('Unknown message type:', data.type, data);
    }
  }

  // Send message through WebSocket
  sendMessage(message) {
    if (this.socket && this.isConnected) {
      this.socket.send(JSON.stringify(message));
    } else {
      console.error('WebSocket is not connected');
    }
  }

  // Start real-time project creation
  async startProjectCreation(projectData) {
    if (!this.isConnected) {
      throw new Error('WebSocket is not connected. Connect first.');
    }

    this.sendMessage({
      type: 'create_project',
      project_data: projectData
    });
  }

  // Cancel ongoing project creation
  async cancelCreation() {
    if (!this.isConnected) {
      throw new Error('WebSocket is not connected.');
    }

    this.sendMessage({
      type: 'cancel_creation'
    });
  }

  // Send keep-alive ping
  sendPing() {
    if (this.isConnected) {
      this.sendMessage({
        type: 'ping',
        timestamp: new Date().toISOString()
      });
    }
  }

  // Disconnect WebSocket
  disconnect() {
    if (this.socket) {
      this.socket.close();
      this.socket = null;
      this.isConnected = false;
    }
  }

  // Get current session ID
  getSessionId() {
    return this.sessionId;
  }

  // Check if connected
  getIsConnected() {
    return this.isConnected;
  }
}

export default new RealTimeProjectService();