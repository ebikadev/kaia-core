"""
app/services/csv_validator.py

Advanced CSV Validation Engine
"""

import pandas as pd
import uuid
from typing import List, Dict

def autogen_uuid():
    return str(uuid.uuid4())

def validate_csv(file, schema):

    errors: List[Dict] = []
    invalid_rows: List[Dict] = []
    valid_rows: List[Dict] = []

    # -----------------------------------------------------------
    # STEP 1 — Read CSV
    # -----------------------------------------------------------

    try:
        df = pd.read_csv(file.file)
        df.columns = df.columns.str.strip()
    except Exception as e:
        return {
            "table": schema.table_name,
            "rows": 0,
            "errors": 1,
            "details": [
                {
                    "column": None,
                    "error": f"Error reading CSV file: {str(e)}"
                }
            ]
        }

    total_rows = len(df)

    schema_columns = [col.name for col in schema.columns]
    csv_columns = df.columns.tolist()

    # -----------------------------------------------------------
    # STEP 2 — Structure validation
    # -----------------------------------------------------------

    missing_columns = set(schema_columns) - set(csv_columns)

    for col in missing_columns:
        errors.append({
            "column": col,
            "error": "Missing required column in CSV"
        })

    unexpected_columns = set(csv_columns) - set(schema_columns)

    for col in unexpected_columns:
        errors.append({
            "column": col,
            "error": "Unexpected column found in CSV"
        })

    # -----------------------------------------------------------
    # STEP 3 — Row level validation
    # -----------------------------------------------------------

    for index, row in df.iterrows():

        row_errors = []
        clean_row = row.where(pd.notnull(row), None)

        for column in schema.columns:

            if column.name not in df.columns:
                continue

            value = row[column.name]

            # Required validation
            if column.required and pd.isna(value):
                row_errors.append(
                    f"{column.name} is required"
                )

            # Datatype validation
            if column.datatype == "integer":

                try:
                    int(value)
                except:
                    row_errors.append(
                        f"{column.name} must be integer"
                    )

            elif column.datatype == "float":

                try:
                    float(value)
                except:
                    row_errors.append(
                        f"{column.name} must be float"
                    )

            elif column.datatype == "string":

                if not isinstance(value, str) and not pd.isna(value):
                    row_errors.append(
                        f"{column.name} must be string"
                    )

        if row_errors:

            invalid_rows.append({
                "row_number": index + 1,
                "errors": row_errors,
                "row": clean_row.to_dict()
            })

        else:
            valid_rows.append(clean_row.to_dict())

    # -----------------------------------------------------------
    # STEP 4 — Unique validation
    # -----------------------------------------------------------

    for column in schema.columns:

        if not column.unique:
            continue

        if column.name not in df.columns:
            continue

        duplicates = df[df[column.name].duplicated()][column.name]

        if not duplicates.empty:

            errors.append({
                "column": column.name,
                "error": f"Duplicate values detected",
                "values": duplicates.tolist()
            })

    # -----------------------------------------------------------
    # STEP 5 — Final report
    # -----------------------------------------------------------

    result = {

        "id": autogen_uuid(),

        "table": schema.table_name,

        "timestamp": pd.Timestamp.now().isoformat(),

        "rows": total_rows,

        "rows_analyzed": total_rows,

        "valid_rows": len(valid_rows),

        "invalid_rows": len(invalid_rows),

        "schema_errors": errors,

        "row_errors": invalid_rows,

        "preview_valid_rows": valid_rows[:10]

    }

    return result