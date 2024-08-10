from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores.faiss import BaseFaiss, Faiss
from langchain.embeddings.base import Embeddings
from RAG.config import KNOWLEDGE_BASE_PATH, GOOGLE_API_KEY
import google.generativeai as genai
import numpy as np

class CustomFaiss(BaseFaiss):
    @classmethod
    def from_documents(cls, documents, embeddings, ids=None, **kwargs):
        if not isinstance(embeddings[0], np.ndarray):
            embeddings = [np.array(embedding) for embedding in embeddings]
        return super().from_documents(documents, embeddings, ids=ids, **kwargs)

class CustomFaissVectorstore(Faiss):
    @classmethod
    def from_documents(cls, documents, embeddings, ids=None, **kwargs):
        return cls(CustomFaiss(embeddings), **kwargs)

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
            return [result['embedding'] for _ in texts]
        else:
            raise KeyError("The response does not contain 'embedding' key.")

    def embed_query(self, text):
        result = genai.embed_content(
            model=self.model,
            content=[text],  # Wrap single text in a list
            task_type="retrieval_document",
            title="Embedding"
        )
        return result['embeddings'][0]  # Return the first (and only) embedding

def get_vectorstore():
    loader = TextLoader(KNOWLEDGE_BASE_PATH)
    documents = loader.load()
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    texts = text_splitter.split_documents(documents)
    embeddings = GeminiEmbeddings(GOOGLE_API_KEY)
    vectorstore = CustomFaissVectorstore.from_documents(texts, embeddings)
    return vectorstore