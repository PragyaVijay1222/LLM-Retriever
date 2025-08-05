import os
from dotenv import load_dotenv

load_dotenv() 

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENV = os.getenv("PINECONE_ENV", "us-west1-gcp")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "llm-policy-index")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
