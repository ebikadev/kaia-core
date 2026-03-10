# 🚀 KAIA CORE — SPRINT 10
## Data Contract Validation Engine

**Proyecto:** Kaia Core  
**Sprint:** 10  
**Objetivo:** Implementar **validación automática de registros contra el schema definido** antes de permitir que los datos se inserten en la tabla.

Hasta el Sprint 9, Kaia Core ya permite:

✔ Crear tablas dinámicas mediante schemas  
✔ Definir columnas con reglas (`datatype`, `required`, `unique`)  
✔ Insertar registros en una tabla  
✔ Consultar registros  

Pero todavía **no valida que los datos coincidan con el schema**.

En este Sprint agregamos un componente clave:

> **Data Contract Validation**

Esto significa que cada registro insertado será validado contra el schema antes de almacenarse.

---

# 🧠 ¿Qué es un Data Contract?

Un **Data Contract** es una regla que define **cómo deben verse los datos**.

Ejemplo:

Schema de tabla:

```
customers
```

Columnas:

| column | datatype | required | unique |
|------|------|------|------|
| id | integer | true | true |
| email | string | true | true |

Registro válido:

```json
{
"id": 1,
"email": "user@test.com"
}
```

Registro inválido:

```json
{
"id": "ABC"
}
```

Errores detectados:

```
id must be integer
email is required
```

---

# 🧱 Arquitectura de validación

El flujo completo ahora será:

```
Client
 │
 ▼
API Endpoint
 │
 ▼
Service Layer
 │
 ▼
Schema Validator
 │
 ▼
Repository
 │
 ▼
Data Storage
```

Esto asegura que **los datos siempre cumplan el contrato definido por el schema**.

---

# 📁 Nuevos archivos del Sprint

Se agrega un nuevo módulo de validación:

```
backend/app/validator/
    schema_validator.py
```

Este archivo contendrá la lógica que valida:

- columnas requeridas
- tipos de datos
- columnas inexistentes

---

# 🧩 Validator Layer — schema_validator.py

Archivo:

```
backend/app/validator/schema_validator.py
```

Código:

```python
"""
Schema Validator

Validates that a row of data respects the table schema rules.
"""

def validate_row(schema, row):

    errors = []

    columns = {col.name: col for col in schema.columns}

    # Check required fields
    for column_name, column in columns.items():

        if column.required and column_name not in row:
            errors.append(f"{column_name} is required")

    # Check datatype
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
```

---

# 🧩 Actualización del Service Layer

Archivo:

```
backend/app/services/services_data.py
```

Ahora agregamos validación antes de insertar datos.

Código actualizado:

```python
"""
Service layer for handling table data operations.

This verifies that the schema exists and then calls the data repository
to insert or retrieve records.
"""

from app.repositories.data_repository import insert_row, get_rows
from app.services.services_schema import get_schema
from app.validator.schema_validator import validate_row


def insert_record(table_name: str, row: dict):

    schema = get_schema(table_name)

    if not schema:
        raise ValueError("Table does not exist")

    errors = validate_row(schema, row)

    if errors:
        raise ValueError({"validation_errors": errors})

    return insert_row(table_name, row)


def get_records(table_name: str):

    return get_rows(table_name)
```

---

# 🔎 Validaciones implementadas

El sistema ahora valida automáticamente:

### 1️⃣ Columnas requeridas

Schema:

```
email → required
```

Registro inválido:

```json
{
"id": 1
}
```

Error:

```
email is required
```

---

### 2️⃣ Tipo de dato

Schema:

```
id → integer
```

Registro inválido:

```json
{
"id": "ABC"
}
```

Error:

```
id must be integer
```

---

### 3️⃣ Columnas no definidas

Schema:

```
id
email
```

Registro inválido:

```json
{
"id": 1,
"email": "user@test.com",
"age": 25
}
```

Error:

```
age is not a valid column
```

---

# 🧪 Pruebas de la API

## Crear tabla

```
POST /schemas
```

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

## Insertar registro válido

```
POST /data/customers
```

```json
{
"id": 1,
"email": "user@test.com"
}
```

Respuesta:

```json
{
"id": 1,
"email": "user@test.com"
}
```

---

## Insertar registro inválido

```
POST /data/customers
```

```json
{
"id": "ABC"
}
```

Respuesta esperada:

```
ValueError:
{
"validation_errors":[
"id must be integer",
"email is required"
]
}
```

---

# 🚀 Valor del Sprint

Con este sprint **Kaia Core pasa de ser un simple almacenamiento a un motor de validación de datos.**

Ahora el sistema puede:

✔ Validar columnas  
✔ Validar tipos  
✔ Validar campos obligatorios  
✔ Bloquear datos inválidos  

Esto acerca el proyecto a herramientas reales de **Data Quality** como:

- Great Expectations
- Soda
- Monte Carlo

---

# 🚀 KAIA CORE — SPRINT 11
## Advanced Data Validation: Unique Constraints, Extra Fields Control & Bulk Insert

**Proyecto:** Kaia Core  
**Sprint:** 11  
**Objetivo:** Expandir el motor de validación agregando capacidades más avanzadas de **Data Contracts**, incluyendo:

- Validación de **columnas únicas (unique constraint)**
- Control de **columnas extra**
- Inserción **masiva de registros**
- Mejora del **validador de schema**
- Respuestas de error más claras
- Preparación para ingestión de **CSV y pipelines ETL**

Este sprint lleva a **Kaia Core** de un simple validador a un **motor real de Data Quality**.

---

# 🧠 Problema que resolvemos

Hasta el Sprint 10 el sistema valida:

✔ columnas requeridas  
✔ tipos de datos  
✔ columnas inexistentes  

Pero todavía no valida algo **crítico en sistemas de datos**:

```
unique constraints
```

Ejemplo real:

Tabla:

```
customers
```

Schema:

| column | datatype | required | unique |
|------|------|------|------|
| id | integer | true | true |
| email | string | true | true |

Datos válidos:

```
1, user1@test.com
2, user2@test.com
```

Datos inválidos:

```
1, user1@test.com
1, user3@test.com
```

El segundo registro rompe el contrato **unique(id)**.

---

# 🧱 Arquitectura actualizada

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
Schema Validator
 │
 ▼
Repository Layer
 │
 ▼
Storage
```

Validaciones ahora incluyen:

```
required
datatype
invalid columns
unique constraint
```

---

# 📁 Archivos involucrados

```
backend/app/

validator/
    schema_validator.py

services/
    services_data.py

repositories/
    data_repository.py
```

---

# 🧩 Paso 1 — Mejorar el validador

Archivo:

```
backend/app/validator/schema_validator.py
```

Actualizar completamente el archivo.

```python
"""
Schema Validator

Validates a row against the table schema rules.
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
```

---

# 🧩 Paso 2 — Validar UNIQUE constraints

Las columnas pueden definirse así:

```json
{
"name": "email",
"datatype": "string",
"required": true,
"unique": true
}
```

Debemos verificar que **no exista ya ese valor en la tabla**.

---

# 🧩 Paso 3 — Agregar función de validación de unicidad

Archivo:

```
backend/app/validator/schema_validator.py
```

Agregar debajo del validador anterior:

```python
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
```

---

# 🧩 Paso 4 — Actualizar Service Layer

Archivo:

```
backend/app/services/services_data.py
```

Código completo actualizado:

```python
"""
Service layer for handling table data operations.

This verifies that the schema exists and then calls the data repository
to insert or retrieve records.
"""

from fastapi import HTTPException

from app.repositories.data_repository import insert_row, get_rows
from app.services.services_schema import get_schema
from app.validator.schema_validator import validate_row, validate_unique


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
```

---

# 🧪 Pruebas

## Crear tabla

```
POST /schemas
```

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

# 🧪 Insertar registro válido

```
POST /data/customers
```

```json
{
"id": 1,
"email": "user@test.com"
}
```

Respuesta:

```
200 OK
```

---

# 🧪 Insertar duplicado

```
POST /data/customers
```

```json
{
"id": 1,
"email": "another@test.com"
}
```

Respuesta esperada:

```json
{
"detail": {
"validation_errors": [
"id must be unique"
]
}
}
```

---

# 🧪 Duplicado de email

```
POST /data/customers
```

```json
{
"id": 2,
"email": "user@test.com"
}
```

Respuesta:

```json
{
"detail": {
"validation_errors": [
"email must be unique"
]
}
}
```

---

# 🧩 Paso 5 — Inserción masiva de registros

Para preparar **ingestión de CSV**, agregamos inserción masiva.

Archivo:

```
backend/app/services/services_data.py
```

Agregar:

```python
def insert_many_records(table_name: str, rows: list):

    results = []

    for row in rows:
        result = insert_record(table_name, row)
        results.append(result)

    return results
```

---

# 🧩 Endpoint futuro para ingestión

En el próximo sprint podremos hacer:

```
POST /data/customers/bulk
```

Body:

```json
[
{"id":1,"email":"a@test.com"},
{"id":2,"email":"b@test.com"}
]
```

---

# 🚀 Valor del Sprint

Kaia Core ahora soporta:

✔ Schema validation  
✔ Required fields  
✔ Datatype validation  
✔ Invalid column detection  
✔ Unique constraints  

Esto acerca el proyecto a herramientas reales de **Data Quality Engineering** como:

- Great Expectations
- Soda
- Monte Carlo
- dbt tests

---

# 🧠 Concepto clave logrado

Tu proyecto ahora implementa **Data Contracts**.

Un **Data Contract** asegura que los datos cumplen reglas definidas antes de entrar al sistema.

Esto es una práctica moderna en:

- Data Platforms
- Data Mesh
- Data Governance

---

# 🧭 Próximo Sprint (SPRINT 12)

Vamos a implementar algo **muy potente**:

## CSV Data Validation Engine

Usuarios podrán subir:

```
customers.csv
```

Kaia Core hará:

```
upload CSV
 ↓
parse file
 ↓
validate rows
 ↓
generate report
```

Reporte ejemplo:

```
10 rows valid
2 rows invalid
```

---

# 📌 Commit sugerido

```
feat: add unique constraint validation and bulk insert support
```

---

# ✅ Resultado del Sprint 11

El sistema ahora permite:

✔ Crear schemas avanzados  
✔ Validar columnas  
✔ Validar tipos de datos  
✔ Validar columnas únicas  
✔ Insertar datos seguros  

Esto posiciona a **Kaia Core** como la base de un **motor real de validación de datos para pipelines de datos**.