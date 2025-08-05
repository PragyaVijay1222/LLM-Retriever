from fastapi import FastAPI
from app.routers import retrieval

app = FastAPI()
app.include_router(retrieval.router)