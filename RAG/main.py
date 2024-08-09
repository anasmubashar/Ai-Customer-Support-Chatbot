from fastapi import FastAPI, HTTPException
import requests

app = FastAPI()

@app.post("/chat")
async def chat(user_input: str):
    response = requests.post("https://api.google.com/gemini", json={"prompt": user_input})
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Google Gemini API error")
    prompt_response = response.json()

    # Call LangChain for RAG
    langchain_response = requests.post("http://localhost:8000/langchain", json={"prompt": prompt_response['result']})
    if langchain_response.status_code != 200:
        raise HTTPException(status_code=langchain_response.status_code, detail="LangChain error")

    return langchain_response.json()
