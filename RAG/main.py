from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv('.env.local')

app = FastAPI()

# Configure Google Gemini
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')

class ChatRequest(BaseModel):
    user_input: str

@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        chat = model.start_chat(
            history=[
                {"role": "user", "parts": "Hello"},
                {"role": "model", "parts": "Great to meet you. What would you like to know?"},
            ]
        )
        chat_response = chat.send_message(request.user_input)
        return {"response": chat_response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
