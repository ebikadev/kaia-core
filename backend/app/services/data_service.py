"""
Service layer for handling table data operations.

This verifies that the schema exists and then calls the data repository
to insert or retrieve records.
Tip profesional de APIs

Las APIs REST deben usar códigos HTTP correctos:
Código	Significado
200	OK
201	Created
400	Bad Request
404	Resource Not Found
500	Server Error
"""
from fastapi import HTTPException

from app.services.csv_service import parse_csv
from app.repositories.data_repository import insert_row, get_rows
from app.services.schema_service import get_schema
from app.validator.schema_validator import validate_row, validate_unique
from app.validator.csv_validator import validate_csv
from app.services.validation_service import create_validation_report


def insert_record(table_name: str, row: dict):

    schema = get_schema(table_name)

    if not schema:
        raise HTTPException(
            status_code=404,
            detail="Table does not exist"
        )

    # validate structure
    errors = validate_row(schema, row)

    if errors:
        raise HTTPException(
            status_code=422,
            detail={"validation_errors": errors}
        )

    # validate unique constraints
    existing_rows = get_rows(table_name)

    unique_errors = validate_unique(schema, row, existing_rows)

    if unique_errors:
        raise HTTPException(
            status_code=422,
            detail={"validation_errors": unique_errors}
        )

    return insert_row(table_name, row)


def get_records(table_name: str):

    return get_rows(table_name)

def insert_many_records(table_name: str, rows: list):

    results = []

    for row in rows:
        result = insert_record(table_name, row)
        results.append(result)

    return results

def validate_csv_file(table_name: str, file_content: str):

    schema = get_schema(table_name)

    if not schema:
        raise HTTPException(
            status_code=404,
            detail="Table does not exist"
        )

    rows = parse_csv(file_content)

    result = validate_csv(file_content, schema)

    return result

def ingest_csv(table_name: str, file):

    schema = get_schema(table_name)

    validation = validate_csv(file, schema)

    report = create_validation_report(table_name, validation)

    inserted = []

    for row in validation["preview_valid_rows"]:

        inserted.append(insert_record(table_name, row))

    return {
        "validation_report_id": report.id,
        "inserted_rows": inserted,
        "invalid_rows": validation["row_errors"]
    }