""" 
    Backend API entrypoint.
    This file starts the server.
    Charge all routes from app/api/router.py, which includes all endpoint routers.

    Executing this file will start the API server and make the endpoints available.
    To run the server:
        uvicorn app.main:app --reload
    The --reload flag is for development and will auto-restart the server on code changes.
    The API will be available at http://localhost:8000 by default.
    It will have the following endpoints:
        GET / - root endpoint, returns a welcome message
        GET /health - returns API status
        POST /validation/{table_name} - validates an uploaded CSV file against a specified schema
        POST /schemas - creates a new table schema
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.router import router

app = FastAPI(
    title="Kaia Core Platform",
    version="0.1"
)

# Configure CORS to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (development only - restrict in production)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

app.include_router(router)