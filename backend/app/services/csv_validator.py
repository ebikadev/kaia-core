import pandas as pd
from typing import Dict, Any

async def validate_csv(file):

    df = pd.read_csv(file.file)

    result = {
        "valid": True,
        "row_count": len(df),
        "columns_detected": list(df.columns),
        "missing_columns": [],
        "unexpected_columns": [],
        "null_values": {}
    }

    EXPECTED_COLUMNS = [
        "id",
        "name",
        "email",
        "created_at"
    ]

    missing_columns = []

    for column in EXPECTED_COLUMNS:
        if column not in df.columns:
            missing_columns.append(column)

    unexpected_columns = []

    for column in df.columns:
        if column not in EXPECTED_COLUMNS:
            unexpected_columns.append(column)

    null_values = {}

    for column in df.columns:
        null_count = df[column].isnull().sum()

        if null_count > 0:
            null_values[column] = int(null_count)

    result = {
        "valid": len(missing_columns) == 0,
        "row_count": len(df),
        "columns_detected": list(df.columns),
        "missing_columns": missing_columns,
        "unexpected_columns": unexpected_columns,
        "null_values": null_values
    }

    return result