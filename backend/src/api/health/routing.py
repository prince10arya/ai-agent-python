"""Health check endpoints for monitoring API status."""

from fastapi import APIRouter, Depends
from sqlmodel import Session, text
from datetime import datetime, timezone
import os

from api.db import get_session

router = APIRouter()


@router.get("/", tags=["Health"])
def health_check():
    """Basic health check endpoint.

    Returns:
        dict: API status and timestamp
    """
    return {
        "status": "healthy",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "service": "Email Agent API"
    }


@router.get("/detailed", tags=["Health"])
def detailed_health_check(session: Session = Depends(get_session)):
    """Detailed health check with database and environment validation.

    Args:
        session: Database session dependency

    Returns:
        dict: Detailed health status of all components
    """
    health_status = {
        "status": "healthy",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "components": {}
    }

    # Check database connection
    try:
        session.exec(text("SELECT 1"))
        health_status["components"]["database"] = {
            "status": "healthy",
            "message": "Database connection successful"
        }
    except Exception as e:
        health_status["status"] = "unhealthy"
        health_status["components"]["database"] = {
            "status": "unhealthy",
            "message": str(e)
        }

    # Check email configuration
    email_config = {
        "EMAIL": bool(os.environ.get("EMAIL")),
        "APP_PASSWORD": bool(os.environ.get("APP_PASSWORD")),
        "EMAIL_HOST": bool(os.environ.get("EMAIL_HOST")),
        "EMAIL_PORT": bool(os.environ.get("EMAIL_PORT"))
    }

    if all(email_config.values()):
        health_status["components"]["email"] = {
            "status": "healthy",
            "message": "Email configuration present"
        }
    else:
        health_status["status"] = "degraded"
        health_status["components"]["email"] = {
            "status": "degraded",
            "message": "Missing email configuration",
            "missing": [k for k, v in email_config.items() if not v]
        }

    # Check AI configuration
    groq_key = bool(os.environ.get("GROQ_API_KEY"))
    if groq_key:
        health_status["components"]["ai"] = {
            "status": "healthy",
            "message": "AI configuration present"
        }
    else:
        health_status["status"] = "degraded"
        health_status["components"]["ai"] = {
            "status": "degraded",
            "message": "Missing GROQ_API_KEY"
        }

    return health_status
