""" services — The business logic
Here lives the real system logic.
This service will be responsible for:
    - saving schemas
    - retrieving schemas

That dictionary is a temporary in-memory database.

schemas_db
Internal example:

    {
       "customers": TableSchema(...)
    }
This is temporary for development.

In future sprints we'll move it to:
BigQuery
Postgres
Firestore

"""

from typing import Dict
from app.models.table_schema import TableSchema
from app.validator.schema_validator import validate_schema

# Dictionary that acts as an in-memory database
schemas_db: Dict[str, TableSchema] = {}

def create_schema(schema: TableSchema):

    """
    Saves a table schema.
    """
    validate_schema(schema)

    schemas_db[schema.table_name] = schema

    print("Stored schemas:", schemas_db)

    return schema

def get_schema(table_name: str):
    """
    Gets the schema of a table.
    """
    return schemas_db.get(table_name)

def list_schemas():
    """
    Lists all registered tables.
    """
    return list(schemas_db.keys())