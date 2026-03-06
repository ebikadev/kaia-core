from fastapi import APIRouter, UploadFile, File
from app.services.csv_validator import validate_csv
from app.schemas.validation_schema import ValidationResult

router = APIRouter()

@router.post("/", response_model=ValidationResult)
async def validate_file(file: UploadFile = File(...)):

    result = await validate_csv(file)

    return result