from langchain_google_genai import GoogleGenerativeAI
from langchain.chains import RetrievalQA
from knowledge_base import get_vectorstore
from config import GOOGLE_API_KEY

def get_qa_chain():
    llm = GoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=GOOGLE_API_KEY)
    vectorstore = get_vectorstore()
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vectorstore.as_retriever()
    )
    return qa_chain