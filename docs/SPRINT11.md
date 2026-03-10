# 🚀 KAIA CORE — SPRINT 12
## CSV Ingestion, Validation Reports & Dataset Preview

**Proyecto:** Kaia Core  
**Sprint:** 12  
**Objetivo:** Implementar un **motor de ingestión de CSV con validación automática**, generación de **reportes de calidad de datos**, y **preview de datasets**.

Con este sprint Kaia Core deja de ser solo una API de inserción de registros y empieza a comportarse como una **plataforma de ingestión y validación de datos**, similar a herramientas usadas en pipelines de Data Engineering.

---

# 🧠 Problema que resolvemos

Hasta ahora Kaia Core permite:

✔ Crear schemas  
✔ Insertar registros  
✔ Validar required  
✔ Validar datatype  
✔ Validar unique  

Pero en el mundo real los datos **no llegan como JSON**.

Normalmente llegan como:

```
CSV
Excel
JSON files
API responses
data lake files
```

Por lo tanto necesitamos una forma de:

```
upload file
 ↓
parse rows
 ↓
validate rows
 ↓
generate report
```

Esto se convierte en un **Data Quality Layer antes del Data Warehouse**.

---

# 🧱 Arquitectura del flujo de ingestión

El nuevo flujo será:

```
Client
 │
 ▼
Upload CSV Endpoint
 │
 ▼
CSV Parser
 │
 ▼
Row Validator
 │
 ▼
Validation Report
 │
 ├── valid_rows
 └── invalid_rows
```

Los registros válidos podrán:

```
insert into table
```

Los registros inválidos se reportan al usuario.

---

# 📁 Nuevos archivos del Sprint

Se agregan nuevos módulos para manejo de archivos.

```
backend/app/

services/
    csv_service.py

validator/
    csv_validator.py
```

Estos archivos manejarán:

```
file parsing
row validation
validation report
```

---

# 🧩 Paso 1 — Servicio para leer CSV

Archivo nuevo:

```
backend/app/services/csv_service.py
```

Código:

```python
"""
CSV Service

Handles CSV parsing and returns rows as dictionaries.
"""

import csv
from io import StringIO


def parse_csv(file_content: str):

    reader = csv.DictReader(StringIO(file_content))

    rows = []

    for row in reader:
        rows.append(row)

    return rows
```

Este servicio transforma un archivo CSV en:

```
List[dict]
```

Ejemplo:

CSV

```
id,email
1,a@test.com
2,b@test.com
```

Resultado:

```python
[
 {"id": "1", "email": "a@test.com"},
 {"id": "2", "email": "b@test.com"}
]
```

---

# 🧩 Paso 2 — Validador de CSV

Archivo nuevo:

```
backend/app/validator/csv_validator.py
```

Código:

```python
"""
CSV Validator

Validates a list of rows against a table schema.
"""

from app.validator.schema_validator import validate_row


def validate_csv(schema, rows):

    valid_rows = []
    invalid_rows = []

    for index, row in enumerate(rows):

        errors = validate_row(schema, row)

        if errors:
            invalid_rows.append({
                "row_number": index + 1,
                "row": row,
                "errors": errors
            })

        else:
            valid_rows.append(row)

    return {
        "valid_rows": valid_rows,
        "invalid_rows": invalid_rows
    }
```

---

# 🧩 Paso 3 — Integrar CSV validation en Service Layer

Archivo:

```
backend/app/services/services_data.py
```

Agregar función nueva.

```python
from app.services.csv_service import parse_csv
from app.validator.csv_validator import validate_csv
from app.services.services_schema import get_schema


def validate_csv_file(table_name: str, file_content: str):

    schema = get_schema(table_name)

    if not schema:
        raise HTTPException(
            status_code=404,
            detail="Table does not exist"
        )

    rows = parse_csv(file_content)

    result = validate_csv(schema, rows)

    return result
```

---

# 🧩 Paso 4 — Endpoint para subir CSV

Archivo:

```
backend/app/api/endpoints/tables.py
```

Agregar endpoint nuevo.

```python
from fastapi import UploadFile, File
from app.services.services_data import validate_csv_file


@router.post("/data/{table_name}/upload")
async def upload_csv(table_name: str, file: UploadFile = File(...)):

    content = await file.read()

    file_content = content.decode("utf-8")

    return validate_csv_file(table_name, file_content)
```

---

# 🧪 Pruebas

## Crear schema

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

# 🧪 CSV de prueba

Archivo:

```
customers.csv
```

```
id,email
1,user@test.com
2,invalid_email
ABC,wrong@test.com
```

---

# 🧪 Subir archivo

```
POST /data/customers/upload
```

Swagger permite subir archivo directamente.

---

# 🧪 Resultado esperado

```json
{
 "valid_rows": [
   {
     "id": "1",
     "email": "user@test.com"
   },
   {
     "id": "2",
     "email": "invalid_email"
   }
 ],
 "invalid_rows": [
   {
     "row_number": 3,
     "row": {
       "id": "ABC",
       "email": "wrong@test.com"
     },
     "errors": [
       "id must be integer"
     ]
   }
 ]
}
```

---

# 🧩 Paso 5 — Inserción automática de filas válidas

Podemos mejorar el endpoint para **insertar automáticamente las filas válidas**.

Actualizar servicio:

```python
from app.services.services_data import insert_record


def ingest_csv(table_name: str, file_content: str):

    schema = get_schema(table_name)

    rows = parse_csv(file_content)

    validation = validate_csv(schema, rows)

    inserted = []

    for row in validation["valid_rows"]:
        inserted.append(insert_record(table_name, row))

    return {
        "inserted_rows": inserted,
        "invalid_rows": validation["invalid_rows"]
    }
```

---

# 🚀 Resultado del flujo completo

Ahora el sistema puede hacer:

```
Upload CSV
 ↓
Parse rows
 ↓
Validate rows
 ↓
Insert valid rows
 ↓
Return validation report
```

Esto es exactamente lo que hace un **Data Ingestion Layer** en un Data Platform.

---

# 📊 Ejemplo de reporte final

```json
{
 "inserted_rows": [
   {"id":1,"email":"user@test.com"}
 ],
 "invalid_rows": [
   {
     "row_number":3,
     "errors":[
       "id must be integer"
     ]
   }
 ]
}
```

---

# 🚀 Valor para Data Engineering

Con este sprint Kaia Core ya implementa conceptos reales de:

```
Data Quality
Data Contracts
Data Ingestion
Schema Validation
```

Esto es muy cercano a herramientas usadas en producción como:

- Great Expectations
- Soda
- Databricks Expectations
- Monte Carlo

---

# 🧠 Concepto logrado

Kaia Core ahora funciona como un **Data Quality Gateway**.

Antes:

```
CSV
 ↓
Warehouse
```

Ahora:

```
CSV
 ↓
Kaia Core
 ↓
Validated Data
 ↓
Warehouse
```

---

# 🧭 Próximo Sprint — SPRINT 13

Vamos a implementar algo **muy importante para un SaaS**:

## Dataset Metadata API

Permite:

```
GET /datasets
GET /datasets/{name}
GET /datasets/{name}/stats
```

Esto permitirá:

✔ contar registros  
✔ obtener estadísticas  
✔ explorar datasets  

Y empezaremos a construir algo tipo **mini data catalog**.

---

# 📌 Commit sugerido

```
feat: add CSV ingestion and validation engine
```

---

# ✅ Resultado del Sprint 12

Después de este sprint el sistema permite:

✔ Crear schemas  
✔ Insertar registros  
✔ Validar datos  
✔ Subir CSV  
✔ Generar reportes de validación  
✔ Insertar datos válidos automáticamente  

Kaia Core se convierte ahora en **una capa real de ingestión y validación de datos para pipelines de datos**.