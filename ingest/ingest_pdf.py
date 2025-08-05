import os
import requests
import fitz  
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from pinecone import Pinecone
from tqdm import tqdm

load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")

pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index(PINECONE_INDEX_NAME)

# model = SentenceTransformer('all-MiniLM-L6-v2')
model = SentenceTransformer('BAAI/bge-base-en-v1.5')  

def chunk_text(text, chunk_size=500, overlap=50):
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunk = ' '.join(words[i:i + chunk_size])
        chunks.append(chunk)
    return chunks

def ingest_pdf_to_pinecone(pdf_url: str):
    response = requests.get(pdf_url)
    doc = fitz.open(stream=response.content, filetype="pdf")

    all_chunks = []
    for page_num, page in enumerate(doc, start=1):
        text = page.get_text()
        chunks = chunk_text(text)
        for chunk in chunks:
            all_chunks.append({
                "text": chunk,
                "page": page_num
            })
            
    batch_size = 20
    for i in tqdm(range(0, len(all_chunks), batch_size)):
        batch = all_chunks[i:i+batch_size]
        texts = [item['text'] for item in batch]
        metadatas = [{"text": item['text'], "page": item['page']} for item in batch]

        vectors = model.encode(texts, show_progress_bar=False, convert_to_numpy=True)
        ids = [f"chunk-{i+j}" for j in range(len(batch))]

        index.upsert(vectors=[(id, vector.tolist(), meta) for id, vector, meta in zip(ids, vectors, metadatas)])

if __name__ == "__main__":
    pdf_url = "https://hackrx.blob.core.windows.net/assets/policy.pdf?sv=2023-01-03&st=2025-07-04T09%3A11%3A24Z&se=2027-07-05T09%3A11%3A00Z&sr=b&sp=r&sig=N4a9OU0w0QXO6AOIBiu4bpl7AXvEZogeT%2FjUHNO7HzQ%3D"
    ingest_pdf_to_pinecone(pdf_url)
    print("Ingestion Completed.")
