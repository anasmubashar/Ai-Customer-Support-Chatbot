from langchain_community.vectorstores import FAISS
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain.embeddings.base import Embeddings
from RAG.config import KNOWLEDGE_BASE_PATH, GOOGLE_API_KEY
import google.generativeai as genai

class GeminiEmbeddings(Embeddings):
    def __init__(self, api_key):
        genai.configure(api_key=api_key)
        self.model = "models/text-embedding-004"

    def embed_documents(self, texts):
        return [self.embed_query(text) for text in texts]

    def embed_query(self, text):
        result = genai.embed_content(
            model=self.model,
            content=text,
            task_type="retrieval_document",
            title="Embedding"
        )
        return result['embedding']

def get_vectorstore():
    loader = TextLoader(KNOWLEDGE_BASE_PATH)
    documents = loader.load()
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    texts = text_splitter.split_documents(documents)
    embeddings = GeminiEmbeddings(GOOGLE_API_KEY)
    vectorstore = FAISS.from_documents(texts, embeddings)
    return vectorstore