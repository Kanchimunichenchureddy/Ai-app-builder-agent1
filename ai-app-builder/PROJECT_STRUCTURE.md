ai-app-builder/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   ├── config.py
│   │   │   ├── security.py
│   │   │   └── database.py
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── project.py
│   │   │   ├── user.py
│   │   │   └── deployment.py
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   ├── project.py
│   │   │   ├── user.py
│   │   │   └── deployment.py
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── auth.py
│   │   │   ├── projects.py
│   │   │   ├── builder.py
│   │   │   └── deployment.py
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── ai_agent.py
│   │   │   ├── code_generator.py
│   │   │   ├── deployer.py
│   │   │   └── integrations/
│   │   │       ├── openrouter_service.py
│   │   │       └── __init__.py
│   │   └── utils/
│   │       ├── __init__.py
│   │       ├── file_handler.py
│   │       └── validators.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env.example
├── frontend/
│   ├── public/
│   │   ├── index.html
│   │   └── favicon.ico
│   ├── src/
│   │   ├── components/
│   │   │   ├── common/
│   │   │   ├── builder/
│   │   │   ├── dashboard/
│   │   │   └── deployment/
│   │   ├── pages/
│   │   │   ├── Home.js
│   │   │   ├── Builder.js
│   │   │   ├── Dashboard.js
│   │   │   └── Deploy.js
│   │   ├── services/
│   │   │   ├── api.js
│   │   │   └── auth.js
│   │   ├── utils/
│   │   ├── styles/
│   │   ├── App.js
│   │   └── index.js
│   ├── package.json
│   ├── Dockerfile
│   └── .env.example
├── database/
│   ├── init.sql
│   ├── migrations/
│   └── schemas/
├── templates/
│   ├── dashboard/
│   ├── ecommerce/
│   ├── blog/
│   ├── crm/
│   └── chat/
├── deployment/
│   ├── docker-compose.yml
│   ├── docker-compose.prod.yml
│   ├── nginx.conf
│   └── ci-cd/
│       ├── github-actions.yml
│       └── gitlab-ci.yml
└── docs/
    ├── api.md
    ├── deployment.md
    └── templates.md