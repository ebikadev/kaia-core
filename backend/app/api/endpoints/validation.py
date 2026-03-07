from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.csv_validator import validate_csv
from app.services.schema_service import save_schema
from app.schemas.validation_result import ValidationResult
from app.services.schema_service import get_schema

router = APIRouter()


@router.post("/{table_name}")
async def validate_file(table_name: str, file: UploadFile = File(...)):

    # Buscar schema
    schema = get_schema(table_name)

    if not schema:
        raise HTTPException(
            status_code=404,
            detail=f"Schema '{table_name}' not found"
        )

    # Ejecutar validador
    result = validate_csv(file, schema)

    return result