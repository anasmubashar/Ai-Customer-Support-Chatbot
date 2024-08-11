from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores.faiss import FAISS
from langchain.embeddings.base import Embeddings
from .config import KNOWLEDGE_BASE_PATH, GOOGLE_API_KEY
import google.generativeai as genai
import numpy as np

class GeminiEmbeddings(Embeddings):
    def __init__(self, api_key):
        genai.configure(api_key=api_key)
        self.model = "models/text-embedding-004"  # Updated model name

    def embed_documents(self, texts):
        result = genai.embed_content(
            model=self.model,
            content=texts,
            task_type="retrieval_document",
            title="Embedding"
        )
        if 'embedding' in result:
            return [np.array(embed) for embed in result['embedding']]  # Ensure embeddings are numpy arrays
        else:
            raise KeyError("The response does not contain 'embedding' key.")

    def embed_query(self, text):
        result = genai.embed_content(
            model=self.model,
            content=[text],  # Wrap single text in a list
            task_type="retrieval_document",
            title="Embedding"
        )
        if 'embedding' in result:
            return np.array(result['embedding'])  # Return the first (and only) embedding
        else:
            raise KeyError("The response does not contain 'embedding' key.")

def get_vectorstore():
    loader = TextLoader(KNOWLEDGE_BASE_PATH)
    documents = loader.load()
    # print(documents)
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    texts = text_splitter.split_documents(documents)
    
    embeddings = GeminiEmbeddings(GOOGLE_API_KEY)
    
    # Get embeddings for each text
    embedded_texts = embeddings.embed_documents([doc.page_content for doc in texts])
    
    # Create vectorstore from documents and embeddings
    vector_db = FAISS.from_documents(texts, embeddings)
    print(vector_db)
    return vector_db