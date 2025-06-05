import os
from twilio.rest import Client

class TwilioSender:
    def __init__(self, sid: str = None, token: str = None, from_whatsapp: str = None):
        self.sid = sid or os.getenv("TWILIO_ACCOUNT_SID")
        self.token = token or os.getenv("TWILIO_AUTH_TOKEN")
        self.from_whatsapp = from_whatsapp or os.getenv("TWILIO_WHATSAPP_FROM")
        self.client = Client(self.sid, self.token)

    def send_whatsapp(self, to: str, body: str):
        """Envía un mensaje de WhatsApp usando Twilio API"""
        message = self.client.messages.create(
            from_=self.from_whatsapp,
            to=to,
            body=body
        )
        return message.sid  # SID
