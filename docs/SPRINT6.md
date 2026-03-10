# Sprint 6 — Primer Frontend para Kaia (UI + Integración con API)

## 🎯 Objetivo del Sprint

El objetivo de este sprint es **agregar una interfaz web básica** para interactuar con la API de **Kaia Core**.

Hasta ahora todo se prueba desde **Swagger o requests HTTP**, pero en este sprint construiremos una **UI simple que permita:**

* **Crear schemas**
* **Subir archivos CSV**
* **Validar datasets**
* **Consultar tablas**

Esto permitirá que **analistas de datos puedan usar Kaia sin necesidad de conocer APIs**.

---

# 🧠 Concepto del Sprint

Actualmente el sistema funciona así:
```
Client
↓
API
↓
Validator
↓
Storage
```
Ahora agregamos:
```
Client Browser
↓
**Frontend Web**
↓
API (FastAPI)
↓
Validator
↓
Storage
```
La UI será **una aplicación web simple que consume la API**.

---

# 🧩 Tecnología elegida para el frontend

Para empezar **NO vamos a usar frameworks complejos todavía**.

Primero construiremos una UI simple con:

* **HTML**
* **CSS**
* **JavaScript**
* **Fetch API**

Esto nos permitirá aprender **cómo se conecta un frontend con una API**.

Más adelante podremos migrar a **React**.

---

# 📁 Nueva estructura del proyecto

Agregaremos una carpeta `frontend`.

```id="tukuz0"
kaia-core
│
├ app
│
├ frontend
│  ├ index.html
│  ├ create_schema.html
│  ├ validate_csv.html
│  ├ insert_data.html
│  ├ styles.css
│  └ api.js
│
└ README.md
```

---

# 🌐 Paso 1 — Crear carpeta frontend

Crear:

```id="8tbvgb"
frontend/
```

Dentro crear archivos:

```id="n7z59h"
index.html
create_schema.html
validate_csv.html
insert_data.html
styles.css
api.js
```

---

# 🏠 Paso 2 — Página principal

Archivo:

```id="j43i5u"
frontend/index.html
```

Código:

```html
<!DOCTYPE html>
<html>
<head>
<title>Kaia</title>
<link rel="stylesheet" href="styles.css">
</head>

<body>

<h1>Kaia Data Platform</h1>

<p>Herramienta para validar y gestionar datasets.</p>

<ul>

<li>
<a href="create_schema.html">
Crear Schema
</a>
</li>

<li>
<a href="validate_csv.html">
Validar CSV
</a>
</li>

<li>
<a href="insert_data.html">
Insertar Datos
</a>
</li>

</ul>

</body>
</html>
```

---

# 🎨 Paso 3 — Estilos básicos

Archivo:

```id="pjx3dk"
frontend/styles.css
```

Código:

```css
body {

font-family: Arial;

margin: 40px;

background-color: #f4f4f4;

}

h1 {

color: #333;

}

button {

padding: 10px;

margin-top: 10px;

}

input {

padding: 8px;

margin: 5px;

}

textarea {

width: 400px;

height: 200px;

}
```

---

# 🔌 Paso 4 — Crear cliente API en JavaScript

Archivo:

```id="3q0bnc"
frontend/api.js
```

Código:

```javascript
const API_URL = "http://127.0.0.1:8000";


async function createSchema(schema) {

const response = await fetch(`${API_URL}/schemas`, {

method: "POST",

headers: {

"Content-Type": "application/json"

},

body: JSON.stringify(schema)

});

return response.json();

}



async function validateCSV(table, file) {

const formData = new FormData();

formData.append("file", file);

const response = await fetch(`${API_URL}/validation/${table}`, {

method: "POST",

body: formData

});

return response.json();

}



async function insertData(table, data) {

const response = await fetch(`${API_URL}/data/${table}`, {

method: "POST",

headers: {

"Content-Type": "application/json"

},

body: JSON.stringify(data)

});

return response.json();

}
```

Este archivo centraliza **todas las llamadas a la API**.

---

# 📊 Paso 5 — Crear página para crear schemas

Archivo:

```id="3xur6a"
frontend/create_schema.html
```

Código:

```html
<!DOCTYPE html>

<html>

<head>

<title>Create Schema</title>

<script src="api.js"></script>

</head>

<body>

<h2>Create Table Schema</h2>

<input id="tableName" placeholder="Table Name">

<br>

<textarea id="columns" placeholder='Columns JSON'></textarea>

<br>

<button onclick="create()">Create</button>

<script>

async function create(){

const table = document.getElementById("tableName").value;

const columns = JSON.parse(

document.getElementById("columns").value

);

const schema = {

table_name: table,

columns: columns

};

const result = await createSchema(schema);

console.log(result);

alert("Schema created");

}

</script>

</body>

</html>
```

Ejemplo para pegar en columns:

```id="g4kwh8"
[
{
"name":"id",
"datatype":"integer",
"required":true,
"unique":true
},
{
"name":"email",
"datatype":"string",
"required":true,
"unique":true
}
]
```

---

# 📂 Paso 6 — Página para validar CSV

Archivo:

```id="4cvcro"
frontend/validate_csv.html
```

Código:

```html
<!DOCTYPE html>

<html>

<head>

<title>Validate CSV</title>

<script src="api.js"></script>

</head>

<body>

<h2>Validate CSV</h2>

<input id="table" placeholder="Table name">

<br>

<input type="file" id="file">

<br>

<button onclick="validate()">Validate</button>

<script>

async function validate(){

const table = document.getElementById("table").value;

const file = document.getElementById("file").files[0];

const result = await validateCSV(table,file);

console.log(result);

alert(JSON.stringify(result));

}

</script>

</body>

</html>
```

---

# 📥 Paso 7 — Página para insertar datos

Archivo:

```id="4s2dtj"
frontend/insert_data.html
```

Código:

```html
<!DOCTYPE html>

<html>

<head>

<title>Insert Data</title>

<script src="api.js"></script>

</head>

<body>

<h2>Insert Data</h2>

<input id="table" placeholder="Table name">

<br>

<textarea id="data" placeholder='JSON data'></textarea>

<br>

<button onclick="insert()">Insert</button>

<script>

async function insert(){

const table = document.getElementById("table").value;

const data = JSON.parse(

document.getElementById("data").value

);

const result = await insertData(table,data);

console.log(result);

alert("Data inserted");

}

</script>

</body>

</html>
```

Ejemplo de data:

```id="8z3hn1"
{
"id":1,
"email":"user@mail.com"
}
```

---

# 🚀 Paso 8 — Ejecutar frontend

No hace falta servidor.

Simplemente abrir:

```id="myo83j"
frontend/index.html
```

en el navegador.

El frontend se conectará a:

```id="s8s69g"
http://127.0.0.1:8000
```

---

# 🧪 Flujo de prueba completo

1️⃣ Crear schema
2️⃣ Insertar datos
3️⃣ Validar CSV

Esto probará **todo el sistema end-to-end**.

---

# 📈 Qué logramos con este sprint

Ahora Kaia tiene:

* **Backend API**
* **Motor de validación**
* **Almacenamiento de datos**
* **Interfaz web**

Esto lo acerca a una **plataforma de datos usable por analistas**.

---

# 🚀 Próximo Sprint (muy importante)

El siguiente paso será:

## **Sprint 7 — Upload masivo de datasets**

Permitirá:

* Subir **CSV o Excel**
* Insertar **miles de registros**
* Validar automáticamente

Esto transformará Kaia en **una plataforma de ingestión de datos**.

---
