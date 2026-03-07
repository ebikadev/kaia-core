from fastapi import APIRouter
from app.api.endpoints import health, validation
from app.api.routes import schemas

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

api_router.include_router(
    schemas.router,
    prefix="/schemas",
    tags=["schemas"]
)