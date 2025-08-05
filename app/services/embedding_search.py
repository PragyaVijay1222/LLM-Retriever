from pinecone import Pinecone
from langchain_community.vectorstores import Pinecone as PineconeVectorDB
from app.utils.config import PINECONE_API_KEY, PINECONE_INDEX_NAME
from sentence_transformers import SentenceTransformer

pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index(PINECONE_INDEX_NAME)

model = SentenceTransformer('BAAI/bge-base-en-v1.5')  

def search_similar_chunks(query: str, top_k: int = 5):
    query_vector = model.encode(query).tolist()
    results = index.query(vector=query_vector, top_k=top_k, include_metadata=True)
    return results['matches']