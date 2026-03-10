# Sprint 5 — Data Tables & Data Ingestion (Kaia Core)

## 🎯 Objetivo del Sprint

El objetivo de este sprint es **evolucionar Kaia Core desde un simple validador de CSV a una plataforma donde los usuarios puedan:**

* **Crear tablas definidas por schemas**
* **Insertar registros manualmente**
* **Insertar registros mediante archivos CSV o Excel**
* **Usar esas tablas como datasets paramétricos**
* **Preparar los datos para análisis o reportes**

Este paso transforma a **Kaia** en una **herramienta de gestión de datasets validables**, útil para **analistas de datos y equipos de BI**.

---

# 🧠 Concepto clave del Sprint

Hasta ahora Kaia permite:

* Crear **schemas**
* Validar **archivos CSV contra schemas**

Ahora agregaremos una capa nueva:

**DATA STORAGE**

Es decir, permitir que el usuario:

1. Cree una **tabla**
2. Inserte **registros**
3. Consulte esos datos

Esto convierte a Kaia en una **mini base de datos validada por schema**.

---

# 🧩 Arquitectura que agregaremos

Actualmente:

```
Client
↓
API
↓
Validator
↓
Response
```
Nueva arquitectura:
```
Client
↓
API
↓
Validator
↓
**Data Storage Layer**
↓
Response
```
---

# 📁 Nuevas carpetas que agregaremos

Dentro de `app/` agregaremos:

```
app
│
├ services
│
├ repositories
│
├ models
│
├ api
│
└ storage
```

Nueva carpeta:

### **repositories**

Esta carpeta será responsable de **guardar y recuperar datos**.

Separar esta lógica es **una buena práctica de arquitectura backend**.

---

# 🗄️ Estructura nueva recomendada

```
app
│
├ main.py
│
├ api
│  ├ router.py
│  └ endpoints
│     ├ schema_endpoint.py
│     ├ validation_endpoint.py
│     ├ health_endpoint.py
│     └ data_endpoint.py
│
├ models
│  ├ table_schema.py
│  └ table_row.py
│
├ services
│  ├ schema_service.py
│  ├ csv_validator.py
│  └ data_service.py
│
├ repositories
│  └ data_repository.py
│
├ validators
│  └ schema_validator.py
│
└ schemas
   └ validation_result.py
```

---

# 📦 Paso 1 — Crear modelo de registros de tabla

Archivo nuevo:

```
app/models/table_row.py
```

Código:

```python
from pydantic import BaseModel
from typing import Dict


class TableRow(BaseModel):
    """
    Represents a row inserted into a table.
    """

    table_name: str
    data: Dict
```

Este modelo representa **una fila de datos insertada en una tabla**.

Ejemplo:

```
{
 "table_name": "customers",
 "data": {
   "id": 1,
   "email": "user@mail.com"
 }
}
```

---

# 🗄️ Paso 2 — Crear repositorio de datos

Archivo nuevo:

```
app/repositories/data_repository.py
```

Código:

```python
from typing import Dict, List

data_db: Dict[str, List[dict]] = {}


def insert_row(table_name: str, row: dict):

    if table_name not in data_db:
        data_db[table_name] = []

    data_db[table_name].append(row)

    return row


def get_rows(table_name: str):

    return data_db.get(table_name, [])
```

Este archivo actúa como **base de datos temporal en memoria**.

Ejemplo interno:

```
data_db = {
 "customers": [
   {"id":1,"email":"a@mail.com"},
   {"id":2,"email":"b@mail.com"}
 ]
}
```

---

# ⚙️ Paso 3 — Crear servicio de datos

Archivo nuevo:

```
app/services/data_service.py
```

Código:

```python
from app.repositories.data_repository import insert_row, get_rows
from app.services.schema_service import get_schema
from app.services.csv_validator import validate_csv


def insert_record(table_name: str, data: dict):

    schema = get_schema(table_name)

    if not schema:
        raise ValueError("Schema not found")

    return insert_row(table_name, data)


def get_records(table_name: str):

    return get_rows(table_name)
```

Este servicio:

* Verifica que el **schema exista**
* Inserta los registros

---

# 🌐 Paso 4 — Crear endpoint de datos

Archivo nuevo:

```
app/api/endpoints/data_endpoint.py
```

Código:

```python
from fastapi import APIRouter
from app.services.data_service import insert_record, get_records

router = APIRouter()


@router.post("/{table_name}")
def insert_data(table_name: str, data: dict):

    return insert_record(table_name, data)


@router.get("/{table_name}")
def read_data(table_name: str):

    return get_records(table_name)
```

Esto crea endpoints nuevos:

```
POST /data/{table_name}
GET /data/{table_name}
```

---

# 🔗 Paso 5 — Registrar el endpoint en el router

Editar:

```
app/api/router.py
```

Agregar:

```python
from app.api.endpoints import data_endpoint
```

y registrar:

```python
api_router.include_router(
    data_endpoint.router,
    prefix="/data",
    tags=["data"]
)
```

---

# 🧪 Paso 6 — Probar la API

Arrancar servidor:

```
uvicorn app.main:app --reload
```

Abrir documentación:

```
http://127.0.0.1:8000/docs
```

---

## 1️⃣ Crear schema

```
POST /schemas
```

---

## 2️⃣ Insertar registro

```
POST /data/customers
```

Body:

```
{
 "id":1,
 "email":"user@mail.com"
}
```

---

## 3️⃣ Consultar registros

```
GET /data/customers
```

Respuesta:

```
[
 {"id":1,"email":"user@mail.com"}
]
```

---

# 📊 Qué habilita este sprint

Ahora Kaia permite:

* **Definir schemas**
* **Validar archivos CSV**
* **Insertar datos en tablas**
* **Consultar datos**

Esto habilita **tablas paramétricas**.

Ejemplo de uso:

| tabla          | uso        |
| -------------- | ---------- |
| countries      | catálogo   |
| products       | catálogo   |
| exchange_rates | parámetros |
| campaigns      | marketing  |

Los **analistas de datos pueden usar estas tablas para reportes**.

---

# 🚀 Evolución futura

Este sprint prepara el terreno para:

### **Sprint 6 — Persistencia real**

Reemplazar:

```
data_db
```

por:

* **PostgreSQL**
* **BigQuery**
* **Firestore**

---

### **Sprint 7 — Data Upload**

Permitir:

```
POST /data/upload
```

para subir:

* CSV
* Excel

---

### **Sprint 8 — Integración con BI**

Permitir conectar Kaia con:

* dashboards
* pipelines
* herramientas de analytics

---

# 🧠 Resultado del Sprint

Después de este sprint Kaia pasa de ser:

**CSV Validator**

a

**Data Validation + Data Table Platform**

Esto es muy útil para:

* Data Analysts
* BI teams
* Data Engineers

porque permite **crear datasets confiables para análisis**.

---
