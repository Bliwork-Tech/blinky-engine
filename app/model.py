from typing import Dict, Optional
from pydantic import BaseModel

class WhatsAppMessage(BaseModel):
    Body: str
    From: str
    To: str
    Context: Optional[Dict[str, str]]
