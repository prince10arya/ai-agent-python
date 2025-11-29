"""Email routing module for handling email operations.

This module provides API endpoints for:
- Generating and sending emails using AI
- Creating email drafts
- Sending edited drafts
- Retrieving email history
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List

from .models import EmailRequest, EmailResponse, EmailHistory, EmailHistoryResponse
from api.db import get_session
from api.ai.services import generate_email_message
from api.myemailer.sender import send_mail
from pydantic import BaseModel


class SendDraftRequest(BaseModel):
    """Request model for sending edited draft emails.
    
    Attributes:
        recipient: Email address of the recipient
        subject: Email subject line
        content: Email body content
    """
    recipient: str
    subject: str
    content: str


router = APIRouter()


@router.get("/", tags=["Email"])
def email_health():
    """Health check endpoint for email service.
    
    Returns:
        dict: Service status information
    """
    return {"status": "ok", "service": "email"}


@router.post("/send", response_model=EmailResponse, tags=["Email"])
def send_email(
    request: EmailRequest,
    session: Session = Depends(get_session)
):
    """Generate and send an email using AI based on user prompt.
    
    This endpoint:
    1. Generates email content using AI from the provided prompt
    2. Sends the email via SMTP
    3. Saves the email record to database
    
    Args:
        request: EmailRequest containing recipient and prompt
        session: Database session dependency
        
    Returns:
        EmailResponse: Contains subject, content, recipient, and status
        
    Raises:
        HTTPException: If email generation or sending fails
    """
    try:
        # Generate email content using AI
        email_data = generate_email_message(request.prompt)
        
        # Send the email via SMTP
        send_mail(
            subject=email_data.subject,
            content=email_data.content,
            to_email=request.recipient
        )
        
        # Save successful email to database
        email_record = EmailHistory(
            recipient=request.recipient,
            subject=email_data.subject,
            content=email_data.content,
            prompt=request.prompt,
            status="sent"
        )
        session.add(email_record)
        session.commit()
        
        return EmailResponse(
            subject=email_data.subject,
            content=email_data.content,
            recipient=request.recipient,
            status="sent"
        )
        
    except Exception as e:
        # Log failed attempt to database for tracking
        email_record = EmailHistory(
            recipient=request.recipient,
            subject="Failed to generate",
            content=str(e),
            prompt=request.prompt,
            status="failed"
        )
        session.add(email_record)
        session.commit()
        
        raise HTTPException(status_code=500, detail=f"Failed to send email: {str(e)}")


@router.get("/history", response_model=List[EmailHistoryResponse], tags=["Email"])
def get_email_history(
    limit: int = 10,
    session: Session = Depends(get_session)
):
    """Retrieve email history with pagination.
    
    Fetches the most recent emails from the database, ordered by creation date.
    
    Args:
        limit: Maximum number of emails to return (default: 10)
        session: Database session dependency
        
    Returns:
        List[EmailHistoryResponse]: List of email history records
    """
    # Query emails ordered by most recent first
    query = select(EmailHistory).order_by(EmailHistory.created_at.desc()).limit(limit)
    results = session.exec(query).all()
    return results


@router.post("/draft", tags=["Email"])
def draft_email(request: EmailRequest):
    """Generate an email draft without sending.
    
    Creates an email draft using AI that can be edited before sending.
    The draft is not saved to database or sent.
    
    Args:
        request: EmailRequest containing recipient and prompt
        
    Returns:
        dict: Draft email with subject, content, and recipient
        
    Raises:
        HTTPException: If draft generation fails
    """
    try:
        # Generate email content using AI
        email_data = generate_email_message(request.prompt)
        return {
            "subject": email_data.subject,
            "content": email_data.content,
            "recipient": request.recipient
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate draft: {str(e)}")


@router.post("/send-draft", response_model=EmailResponse, tags=["Email"])
def send_edited_draft(
    request: SendDraftRequest,
    session: Session = Depends(get_session)
):
    """Send a user-edited draft email.
    
    Sends an email with manually edited subject and content.
    Used after user modifies an AI-generated draft.
    
    Args:
        request: SendDraftRequest with recipient, subject, and content
        session: Database session dependency
        
    Returns:
        EmailResponse: Contains subject, content, recipient, and status
        
    Raises:
        HTTPException: If email sending fails
    """
    try:
        # Send the edited email via SMTP
        send_mail(
            subject=request.subject,
            content=request.content,
            to_email=request.recipient
        )
        
        email_record = EmailHistory(
            recipient=request.recipient,
            subject=request.subject,
            content=request.content,
            prompt="Edited draft",
            status="sent"
        )
        session.add(email_record)
        session.commit()
        
        return EmailResponse(
            subject=request.subject,
            content=request.content,
            recipient=request.recipient,
            status="sent"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send draft: {str(e)}")