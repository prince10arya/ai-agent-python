
from pydantic import BaseModel, Field

class EmailMessage(BaseModel):
    subject: str
    content: str
    invalid_requests: bool | None = Field(default=False)


class AgentMessageSchema(BaseModel):
    content: str
    
