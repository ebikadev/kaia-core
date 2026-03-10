# 🚀 Kaia Core — Sprint 8

## 🌐 Crear Schemas desde el Frontend (UI → API)

En este **Sprint 8** vamos a dar un paso muy importante:
permitir que los usuarios **creen tablas directamente desde la interfaz web**.

Hasta ahora el flujo era:

```text
Usuario → FastAPI Docs → POST /schemas
```

Eso funciona para desarrollo, pero **no es usable para analistas**.

Ahora construiremos una **UI para crear schemas dinámicamente**.

---

# Objetivos del Sprint

En este sprint vamos a:

✅ Crear una **pantalla para crear schemas**
✅ Conectar el **frontend con la API**
✅ Permitir definir **columnas dinámicas**
✅ Enviar el schema a **POST /schemas**

Esto acerca el proyecto a una **plataforma de datasets self-service**.

---

# Arquitectura del flujo

```text
Browser
   ↓
Frontend Form
   ↓
api.js
   ↓
POST /schemas
   ↓
FastAPI
   ↓
services_schema
   ↓
schema_store
```

---

# 📁 Archivos involucrados

Frontend:

```text
frontend/
│
├── index.html
├── create_schema.html
├── insert_data.html
├── validate_csv.html
├── api.js
├── styles.css
```

Backend:

```text
backend/app/api/endpoints/tables.py
backend/app/services/services_schema.py
```

---

# 🧠 Endpoint utilizado

Ya existe en el backend:

```http
POST /schemas
```

Body esperado:

```json
{
  "table_name": "customers",
  "columns": [
    {
      "name": "id",
      "datatype": "integer",
      "required": true,
      "unique": true
    }
  ]
}
```

---

# 🎨 Paso 1 — Crear la UI

Archivo:

```text
frontend/create_schema.html
```

Código:

```html
<!DOCTYPE html>
<html>
<head>
    <title>Create Schema</title>
    <link rel="stylesheet" href="styles.css">
</head>

<body>

<h1>📊 Create Table Schema</h1>

<label>Table Name</label>
<input id="table_name" type="text"/>

<h3>Columns</h3>

<div id="columns"></div>

<button onclick="addColumn()">Add Column</button>

<br><br>

<button onclick="createSchema()">Create Schema</button>

<script src="api.js"></script>

</body>
</html>
```

Esta página permite:

* ingresar nombre de tabla
* agregar columnas dinámicamente

---

# ⚙️ Paso 2 — Agregar columnas dinámicas

Archivo:

```text
frontend/api.js
```

Agregar función:

```javascript
function addColumn(){

    const container = document.getElementById("columns")

    const div = document.createElement("div")

    div.innerHTML = `
        <input placeholder="column name" class="col_name"/>
        
        <select class="col_type">
            <option>string</option>
            <option>integer</option>
            <option>float</option>
        </select>

        required <input type="checkbox" class="col_required"/>
        unique <input type="checkbox" class="col_unique"/>
    `

    container.appendChild(div)

}
```

Esto permite agregar múltiples columnas.

---

# 🌐 Paso 3 — Enviar schema a la API

Continuamos en `api.js`.

```javascript
async function createSchema(){

    const tableName = document.getElementById("table_name").value

    const names = document.querySelectorAll(".col_name")
    const types = document.querySelectorAll(".col_type")
    const requireds = document.querySelectorAll(".col_required")
    const uniques = document.querySelectorAll(".col_unique")

    const columns = []

    for(let i=0;i<names.length;i++){

        columns.push({
            name:names[i].value,
            datatype:types[i].value,
            required:requireds[i].checked,
            unique:uniques[i].checked
        })

    }

    const payload = {
        table_name:tableName,
        columns:columns
    }

    const response = await fetch("http://127.0.0.1:8000/schemas",{
        method:"POST",
        headers:{
            "Content-Type":"application/json"
        },
        body:JSON.stringify(payload)
    })

    const result = await response.json()

    alert("Schema created!")

    console.log(result)

}
```

---

# 📊 Resultado visual

El usuario verá una pantalla así:

```
Create Table Schema

Table Name: [ customers ]

Columns

column name [ id ]
datatype    [ integer ]
required ☑
unique ☑

column name [ email ]
datatype    [ string ]
required ☑
unique ☑

[ Add Column ]

[ Create Schema ]
```

---

# ▶️ Cómo probar

## 1️⃣ Levantar backend

```bash
uvicorn app.main:app --reload
```

---

## 2️⃣ Abrir frontend

Abrir en el navegador:

```text
frontend/create_schema.html
```

---

## 3️⃣ Crear una tabla

Ejemplo:

```
Table name: customers
```

Columnas:

```
id integer required unique
email string required unique
country string optional
```

---

# 🔍 Verificar en la API

Ir a:

```text
http://127.0.0.1:8000/docs
```

y ejecutar:

```
GET /schemas
```

Debería devolver:

```json
[
 "customers"
]
```

---

# 🧠 Qué logramos en este sprint

Ahora **Kaia Core tiene creación de schemas desde UI**.

Flujo completo:

```text
User
 ↓
Frontend UI
 ↓
POST /schemas
 ↓
FastAPI
 ↓
services_schema
 ↓
schema_store
```

Esto convierte el sistema en un **Data Catalog dinámico**.

---

# 🚀 Próximo Sprint (9)

En el siguiente sprint podemos agregar algo muy potente:

### 📂 Insertar datos desde el frontend

Pantalla:

```
insert_data.html
```

donde el usuario podrá:

* seleccionar tabla
* cargar registros manualmente
* subir CSV

Esto transformará Kaia en una **mini plataforma de ingestión de datos**.

---

# 🧠 Visión del proyecto

La meta de **Kaia Core** es convertirse en una plataforma donde analistas puedan:

✔ Crear datasets
✔ Validar datasets
✔ Subir datos
✔ Consultar tablas

sin depender de ingeniería de datos.
