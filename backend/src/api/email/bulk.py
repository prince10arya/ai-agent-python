"""Bulk email and scheduling models."""

from sqlmodel import SQLModel, Field
from datetime import datetime, timezone
from typing import Optional, List
from pydantic import BaseModel


def get_utc_now():
    return datetime.now(timezone.utc)


class BulkEmailRequest(BaseModel):
    """Request for bulk email sending."""
    recipients: List[str]
    subject: str
    content: str
    tone: Optional[str] = "professional"


class ScheduledEmail(SQLModel, table=True):
    """Scheduled email database model."""
    id: Optional[int] = Field(default=None, primary_key=True)
    recipient: str
    subject: str
    content: str
    scheduled_time: datetime
    timezone: str = "UTC"
    status: str = "pending"  # pending, sent, cancelled, failed
    created_at: datetime = Field(default_factory=get_utc_now)


class ScheduleEmailRequest(BaseModel):
    """Request for scheduling email."""
    recipient: str
    subject: str
    content: str
    scheduled_time: str  # ISO format
    timezone: str = "UTC"


class BulkEmailProgress(BaseModel):
    """Progress response for bulk email."""
    total: int
    sent: int
    failed: int
    progress_percent: float
