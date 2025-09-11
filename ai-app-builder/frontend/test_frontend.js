/**
 * Simple test script to verify the frontend can start
 */

const fs = require('fs');
const path = require('path');

function testFrontendSetup() {
    console.log('Testing AI App Builder Frontend Setup...');
    console.log('='.repeat(50));
    
    // Check if required files exist
    const requiredFiles = ['package.json', 'src/App.js', 'src/index.js'];
    const frontendDir = __dirname;
    
    console.log(`Current directory: ${frontendDir}`);
    
    for (const file of requiredFiles) {
        const filePath = path.join(frontendDir, file);
        if (!fs.existsSync(filePath)) {
            console.log(`❌ Missing required file: ${file}`);
            return false;
        }
        console.log(`✅ Found required file: ${file}`);
    }
    
    // Read package.json to verify it's a React app
    try {
        const packageJson = JSON.parse(fs.readFileSync(path.join(frontendDir, 'package.json'), 'utf8'));
        console.log(`✅ Package name: ${packageJson.name}`);
        console.log(`✅ Package version: ${packageJson.version}`);
        
        // Check for React dependencies
        if (packageJson.dependencies && packageJson.dependencies.react) {
            console.log(`✅ React dependency found: v${packageJson.dependencies.react}`);
        } else {
            console.log('⚠️  React dependency not found in package.json');
        }
        
        // Check for start script
        if (packageJson.scripts && packageJson.scripts.start) {
            console.log(`✅ Start script found: ${packageJson.scripts.start}`);
        } else {
            console.log('❌ Start script not found in package.json');
            return false;
        }
    } catch (error) {
        console.log(`❌ Failed to read package.json: ${error.message}`);
        return false;
    }
    
    console.log('\n✅ All tests passed! The frontend should start successfully.');
    console.log('\nTo start the frontend, run:');
    console.log('   npm start');
    
    return true;
}

// Run the test
testFrontendSetup();