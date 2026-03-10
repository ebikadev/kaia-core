"""
    Validation API endpoint.
    POST /validation/{table_name}
    This endpoint receives a CSV file and validates it against a specified table schema.
    The validation process includes:
    - Checking if the schema exists
    - Validating column structure
    - Validating required fields
    - Validating unique fields
    - Validating data types
    The endpoint returns a structured validation report with details on any errors found.
"""
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.validator.csv_validator import validate_csv
from app.schemas.validation_result import ValidationResult
from app.services.schema_service import get_schema

router = APIRouter()


@router.post("/{table_name}")
async def validate_file(table_name: str, file: UploadFile = File(...)):

    # Search for schema
    schema = get_schema(table_name)

    if not schema:
        raise HTTPException(
            status_code=404,
            detail=f"Schema '{table_name}' not found"
        )

    # Run validator
    result = validate_csv(file, schema)

    return result