# Email Agent Architecture

## System Overview

```
┌─────────────┐      ┌─────────────┐      ┌─────────────┐
│   React     │─────▶│   FastAPI   │─────▶│ PostgreSQL  │
│  Frontend   │◀─────│   Backend   │◀─────│  Database   │
└─────────────┘      └─────────────┘      └─────────────┘
                            │
                            ├─────▶ Groq/LLaMA (AI)
                            │
                            └─────▶ Gmail SMTP
```

## Technology Stack

### Frontend
- **Framework**: React 18
- **HTTP Client**: Axios
- **Styling**: CSS (Supabase-inspired dark theme)
- **Port**: 3000

### Backend
- **Framework**: FastAPI
- **ORM**: SQLModel
- **Database Driver**: psycopg (PostgreSQL)
- **AI Framework**: LangChain + LangGraph
- **LLM Provider**: Groq (LLaMA 3.1)
- **Email**: SMTP (Gmail)
- **Port**: 8001

### Database
- **Type**: PostgreSQL 17.5
- **Deployment**: Docker (local) or AWS RDS (cloud)
- **Port**: 5432

### Infrastructure
- **Containerization**: Docker + Docker Compose
- **Environment**: .env configuration

---

## Project Structure

```
AI-Agent/
├── backend/
│   ├── src/
│   │   ├── api/
│   │   │   ├── ai/              # AI services
│   │   │   │   ├── agents.py    # LangGraph agents
│   │   │   │   ├── llms.py      # LLM initialization
│   │   │   │   ├── schemas.py   # Pydantic models
│   │   │   │   ├── services.py  # AI email generation
│   │   │   │   └── tools.py     # LangChain tools
│   │   │   ├── chat/            # Chat endpoints (legacy)
│   │   │   │   ├── models.py
│   │   │   │   └── routing.py
│   │   │   ├── email/           # Email operations
│   │   │   │   ├── models.py    # Email data models
│   │   │   │   └── routing.py   # Email API endpoints
│   │   │   ├── health/          # Health check
│   │   │   │   └── routing.py
│   │   │   ├── myemailer/       # Email utilities
│   │   │   │   ├── sender.py    # SMTP sender
│   │   │   │   └── myinbox_reader.py
│   │   │   └── db.py            # Database setup
│   │   └── main.py              # FastAPI app entry
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── App.js               # Main React component
│   │   ├── index.js             # React entry point
│   │   └── index.css            # Styles
│   ├── Dockerfile
│   └── package.json
├── .env                         # Environment variables
├── docker-compose.yaml          # Container orchestration
├── health-check.html            # API testing tool
└── README.md
```

---

## Architecture Layers

### 1. Presentation Layer (Frontend)

**Components:**
- Email composition form
- Draft editor
- Email history display
- Status notifications

**Responsibilities:**
- User input validation
- API communication
- State management
- UI rendering

**Data Flow:**
```
User Input → Validation → API Request → Display Response
```

---

### 2. API Layer (Backend)

**Endpoints:**

```
GET  /                          # Root health check
GET  /api/health/               # Basic health
GET  /api/health/detailed       # Detailed health with components

POST /api/emails/send           # Generate & send email
POST /api/emails/draft          # Generate draft only
POST /api/emails/send-draft     # Send edited draft
GET  /api/emails/history        # Get email history

POST /api/chats/                # Chat endpoint (legacy)
GET  /api/chats/recent/         # Recent chats
```

**Middleware:**
- CORS (allow all origins)
- Environment variable injection

---

### 3. Business Logic Layer

#### AI Service (`api/ai/`)

**Components:**
- **LLM Provider** (`llms.py`): Groq API initialization
- **Email Generator** (`services.py`): Prompt → Email conversion
- **Agents** (`agents.py`): LangGraph ReAct agents
- **Tools** (`tools.py`): Email sending, inbox reading

**Flow:**
```
User Prompt → LLM (Groq) → Structured Output → Email (subject + content)
```

**AI Model:**
- Provider: Groq
- Model: llama-3.1-8b-instant
- Output: Structured (EmailMessage schema)

#### Email Service (`api/myemailer/`)

**Components:**
- **Sender** (`sender.py`): SMTP email delivery
- **Inbox Reader** (`myinbox_reader.py`): IMAP email retrieval

**SMTP Configuration:**
```
Host: smtp.gmail.com
Port: 465 (SSL)
Auth: Gmail App Password
```

---

### 4. Data Layer

#### Database Schema

**EmailHistory Table:**
```sql
CREATE TABLE emailhistory (
    id SERIAL PRIMARY KEY,
    recipient VARCHAR NOT NULL,
    subject VARCHAR NOT NULL,
    content TEXT NOT NULL,
    prompt TEXT NOT NULL,
    status VARCHAR NOT NULL,  -- 'sent' or 'failed'
    created_at TIMESTAMP WITH TIME ZONE NOT NULL
);
```

**ChatMessage Table (Legacy):**
```sql
CREATE TABLE chatmessage (
    id SERIAL PRIMARY KEY,
    message TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL
);
```

**ORM:**
- SQLModel (Pydantic + SQLAlchemy)
- Auto-creates tables on startup

---

## Data Flow Diagrams

### Email Sending Flow

```
┌──────────┐
│  User    │
└────┬─────┘
     │ 1. Enter recipient & prompt
     ▼
┌──────────────────┐
│  React Frontend  │
└────┬─────────────┘
     │ 2. POST /api/emails/send
     ▼
┌──────────────────┐
│  FastAPI Router  │
└────┬─────────────┘
     │ 3. Call generate_email_message()
     ▼
┌──────────────────┐
│  AI Service      │
│  (Groq LLM)      │
└────┬─────────────┘
     │ 4. Return EmailMessage(subject, content)
     ▼
┌──────────────────┐
│  Email Sender    │
│  (SMTP)          │
└────┬─────────────┘
     │ 5. Send via Gmail
     ▼
┌──────────────────┐
│  Database        │
│  (Save record)   │
└────┬─────────────┘
     │ 6. Return success response
     ▼
┌──────────────────┐
│  React Frontend  │
│  (Show success)  │
└──────────────────┘
```

### Draft Editing Flow

```
User → Generate Draft → AI → Display Editable Fields
                                      │
User Edits Subject/Content ───────────┘
                                      │
                                      ▼
                            POST /api/emails/send-draft
                                      │
                                      ▼
                              Send via SMTP → Save → Success
```

---

## Security Architecture

### Authentication
- No user authentication (single-user app)
- Gmail: App Password (2FA required)
- Groq: API Key

### Data Protection
- Environment variables for secrets
- SSL/TLS for SMTP (port 465)
- PostgreSQL password authentication
- CORS enabled (configure for production)

### Secrets Management
```
.env file (not committed to git)
├── EMAIL credentials
├── GROQ_API_KEY
├── DATABASE_URL
└── AWS_RDS credentials (optional)
```

---

## Deployment Architecture

### Development (Docker Compose)

```
┌─────────────────────────────────────┐
│         Docker Network              │
│                                     │
│  ┌──────────┐  ┌──────────┐       │
│  │ Frontend │  │ Backend  │       │
│  │  :3000   │  │  :8001   │       │
│  └────┬─────┘  └────┬─────┘       │
│       │             │              │
│       │             ▼              │
│       │      ┌──────────┐         │
│       │      │PostgreSQL│         │
│       │      │  :5432   │         │
│       │      └──────────┘         │
└───────┼──────────────────────────┘
        │
        ▼
   Host Machine
   (localhost:3000)
```

### Production (AWS)

```
┌─────────────────────────────────────┐
│         AWS Cloud                   │
│                                     │
│  ┌──────────┐  ┌──────────┐       │
│  │   EC2    │  │   EC2    │       │
│  │ Frontend │  │ Backend  │       │
│  └────┬─────┘  └────┬─────┘       │
│       │             │              │
│       │             ▼              │
│       │      ┌──────────┐         │
│       │      │   RDS    │         │
│       │      │PostgreSQL│         │
│       │      └──────────┘         │
└───────┼──────────────────────────┘
        │
        ▼
   Internet Users
```

---

## API Request/Response Examples

### Send Email

**Request:**
```json
POST /api/emails/send
{
  "recipient": "user@example.com",
  "prompt": "Write a thank you email for the interview"
}
```

**Response:**
```json
{
  "subject": "Thank You for the Interview Opportunity",
  "content": "Dear Hiring Manager,\n\nI wanted to express...",
  "recipient": "user@example.com",
  "status": "sent"
}
```

### Generate Draft

**Request:**
```json
POST /api/emails/draft
{
  "recipient": "user@example.com",
  "prompt": "Follow-up email about project status"
}
```

**Response:**
```json
{
  "subject": "Project Status Update",
  "content": "Hi Team,\n\nI wanted to follow up...",
  "recipient": "user@example.com"
}
```

### Health Check

**Request:**
```
GET /api/health/detailed
```

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-11-30T15:30:00+00:00",
  "components": {
    "database": {
      "status": "healthy",
      "message": "Database connection successful"
    },
    "email": {
      "status": "healthy",
      "message": "Email configuration present"
    },
    "ai": {
      "status": "healthy",
      "message": "AI configuration present"
    }
  }
}
```

---

## Performance Considerations

### Caching
- No caching implemented (stateless API)
- Consider Redis for:
  - Email templates
  - Frequent prompts
  - Rate limiting

### Database Optimization
- Indexes on: `created_at`, `recipient`, `status`
- Connection pooling (SQLAlchemy default)
- Query limit: 10 emails per history request

### AI Optimization
- Model: llama-3.1-8b-instant (fast inference)
- Structured output (reduces parsing overhead)
- No streaming (simple request/response)

---

## Scalability

### Current Limitations
- Single instance (no load balancing)
- Synchronous email sending
- No queue system

### Future Improvements
- **Horizontal Scaling**: Multiple backend instances + load balancer
- **Queue System**: Celery/RabbitMQ for async email sending
- **Caching**: Redis for templates and rate limiting
- **CDN**: CloudFront for frontend static assets
- **Read Replicas**: PostgreSQL read replicas for history queries

---

## Monitoring & Observability

### Health Checks
- Basic: `/api/health/`
- Detailed: `/api/health/detailed`
- Components: Database, Email config, AI config

### Logging
- FastAPI access logs
- Application logs (print statements)
- Database query logs

### Metrics (Future)
- Email send success rate
- AI generation latency
- Database query performance
- API response times

---

## Error Handling

### Frontend
- Form validation (email format, prompt length)
- API error display (user-friendly messages)
- Network error handling

### Backend
- Try-catch blocks for all operations
- Failed emails saved to database with status='failed'
- HTTP exceptions with detailed messages
- Database transaction rollback on errors

### Database
- Connection retry logic
- Transaction management
- Constraint validation

---

## Configuration Management

### Environment Variables

```env
# Database
DATABASE_URL=postgresql+psycopg://user:pass@host:5432/db

# Email
EMAIL=sender@gmail.com
APP_PASSWORD=gmail-app-password
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=465

# AI
GROQ_API_KEY=gsk_xxxxx

# Optional
GEMINI_API_KEY=AIza_xxxxx
```

### Docker Compose

```yaml
services:
  frontend:
    - Port mapping: 3000:3000
    - Volume mount for hot reload
    
  backend:
    - Port mapping: 8001:8000
    - Environment from .env
    - Depends on db_service
    
  db_service:
    - PostgreSQL 17.5
    - Volume for data persistence
```

---

## Testing Strategy

### Manual Testing
- `health-check.html` - API endpoint testing
- Browser DevTools - Frontend debugging
- Postman/cURL - API testing

### Future Testing
- **Unit Tests**: pytest for backend functions
- **Integration Tests**: API endpoint tests
- **E2E Tests**: Playwright for frontend flows
- **Load Tests**: Locust for performance testing

---

## Dependencies

### Backend
```
fastapi - Web framework
uvicorn - ASGI server
sqlmodel - ORM
psycopg - PostgreSQL driver
langchain - AI framework
langchain-groq - Groq integration
langgraph - Agent framework
pydantic - Data validation
```

### Frontend
```
react - UI framework
react-dom - React renderer
axios - HTTP client
react-scripts - Build tools
```

---

## Future Enhancements

1. **User Authentication**: Multi-user support with JWT
2. **Email Templates**: Pre-defined templates library
3. **Bulk Sending**: CSV upload for multiple recipients
4. **Scheduling**: Schedule emails for later
5. **Attachments**: File upload support
6. **Analytics**: Dashboard with charts
7. **Webhooks**: Email delivery notifications
8. **API Rate Limiting**: Prevent abuse
9. **Internationalization**: Multi-language support
10. **Mobile App**: React Native version
