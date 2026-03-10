from fastapi import APIRouter
from app.api.endpoints import endpoint_health, endpoint_data, endpoint_validation, tables
from app.api.endpoints import validation_reports

router = APIRouter()

router.include_router(
    endpoint_health.router,
    prefix="/health",
    tags=["health"]
)

router.include_router(
    endpoint_validation.router,
    prefix="/validation",
    tags=["validation"]
)

router.include_router(
    tables.router,
    tags=["tables"]
)

router.include_router(
    endpoint_data.router,
    prefix="/data",
    tags=["data"]
)

router.include_router(validation_reports.router)