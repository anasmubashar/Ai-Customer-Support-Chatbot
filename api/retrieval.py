from langchain_text_splitters.character import CharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores.faiss import FAISS
from langchain.embeddings.base import Embeddings
from .config import KNOWLEDGE_BASE_PATH, GOOGLE_API_KEY
import os
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
import google.generativeai as genai

GOOGLE_API_KEY = os.environ["NEXT_PUBLIC_GEMINI_KEY"]

def retrieval(user_input):
    # Load documents
    loader = TextLoader(KNOWLEDGE_BASE_PATH)
    documents = loader.load()
    
    # Split documents into chunks
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    texts = text_splitter.split_documents(documents)
    
    # Initialize the embeddings class with the correct model name
    embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004", google_api_key=GOOGLE_API_KEY)
    
    # Create a vector database
    vector_db = FAISS.from_documents(texts, embeddings)
    
    # Create a retriever
    retriever = vector_db.as_retriever(search_kwargs={"k": 5})
    
    # Define the prompt template
    template = """
    You are a helpful AI assistant for coding interviews.
    Answer based on the context provided.
    Keep answers short and do not return text between asterisks ().
    context: {context}
    input: {input}
    answer:
    """

    
    # Create a prompt
    prompt = PromptTemplate.from_template(template)
    
    # Create a chain for combining documents
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=GOOGLE_API_KEY)
    combine_docs_chain = create_stuff_documents_chain(llm, prompt)
    
    # Retrieve relevant documents
    relevant_docs = retriever.get_relevant_documents(user_input)
    
    # Invoke the chain with the user input and relevant documents
    answer = combine_docs_chain.invoke({"input": user_input, "context": relevant_docs})
    
    return answer

# Example usage
# # user_input = "Find the Maximum Element in an Array"
# answer = retrieval(user_input)
# print(answer)