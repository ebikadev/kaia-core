from fastapi import APIRouter, UploadFile, File, HTTPException

from app.models.table_schema import TableSchema
from app.services.schema_service import create_schema, list_schemas, get_schema
from app.services.data_service import insert_record, get_records, validate_csv_file
from app.validator.csv_validator import validate_csv
from app.services.validation_service import create_validation_report

router = APIRouter()


@router.post("/schemas")
def create_table(schema: TableSchema):
    return create_schema(schema)


@router.get("/schemas")
def get_tables():
    return list_schemas()


@router.post("/data/{table_name}")
def insert_data(table_name: str, row: dict):
    return insert_record(table_name, row)


@router.get("/data/{table_name}")
def read_data(table_name: str):
    return get_records(table_name)

@router.post("/data/{table_name}/upload")
async def upload_csv(table_name: str, file: UploadFile = File(...)):

    schema = get_schema(table_name)

    if not schema:
        raise HTTPException(status_code=404, detail="Table not found")

    # STEP 1 — validate csv
    validation_result = validate_csv(file, schema)

    # STEP 2 — create validation report
    report = create_validation_report(table_name, validation_result)

    return {
        "report_id": report.id,
        "validation": validation_result
    }