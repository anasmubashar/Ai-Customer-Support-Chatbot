import uvicorn
from fastapi import FastAPI, HTTPException
from RAG.models import ChatRequest
from RAG.qa_chain import get_qa_chain
from RAG.utils import generate_analysis_and_tips
from RAG.retrieval import retrieval


app = FastAPI()

qa_chain = get_qa_chain()

@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        answer = retrieval(request.user_input)
        analysis, tips = generate_analysis_and_tips(request.user_input)
        return {
            "question_analysis": analysis,
            "answer": answer,
            "tips": tips
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("RAG.main:app", host="127.0.0.1", port=8000, reload=True)