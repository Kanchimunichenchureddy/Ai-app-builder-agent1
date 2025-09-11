/**
 * Script to verify that the frontend service is running correctly
 * This is a simple Node.js script to check if the frontend port is accessible
 */

const http = require('http');

function checkFrontend() {
  const options = {
    hostname: 'localhost',
    port: 3000,
    path: '/',
    method: 'GET',
    timeout: 5000
  };

  const req = http.request(options, (res) => {
    console.log('✅ Frontend server is running!');
    console.log(`   Status Code: ${res.statusCode}`);
    console.log('   Frontend should be accessible at: http://localhost:3000');
  });

  req.on('error', (e) => {
    console.log('❌ Frontend is not accessible - make sure it\'s running');
    console.log('   Start it with: npm start');
    console.log('   Error:', e.message);
  });

  req.on('timeout', () => {
    console.log('❌ Frontend connection timed out');
    req.destroy();
  });

  req.end();
}

function main() {
  console.log('AI App Builder - Frontend Verification');
  console.log('=====================================');
  
  console.log('\n1. Checking Frontend Service...');
  checkFrontend();
  
  console.log('\n' + '='.repeat(37));
  console.log('ACCESS INSTRUCTIONS:');
  console.log('✅ Frontend Application: http://localhost:3000');
  
  console.log('\nREMINDERS:');
  console.log('⚠️  The first startup may take 1-2 minutes due to compilation');
  console.log('⚠️  Keep the frontend terminal open while using the application');
}

main();