# AI Email Agent

An AI-powered email drafting and sending application with a React frontend and FastAPI backend.

## UI
https://github.com/prince10arya/ai-agent-python/blob/main/assets/Screenshot%20(16).png


## Features

- 🤖 AI-powered email generation using Groq/LLaMA
- 📧 Send emails via Gmail SMTP
- 📝 Draft emails before sending
- 📊 Email history tracking
- 🎨 Clean React frontend interface
- 🐳 Docker containerized setup

## Quick Start

1. **Clone and setup environment:**
   ```bash
   cd "AI-Agent"
   cp .env.example .env
   # Edit .env with your credentials
   ```

2. **Start with Docker:**
   ```bash
   docker-compose up --build
   ```

3. **Access the application:**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8001
   - API Docs: http://localhost:8001/docs

## Configuration

Update `.env` file with your credentials:

```env
# Email Configuration
EMAIL=your-email@gmail.com
APP_PASSWORD=your-app-password
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=465

# AI Configuration
GROQ_API_KEY=your-groq-api-key

# Database
POSTGRES_USER=dbuser
POSTGRES_PASSWORD=db-password
POSTGRES_DB=mydb
DATABASE_URL=postgresql+psycopg://dbuser:db-password@db_service:5432/mydb
```

## API Endpoints

- `POST /api/emails/send` - Generate and send email
- `POST /api/emails/draft` - Generate email draft
- `GET /api/emails/history` - Get email history
- `GET /docs` - API documentation

## Development

**Backend only:**
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8001
```

**Frontend only:**
```bash
cd frontend
npm install
npm start
```

## Gmail Setup

1. Enable 2-factor authentication
2. Generate an App Password
3. Use the App Password in the `APP_PASSWORD` field
