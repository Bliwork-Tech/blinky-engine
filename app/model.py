from pydantic import BaseModel

class WhatsAppMessage(BaseModel):
    Body: str
    From: str
    To: str
