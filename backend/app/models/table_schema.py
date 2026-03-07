"""
Este archivo define cómo se representa una tabla dentro del sistema.
Permite representar estructuras como:

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

from pydantic import BaseModel
from typing import List


class ColumnSchema(BaseModel):
    name: str
    datatype: str
    required: bool = False
    unique: bool = False


class TableSchema(BaseModel):
    table_name: str
    columns: List[ColumnSchema]