from api.chat.routing import router as chat_router
from api.email.routing import router as email_router
from api.health.routing import router as health_router
from api.db import init_db

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Application startup: Initializing database...")
    init_db()
    print("Application startup: Database initialized.")
    yield
    print("Application shutdown: Cleaning up resources (if any)...")

app = FastAPI(
    title="Email Agent API",
    description="AI-powered email drafting and sending service",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router, prefix='/api/chats', tags=["Chat"])
app.include_router(email_router, prefix='/api/emails', tags=["Email"])
app.include_router(health_router, prefix='/api/health', tags=["Health"])

@app.get('/', tags=["Health"])
def read_index():
    return {"message": "Email Agent API is running", "status": "healthy"}
