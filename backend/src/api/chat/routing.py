from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from typing import List

from .models import ChatMessagePayLoad, ChatMessage, ChatMessageListItem
from api.db import get_session
from api.ai.services import generate_email_message
from api.ai.schemas import EmailMessage
router = APIRouter()

@router.get("/")
def chat_health():
    return {"status": "ok"}



@router.get("/recent/", response_model=List[ChatMessageListItem])
def chat_list_messages(session: Session = Depends(get_session)):
    """
    docstring
    """
    query = select(ChatMessage) #* sql -> query
    results = session.exec(query).fetchall()[:10]
    return results




@router.post("/", response_model=EmailMessage)
def chat_create_message(
    payload: ChatMessagePayLoad,
    session: Session = Depends(get_session)
):
    """
    docstring
    """
    data = payload.model_dump()
    print(data)
    obj = ChatMessage.model_validate(data)
    session.add(obj)
    session.commit()
    #* session.refresh(obj) #* ensure id/primary key added to the obj instance

    #* ready to store in the database
    response = generate_email_message(payload.message)

    return response
