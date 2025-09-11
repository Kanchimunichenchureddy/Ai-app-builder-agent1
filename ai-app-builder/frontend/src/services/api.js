import axios from 'axios';

const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL || 'http://localhost:8000/api',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    if (error.response?.status === 401) {
      // Check if we're in demo mode
      const savedUser = localStorage.getItem('user');
      if (savedUser) {
        try {
          const userData = JSON.parse(savedUser);
          if (userData.email === 'demo@appforge.dev') {
            // In demo mode, don't redirect to login
            console.warn('Demo mode: Ignoring 401 error');
            return Promise.reject(error);
          }
        } catch (e) {
          // If parsing fails, continue with normal flow
        }
      }
      
      // Token expired or invalid - only redirect if not in demo mode
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      window.location.href = '/login';
    } else if (error.code === 'ECONNREFUSED' || error.code === 'ERR_NETWORK' || !error.response) {
      // Backend not available - this is OK for frontend-only testing
      console.warn('Backend not available - using frontend-only mode');
    }
    return Promise.reject(error);
  }
);

export default api;