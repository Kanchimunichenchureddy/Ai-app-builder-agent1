-- AI App Builder Database Schema
-- MySQL Database for the AI Agent Application Builder

CREATE DATABASE IF NOT EXISTS ai_app_builder;
USE ai_app_builder;

-- Users table
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(100) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    full_name VARCHAR(255),
    is_active BOOLEAN DEFAULT TRUE,
    is_superuser BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_email (email),
    INDEX idx_username (username),
    INDEX idx_active (is_active)
);

-- Projects table
CREATE TABLE projects (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    project_type ENUM('web_app', 'mobile_app', 'api', 'dashboard', 'ecommerce', 'blog', 'crm', 'chat', 'custom') NOT NULL,
    status ENUM('creating', 'active', 'building', 'deploying', 'deployed', 'error', 'archived') DEFAULT 'creating',
    
    -- Technical Configuration
    frontend_framework VARCHAR(100) DEFAULT 'react',
    backend_framework VARCHAR(100) DEFAULT 'fastapi',
    database_type VARCHAR(100) DEFAULT 'mysql',
    
    -- Project Configuration (JSON)
    config JSON,
    features JSON,
    integrations JSON,
    
    -- File Paths
    project_path VARCHAR(500),
    repository_url VARCHAR(500),
    
    -- Metadata
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- Foreign Keys
    owner_id INT NOT NULL,
    
    INDEX idx_name (name),
    INDEX idx_type (project_type),
    INDEX idx_status (status),
    INDEX idx_owner (owner_id),
    INDEX idx_created (created_at),
    
    FOREIGN KEY (owner_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Deployments table
CREATE TABLE deployments (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    platform ENUM('docker', 'vercel', 'netlify', 'aws', 'gcp', 'azure', 'heroku', 'digital_ocean') NOT NULL,
    status ENUM('pending', 'building', 'deploying', 'deployed', 'failed', 'stopped') DEFAULT 'pending',
    
    -- Deployment URLs
    url VARCHAR(500),
    api_url VARCHAR(500),
    admin_url VARCHAR(500),
    
    -- Configuration (JSON)
    config JSON,
    environment_variables JSON,
    
    -- Build Information
    build_logs TEXT,
    deployment_logs TEXT,
    error_message TEXT,
    
    -- Metadata
    deployed_at TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- Foreign Keys
    project_id INT NOT NULL,
    user_id INT NOT NULL,
    
    INDEX idx_platform (platform),
    INDEX idx_status (status),
    INDEX idx_project (project_id),
    INDEX idx_user (user_id),
    INDEX idx_created (created_at),
    
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Project Files table (for storing generated code)
CREATE TABLE project_files (
    id INT PRIMARY KEY AUTO_INCREMENT,
    project_id INT NOT NULL,
    file_path VARCHAR(500) NOT NULL,
    file_name VARCHAR(255) NOT NULL,
    file_content LONGTEXT,
    file_type VARCHAR(50),
    file_size INT DEFAULT 0,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_project (project_id),
    INDEX idx_path (file_path),
    INDEX idx_type (file_type),
    
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE
);

-- AI Generations table (for tracking AI requests and responses)
CREATE TABLE ai_generations (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    project_id INT,
    
    -- Request Information
    request_type ENUM('analyze', 'generate', 'modify', 'deploy') NOT NULL,
    user_prompt TEXT NOT NULL,
    system_prompt TEXT,
    
    -- AI Response
    ai_service ENUM('openai', 'gemini', 'deepseek', 'fallback') NOT NULL,
    ai_response LONGTEXT,
    
    -- Processing Information
    processing_time_ms INT,
    tokens_used INT,
    success BOOLEAN DEFAULT TRUE,
    error_message TEXT,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_user (user_id),
    INDEX idx_project (project_id),
    INDEX idx_type (request_type),
    INDEX idx_service (ai_service),
    INDEX idx_created (created_at),
    
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE SET NULL
);

-- Templates table (for storing reusable project templates)
CREATE TABLE templates (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    template_type ENUM('dashboard', 'ecommerce', 'blog', 'chat', 'crm', 'api', 'custom') NOT NULL,
    
    -- Template Configuration
    config JSON,
    features JSON,
    tech_stack JSON,
    
    -- Template Files (JSON structure)
    file_structure JSON,
    
    -- Metadata
    is_public BOOLEAN DEFAULT TRUE,
    created_by INT,
    usage_count INT DEFAULT 0,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_name (name),
    INDEX idx_type (template_type),
    INDEX idx_public (is_public),
    INDEX idx_usage (usage_count),
    
    FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE SET NULL
);

-- API Keys table (for storing user's external API configurations)
CREATE TABLE api_keys (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    
    service_name VARCHAR(100) NOT NULL,
    api_key_encrypted TEXT NOT NULL,
    
    -- Configuration
    is_active BOOLEAN DEFAULT TRUE,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_user (user_id),
    INDEX idx_service (service_name),
    INDEX idx_active (is_active),
    
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE KEY unique_user_service (user_id, service_name)
);

-- Insert default demo user
INSERT INTO users (email, username, hashed_password, full_name, is_active) 
VALUES (
    'demo@appforge.dev', 
    'demo',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj2PSF1nwKmW', -- demo123
    'Demo User',
    TRUE
);

-- Insert default templates
INSERT INTO templates (name, description, template_type, config, features, tech_stack, file_structure, is_public, created_by) VALUES
(
    'Dashboard Template',
    'Analytics dashboard with charts and widgets',
    'dashboard',
    '{"theme": "modern", "layout": "grid"}',
    '["authentication", "charts", "widgets", "responsive"]',
    '["react", "fastapi", "mysql"]',
    '{"frontend": {"components": ["Dashboard", "Charts", "Widgets"]}, "backend": {"endpoints": ["analytics", "data"]}}',
    TRUE,
    1
),
(
    'E-commerce Template', 
    'Complete online store with payments',
    'ecommerce',
    '{"payment": "stripe", "inventory": true}',
    '["products", "cart", "checkout", "payments", "admin"]',
    '["react", "fastapi", "mysql", "stripe"]',
    '{"frontend": {"components": ["Products", "Cart", "Checkout"]}, "backend": {"endpoints": ["products", "orders", "payments"]}}',
    TRUE,
    1
),
(
    'Blog Template',
    'Content management system',
    'blog', 
    '{"editor": "rich_text", "comments": true}',
    '["posts", "comments", "categories", "admin"]',
    '["react", "fastapi", "mysql"]',
    '{"frontend": {"components": ["BlogPost", "Editor", "Comments"]}, "backend": {"endpoints": ["posts", "comments"]}}',
    TRUE,
    1
);

-- Create indexes for better performance
CREATE INDEX idx_projects_composite ON projects(owner_id, status, created_at);
CREATE INDEX idx_deployments_composite ON deployments(project_id, status, created_at);
CREATE INDEX idx_files_composite ON project_files(project_id, file_type);
CREATE INDEX idx_generations_composite ON ai_generations(user_id, request_type, created_at);