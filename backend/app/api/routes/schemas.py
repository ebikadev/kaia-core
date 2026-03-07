"""Endpoint para crear schemas

    Returns:
           Qué hace este endpoint
           Permite crear un schema de tabla desde una petición HTTP.
           
           Endpoint:
           
           POST /schema
           Ejemplo de request:

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
"""
from fastapi import APIRouter
from app.models.table_schema import TableSchema
from app.services.schema_service import create_schema

router = APIRouter()

@router.post("/")
def create_table_schema(schema: TableSchema):
    return create_schema(schema)