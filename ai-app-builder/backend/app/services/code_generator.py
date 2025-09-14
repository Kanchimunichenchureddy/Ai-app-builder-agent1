from typing import Dict, Any, List
import os
import json
from pathlib import Path

class CodeGenerator:
    """
    Advanced code generator for creating complete full-stack applications.
    """
    
    def __init__(self):
        # No external dependencies - generate code internally
        pass
        
    async def generate_react_app(self, analysis: Dict[str, Any]) -> Dict[str, str]:
        """Generate complete React frontend application."""
        files = {}
        project_type = analysis.get("project_type", "web_app")
        features = analysis.get("features", [])
        
        # Generate main App.js
        files["frontend/src/App.js"] = self._generate_react_app_js(project_type, features)
        
        # Generate components based on project type
        if project_type == "dashboard":
            files.update(self._generate_dashboard_components())
        elif project_type == "ecommerce":
            files.update(self._generate_ecommerce_components())
        elif project_type == "blog":
            files.update(self._generate_blog_components())
        elif project_type == "chat":
            files.update(self._generate_chat_components())
        elif project_type == "crm":
            files.update(self._generate_crm_components())
        else:
            files.update(self._generate_default_components())
            
        # Generate common components
        files.update(self._generate_common_components())
        
        # Generate package.json
        files["frontend/package.json"] = self._generate_package_json(project_type, features)
        
        # Generate index.html
        files["frontend/public/index.html"] = self._generate_index_html(project_type)
        
        # Generate CSS files
        files["frontend/src/index.css"] = self._generate_index_css()
        files["frontend/src/App.css"] = self._generate_app_css(project_type)
        
        return files
    
    async def generate_fastapi_app(self, analysis: Dict[str, Any]) -> Dict[str, str]:
        """Generate complete FastAPI backend application."""
        files = {}
        project_type = analysis.get("project_type", "web_app")
        features = analysis.get("features", [])
        
        # Generate main.py
        files["backend/app/main.py"] = self._generate_fastapi_main(project_type, features)
        
        # Generate models
        files.update(self._generate_fastapi_models(project_type, features))
        
        # Generate API routes
        files.update(self._generate_fastapi_routes(project_type, features))
        
        # Generate schemas
        files.update(self._generate_fastapi_schemas(project_type, features))
        
        # Generate services
        files.update(self._generate_fastapi_services(project_type, features))
        
        # Generate core files
        files.update(self._generate_fastapi_core())
        
        # Generate requirements.txt
        files["backend/requirements.txt"] = self._generate_requirements(project_type, features)
        
        # Generate config files
        files["backend/app/core/config.py"] = self._generate_config_file()
        files["backend/app/core/database.py"] = self._generate_database_file()
        files["backend/app/core/security.py"] = self._generate_security_file()
        
        return files
    
    async def generate_database_schema(self, analysis: Dict[str, Any]) -> Dict[str, str]:
        """Generate MySQL database schema."""
        files = {}
        project_type = analysis.get("project_type", "web_app")
        features = analysis.get("features", [])
        
        # Generate database schema
        schema_sql = self._generate_mysql_schema(project_type, features)
        files["database/schema.sql"] = schema_sql
        
        # Generate migrations
        migration_sql = self._generate_mysql_migrations(project_type, features)
        files["database/migrations/001_initial.sql"] = migration_sql
        
        return files
    
    async def generate_deployment_config(self, analysis: Dict[str, Any]) -> Dict[str, str]:
        """Generate deployment configurations."""
        files = {}
        project_type = analysis.get("project_type", "web_app")
        
        # Generate Docker files
        files["Dockerfile"] = self._generate_main_dockerfile()
        files["docker-compose.yml"] = self._generate_docker_compose(project_type)
        files["nginx.conf"] = self._generate_nginx_config()
        
        # Generate deployment scripts
        files["deploy.sh"] = self._generate_deploy_script()
        
        return files
    
    def _generate_react_app_js(self, project_type: str, features: List[str]) -> str:
        """Generate main React App.js file."""
        auth_required = "authentication" in features or "user_management" in features
        
        app_js = """import React, { useState, useEffect } from 'react';
import './App.css';

"""
        
        if auth_required:
            app_js += """import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Login from './components/auth/Login';
import Register from './components/auth/Register';
import Dashboard from './components/dashboard/Dashboard';
import Navbar from './components/layout/Navbar';
"""
        else:
            app_js += """import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './components/Home';
import Navbar from './components/layout/Navbar';
"""
        
        app_js += """
function App() {
"""
        
        if auth_required:
            app_js += """  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Check if user is logged in
    const token = localStorage.getItem('token');
    if (token) {
      // In a real app, you would verify the token with your backend
      setUser({ id: 1, name: 'Demo User' });
    }
    setLoading(false);
  }, []);

  const handleLogin = (userData) => {
    setUser(userData);
    localStorage.setItem('token', 'demo-token');
  };

  const handleLogout = () => {
    setUser(null);
    localStorage.removeItem('token');
  };

  if (loading) {
    return <div className="loading">Loading...</div>;
  }

  return (
    <Router>
      <div className="App">
        <Navbar user={user} onLogout={handleLogout} />
        <Routes>
          <Route path="/" element={<Home />} />
          {!user ? (
            <>
              <Route path="/login" element={<Login onLogin={handleLogin} />} />
              <Route path="/register" element={<Register />} />
              <Route path="*" element={<Navigate to="/login" />} />
            </>
          ) : (
            <>
              <Route path="/dashboard" element={<Dashboard user={user} />} />
              <Route path="*" element={<Navigate to="/dashboard" />} />
            </>
          )}
        </Routes>
      </div>
    </Router>
  );
"""
        else:
            app_js += """  return (
    <Router>
      <div className="App">
        <Navbar />
        <Routes>
          <Route path="/" element={<Home />} />
        </Routes>
      </div>
    </Router>
  );
"""
        
        app_js += """}

export default App;
"""
        return app_js
    
    def _generate_dashboard_components(self) -> Dict[str, str]:
        """Generate dashboard-specific React components."""
        components = {}
        
        # Dashboard component
        components["frontend/src/components/dashboard/Dashboard.js"] = """import React from 'react';
import './Dashboard.css';

const Dashboard = ({ user }) => {
  return (
    <div className="dashboard">
      <header className="dashboard-header">
        <h1>Dashboard</h1>
        <p>Welcome, {user?.name}!</p>
      </header>
      
      <div className="dashboard-content">
        <div className="stats-grid">
          <div className="stat-card">
            <h3>Total Users</h3>
            <p className="stat-value">1,234</p>
          </div>
          <div className="stat-card">
            <h3>Revenue</h3>
            <p className="stat-value">$12,345</p>
          </div>
          <div className="stat-card">
            <h3>Orders</h3>
            <p className="stat-value">567</p>
          </div>
          <div className="stat-card">
            <h3>Conversion</h3>
            <p className="stat-value">2.3%</p>
          </div>
        </div>
        
        <div className="charts-section">
          <div className="chart-container">
            <h3>Monthly Activity</h3>
            <div className="chart-placeholder">
              <p>Chart visualization would go here</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
"""
        
        # Dashboard CSS
        components["frontend/src/components/dashboard/Dashboard.css"] = """.dashboard {
  padding: 20px;
}

.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
}

.dashboard-header h1 {
  color: #333;
  margin: 0;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.stat-card {
  background: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
  text-align: center;
}

.stat-card h3 {
  margin: 0 0 10px 0;
  color: #666;
  font-size: 16px;
}

.stat-value {
  font-size: 24px;
  font-weight: bold;
  color: #333;
  margin: 0;
}

.charts-section {
  background: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.chart-container {
  margin-bottom: 20px;
}

.chart-container h3 {
  margin-top: 0;
  color: #333;
}

.chart-placeholder {
  height: 300px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f5f5f5;
  border-radius: 4px;
}
"""
        
        return components
    
    def _generate_ecommerce_components(self) -> Dict[str, str]:
        """Generate e-commerce specific React components."""
        components = {}
        
        # Product List component
        components["frontend/src/components/products/ProductList.js"] = """import React, { useState, useEffect } from 'react';
import ProductCard from './ProductCard';
import './ProductList.css';

const ProductList = () => {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState('all');

  useEffect(() => {
    // In a real app, this would fetch from your backend API
    const mockProducts = [
      {
        id: 1,
        name: 'Premium Headphones',
        price: 199.99,
        image: '/images/headphones.jpg',
        category: 'electronics',
        rating: 4.5
      },
      {
        id: 2,
        name: 'Running Shoes',
        price: 89.99,
        image: '/images/shoes.jpg',
        category: 'clothing',
        rating: 4.2
      },
      {
        id: 3,
        name: 'Smart Watch',
        price: 299.99,
        image: '/images/watch.jpg',
        category: 'electronics',
        rating: 4.8
      },
      {
        id: 4,
        name: 'Coffee Maker',
        price: 79.99,
        image: '/images/coffee-maker.jpg',
        category: 'home',
        rating: 4.0
      }
    ];
    
    setProducts(mockProducts);
    setLoading(false);
  }, []);

  const filteredProducts = filter === 'all' 
    ? products 
    : products.filter(product => product.category === filter);

  if (loading) {
    return <div className="loading">Loading products...</div>;
  }

  return (
    <div className="product-list">
      <div className="product-filters">
        <button 
          className={filter === 'all' ? 'active' : ''} 
          onClick={() => setFilter('all')}
        >
          All Products
        </button>
        <button 
          className={filter === 'electronics' ? 'active' : ''} 
          onClick={() => setFilter('electronics')}
        >
          Electronics
        </button>
        <button 
          className={filter === 'clothing' ? 'active' : ''} 
          onClick={() => setFilter('clothing')}
        >
          Clothing
        </button>
        <button 
          className={filter === 'home' ? 'active' : ''} 
          onClick={() => setFilter('home')}
        >
          Home
        </button>
      </div>
      
      <div className="products-grid">
        {filteredProducts.map(product => (
          <ProductCard key={product.id} product={product} />
        ))}
      </div>
    </div>
  );
};

export default ProductList;
"""
        
        # Product Card component
        components["frontend/src/components/products/ProductCard.js"] = """import React from 'react';
import './ProductCard.css';

const ProductCard = ({ product }) => {
  const handleAddToCart = () => {
    // In a real app, this would dispatch an action to add to cart
    console.log('Added to cart:', product);
    alert(`${product.name} added to cart!`);
  };

  return (
    <div className="product-card">
      <div className="product-image">
        <img src={product.image || '/images/placeholder.jpg'} alt={product.name} />
      </div>
      
      <div className="product-info">
        <h3 className="product-name">{product.name}</h3>
        <div className="product-rating">
          {'★'.repeat(Math.floor(product.rating))}{'☆'.repeat(5 - Math.floor(product.rating))}
          <span className="rating-value">({product.rating})</span>
        </div>
        <p className="product-price">${product.price.toFixed(2)}</p>
        <button className="add-to-cart-btn" onClick={handleAddToCart}>
          Add to Cart
        </button>
      </div>
    </div>
  );
};

export default ProductCard;
"""
        
        # Product List CSS
        components["frontend/src/components/products/ProductList.css"] = """.product-list {
  padding: 20px;
}

.product-filters {
  display: flex;
  gap: 10px;
  margin-bottom: 30px;
  flex-wrap: wrap;
}

.product-filters button {
  padding: 10px 20px;
  border: 1px solid #ddd;
  background: white;
  border-radius: 20px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.product-filters button:hover {
  background: #f0f0f0;
}

.product-filters button.active {
  background: #007bff;
  color: white;
  border-color: #007bff;
}

.products-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
}

@media (max-width: 768px) {
  .products-grid {
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  }
}
"""
        
        # Product Card CSS
        components["frontend/src/components/products/ProductCard.css"] = """.product-card {
  border: 1px solid #ddd;
  border-radius: 8px;
  overflow: hidden;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  background: white;
}

.product-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(0,0,0,0.1);
}

.product-image {
  height: 200px;
  overflow: hidden;
}

.product-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.product-info {
  padding: 20px;
}

.product-name {
  margin: 0 0 10px 0;
  font-size: 18px;
  color: #333;
}

.product-rating {
  margin-bottom: 10px;
  color: #ffc107;
}

.rating-value {
  color: #666;
  font-size: 14px;
  margin-left: 5px;
}

.product-price {
  font-size: 20px;
  font-weight: bold;
  color: #333;
  margin: 15px 0;
}

.add-to-cart-btn {
  width: 100%;
  padding: 12px;
  background: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 16px;
  cursor: pointer;
  transition: background 0.3s ease;
}

.add-to-cart-btn:hover {
  background: #0056b3;
}
"""
        
        return components
    
    def _generate_blog_components(self) -> Dict[str, str]:
        """Generate blog-specific React components."""
        components = {}
        
        # Blog Post List component
        components["frontend/src/components/blog/PostList.js"] = """import React, { useState, useEffect } from 'react';
import PostCard from './PostCard';
import './PostList.css';

const PostList = () => {
  const [posts, setPosts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    // In a real app, this would fetch from your backend API
    const mockPosts = [
      {
        id: 1,
        title: 'Getting Started with React Hooks',
        excerpt: 'Learn how to use React Hooks to simplify your functional components and manage state effectively.',
        author: 'Jane Developer',
        date: '2023-06-15',
        category: 'React',
        readTime: '5 min read'
      },
      {
        id: 2,
        title: 'Building RESTful APIs with FastAPI',
        excerpt: 'Discover how to create powerful and efficient REST APIs using FastAPI and Python.',
        author: 'John Backend',
        date: '2023-06-10',
        category: 'Python',
        readTime: '8 min read'
      },
      {
        id: 3,
        title: 'CSS Grid vs Flexbox: When to Use Which',
        excerpt: 'A comprehensive guide to choosing between CSS Grid and Flexbox for your layout needs.',
        author: 'CSS Master',
        date: '2023-06-05',
        category: 'CSS',
        readTime: '6 min read'
      }
    ];
    
    setPosts(mockPosts);
    setLoading(false);
  }, []);

  const filteredPosts = posts.filter(post => 
    post.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
    post.excerpt.toLowerCase().includes(searchTerm.toLowerCase()) ||
    post.author.toLowerCase().includes(searchTerm.toLowerCase())
  );

  if (loading) {
    return <div className="loading">Loading posts...</div>;
  }

  return (
    <div className="post-list">
      <div className="search-container">
        <input
          type="text"
          placeholder="Search posts..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="search-input"
        />
      </div>
      
      <div className="posts-grid">
        {filteredPosts.map(post => (
          <PostCard key={post.id} post={post} />
        ))}
      </div>
      
      {filteredPosts.length === 0 && searchTerm && (
        <div className="no-results">
          <p>No posts found matching "{searchTerm}"</p>
        </div>
      )}
    </div>
  );
};

export default PostList;
"""
        
        # Blog Post Card component
        components["frontend/src/components/blog/PostCard.js"] = """import React from 'react';
import './PostCard.css';

const PostCard = ({ post }) => {
  return (
    <div className="post-card">
      <div className="post-header">
        <span className="post-category">{post.category}</span>
        <span className="post-date">{post.date}</span>
      </div>
      
      <h3 className="post-title">{post.title}</h3>
      
      <p className="post-excerpt">{post.excerpt}</p>
      
      <div className="post-footer">
        <span className="post-author">By {post.author}</span>
        <span className="post-read-time">{post.readTime}</span>
      </div>
      
      <button className="read-more-btn">
        Read More
      </button>
    </div>
  );
};

export default PostCard;
"""
        
        return components
    
    def _generate_chat_components(self) -> Dict[str, str]:
        """Generate chat-specific React components."""
        components = {}
        
        # Chat component
        components["frontend/src/components/chat/Chat.js"] = """import React, { useState, useEffect, useRef } from 'react';
import './Chat.css';

const Chat = () => {
  const [messages, setMessages] = useState([
    {
      id: 1,
      text: 'Hello! Welcome to our chat app.',
      sender: 'system',
      timestamp: new Date(Date.now() - 300000)
    }
  ]);
  const [newMessage, setNewMessage] = useState('');
  const messagesEndRef = useRef(null);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleSendMessage = (e) => {
    e.preventDefault();
    
    if (newMessage.trim() === '') return;
    
    const message = {
      id: messages.length + 1,
      text: newMessage,
      sender: 'user',
      timestamp: new Date()
    };
    
    setMessages([...messages, message]);
    setNewMessage('');
    
    // Simulate bot response
    setTimeout(() => {
      const botResponse = {
        id: messages.length + 2,
        text: `Thanks for your message: "${newMessage}". This is an automated response.`,
        sender: 'bot',
        timestamp: new Date()
      };
      setMessages(prev => [...prev, botResponse]);
    }, 1000);
  };

  const formatTime = (date) => {
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  return (
    <div className="chat-container">
      <div className="chat-header">
        <h2>Chat Room</h2>
      </div>
      
      <div className="messages-container">
        {messages.map(message => (
          <div 
            key={message.id} 
            className={`message ${message.sender}`}
          >
            <div className="message-content">
              <p className="message-text">{message.text}</p>
              <span className="message-time">{formatTime(message.timestamp)}</span>
            </div>
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>
      
      <form className="message-form" onSubmit={handleSendMessage}>
        <input
          type="text"
          value={newMessage}
          onChange={(e) => setNewMessage(e.target.value)}
          placeholder="Type your message..."
          className="message-input"
        />
        <button type="submit" className="send-button">
          Send
        </button>
      </form>
    </div>
  );
};

export default Chat;
"""
        
        return components
    
    def _generate_crm_components(self) -> Dict[str, str]:
        """Generate CRM-specific React components."""
        components = {}
        
        # Customer List component
        components["frontend/src/components/crm/CustomerList.js"] = """import React, { useState, useEffect } from 'react';
import './CustomerList.css';

const CustomerList = () => {
  const [customers, setCustomers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    // In a real app, this would fetch from your backend API
    const mockCustomers = [
      {
        id: 1,
        name: 'John Smith',
        email: 'john.smith@example.com',
        phone: '+1 (555) 123-4567',
        company: 'Tech Corp',
        status: 'active',
        lastContact: '2023-06-15'
      },
      {
        id: 2,
        name: 'Sarah Johnson',
        email: 'sarah.j@example.com',
        phone: '+1 (555) 987-6543',
        company: 'Design Studio',
        status: 'lead',
        lastContact: '2023-06-10'
      },
      {
        id: 3,
        name: 'Mike Wilson',
        email: 'mike.w@example.com',
        phone: '+1 (555) 456-7890',
        company: 'Marketing Agency',
        status: 'inactive',
        lastContact: '2023-05-20'
      }
    ];
    
    setCustomers(mockCustomers);
    setLoading(false);
  }, []);

  const filteredCustomers = customers.filter(customer => 
    customer.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    customer.email.toLowerCase().includes(searchTerm.toLowerCase()) ||
    customer.company.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const getStatusClass = (status) => {
    switch (status) {
      case 'active': return 'status-active';
      case 'lead': return 'status-lead';
      case 'inactive': return 'status-inactive';
      default: return '';
    }
  };

  if (loading) {
    return <div className="loading">Loading customers...</div>;
  }

  return (
    <div className="customer-list">
      <div className="list-header">
        <h2>Customer Management</h2>
        <div className="header-actions">
          <input
            type="text"
            placeholder="Search customers..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="search-input"
          />
          <button className="add-customer-btn">
            Add Customer
          </button>
        </div>
      </div>
      
      <div className="customers-table">
        <div className="table-header">
          <div className="table-cell">Name</div>
          <div className="table-cell">Email</div>
          <div className="table-cell">Company</div>
          <div className="table-cell">Status</div>
          <div className="table-cell">Last Contact</div>
          <div className="table-cell">Actions</div>
        </div>
        
        {filteredCustomers.map(customer => (
          <div key={customer.id} className="table-row">
            <div className="table-cell">
              <strong>{customer.name}</strong>
              <div className="customer-phone">{customer.phone}</div>
            </div>
            <div className="table-cell">{customer.email}</div>
            <div className="table-cell">{customer.company}</div>
            <div className="table-cell">
              <span className={`status-badge ${getStatusClass(customer.status)}`}>
                {customer.status}
              </span>
            </div>
            <div className="table-cell">{customer.lastContact}</div>
            <div className="table-cell">
              <button className="action-btn view-btn">View</button>
              <button className="action-btn edit-btn">Edit</button>
            </div>
          </div>
        ))}
      </div>
      
      {filteredCustomers.length === 0 && searchTerm && (
        <div className="no-results">
          <p>No customers found matching "{searchTerm}"</p>
        </div>
      )}
    </div>
  );
};

export default CustomerList;
"""
        
        return components
    
    def _generate_default_components(self) -> Dict[str, str]:
        """Generate default React components."""
        components = {}
        
        # Home component
        components["frontend/src/components/Home.js"] = """import React from 'react';
import './Home.css';

const Home = () => {
  return (
    <div className="home">
      <div className="hero-section">
        <h1>Welcome to Your New Application</h1>
        <p>This is a fully functional web application built with React and FastAPI.</p>
        <div className="hero-buttons">
          <button className="primary-btn">Get Started</button>
          <button className="secondary-btn">Learn More</button>
        </div>
      </div>
      
      <div className="features-section">
        <div className="feature-card">
          <h3>Modern Technology</h3>
          <p>Built with React, FastAPI, and MySQL for optimal performance.</p>
        </div>
        <div className="feature-card">
          <h3>Responsive Design</h3>
          <p>Looks great on all devices from mobile to desktop.</p>
        </div>
        <div className="feature-card">
          <h3>Easy to Extend</h3>
          <p>Well-structured codebase that's easy to customize and extend.</p>
        </div>
      </div>
    </div>
  );
};

export default Home;
"""
        
        # Navbar component
        components["frontend/src/components/layout/Navbar.js"] = """import React from 'react';
import { Link } from 'react-router-dom';
import './Navbar.css';

const Navbar = ({ user, onLogout }) => {
  return (
    <nav className="navbar">
      <div className="nav-container">
        <Link to="/" className="nav-logo">
          AppBuilder
        </Link>
        
        <ul className="nav-menu">
          <li className="nav-item">
            <Link to="/" className="nav-link">
              Home
            </Link>
          </li>
          {user ? (
            <>
              <li className="nav-item">
                <Link to="/dashboard" className="nav-link">
                  Dashboard
                </Link>
              </li>
              <li className="nav-item">
                <button onClick={onLogout} className="nav-link logout-btn">
                  Logout
                </button>
              </li>
            </>
          ) : (
            <>
              <li className="nav-item">
                <Link to="/login" className="nav-link">
                  Login
                </Link>
              </li>
              <li className="nav-item">
                <Link to="/register" className="nav-link">
                  Register
                </Link>
              </li>
            </>
          )}
        </ul>
      </div>
    </nav>
  );
};

export default Navbar;
"""
        
        return components
    
    def _generate_common_components(self) -> Dict[str, str]:
        """Generate common React components."""
        components = {}
        
        # Login component
        components["frontend/src/components/auth/Login.js"] = """import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import './Auth.css';

const Login = ({ onLogin }) => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    
    // In a real app, this would be an API call
    try {
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      // Mock successful login
      onLogin({
        id: 1,
        name: 'Demo User',
        email: email
      });
      
      navigate('/dashboard');
    } catch (err) {
      setError('Invalid email or password');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-container">
      <div className="auth-form">
        <h2>Login</h2>
        
        {error && <div className="error-message">{error}</div>}
        
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="email">Email</label>
            <input
              type="email"
              id="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>
          
          <div className="form-group">
            <label htmlFor="password">Password</label>
            <input
              type="password"
              id="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>
          
          <button type="submit" disabled={loading} className="submit-btn">
            {loading ? 'Logging in...' : 'Login'}
          </button>
        </form>
        
        <div className="auth-footer">
          <p>Don't have an account? <Link to="/register">Register</Link></p>
        </div>
      </div>
    </div>
  );
};

export default Login;
"""
        
        return components
    
    def _generate_package_json(self, project_type: str, features: List[str]) -> str:
        """Generate package.json file."""
        dependencies = {
            "react": "^18.2.0",
            "react-dom": "^18.2.0",
            "react-router-dom": "^6.8.0",
            "react-scripts": "5.0.1"
        }
        
        if "charts" in features or project_type == "dashboard":
            dependencies["chart.js"] = "^4.0.0"
            dependencies["react-chartjs-2"] = "^5.0.0"
        
        package_json = {
            "name": f"{project_type}-app",
            "version": "0.1.0",
            "private": True,
            "dependencies": dependencies,
            "scripts": {
                "start": "react-scripts start",
                "build": "react-scripts build",
                "test": "react-scripts test",
                "eject": "react-scripts eject"
            },
            "eslintConfig": {
                "extends": [
                    "react-app",
                    "react-app/jest"
                ]
            },
            "browserslist": {
                "production": [
                    ">0.2%",
                    "not dead",
                    "not op_mini all"
                ],
                "development": [
                    "last 1 chrome version",
                    "last 1 firefox version",
                    "last 1 safari version"
                ]
            }
        }
        
        return json.dumps(package_json, indent=2)
    
    def _generate_index_html(self, project_type: str) -> str:
        """Generate index.html file."""
        return f"""<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <link rel="icon" href="%PUBLIC_URL%/favicon.ico" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <meta name="theme-color" content="#000000" />
    <meta
      name="description"
      content="Generated {project_type} application"
    />
    <link rel="apple-touch-icon" href="%PUBLIC_URL%/logo192.png" />
    <link rel="manifest" href="%PUBLIC_URL%/manifest.json" />
    <title>{project_type.title()} App</title>
  </head>
  <body>
    <noscript>You need to enable JavaScript to run this app.</noscript>
    <div id="root"></div>
  </body>
</html>
"""
    
    def _generate_index_css(self) -> str:
        """Generate index.css file."""
        return """body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
    'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
    sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  background-color: #f5f5f5;
}

code {
  font-family: source-code-pro, Menlo, Monaco, Consolas, 'Courier New',
    monospace;
}

.loading {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  font-size: 18px;
  color: #666;
}

.error-message {
  background-color: #f8d7da;
  color: #721c24;
  padding: 10px;
  border-radius: 4px;
  margin-bottom: 15px;
}
"""
    
    def _generate_app_css(self, project_type: str) -> str:
        """Generate App.css file."""
        return f""".App {{
  text-align: center;
}}

.App-logo {{
  height: 40vmin;
  pointer-events: none;
}}

@media (prefers-reduced-motion: no-preference) {{
  .App-logo {{
    animation: App-logo-spin infinite 20s linear;
  }}
}}

.App-header {{
  background-color: #282c34;
  padding: 20px;
  color: white;
}}

.App-link {{
  color: #61dafb;
}}

@keyframes App-logo-spin {{
  from {{
    transform: rotate(0deg);
  }}
  to {{
    transform: rotate(360deg);
  }}
}}

/* {project_type.title()} specific styles */
"""
    
    def _generate_fastapi_main(self, project_type: str, features: List[str]) -> str:
        """Generate FastAPI main.py file."""
        auth_required = "authentication" in features or "user_management" in features
        
        main_py = '''from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
import traceback

from .core.config import settings
'''
        
        if auth_required:
            main_py += '''from .core.security import verify_token
from .models.user import User
'''
        
        main_py += '''from .api import auth, users, projects

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    description="Generated ''' + project_type + ''' application"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS_LIST,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()

# Include routers
try:
'''
        
        if auth_required:
            main_py += '''    app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
    app.include_router(users.router, prefix="/api/users", tags=["Users"])
'''
        
        main_py += '''    app.include_router(projects.router, prefix="/api/projects", tags=["Projects"])
    print("All routers included successfully")
except Exception as e:
    print(f"Error including routers: {e}")
    print(traceback.format_exc())

@app.on_event("startup")
async def startup_event():
    """Initialize the application on startup."""
    try:
        print(f"🚀 {settings.APP_NAME} v{settings.VERSION} started successfully!")
        print(f"📖 API Documentation: http://localhost:8000/docs")
        print(f"🌐 CORS Origins: {settings.CORS_ORIGINS_LIST}")
    except Exception as e:
        print(f"Startup error: {e}")
        print(traceback.format_exc())
        print("Application will start with limited functionality")

@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": f"Welcome to {settings.APP_NAME}",
        "version": settings.VERSION,
        "description": "Generated ''' + project_type + ''' application",
        "docs": "/docs",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": "2024-01-01T00:00:00Z"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="localhost",
        port=8000,
        reload=settings.DEBUG,
        log_level="info"
    )
'''
        
        return main_py
    
    def _generate_fastapi_models(self, project_type: str, features: List[str]) -> Dict[str, str]:
        """Generate FastAPI models."""
        models = {}
        
        # User model
        models["backend/app/models/user.py"] = """from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from ..core.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
"""
        
        # Project model
        models["backend/app/models/project.py"] = """from sqlalchemy import Column, Integer, String, Text, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..core.database import Base
import enum

class ProjectType(str, enum.Enum):
    WEB_APP = "web_app"
    DASHBOARD = "dashboard"
    ECOMMERCE = "ecommerce"
    BLOG = "blog"
    CHAT = "chat"
    CRM = "crm"

class ProjectStatus(str, enum.Enum):
    CREATING = "creating"
    ACTIVE = "active"
    BUILDING = "building"
    DEPLOYED = "deployed"
    ERROR = "error"

class Project(Base):
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    project_type = Column(Enum(ProjectType), nullable=False)
    status = Column(Enum(ProjectStatus), default=ProjectStatus.CREATING)
    
    # Technical Configuration
    frontend_framework = Column(String(100), default="react")
    backend_framework = Column(String(100), default="fastapi")
    database_type = Column(String(100), default="mysql")
    
    # File Paths
    project_path = Column(String(500), nullable=True)
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Foreign Keys
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Relationships
    owner = relationship("User", back_populates="projects")
"""
        
        return models
    
    def _generate_fastapi_routes(self, project_type: str, features: List[str]) -> Dict[str, str]:
        """Generate FastAPI routes."""
        routes = {}
        
        # Auth routes
        routes["backend/app/api/auth.py"] = """from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from typing import Dict, Any
from sqlalchemy.orm import Session

from ..core.database import get_db
from ..core.security import create_access_token, verify_password, get_password_hash
from ..models.user import User

router = APIRouter()
security = HTTPBearer()

@router.post("/login")
async def login(credentials: Dict[str, str], db: Session = Depends(get_db)):
    '''User login endpoint.'''
    email = credentials.get("email")
    password = credentials.get("password")
    
    if not email or not password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email and password are required"
        )
    
    user = db.query(User).filter(User.email == email).first()
    
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User account is disabled"
        )
    
    access_token = create_access_token(data={"sub": str(user.id)})
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "email": user.email,
            "username": user.username,
            "full_name": user.full_name
        }
    }

@router.post("/register")
async def register(user_data: Dict[str, str], db: Session = Depends(get_db)):
    '''User registration endpoint.'''
    email = user_data.get("email")
    username = user_data.get("username")
    password = user_data.get("password")
    full_name = user_data.get("full_name")
    
    if not email or not username or not password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email, username, and password are required"
        )
    
    # Check if user already exists
    existing_user = db.query(User).filter(
        (User.email == email) | (User.username == username)
    ).first()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email or username already exists"
        )
    
    # Create new user
    hashed_password = get_password_hash(password)
    user = User(
        email=email,
        username=username,
        hashed_password=hashed_password,
        full_name=full_name
    )
    
    db.add(user)
    db.commit()
    db.refresh(user)
    
    access_token = create_access_token(data={"sub": str(user.id)})
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "email": user.email,
            "username": user.username,
            "full_name": user.full_name
        },
        "message": "User registered successfully"
    }
"""
        
        # Project routes
        routes["backend/app/api/projects.py"] = """from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session

from ..core.database import get_db
from ..models.user import User
from ..models.project import Project, ProjectStatus, ProjectType

router = APIRouter()
security = HTTPBearer()

@router.get("/")
async def get_projects(
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    '''Get all projects.'''
    projects = db.query(Project).offset(skip).limit(limit).all()
    
    return {
        "success": True,
        "projects": [
            {
                "id": project.id,
                "name": project.name,
                "description": project.description,
                "type": project.project_type,
                "status": project.status,
                "created_at": project.created_at.isoformat() if project.created_at else None,
                "updated_at": project.updated_at.isoformat() if project.updated_at else None
            }
            for project in projects
        ]
    }

@router.post("/")
async def create_project(
    project_data: Dict[str, Any],
    db: Session = Depends(get_db)
):
    '''Create a new project.'''
    name = project_data.get("name")
    description = project_data.get("description", "")
    project_type = project_data.get("project_type", "web_app")
    
    if not name:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Project name is required"
        )
    
    try:
        project_type_enum = ProjectType(project_type)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid project type: {project_type}"
        )
    
    project = Project(
        name=name,
        description=description,
        project_type=project_type_enum,
        status=ProjectStatus.CREATING
    )
    
    db.add(project)
    db.commit()
    db.refresh(project)
    
    return {
        "success": True,
        "project": {
            "id": project.id,
            "name": project.name,
            "description": project.description,
            "type": project.project_type,
            "status": project.status,
            "created_at": project.created_at.isoformat() if project.created_at else None
        },
        "message": "Project created successfully"
    }

@router.get("/{project_id}")
async def get_project(
    project_id: int,
    db: Session = Depends(get_db)
):
    '''Get a specific project.'''
    project = db.query(Project).filter(Project.id == project_id).first()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    return {
        "success": True,
        "project": {
            "id": project.id,
            "name": project.name,
            "description": project.description,
            "type": project.project_type,
            "status": project.status,
            "created_at": project.created_at.isoformat() if project.created_at else None,
            "updated_at": project.updated_at.isoformat() if project.updated_at else None
        }
    }
"""
        
        return routes
    
    def _generate_fastapi_schemas(self, project_type: str, features: List[str]) -> Dict[str, str]:
        """Generate FastAPI schemas."""
        schemas = {}
        
        schemas["backend/app/schemas/user.py"] = """from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    email: str
    username: str
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class User(UserBase):
    id: int
    is_active: bool
    is_superuser: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: Optional[str] = None
"""
        
        return schemas
    
    def _generate_fastapi_services(self, project_type: str, features: List[str]) -> Dict[str, str]:
        """Generate FastAPI services."""
        services = {}
        
        services["backend/app/services/auth_service.py"] = """from typing import Optional
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def verify_token(token: str):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        return None
"""
        
        return services
    
    def _generate_fastapi_core(self) -> Dict[str, str]:
        """Generate FastAPI core files."""
        core = {}
        
        core["backend/app/core/__init__.py"] = ""
        
        core["backend/app/api/__init__.py"] = ""
        
        core["backend/app/models/__init__.py"] = ""
        
        core["backend/app/schemas/__init__.py"] = ""
        
        core["backend/app/services/__init__.py"] = ""
        
        return core
    
    def _generate_requirements(self, project_type: str, features: List[str]) -> str:
        """Generate requirements.txt file."""
        requirements = [
            "fastapi==0.104.1",
            "uvicorn[standard]==0.24.0",
            "sqlalchemy==2.0.23",
            "python-jose[cryptography]==3.3.0",
            "passlib[bcrypt]==1.7.4",
            "python-multipart==0.0.6",
            "pydantic==2.5.0",
            "pydantic-settings==2.1.0",
            "httpx==0.25.2",
            "python-dotenv==1.0.0"
        ]
        
        if "mysql" in features or project_type == "web_app":
            requirements.append("pymysql==1.1.0")
        
        return "\n".join(requirements) + "\n"
    
    def _generate_config_file(self) -> str:
        """Generate config.py file."""
        return """from pydantic_settings import BaseSettings
from typing import List
import os

class Settings(BaseSettings):
    APP_NAME: str = "Generated App"
    VERSION: str = "0.1.0"
    DEBUG: bool = True
    
    # Security
    SECRET_KEY: str = "your-secret-key-here"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Database
    DATABASE_URL: str = "mysql+pymysql://user:password@localhost/dbname"
    
    # CORS
    CORS_ORIGINS: str = "http://localhost:3000,http://localhost:8000"
    
    @property
    def CORS_ORIGINS_LIST(self) -> List[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]
    
    class Config:
        env_file = ".env"

settings = Settings()
"""
    
    def _generate_database_file(self) -> str:
        """Generate database.py file."""
        return """from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
"""
    
    def _generate_security_file(self) -> str:
        """Generate security.py file."""
        return """from typing import Optional
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from .config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def verify_token(token: str):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        return None
"""
    
    def _generate_mysql_schema(self, project_type: str, features: List[str]) -> str:
        """Generate MySQL schema."""
        schema = """-- Generated Database Schema
-- Project Type: """ + project_type + """

CREATE DATABASE IF NOT EXISTS """ + project_type + """_db;
USE """ + project_type + """_db;

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
    project_type ENUM('web_app', 'dashboard', 'ecommerce', 'blog', 'chat', 'crm') NOT NULL,
    status ENUM('creating', 'active', 'building', 'deployed', 'error') DEFAULT 'creating',
    
    -- Technical Configuration
    frontend_framework VARCHAR(100) DEFAULT 'react',
    backend_framework VARCHAR(100) DEFAULT 'fastapi',
    database_type VARCHAR(100) DEFAULT 'mysql',
    
    -- File Paths
    project_path VARCHAR(500),
    
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

"""
        
        # Add project-specific tables
        if project_type == "ecommerce":
            schema += """-- Products table
CREATE TABLE products (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    category VARCHAR(100),
    image_url VARCHAR(500),
    stock_quantity INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_category (category),
    INDEX idx_price (price)
);

-- Orders table
CREATE TABLE orders (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    total_amount DECIMAL(10, 2) NOT NULL,
    status ENUM('pending', 'processing', 'shipped', 'delivered', 'cancelled') DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_user (user_id),
    INDEX idx_status (status),
    INDEX idx_created (created_at),
    
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Order Items table
CREATE TABLE order_items (
    id INT PRIMARY KEY AUTO_INCREMENT,
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_order (order_id),
    INDEX idx_product (product_id),
    
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
);

"""
        elif project_type == "blog":
            schema += """-- Posts table
CREATE TABLE posts (
    id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    author_id INT NOT NULL,
    published BOOLEAN DEFAULT FALSE,
    published_at TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_author (author_id),
    INDEX idx_published (published),
    INDEX idx_published_at (published_at),
    INDEX idx_created (created_at),
    
    FOREIGN KEY (author_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Comments table
CREATE TABLE comments (
    id INT PRIMARY KEY AUTO_INCREMENT,
    post_id INT NOT NULL,
    author_id INT NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_post (post_id),
    INDEX idx_author (author_id),
    INDEX idx_created (created_at),
    
    FOREIGN KEY (post_id) REFERENCES posts(id) ON DELETE CASCADE,
    FOREIGN KEY (author_id) REFERENCES users(id) ON DELETE CASCADE
);

"""
        elif project_type == "chat":
            schema += """-- Conversations table
CREATE TABLE conversations (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255),
    is_group BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Conversation Participants table
CREATE TABLE conversation_participants (
    id INT PRIMARY KEY AUTO_INCREMENT,
    conversation_id INT NOT NULL,
    user_id INT NOT NULL,
    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_conversation (conversation_id),
    INDEX idx_user (user_id),
    
    FOREIGN KEY (conversation_id) REFERENCES conversations(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Messages table
CREATE TABLE messages (
    id INT PRIMARY KEY AUTO_INCREMENT,
    conversation_id INT NOT NULL,
    sender_id INT NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_conversation (conversation_id),
    INDEX idx_sender (sender_id),
    INDEX idx_created (created_at),
    
    FOREIGN KEY (conversation_id) REFERENCES conversations(id) ON DELETE CASCADE,
    FOREIGN KEY (sender_id) REFERENCES users(id) ON DELETE CASCADE
);

"""
        elif project_type == "crm":
            schema += """-- Customers table
CREATE TABLE customers (
    id INT PRIMARY KEY AUTO_INCREMENT,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone VARCHAR(20),
    company VARCHAR(255),
    status ENUM('lead', 'active', 'inactive') DEFAULT 'lead',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_email (email),
    INDEX idx_status (status),
    INDEX idx_company (company),
    INDEX idx_created (created_at)
);

-- Contacts table
CREATE TABLE contacts (
    id INT PRIMARY KEY AUTO_INCREMENT,
    customer_id INT NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(255),
    phone VARCHAR(20),
    position VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_customer (customer_id),
    INDEX idx_email (email),
    INDEX idx_created (created_at),
    
    FOREIGN KEY (customer_id) REFERENCES customers(id) ON DELETE CASCADE
);

"""
        
        schema += """-- Insert default admin user
INSERT INTO users (email, username, hashed_password, full_name, is_active, is_superuser) 
VALUES (
    'admin@example.com', 
    'admin',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj2PSF1nwKmW', -- password: admin123
    'Administrator',
    TRUE,
    TRUE
);

COMMIT;
"""
        
        return schema
    
    def _generate_mysql_migrations(self, project_type: str, features: List[str]) -> str:
        """Generate MySQL migrations."""
        return f"""-- Initial migration for {project_type} application
-- This file contains the initial database schema

-- Migration: 001_initial
-- Date: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

-- Apply the schema from schema.sql
-- This is a placeholder for actual migration logic

-- In a real application, you would use a migration tool like Alembic
-- to manage database schema changes over time

SELECT 'Migration 001 applied successfully' as migration_status;
"""
    
    def _generate_main_dockerfile(self) -> str:
        """Generate main Dockerfile."""
        return """# Multi-stage Dockerfile for React + FastAPI application

# Frontend build stage
FROM node:18-alpine as frontend-build
WORKDIR /app
COPY frontend/package*.json ./
RUN npm ci --silent
COPY frontend/. .
RUN npm run build

# Backend stage
FROM python:3.11-slim
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    gcc \\
    default-libmysqlclient-dev \\
    pkg-config \\
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY backend/. .

# Copy frontend build
COPY --from=frontend-build /app/build /app/frontend/build

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
"""
    
    def _generate_docker_compose(self, project_type: str) -> str:
        """Generate docker-compose.yml file."""
        return f"""version: '3.8'

services:
  backend:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=mysql+pymysql://user:password@db:3306/{project_type}_db
      - SECRET_KEY=your-secret-key-here
    depends_on:
      - db
    volumes:
      - ./backend:/app

  db:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: rootpassword
      MYSQL_DATABASE: {project_type}_db
      MYSQL_USER: user
      MYSQL_PASSWORD: password
    ports:
      - "3306:3306"
    volumes:
      - db_data:/var/lib/mysql
      - ./database/schema.sql:/docker-entrypoint-initdb.d/schema.sql

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./frontend/build:/usr/share/nginx/html
    depends_on:
      - backend

volumes:
  db_data:
"""
    
    def _generate_nginx_config(self) -> str:
        """Generate nginx.conf file."""
        return """events {
    worker_connections 1024;
}

http {
    upstream frontend {
        server frontend:3000;
    }
    
    upstream backend {
        server backend:8000;
    }
    
    server {
        listen 80;
        
        location / {
            root /usr/share/nginx/html;
            index index.html index.htm;
            try_files $uri $uri/ /index.html;
        }
        
        location /api/ {
            proxy_pass http://backend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
        
        location /docs {
            proxy_pass http://backend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
        
        location /openapi.json {
            proxy_pass http://backend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }
}
"""
    
    def _generate_deploy_script(self) -> str:
        """Generate deploy.sh file."""
        return """#!/bin/bash

# Deployment script for the application

# Exit on any error
set -e

echo "Starting deployment process..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Build and start services
echo "Building and starting services..."
docker-compose up -d --build

# Wait for services to start
echo "Waiting for services to start..."
sleep 10

# Check if services are running
echo "Checking service status..."
docker-compose ps

echo "Deployment completed successfully!"
echo "Frontend: http://localhost"
echo "Backend API: http://localhost/api"
echo "API Documentation: http://localhost/docs"
"""