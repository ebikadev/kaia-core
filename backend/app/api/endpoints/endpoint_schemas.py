"""(API endpoints)
    Endpoint for creating schemas
    This file:
    ✔ receives HTTP requests
    ✔ converts JSON to Python objects
    ✔ calls services
    Returns:
           What does this endpoint do?
           Allows creating a table schema from an HTTP request.
           
           Endpoint:           
           POST /schema
           Example request:

                  {
                    "table_name": "customers",
                    "columns": [
                      {
                        "name": "id",
                        "datatype": "integer",
                        "required": true,
                        "unique": true
                      },
                      {
                        "name": "email",
                        "datatype": "string",
                        "required": true,
                        "unique": true
                      }
                    ]
                  }
          The route receives it and creates an object:
          TableSchema
"""
from fastapi import APIRouter
from app.models.table_schema import TableSchema
from app.services.schema_service import create_schema, schemas_db

router = APIRouter()

@router.post("/")
def create_table_schema(schema: TableSchema):
    return create_schema(schema)

@router.get("/")
def list_schemas():
    return list(schemas_db.keys())
"""
[
 "customers",
 "exchange_rates",
 "products"
]
"""
