from fastapi import APIRouter
from app.api.endpoints import health, validation

api_router = APIRouter()

api_router.include_router(
    health.router,
    prefix="/health",
    tags=["health"]
)

api_router.include_router(
    validation.router,
    prefix="/validation",
    tags=["validation"]
)