from langchain_google_genai import GoogleGenerativeAI
from langchain.chains.retrieval_qa.base import RetrievalQA
from langchain.chains.question_answering import load_qa_chain
from .knowledge_base import get_vectorstore
from .config import GOOGLE_API_KEY

def get_qa_chain():
    llm = GoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=GOOGLE_API_KEY)
    vectorstore = get_vectorstore()
    
    # Create a chain to combine documents using the LLM
    combine_documents_chain = load_qa_chain(llm, chain_type="stuff")
    
    # Pass the combine_documents_chain and retriever to RetrievalQA
    qa_chain = RetrievalQA(
        combine_documents_chain=combine_documents_chain,
        retriever=vectorstore.as_retriever()
    )
    print(qa_chain)

    return qa_chain

def run_qa_chain(qa_chain: RetrievalQA , user_input):
    try:
        print(user_input)
        print(qa_chain.invoke(user_input))  # Change here
        # print(answer)
        # return answer
    except Exception as e:
        raise ValueError(f"Error running QA chain: {str(e)}")