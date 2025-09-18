const { spawn } = require('child_process');
const path = require('path');

// Change to the frontend directory
const frontendDir = path.resolve(__dirname);

console.log(`Starting frontend server in: ${frontendDir}`);
console.log('Frontend will be available at: http://localhost:3000');

// Spawn the npm start process
const child = spawn('npx', ['react-scripts', 'start'], {
  cwd: frontendDir,
  stdio: 'inherit',
  shell: true
});

child.on('error', (error) => {
  console.error('Failed to start frontend:', error);
});

child.on('close', (code) => {
  console.log(`Frontend process exited with code ${code}`);
});