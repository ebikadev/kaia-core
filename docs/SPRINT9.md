# 🚀 KAIA CORE — SPRINT 9
## Schema-based Data Storage

En este sprint se agregó la capacidad de **insertar y consultar datos dentro de tablas dinámicas previamente definidas mediante schemas**.

Esto transforma a **Kaia Core** en una plataforma que no solo valida archivos, sino que también permite:

- Crear **tablas dinámicas**
- Insertar registros
- Consultar registros
- Validar que la tabla exista antes de insertar datos

Esta arquitectura sigue el patrón:

```
API → Service → Repository
```

---

# 🧠 Objetivo del Sprint

Permitir que los usuarios:

1. **Creen un schema de tabla**
2. **Inserten registros en esa tabla**
3. **Consulten los registros almacenados**

Antes de insertar un registro, el sistema valida que:

- **El schema exista**

Si el schema no existe, el sistema devuelve un error.

---

# 🧱 Arquitectura

El flujo completo del sistema queda así:

```
Client
   │
   ▼
FastAPI Endpoint
   │
   ▼
Service Layer
   │
   ▼
Repository Layer
   │
   ▼
Data Storage (In-memory)
```

### Responsabilidad de cada capa

**API Layer**

- Define endpoints
- Recibe requests HTTP

**Service Layer**

- Aplica reglas de negocio
- Verifica que el schema exista

**Repository Layer**

- Inserta y obtiene datos

---

# 📁 Archivos involucrados

```
backend/app/

api/endpoints/
    tables.py

services/
    services_data.py
    services_schema.py

repositories/
    data_repository.py

models/
    table_schema.py
```

---

# 🧩 Service Layer — services_data.py

Archivo:

```
backend/app/services/services_data.py
```

Este servicio se encarga de:

- Validar que la tabla exista
- Insertar registros
- Obtener registros

Código actual:

```python
"""
Service layer for handling table data operations.

This verifies that the schema exists and then calls the data repository
to insert or retrieve records.
"""

from app.repositories.data_repository import insert_row, get_rows
from app.services.services_schema import get_schema


def insert_record(table_name: str, row: dict):

    schema = get_schema(table_name)

    if not schema:
        raise ValueError("Table does not exist")

    return insert_row(table_name, row)


def get_records(table_name: str):

    return get_rows(table_name)
```

---

# 🔍 Explicación del flujo

Cuando se intenta insertar un registro:

```
API
 ↓
insert_record()
 ↓
get_schema()
 ↓
if schema not exists → error
 ↓
insert_row()
```

Esto asegura que **solo se puedan insertar datos en tablas válidas**.

---

# 🧩 API Layer — tables.py

Archivo:

```
backend/app/api/endpoints/tables.py
```

Este archivo define los endpoints para:

- Crear schemas
- Listar schemas
- Insertar registros
- Consultar registros

Código actual:

```python
from fastapi import APIRouter

from app.models.table_schema import TableSchema
from app.services.services_schema import create_schema, list_schemas
from app.services.services_data import insert_record, get_records

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
```

---

# 🧪 Pruebas de la API

Ejecutar la API:

```
uvicorn app.main:app --reload
```

Swagger estará disponible en:

```
http://127.0.0.1:8000/docs
```

---

# 🧪 Crear un Schema

Endpoint

```
POST /schemas
```

Body de ejemplo

```json
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
```

Respuesta esperada

```json
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
```

---

# 🧪 Listar tablas

Endpoint

```
GET /schemas
```

Respuesta

```json
[
  "customers",
  "countries"
]
```

---

# 🧪 Insertar datos en una tabla

Endpoint

```
POST /data/countries
```

Body

```json
{
  "id": 1,
  "name": "Argentina"
}
```

Flujo interno:

```
Endpoint
 ↓
insert_record()
 ↓
get_schema()
 ↓
insert_row()
```

Respuesta

```json
{
  "id": 1,
  "name": "Argentina"
}
```

---

# 🧪 Insertar otro registro

```
POST /data/countries
```

```json
{
  "id": 25,
  "name": "Peru"
}
```

---

# 🧪 Obtener registros

Endpoint

```
GET /data/countries
```

Respuesta esperada

```json
[
  {
    "id": 1,
    "name": "Argentina"
  },
  {
    "id": 25,
    "name": "Peru"
  }
]
```

---

# ❗ Manejo de errores

Si se intenta insertar datos en una tabla que **no existe**, el sistema devuelve error.

Ejemplo:

```
POST /data/products
```

Respuesta:

```
ValueError: Table does not exist
```

Esto protege la integridad de los datos.

---

# 🚀 Valor del Sprint

Con este sprint **Kaia Core ahora puede funcionar como un mini Data Platform**.

Permite:

✔ Definir estructuras de datos  
✔ Insertar registros  
✔ Consultar datasets  
✔ Validar existencia de tablas  

Esto es la base para funcionalidades futuras como:

- Validación de datos por tipo
- Upload de CSV
- Integración con BigQuery
- Data contracts

---

# 🔮 Próximo Sprint (SPRINT 10)

En el próximo sprint se agregará:

### Validación de columnas

Antes de insertar un registro se validará que:

- Las columnas existan en el schema
- El tipo de dato sea correcto

Ejemplo:

```
schema:
id → integer
name → string
```

Si se intenta insertar:

```
{
"id": "ABC"
}
```

El sistema devolverá error.

---

# 📌 Commit sugerido

```
feat: add schema-based data storage and retrieval
```

---

# ✅ Resultado

Después del Sprint 9 el sistema permite:

✔ Crear tablas dinámicas  
✔ Insertar registros  
✔ Consultar registros  
✔ Validar que la tabla exista  

Esto representa un paso importante hacia el objetivo de **Kaia Core como plataforma de validación y preparación de datos**.