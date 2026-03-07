"""
Este servicio se encargará de:

guardar schemas
recuperar schemas

El sistema utiliza un diccionario en memoria:

schemas_db
Ejemplo interno:

{
   "customers": TableSchema(...)
}
Esto es temporal para desarrollo.

En futuros sprints lo moveremos a:

BigQuery
Postgres
Firestore


"""

from typing import Dict
from app.models.table_schema import TableSchema

# Diccionario que actúa como base de datos en memoria
schemas_db: Dict[str, TableSchema] = {}


def create_schema(schema: TableSchema):
    """
    Guarda un schema nuevo.
    """
    schemas_db[schema.table_name] = schema
    return schema


def save_schema(schema):
    """
    Guarda un schema en memoria.
    """

    schemas_db[schema.table_name] = schema

    print("Schemas almacenados:", schemas_db)


def get_schema(table_name: str):
    """
    Obtiene un schema por nombre de tabla.
    """

    return schemas_db.get(table_name)