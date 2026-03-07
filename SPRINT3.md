#  Sprint 3 — Dynamic Schema Engine

**Proyecto:** Data Validator
**Sprint:** SPIN3
**Objetivo:** Permitir que el usuario defina la estructura de una tabla (schema) y que el sistema utilice esa estructura para validar archivos CSV dinámicamente.

---

# Introducción

En **Sprint 2** construimos un **validador básico de archivos CSV**.
Ese validador tenía columnas definidas en el código como:

```
expected_columns = [...]
```

Ese enfoque **no es escalable**, porque cada dataset puede tener estructuras diferentes.

Por eso en **Sprint 3** construiremos un sistema donde:

* El **usuario define la estructura de la tabla**
* El sistema **guarda esa definición**
* El **validador usa esa definición** para validar archivos

Esto es lo que en ingeniería de datos se conoce como:

**Data Contract**
o
**Schema-driven validation**

---

# Objetivos del Sprint

Al finalizar este sprint el sistema permitirá:

* Crear **definiciones de tablas**
* Definir **columnas**
* Definir **tipos de datos**
* Marcar columnas **obligatorias**
* Marcar columnas **únicas**
* Guardar esa definición
* Usar esa definición para validar CSV

---

# Concepto clave: Table Schema

Un **Table Schema** describe cómo debe verse una tabla.

Ejemplo conceptual:

```
Tabla: customers

Columnas:

id        -> integer -> requerido -> único
email     -> string  -> requerido -> único
name      -> string  -> opcional
country   -> string  -> opcional
```

Cuando un usuario cargue un CSV:

```
id,email,name,country
1,test@mail.com,Ana,AR
2,test@mail.com,Juan,AR
```

El sistema utilizará el schema para validar el archivo.

Si el CSV contiene errores:

```
ERROR: columna requerida faltante
ERROR: valores duplicados
ERROR: tipo incorrecto
```

---

# Cambios en la arquitectura del backend

Hasta ahora la estructura del backend era:

```
backend/
 ├── app/
 │    ├── main.py
 │    ├── api/
 │    │     └── routes/
 │    │           └── validate.py
 │    ├── services/
 │    │     └── csv_validator.py
 │    ├── schemas/
 │    │     └── validation_schema.py
```

En este sprint agregaremos **nuevos módulos para manejar schemas**.

Nueva estructura:

```
backend/
 ├── app/
 │
 │    ├── main.py
 │
 │    ├── api/
 │    │     └── routes/
 │    │           ├── validate.py
 │    │           └── schemas.py
 │
 │    ├── services/
 │    │     ├── csv_validator.py
 │    │     └── schema_service.py
 │
 │    ├── models/
 │    │     └── table_schema.py
 │
 │    └── schemas/
 │          └── validation_schema.py
```

---

# Tarea 1 — Crear modelo de Table Schema

Crear el archivo:

```
backend/app/models/table_schema.py
```

Este archivo define **cómo se representa una tabla dentro del sistema**.

---

## Código

```python
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
```

---

# Qué significa este modelo

Este modelo permite representar estructuras como:

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

Este JSON será enviado desde el **frontend hacia el backend**.

---

# Tarea 2 — Crear servicio para manejar schemas

Crear archivo:

```
backend/app/services/schema_service.py
```

Este servicio se encargará de:

* **guardar schemas**
* **recuperar schemas**

Para la primera versión los guardaremos **en memoria**.

---

## Código

```python
from typing import Dict
from app.models.table_schema import TableSchema

schemas_db: Dict[str, TableSchema] = {}


def create_schema(schema: TableSchema):
    schemas_db[schema.table_name] = schema
    return schema


def get_schema(table_name: str):
    return schemas_db.get(table_name)
```

---

# Cómo funciona este servicio

El sistema utiliza un diccionario en memoria:

```
schemas_db
```

Ejemplo interno:

```
{
   "customers": TableSchema(...)
}
```

Esto es **temporal para desarrollo**.

En futuros sprints lo moveremos a:

* **BigQuery**
* **Postgres**
* **Firestore**

---

# Tarea 3 — Crear endpoint para crear schemas

Crear archivo:

```
backend/app/api/routes/schemas.py
```

---

## Código

```python
from fastapi import APIRouter
from app.models.table_schema import TableSchema
from app.services.schema_service import create_schema

router = APIRouter()

@router.post("/schema")
def create_table_schema(schema: TableSchema):
    return create_schema(schema)
```

---

# Qué hace este endpoint

Permite crear un **schema de tabla** desde una petición HTTP.

Endpoint:

```
POST /schema
```

Ejemplo de request:

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

# Tarea 4 — Registrar el router en FastAPI

Abrir archivo:

```
backend/app/main.py
```

Agregar el router.

---

## Código

```python
from app.api.routes import schemas

app.include_router(schemas.router)
```

Esto permite que FastAPI registre el endpoint:

```
POST /schema
```

---

# Tarea 5 — Conectar el schema al validador

Modificar archivo:

```
backend/app/services/csv_validator.py
```

El validador ahora debe recibir **el schema de la tabla**.

---

## Nueva firma de función

```python
def validate_csv(file, table_schema):
```

Esto permitirá que el validador acceda a:

```
table_schema.columns
```

---

# Tarea 6 — Validar columnas del CSV contra el schema

Dentro del validador debemos construir la lista de columnas esperadas.

---

## Código

```python
expected_columns = [col.name for col in table_schema.columns]
```

Esto reemplaza el antiguo:

```
expected_columns = [...]
```

---

# Tarea 7 — Validar columnas obligatorias

Ejemplo de lógica de validación.

---

```python
for column in table_schema.columns:
    if column.required:
        if column.name not in dataframe.columns:
            errors.append(f"Missing required column: {column.name}")
```

---

# Tarea 8 — Validar columnas únicas

Validación de duplicados.

---

```python
for column in table_schema.columns:
    if column.unique:
        if dataframe[column.name].duplicated().any():
            errors.append(f"Column {column.name} has duplicate values")
```

---
### Código csv_validator completo
```
backend/app/services/csv_validator.py
```

Este código hace lo siguiente:

- **Lee el CSV con pandas**
- **Obtiene columnas esperadas desde el schema**
- **Detecta columnas faltantes**
- **Detecta columnas inesperadas**
- **Valida columnas obligatorias**
- **Valida columnas únicas**
- **Cuenta valores nulos**
- **Genera el resultado estructurado**

```python
import pandas as pd


def validate_csv(file, table_schema):

    # Leer archivo CSV
    dataframe = pd.read_csv(file.file)

    errors = []

    # Obtener columnas esperadas desde el schema
    expected_columns = [col.name for col in table_schema.columns]

    detected_columns = list(dataframe.columns)

    # Detectar columnas faltantes
    missing_columns = []

    for column in expected_columns:
        if column not in detected_columns:
            missing_columns.append(column)
            errors.append(f"Missing column: {column}")

    # Detectar columnas inesperadas
    unexpected_columns = []

    for column in detected_columns:
        if column not in expected_columns:
            unexpected_columns.append(column)
            errors.append(f"Unexpected column: {column}")

    # Validar columnas obligatorias
    for column in table_schema.columns:

        if column.required:
            if column.name not in detected_columns:
                errors.append(f"Required column missing: {column.name}")

    # Validar columnas únicas
    for column in table_schema.columns:

        if column.unique and column.name in detected_columns:

            if dataframe[column.name].duplicated().any():
                errors.append(f"Column '{column.name}' contains duplicate values")

    # Detectar valores nulos
    null_values = {}

    for column in detected_columns:

        null_count = dataframe[column].isnull().sum()

        if null_count > 0:
            null_values[column] = int(null_count)

    # Construir resultado
    result = {
        "valid": len(errors) == 0,
        "row_count": len(dataframe),
        "columns_detected": detected_columns,
        "missing_columns": missing_columns,
        "unexpected_columns": unexpected_columns,
        "null_values": null_values,
        "errors": errors
    }

    return result
```


# Cómo probar el sistema

Iniciar el servidor:

```
uvicorn app.main:app --reload
```

Abrir la documentación automática:

```
http://localhost:8000/docs
```

---

## Paso 1 — Crear schema

Usar endpoint:

```
POST /schema
```

---

## Paso 2 — Subir CSV
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
    },
    {
      "name": "name",
      "datatype": "string",
      "required": false,
      "unique": false
    }
  ]
}
```
Utilizar el endpoint de validación creado en Sprint 2.

El sistema ahora usará **el schema almacenado**.

---

# Flujo completo del sistema

El flujo ahora funciona así:

```
Usuario crea tabla
        ↓
Sistema guarda schema
        ↓
Usuario sube CSV
        ↓
Validador obtiene schema
        ↓
Se ejecutan reglas
        ↓
Se genera reporte
```

---

# Resultado del Sprint

Al finalizar este sprint el sistema tendrá:

**✔ Definición dinámica de tablas**

**✔ Validación basada en schemas**

**✔ Motor extensible de reglas**

Esto transforma el proyecto en un **motor de validación configurable**.

---

# Qué construiremos en Sprint 4

En el siguiente sprint desarrollaremos:

**La interfaz web (Frontend)** para que el usuario pueda:

* Crear tablas
* Agregar columnas
* Marcar columnas únicas
* Marcar columnas obligatorias
* Subir archivos CSV

Todo **sin escribir código**.

---

# Nota importante

Este tipo de sistemas se usan en plataformas modernas de datos como:

* Data Contracts
* Data Quality Platforms
* Data Observability Tools

Ejemplos reales incluyen herramientas como **Great Expectations**, **Soda** y **Monte Carlo**.

Tu proyecto se está acercando a ese tipo de arquitectura.
