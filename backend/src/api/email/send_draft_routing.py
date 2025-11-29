from pydantic import BaseModel

class SendDraftRequest(BaseModel):
    recipient: str
    subject: str
    content: str