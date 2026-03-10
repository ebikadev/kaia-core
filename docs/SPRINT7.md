# 🚀 Kaia Core — Sprint 7

## 📊 Visualización de Tablas y Registros desde el Frontend

En este **Sprint 7** comenzamos a transformar **Kaia Core** en una herramienta realmente usable para analistas de datos.

Hasta ahora el sistema permite:

* Crear **schemas dinámicos**
* Insertar **registros**
* Validar **datasets**
* Subir **CSV**

Pero todo se hace desde la API.

El objetivo de este sprint es **empezar a construir una interfaz visual** que permita:

* 👀 Ver tablas creadas
* 📊 Consultar registros
* 📂 Seleccionar tablas desde el frontend
* 🔎 Explorar datos fácilmente

Esto acerca Kaia a un **mini Data Platform** para analistas.

---

# 🎯 Objetivos del Sprint 7

Construir los primeros componentes visuales para:

✅ Listar tablas disponibles
✅ Consultar registros de una tabla
✅ Mostrar datos en una tabla HTML
✅ Conectar el frontend con la API

---

# Arquitectura actualizada

El flujo ahora es:

Frontend → API → Services → Validators → Data

```
Browser
   ↓
HTML + JavaScript
   ↓
FastAPI API
   ↓
Services
   ↓
Data storage (in memory)
```

Seguimos usando **FastAPI** como backend.

---

# 📁 Nueva estructura del proyecto

Agregamos una carpeta de frontend.

```
kaia_core
│
├── api
│   ├── endpoints
│   └── routes
│
├── services
├── validators
├── schemas
│
├── frontend
│   ├── index.html
│   ├── tables.html
│   └── app.js
│
└── main.py
```

---

# 🧠 Nuevo endpoint necesario

Para mostrar tablas en el frontend necesitamos un endpoint nuevo.

## GET /schemas

Permite listar los schemas existentes.

---

# ⚙️ Endpoint para listar schemas

Archivo:

```
api/endpoints/schema_endpoint.py
```

Agregar:

```python
from fastapi import APIRouter
from services.schema_service import schema_store

router = APIRouter()

@router.get("/schemas")
def list_schemas():
    return list(schema_store.keys())
```

Esto devolverá:

```json
[
 "customers",
 "exchange_rates",
 "products"
]
```

---

# 🌐 Crear el Frontend

Creamos una carpeta:

```
frontend
```

---

# 📄 index.html

Pantalla principal de Kaia.

```
frontend/index.html
```

```html
<!DOCTYPE html>
<html>
<head>
    <title>Kaia Core</title>
</head>

<body>

<h1>🚀 Kaia Core</h1>

<h2>Tablas disponibles</h2>

<ul id="tables"></ul>

<script src="app.js"></script>

</body>
</html>
```

Esta página mostrará la lista de tablas.

---

# ⚙️ app.js

Archivo:

```
frontend/app.js
```

Este archivo conecta con la API.

```javascript
const API_URL = "http://127.0.0.1:8000"

async function loadTables() {

    const response = await fetch(`${API_URL}/schemas`)
    const tables = await response.json()

    const list = document.getElementById("tables")

    tables.forEach(table => {

        const item = document.createElement("li")

        const link = document.createElement("a")

        link.href = `tables.html?table=${table}`

        link.innerText = table

        item.appendChild(link)

        list.appendChild(item)
    })

}

loadTables()
```

Este script:

1️⃣ Consulta `/schemas`
2️⃣ Obtiene las tablas
3️⃣ Las muestra como links

---

# 📄 tables.html

Página para visualizar registros.

```
frontend/tables.html
```

```html
<!DOCTYPE html>
<html>
<head>
    <title>Table Viewer</title>
</head>

<body>

<h1>📊 Table Viewer</h1>

<table border="1" id="data-table">
</table>

<script src="app.js"></script>

</body>
</html>
```

---

# 🧠 Actualizar app.js para cargar datos

Extender el archivo `app.js`.

```javascript
async function loadTableData() {

    const params = new URLSearchParams(window.location.search)

    const table = params.get("table")

    if (!table) return

    const response = await fetch(`${API_URL}/data/${table}`)

    const data = await response.json()

    const tableElement = document.getElementById("data-table")

    if (data.length === 0) return

    const headers = Object.keys(data[0])

    const headerRow = document.createElement("tr")

    headers.forEach(h => {

        const th = document.createElement("th")

        th.innerText = h

        headerRow.appendChild(th)

    })

    tableElement.appendChild(headerRow)

    data.forEach(row => {

        const tr = document.createElement("tr")

        headers.forEach(h => {

            const td = document.createElement("td")

            td.innerText = row[h]

            tr.appendChild(td)

        })

        tableElement.appendChild(tr)

    })

}

loadTableData()
```

---

# ▶️ Cómo ejecutar todo

## 1️⃣ Levantar la API

```
uvicorn main:app --reload
```

---

## 2️⃣ Abrir el frontend

Abrir:

```
frontend/index.html
```

en el navegador.

---

## 3️⃣ Flujo de uso

1️⃣ Crear schema desde `/docs`

```
POST /schemas

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

2️⃣ Insertar registros

```
POST /data/{table}

{
 "id": 1,
 "email": "test@email.com"
}

GET /data/customers > Consultar tabla
```

3️⃣ Abrir:

```
index.html
```

4️⃣ Ver tablas disponibles

5️⃣ Click en tabla

6️⃣ Visualizar registros

---

# 📊 Resultado esperado

El usuario verá algo como:

```
🚀 Kaia Core

Tablas disponibles

customers
products
exchange_rates
```

Al hacer click:

```
customers
```

verá:

| id | email                             | country   |
| -- | --------------------------------- | --------- |
| 1  | [a@email.com](mailto:a@email.com) | USA       |
| 2  | [b@email.com](mailto:b@email.com) | Argentina |

---
# 🚀 Refactor de Arquitectura: Services vs Repository

## 🎯 Objetivo

En esta mejora del proyecto **Kaia Core** se corrige un problema de arquitectura detectado durante el desarrollo:
la **duplicación de responsabilidades entre la capa de services y la capa de repositories**.

El objetivo de este refactor es lograr una **arquitectura limpia y escalable**, siguiendo el patrón clásico de aplicaciones backend modernas.

---

# 🧠 Problema Detectado

Actualmente existían **dos lugares donde se almacenaban los datos**:

1️⃣ En `services_data.py`
2️⃣ En `data_repository.py`

Esto generaba **dos bases de datos en memoria diferentes**.

Ejemplo:

```
schemas_db
data_db
```

Esto provoca problemas como:

* ❌ Inconsistencia de datos
* ❌ Duplicación de lógica
* ❌ Violación del principio de separación de responsabilidades
* ❌ Dificultad para escalar el sistema a una base de datos real

---

# 🏗 Arquitectura Correcta

La arquitectura correcta en una API backend sigue este flujo:

```
Client
   ↓
API Endpoint
   ↓
Service Layer
   ↓
Repository Layer
   ↓
Storage
```

## Responsabilidades de cada capa

### 🌐 API Layer

Ubicación:

```
backend/app/api/endpoints
```

Responsabilidad:

* Manejar HTTP
* Recibir requests
* Devolver responses

No contiene lógica de negocio.

---

### 🧠 Service Layer

Ubicación:

```
backend/app/services
```

Responsabilidad:

* Lógica de negocio
* Validaciones
* Verificar existencia de tablas
* Orquestar operaciones

No guarda datos directamente.

---

### 💾 Repository Layer

Ubicación:

```
backend/app/repositories
```

Responsabilidad:

* Persistencia de datos
* Guardar registros
* Leer registros

Este es el **único lugar donde se almacenan los datos**.

---

# 📁 Estructura del Proyecto

```
kaia-core
│
├── backend
│   ├── app
│   │
│   ├── api
│   │   └── endpoints
│   │       └── tables.py
│   │
│   ├── services
│   │   ├── services_schema.py
│   │   └── services_data.py
│   │
│   ├── repositories
│   │   └── data_repository.py
│
```

---

# ⚙️ Implementación Correcta

## 📄 services_data.py (Service Layer)

Ruta:

```
backend/app/services/services_data.py
```

Responsabilidad:

* Verificar que la tabla exista
* Llamar al repository para insertar datos

Código:

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

# ❗ Cambios Importantes

Se eliminó esta lógica incorrecta:

```
schemas_db[table_name].append(row)
```

Y también:

```
if table_name not in schemas_db
```

Esto era incorrecto porque:

* `schemas_db` debe almacenar **solo schemas**
* No debe almacenar **datos**

---

# 💾 data_repository.py (Repository Layer)

Ruta:

```
backend/app/repositories/data_repository.py
```

Responsabilidad:

* Guardar datos
* Recuperar datos

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

---

# 🔄 Flujo de Inserción de Datos

Cuando el cliente hace una request:

```
POST /data/customers
```

Ocurre el siguiente flujo:

```
Client
   ↓
tables.py (endpoint)
   ↓
services_data.insert_record()
   ↓
data_repository.insert_row()
   ↓
data_db
```

---

# 🔍 Flujo de Lectura de Datos

Para consultar datos:

```
GET /data/customers
```

El flujo es:

```
Client
   ↓
tables.py
   ↓
services_data.get_records()
   ↓
data_repository.get_rows()
   ↓
data_db
```

---

# 📚 Regla Arquitectónica Importante

Una buena arquitectura backend sigue esta regla:

```
Controllers → Services → Repositories
```

Nunca:

```
Controllers → Repositories directamente
```

Y nunca:

```
Services guardando datos directamente
```

Esto garantiza:

* ✔ Código mantenible
* ✔ Separación de responsabilidades
* ✔ Escalabilidad
* ✔ Facilidad para migrar a bases de datos reales

---

# 🚀 Beneficios de este Refactor

Después de aplicar esta mejora:

✅ Arquitectura más limpia
✅ Eliminación de duplicación de datos
✅ Preparado para conectar con PostgreSQL / MongoDB
✅ Código más mantenible
✅ Mejor separación de capas

---

# 🔮 Próximos pasos sugeridos

Este refactor deja el sistema listo para evolucionar hacia:

### 📊 Persistencia real

Migrar de memoria a:

* PostgreSQL
* MongoDB
* Snowflake
* BigQuery

---

### 📂 Upload masivo de datasets

Agregar endpoint:

```
POST /data/upload
```

Para subir:

* CSV
* Excel

---

### 🌐 UI completa

Permitir desde el frontend:

* Crear tablas
* Insertar datos
* Subir datasets
* Visualizar registros

---

# 🧠 Conclusión

Este refactor transforma **Kaia Core** en un sistema con una arquitectura mucho más cercana a la utilizada en proyectos profesionales.

La separación clara entre:

* **API**
* **Services**
* **Repositories**

permite que el proyecto evolucione fácilmente hacia una **plataforma de gestión de datasets para analistas de datos**.
