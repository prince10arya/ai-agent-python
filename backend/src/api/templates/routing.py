"""Email template routing."""

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List

from .models import EmailTemplate, TemplateRequest, TemplateResponse
from api.db import get_session

router = APIRouter()


@router.get("/", response_model=List[TemplateResponse], tags=["Templates"])
def get_templates(
    category: str = None,
    session: Session = Depends(get_session)
):
    """Get all email templates, optionally filtered by category."""
    query = select(EmailTemplate)
    if category:
        query = query.where(EmailTemplate.category == category)
    templates = session.exec(query).all()
    return templates


@router.post("/", response_model=TemplateResponse, tags=["Templates"])
def create_template(
    template: TemplateRequest,
    session: Session = Depends(get_session)
):
    """Create a new custom email template."""
    db_template = EmailTemplate(
        name=template.name,
        category=template.category,
        subject=template.subject,
        content=template.content,
        is_predefined=False
    )
    session.add(db_template)
    session.commit()
    session.refresh(db_template)
    return db_template


@router.delete("/{template_id}", tags=["Templates"])
def delete_template(
    template_id: int,
    session: Session = Depends(get_session)
):
    """Delete a custom template."""
    template = session.get(EmailTemplate, template_id)
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    if template.is_predefined:
        raise HTTPException(status_code=400, detail="Cannot delete predefined templates")
    session.delete(template)
    session.commit()
    return {"message": "Template deleted"}


@router.post("/seed", tags=["Templates"])
def seed_predefined_templates(session: Session = Depends(get_session)):
    """Seed predefined templates."""
    predefined = [
        {
            "name": "Follow-up Email",
            "category": "follow-up",
            "subject": "Following Up on Our Previous Conversation",
            "content": "Hi [Name],\n\nI wanted to follow up on our previous conversation regarding [Topic]. I hope this message finds you well.\n\n[Your message here]\n\nLooking forward to hearing from you.\n\nBest regards"
        },
        {
            "name": "Thank You Email",
            "category": "thank-you",
            "subject": "Thank You",
            "content": "Dear [Name],\n\nThank you for [Reason]. I truly appreciate your time and consideration.\n\n[Additional message]\n\nWarm regards"
        },
        {
            "name": "Meeting Request",
            "category": "meeting-request",
            "subject": "Meeting Request - [Topic]",
            "content": "Hi [Name],\n\nI would like to schedule a meeting to discuss [Topic]. Would you be available for a [Duration] meeting sometime this week?\n\nPlease let me know your availability.\n\nBest regards"
        }
    ]
    
    for template_data in predefined:
        existing = session.exec(
            select(EmailTemplate).where(EmailTemplate.name == template_data["name"])
        ).first()
        if not existing:
            template = EmailTemplate(**template_data, is_predefined=True)
            session.add(template)
    
    session.commit()
    return {"message": "Predefined templates seeded"}
