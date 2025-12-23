<div align="center">

# 🤖 AI Email Agent

### *Intelligent Email Drafting & Sending Platform*

[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)](https://reactjs.org/)
[![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Zustand](https://img.shields.io/badge/Zustand-000000?style=for-the-badge&logo=react&logoColor=white)](https://zustand-demo.pmnd.rs/)

*An AI-powered email drafting and sending application with a modern React frontend and FastAPI backend*

[Features](#-features) • [Quick Start](#-quick-start) • [API Docs](#-api-endpoints) • [Configuration](#-configuration)

</div>

---

## 📸 UI Preview

<div align="center">
  <img src="./assets/Screenshot%20(16).png" alt="AI Email Agent Interface" width="800px" />
</div>

---

## ✨ Features

<table>
<tr>
<td width="50%">

### 🎯 Core Features
- 🤖 **AI-Powered Generation** - Using Groq/LLaMA
- 📧 **Gmail Integration** - SMTP email sending
- 📝 **Draft & Edit** - Review before sending
- 📊 **History Tracking** - Complete email logs
- 🎨 **Modern UI** - Beautiful gradient design

</td>
<td width="50%">

### 🛠️ Technical Stack
- ⚡ **FastAPI Backend** - High performance
- ⚛️ **React Frontend** - Modern UI/UX
- 🐳 **Docker Ready** - Easy deployment
- 🗄️ **PostgreSQL** - Reliable database
- 🎭 **Zustand** - State management

</td>
</tr>
</table>

---

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose
- Gmail account with App Password
- Groq API key

### Installation

```bash
# 1️⃣ Clone the repository
git clone <your-repo-url>
cd AI-Agent

# 2️⃣ Setup environment variables
cp .env.example .env
# Edit .env with your credentials

# 3️⃣ Start with Docker
docker-compose up --build
```

### 🌐 Access Points

| Service | URL | Description |
|---------|-----|-------------|
| 🎨 Frontend | http://localhost:3000 | React UI |
| ⚡ Backend API | http://localhost:8001 | FastAPI Server |
| 📚 API Docs | http://localhost:8001/docs | Swagger UI |

---

## ⚙️ Configuration

Create a `.env` file in the root directory:

```env
# 📧 Email Configuration
EMAIL=your-email@gmail.com
APP_PASSWORD=your-16-char-app-password
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=465

# 🤖 AI Configuration
GROQ_API_KEY=your-groq-api-key

# 🗄️ Database Configuration
POSTGRES_USER=dbuser
POSTGRES_PASSWORD=db-password
POSTGRES_DB=mydb
DATABASE_URL=postgresql+psycopg://dbuser:db-password@db_service:5432/mydb
```

### 🔐 Gmail App Password Setup

1. Go to [Google Account Settings](https://myaccount.google.com/)
2. Enable **2-Factor Authentication**
3. Navigate to **Security** → **App Passwords**
4. Generate a new app password for "Mail"
5. Copy the 16-character password to `.env`

---

## 📡 API Endpoints

### Email Operations

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/emails/send` | Generate and send email |
| `POST` | `/api/emails/draft` | Generate email draft |
| `POST` | `/api/emails/send-draft` | Send edited draft |
| `GET` | `/api/emails/history` | Retrieve email history |

### TTS Operations

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/tts/speak` | Convert draft to speech |

### Documentation

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/docs` | Interactive API documentation |
| `GET` | `/redoc` | Alternative API documentation |

---

## 🏗️ Project Structure

```
AI-Agent/
├── 📁 backend/
│   ├── src/
│   │   ├── api/
│   │   │   ├── email/      # Email operations
│   │   │   ├── tts/        # Text-to-speech
│   │   │   └── templates/  # Email templates
│   │   └── main.py         # FastAPI app
│   ├── Dockerfile
│   └── requirements.txt
│
├── 📁 frontend/
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── hooks/          # Custom hooks
│   │   ├── services/       # API services
│   │   ├── store/          # Zustand store
│   │   ├── styles/         # CSS modules
│   │   └── utils/          # Utilities
│   ├── Dockerfile
│   └── package.json
│
├── docker-compose.yaml
├── .env
└── README.md
```

---

## 💻 Development

### Backend Development

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8002
```

### Frontend Development

```bash
cd frontend
npm install
npm start
```

---

## 🎨 Tech Stack Details

### Backend
- **FastAPI** - Modern Python web framework
- **SQLModel** - SQL database ORM
- **Pydantic** - Data validation
- **LangChain** - AI integration
- **PostgreSQL** - Database

### Frontend
- **React 18** - UI library
- **Zustand** - State management
- **Axios** - HTTP client
- **CSS3** - Modern styling with gradients

### DevOps
- **Docker** - Containerization
- **Docker Compose** - Multi-container orchestration
- **PostgreSQL** - Database container

---

## 🚀 Future Enhancements

### 🔮 Coming Soon

<table>
<tr>
<td width="50%">

#### 📅 Phase 1 - Q1 2025
- 🔄 **Email Scheduling** - Schedule emails for later
- 📎 **File Attachments** - Attach files to emails
- 🎯 **Bulk Email** - Send to multiple recipients
- 📧 **Email Templates** - Pre-built templates
- 🌍 **Multi-language** - Support for multiple languages

</td>
<td width="50%">

#### 🎨 Phase 2 - Q2 2025
- 📊 **Analytics Dashboard** - Email performance metrics
- 🔔 **Email Notifications** - Real-time alerts
- 🎭 **Custom Themes** - Personalize UI
- 🔐 **OAuth Integration** - Secure authentication
- 📱 **Mobile App** - iOS & Android support

</td>
</tr>
</table>

### 💡 Planned Features

- ✅ **AI Reply Suggestions** - Smart reply recommendations
- ✅ **Email Categorization** - Auto-categorize emails
- ✅ **Sentiment Analysis** - Analyze email tone
- ✅ **A/B Testing** - Test different email versions
- ✅ **Integration Hub** - Connect with Slack, Teams, etc.
- ✅ **Voice Commands** - Control via voice
- ✅ **Email Tracking** - Track opens and clicks
- ✅ **Spam Detection** - AI-powered spam filter

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

## 📝 License

This project is licensed under the MIT License.

---

<div align="center">

### Made with ❤️ by Prince

**[⬆ Back to Top](#-ai-email-agent)**

</div>
