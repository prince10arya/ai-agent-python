"""Email template models."""

from sqlmodel import SQLModel, Field
from datetime import datetime, timezone
from typing import Optional


def get_utc_now():
    return datetime.now(timezone.utc)


class EmailTemplate(SQLModel, table=True):
    """Email template database model."""
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    category: str  # follow-up, thank-you, meeting-request, custom
    subject: str
    content: str
    is_predefined: bool = Field(default=False)
    created_at: datetime = Field(default_factory=get_utc_now)


class TemplateRequest(SQLModel):
    """Request model for creating template."""
    name: str
    category: str
    subject: str
    content: str


class TemplateResponse(SQLModel):
    """Response model for template."""
    id: int
    name: str
    category: str
    subject: str
    content: str
    is_predefined: bool
    created_at: datetime
