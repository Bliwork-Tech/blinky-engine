from fastapi import FastAPI
from fastapi.responses import JSONResponse
from app.gpt import GPTHandler
from app.model import WhatsAppMessage
from app.conversation import conversation_handler
#from app.sender import TwilioSender
import os
from dotenv import load_dotenv
import pandas as pd

load_dotenv()

gpt_handler = GPTHandler(os.getenv("OPENAI_API_KEY"))
#twilio_sender = TwilioSender()
allowed_channels = ['whatsapp','http']
catalog_df = pd.read_csv("bliwork.csv")
products_cat_df = pd.read_csv("bliwork.csv")

app = FastAPI()

@app.post("/chatbot/{channel}")
async def whatsapp_webhook(channel: str, msg: WhatsAppMessage):
    print(f"Received message on channel {channel}: {msg}")
    user_msg = msg.Body
    from_number = msg.From

    if channel not in allowed_channels:
        return JSONResponse(status_code=403)
    
    reply = conversation_handler(catalog_df, products_cat_df, user_msg, gpt_handler)
    # Habilita enviar por canales o simplemente por http directo
    if channel == 'whatsapp':
        #twilio_sender.send_whatsapp(from_number, reply)
        reply = "ok"

    return JSONResponse(status_code=200, content={"message": reply})
