# Entrypoint del backend.
from fastapi import FastAPI
from app.api.router import api_router

app = FastAPI(
    title="Kaia Data Validator",
    version="0.1"
)

app.include_router(api_router)

@app.get("/")
def root():
    return {"message": "Kaia API running"}