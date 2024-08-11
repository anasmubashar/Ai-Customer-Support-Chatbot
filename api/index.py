from fastapi import FastAPI, HTTPException
from .models import ChatRequest
from .qa_chain import get_qa_chain, run_qa_chain
from .utils import generate_analysis_and_tips
from .retrieval import retrieval
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
qa_chain = get_qa_chain()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for now, adjust this in production
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

@app.post("/api/chat")
async def chat(request: ChatRequest):
    try:
        # run_qa_chain(qa_chain, request.user_input)

        # print(answer)
        answer = retrieval(request.user_input)
        analysis, tips = generate_analysis_and_tips(request.user_input)
        return {
            "question_analysis": analysis,
            "answer": answer,
            "tips": tips
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# chat(ChatRequest(user_input="What is a linked list?"))