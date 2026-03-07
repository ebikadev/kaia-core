# Entrypoint del backend.
from fastapi import FastAPI
from app.api.router import api_router
from app.api.routes import schemas

app = FastAPI(
    title="Kaia",
    version="0.1"
)

app.include_router(api_router)

@app.get("/")
def root():
    return {"message": "Kaia API running"}