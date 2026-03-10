# 🚀 KAIA CORE — SPRINT 13
## Validation Reports, Dataset History & Data Quality Tracking

**Proyecto:** Kaia Core  
**Sprint:** 13  
**Objetivo:** Implementar un sistema de **historial de validaciones de datasets**, permitiendo guardar cada ejecución de validación de CSV y consultarla posteriormente.

Con este sprint Kaia Core evoluciona desde:

```
CSV Validator API
```

a algo más cercano a una **plataforma de Data Quality con historial de ejecuciones**.

Esto es exactamente lo que hacen herramientas modernas como:

- :contentReference[oaicite:0]{index=0}
- :contentReference[oaicite:1]{index=1}
- :contentReference[oaicite:2]{index=2}

---

# 🧠 Problema que resolvemos

Actualmente el flujo es:

```
upload CSV
↓
validate
↓
response
```

El problema es que **no queda registro de la validación**.

Si un usuario quiere saber:

```
¿qué pasó con el CSV de ayer?
```

no hay forma de saberlo.

---

# 🎯 Nuevo flujo del sistema

Ahora el flujo será:

```
Upload CSV
     ↓
Validate
     ↓
Generate validation report
     ↓
Store report
     ↓
Return report_id
```

Luego podremos consultar:

```
GET /validation-reports
GET /validation-reports/{id}
GET /validation-reports/table/{table_name}
```

Esto crea un **historial de calidad de datos**.

---

# 🧱 Arquitectura del sistema

Nueva capa:

```
API
 ↓
Services
 ↓
Validation Reports Service
 ↓
Repository
 ↓
Storage
```

---

# 📁 Nuevos archivos del Sprint

Agregar nueva carpeta:

```
backend/app/repositories
```

y nuevos archivos:

```
repositories/
    validation_repository.py

services/
    validation_service.py

models/
    validation_report.py
```

---

# 🧩 Paso 1 — Modelo de Validation Report

Archivo:

```
app/models/validation_report.py
```

```python
"""
Validation Report Model
"""

from pydantic import BaseModel
from typing import List, Dict
from datetime import datetime


class ValidationReport(BaseModel):

    id: str

    table_name: str

    timestamp: datetime

    rows_analyzed: int

    valid_rows: int

    invalid_rows: int

    schema_errors: List[Dict]

    row_errors: List[Dict]
```

---

# 🧩 Paso 2 — Repository de reportes

Archivo:

```
app/repositories/validation_repository.py
```

Por ahora usaremos almacenamiento en memoria.

```python
"""
Validation Report Repository
"""

from typing import Dict
from app.models.validation_report import ValidationReport


validation_reports_db: Dict[str, ValidationReport] = {}


def save_report(report: ValidationReport):

    validation_reports_db[report.id] = report

    return report


def get_report(report_id: str):

    return validation_reports_db.get(report_id)


def get_all_reports():

    return list(validation_reports_db.values())


def get_reports_by_table(table_name: str):

    return [
        r for r in validation_reports_db.values()
        if r.table_name == table_name
    ]
```

---

# 🧩 Paso 3 — Service de reportes

Archivo:

```
app/services/validation_service.py
```

```python
"""
Validation Report Service
"""

import uuid
from datetime import datetime

from app.models.validation_report import ValidationReport
from app.repositories.validation_repository import (
    save_report,
    get_report,
    get_all_reports,
    get_reports_by_table
)


def create_validation_report(table_name, validation_result):

    report = ValidationReport(

        id=str(uuid.uuid4()),

        table_name=table_name,

        timestamp=datetime.utcnow(),

        rows_analyzed=validation_result["rows_analyzed"],

        valid_rows=validation_result["valid_rows"],

        invalid_rows=validation_result["invalid_rows"],

        schema_errors=validation_result["schema_errors"],

        row_errors=validation_result["row_errors"]

    )

    save_report(report)

    return report


def fetch_report(report_id: str):

    return get_report(report_id)


def fetch_all_reports():

    return get_all_reports()


def fetch_reports_by_table(table_name: str):

    return get_reports_by_table(table_name)
```

---

# 🧩 Paso 4 — Integrar reportes en ingestión CSV

Actualizar:

```
app/services/services_data.py
```

```python
from app.services.validation_service import create_validation_report
```

Actualizar función `ingest_csv`:

```python
def ingest_csv(table_name: str, file):

    schema = get_schema(table_name)

    validation = validate_csv(file, schema)

    report = create_validation_report(table_name, validation)

    inserted = []

    for row in validation["preview_valid_rows"]:

        inserted.append(insert_record(table_name, row))

    return {
        "validation_report_id": report.id,
        "inserted_rows": inserted,
        "invalid_rows": validation["row_errors"]
    }
```

---

# 🧩 Paso 5 — Endpoints de Validation Reports

Archivo:

```
app/api/endpoints/validation_reports.py
```

```python
from fastapi import APIRouter

from app.services.validation_service import (
    fetch_report,
    fetch_all_reports,
    fetch_reports_by_table
)

router = APIRouter(prefix="/validation-reports")


@router.get("/")
def get_reports():

    return fetch_all_reports()


@router.get("/{report_id}")
def get_report(report_id: str):

    return fetch_report(report_id)


@router.get("/table/{table_name}")
def get_table_reports(table_name: str):

    return fetch_reports_by_table(table_name)
```

---

# 🧩 Paso 6 — Registrar el router

Archivo:

```
app/api/router.py
```

Agregar:

```python
from app.api.endpoints import validation_reports
```

y registrar:

```python
router.include_router(validation_reports.router)
```

---

# 🧪 Pruebas

## 1️⃣ Subir CSV

```
POST /data/customers/upload
```

Respuesta:

```json
{
 "validation_report_id": "c3c6c9c5-1f7e-4e52-a2c7-8c0fcb25c9d5",
 "inserted_rows": [...],
 "invalid_rows": [...]
}
```

---

## 2️⃣ Ver historial

```
GET /validation-reports
```

---

## 3️⃣ Ver reporte específico

```
GET /validation-reports/{report_id}
```

---

## 4️⃣ Ver historial por tabla

```
GET /validation-reports/table/customers
```

---

# 📊 Ejemplo de reporte almacenado

```json
{
 "id": "c3c6c9c5",
 "table_name": "customers",
 "timestamp": "2026-03-10T12:21:00",
 "rows_analyzed": 100,
 "valid_rows": 92,
 "invalid_rows": 8,
 "schema_errors": [],
 "row_errors": [...]
}
```

---

# 🚀 Qué logramos con este Sprint

Kaia Core ahora tiene:

✔ CSV Validation Engine  
✔ Data Quality Checks  
✔ Validation History  
✔ Dataset Validation Reports  

Esto ya se parece a una **mini plataforma de observabilidad de datos**.

---

# 🧠 Concepto clave logrado

Implementaste algo equivalente a:

```
Data Quality Observability Layer
```

Esto se usa en plataformas modernas de datos.

---

# 🧭 Próximo Sprint — SPRINT 14

El próximo sprint va a ser **MUY potente**:

## Dataset Statistics & Profiling Engine

Vamos a calcular automáticamente:

```
row count
null count
unique values
min
max
avg
```

para cada dataset.

Esto crea un **Data Profiling Engine**, como el que usan herramientas de Data Governance.

---

# 📌 Commit sugerido

```
feat: add validation reports and dataset history
```

---

# ✅ Resultado del Sprint 13

Kaia Core ahora puede:

✔ Validar CSV  
✔ Insertar datos válidos  
✔ Generar reportes de validación  
✔ Guardar historial de validaciones  
✔ Consultar historial por tabla  

Tu proyecto ya está evolucionando hacia una **plataforma real de Data Quality para Data Engineers**.