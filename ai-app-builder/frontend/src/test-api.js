// Test API connection
fetch('http://localhost:8000/api/health')
  .then(response => response.json())
  .then(data => console.log('API Health Check:', data))
  .catch(error => console.error('API Connection Error:', error));