from sqlmodel import SQLModel, Field, DateTime
from datetime import timezone, datetime
from typing import Optional


def get_utc_now():
    return datetime.now().replace(tzinfo=timezone.utc)


class EmailRequest(SQLModel):
    recipient: str = Field(description="Email address of the recipient")
    prompt: str = Field(description="User prompt for email generation")


class EmailResponse(SQLModel):
    subject: str
    content: str
    recipient: str
    status: str = "sent"


class EmailHistory(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    recipient: str
    subject: str
    content: str
    prompt: str
    status: str = "sent"
    created_at: datetime = Field(
        default_factory=get_utc_now,
        sa_type=DateTime(timezone=True),
        nullable=False,
    )


class EmailHistoryResponse(SQLModel):
    id: int
    recipient: str
    subject: str
    content: str
    prompt: str
    status: str
    created_at: datetime