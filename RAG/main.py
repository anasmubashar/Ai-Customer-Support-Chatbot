from fastapi import FastAPI, HTTPException
from RAG.models import ChatRequest
from RAG.qa_chain import get_qa_chain
from RAG.utils import generate_analysis_and_tips

app = FastAPI()
qa_chain = get_qa_chain()

@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        answer = qa_chain.run(request.user_input)
        analysis, tips = generate_analysis_and_tips(request.user_input)
        return {
            "question_analysis": analysis,
            "answer": answer,
            "tips": tips
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))