"""
Schema Validator

Validates table schemas before storing them in the system.
Ensures schema integrity.
"""

from app.models.table_schema import TableSchema


ALLOWED_TYPES = {"string", "integer", "float", "bool"}


def validate_schema(schema: TableSchema):
    """
    Validate the schema structure.
    """

    # Validate table name
    if not schema.table_name:
        raise ValueError("Table name cannot be empty")

    # Validate columns exist
    if not schema.columns:
        raise ValueError("Schema must contain at least one column")

    column_names = []

    for column in schema.columns:

        # Column name
        if not column.name:
            raise ValueError("Column name cannot be empty")

        # Duplicate columns
        if column.name in column_names:
            raise ValueError(f"Duplicate column '{column.name}' detected")

        column_names.append(column.name)

        # Validate datatype
        if column.datatype not in ALLOWED_TYPES:
            raise ValueError(
                f"Invalid datatype '{column.datatype}' for column '{column.name}'"
            )

"""
Schema Validator

Validates that a row of data respects the table schema rules.
"""

def validate_row(schema, row):

    errors = []

    columns = {col.name: col for col in schema.columns}

    # -----------------------------
    # Required fields validation
    # -----------------------------
    for column_name, column in columns.items():

        if column.required and column_name not in row:
            errors.append(f"{column_name} is required")

    # -----------------------------
    # Datatype validation
    # -----------------------------
    for key, value in row.items():

        if key not in columns:
            errors.append(f"{key} is not a valid column")
            continue

        datatype = columns[key].datatype

        if datatype == "integer" and not isinstance(value, int):
            errors.append(f"{key} must be integer")

        if datatype == "string" and not isinstance(value, str):
            errors.append(f"{key} must be string")

    return errors

def validate_unique(schema, row, existing_rows):

    errors = []

    unique_columns = [col.name for col in schema.columns if col.unique]

    for column in unique_columns:

        if column not in row:
            continue

        value = row[column]

        for existing in existing_rows:

            if existing.get(column) == value:
                errors.append(f"{column} must be unique")

    return errors