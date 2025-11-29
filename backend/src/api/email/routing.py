from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List

from .models import EmailRequest, EmailResponse, EmailHistory, EmailHistoryResponse
from api.db import get_session
from api.ai.services import generate_email_message
from api.myemailer.sender import send_mail
from pydantic import BaseModel

class SendDraftRequest(BaseModel):
    recipient: str
    subject: str
    content: str

router = APIRouter()


@router.get("/", tags=["Email"])
def email_health():
    return {"status": "ok", "service": "email"}


@router.post("/send", response_model=EmailResponse, tags=["Email"])
def send_email(
    request: EmailRequest,
    session: Session = Depends(get_session)
):
    """Generate and send an email based on user prompt"""
    try:
        # Generate email content using AI
        email_data = generate_email_message(request.prompt)
        
        # Send the email
        send_mail(
            subject=email_data.subject,
            content=email_data.content,
            to_email=request.recipient
        )
        
        # Save to database
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
        # Save failed attempt to database
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
    """Get email history"""
    query = select(EmailHistory).order_by(EmailHistory.created_at.desc()).limit(limit)
    results = session.exec(query).all()
    return results


@router.post("/draft", tags=["Email"])
def draft_email(request: EmailRequest):
    """Generate email draft without sending"""
    try:
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
    """Send an edited draft email"""
    try:
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