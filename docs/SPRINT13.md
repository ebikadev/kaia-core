# 🚀 Kaia Core — Sprint 14: Data Profiling Engine

## 📌 Objetivo del Sprint

En este sprint agregamos **Data Profiling automático** al sistema.

Hasta ahora **Kaia Core** permite:

* Crear **schemas dinámicos**
* Insertar datos
* Validar CSV contra schemas
* Generar **validation reports**

Ahora agregaremos una nueva capacidad clave usada en **Data Engineering real**:

**Data Profiling**

Esto permite analizar automáticamente los datos cargados y obtener estadísticas útiles como:

* cantidad de valores **NULL**
* cantidad de **valores únicos**
* **mínimo**
* **máximo**
* **promedio**

Esto ayuda a detectar problemas como:

* columnas con muchos NULL
* duplicados inesperados
* datos fuera de rango
* columnas mal cargadas

Herramientas profesionales como **Monte Carlo**, **Soda** o **Great Expectations** implementan exactamente este concepto.

---

# 🧠 Concepto: Data Profiling

Ejemplo de perfil generado:

```json
{
 "table": "customers",
 "columns_profile": {
   "id": {
     "null_count": 0,
     "unique_values": 100,
     "min": 1,
     "max": 100
   },
   "email": {
     "null_count": 2,
     "unique_values": 95
   }
 }
}
```

---

# 📂 Estructura de archivos

Se agregan nuevos módulos al proyecto:

```
app
│
├── profiling
│     └── data_profiler.py
│
├── models
│     └── data_profile.py
│
├── services
│     └── profiling_service.py
│
├── repositories
│     └── profiling_repository.py
│
├── api
│     └── endpoints
│           └── profiling.py
```

---

# 1️⃣ Modelo de Perfil de Datos

📄 **app/models/data_profile.py**

Define la estructura de un perfil de datos.

```python
"""
Data Profile Model

Represents statistical analysis of a dataset
"""

from pydantic import BaseModel
from typing import Dict
from datetime import datetime


class ColumnProfile(BaseModel):

    null_count: int
    unique_values: int
    min_value: float | None = None
    max_value: float | None = None
    mean: float | None = None


class DataProfile(BaseModel):

    id: str
    table_name: str
    timestamp: datetime
    rows_analyzed: int
    columns: Dict[str, ColumnProfile]
```

---

# 2️⃣ Data Profiling Engine

📄 **app/profiling/data_profiler.py**

Este módulo analiza un DataFrame y calcula estadísticas automáticamente.

```python
"""
Automatic Data Profiling Engine
"""

import pandas as pd
from typing import Dict
from app.models.data_profile import ColumnProfile


def generate_profile(df: pd.DataFrame) -> Dict[str, ColumnProfile]:

    profiles = {}

    for column in df.columns:

        series = df[column]

        profile = ColumnProfile(

            null_count=int(series.isna().sum()),

            unique_values=int(series.nunique()),

            min_value=float(series.min()) if pd.api.types.is_numeric_dtype(series) else None,

            max_value=float(series.max()) if pd.api.types.is_numeric_dtype(series) else None,

            mean=float(series.mean()) if pd.api.types.is_numeric_dtype(series) else None

        )

        profiles[column] = profile

    return profiles
```

---

# 3️⃣ Repository de perfiles

📄 **app/repositories/profiling_repository.py**

Se encarga de almacenar los perfiles generados.

```python
"""
Data Profile Repository
"""

from typing import Dict
from app.models.data_profile import DataProfile

profiles_db: Dict[str, DataProfile] = {}


def save_profile(profile: DataProfile):

    profiles_db[profile.id] = profile

    return profile


def get_profiles():

    return list(profiles_db.values())


def get_profile(profile_id):

    return profiles_db.get(profile_id)


def get_profiles_by_table(table_name):

    return [
        p for p in profiles_db.values()
        if p.table_name == table_name
    ]
```

---

# 4️⃣ Servicio de profiling

📄 **app/services/profiling_service.py**

Orquesta la generación del perfil.

```python
"""
Profiling Service
"""

import uuid
from datetime import datetime
import pandas as pd

from app.models.data_profile import DataProfile
from app.repositories.profiling_repository import save_profile
from app.profiling.data_profiler import generate_profile


def create_profile(table_name: str, df: pd.DataFrame):

    columns_profile = generate_profile(df)

    profile = DataProfile(

        id=str(uuid.uuid4()),

        table_name=table_name,

        timestamp=datetime.utcnow(),

        rows_analyzed=len(df),

        columns=columns_profile

    )

    save_profile(profile)

    return profile
```

---

# 5️⃣ Integración con el Upload de CSV

📄 **Modificar `tables.py`**

Agregar imports:

```python
import pandas as pd
from app.services.profiling_service import create_profile
```

Modificar endpoint:

```python
@router.post("/data/{table_name}/upload")
async def upload_csv(table_name: str, file: UploadFile = File(...)):

    schema = get_schema(table_name)

    if not schema:
        raise HTTPException(status_code=404, detail="Table not found")

    validation_result = validate_csv(file, schema)

    df = pd.read_csv(file.file)

    profile = create_profile(table_name, df)

    report = create_validation_report(table_name, validation_result)

    return {

        "validation_report_id": report.id,

        "profile_id": profile.id,

        "validation_summary": {

            "rows": validation_result["rows"],
            "valid_rows": validation_result["valid_rows"],
            "invalid_rows": validation_result["invalid_rows"]

        }

    }
```

---

# 6️⃣ Endpoints para consultar perfiles

📄 **app/api/endpoints/profiling.py**

```python
from fastapi import APIRouter

from app.repositories.profiling_repository import (
    get_profiles,
    get_profile,
    get_profiles_by_table
)

router = APIRouter(prefix="/profiles")


@router.get("/")
def list_profiles():

    return get_profiles()


@router.get("/{profile_id}")
def read_profile(profile_id: str):

    return get_profile(profile_id)


@router.get("/table/{table_name}")
def profiles_by_table(table_name: str):

    return get_profiles_by_table(table_name)
```

---

# 7️⃣ Registrar router en la API

📄 **router.py**

Agregar:

```python
from app.api.endpoints import profiling
```

Registrar:

```python
router.include_router(profiling.router)
```

---

# 🧪 Testing del sistema

### 1️⃣ Crear schema

```
POST /schemas
```

Ejemplo:

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
   "required": true
  }
 ]
}
```

---

### 2️⃣ Subir CSV

```
POST /data/customers/upload
```

Respuesta esperada:

```json
{
 "validation_report_id": "uuid",
 "profile_id": "uuid",
 "validation_summary": {
   "rows": 100,
   "valid_rows": 95,
   "invalid_rows": 5
 }
}
```

---

### 3️⃣ Consultar perfiles

```
GET /profiles
```

---

### 4️⃣ Perfiles por tabla

```
GET /profiles/table/customers
```

---

# 📊 Resultado del Sprint

| Feature            | Estado |
| ------------------ | ------ |
| Schema Engine      | ✅      |
| CSV Validation     | ✅      |
| Validation Reports | ✅      |
| Data Profiling     | ✅      |

Kaia Core ahora tiene **motor de profiling automático**, una funcionalidad usada en herramientas profesionales de **Data Quality y Data Observability**.

---

# 🚀 Próximo Sprint

El siguiente paso será implementar un:

## **Data Quality Rules Engine**

Ejemplo de reglas:

```
email must contain "@"
age must be > 18
country must be in list
salary must be positive
```

Esto permitirá definir **reglas personalizadas de calidad de datos**, transformando Kaia Core en una verdadera **plataforma de Data Quality para Data Engineers**.
