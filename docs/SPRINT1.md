# Kaia Core

## Sprint 1 — Backend Foundation

### Introducción

Este documento describe todo el trabajo realizado durante el Sprint 1 del proyecto Kaia Data Validator. El objetivo de este sprint fue construir la base técnica del sistema, creando la estructura del proyecto, configurando el entorno de desarrollo y desarrollando un backend inicial utilizando FastAPI.

El propósito de este sprint no es todavía implementar la lógica de validación de archivos, sino construir una base sólida y profesional sobre la cual se desarrollará el resto del producto. En proyectos reales de software, esta etapa es fundamental porque define cómo se organizará el código, cómo se ejecutará el backend y cómo se estructurará la API que utilizarán los usuarios o el frontend.

Este sprint corresponde a la fase de “Foundation” del sistema.

---

# Objetivo del Sprint 1

El objetivo principal fue crear un backend funcional que permita:

1- levantar un servidor API
2- tener endpoints iniciales funcionando
3- poder subir archivos desde una API
4- definir una arquitectura de proyecto clara

Al finalizar este sprint el sistema ya puede ejecutarse localmente y expone una API documentada automáticamente.

---

# Estructura del Proyecto

Se creó la siguiente estructura base del repositorio.

```
kaia-data-core/

backend/
    app/
        main.py
        api/
            router.py
            endpoints/
                health.py
                validation.py
        models/
        schemas/
        services/
        db/
        core/

    requirements.txt
    venv/

frontend/

infra/

.gitignore
README.md
```

Esta estructura separa claramente las distintas partes del sistema.

- backend contiene el servidor API.
- frontend contendrá más adelante la interfaz web.
- infra contendrá la infraestructura como código.

En este sprint solo trabajamos en el backend.

---

# Configuración del entorno de desarrollo

Se creó un entorno virtual de Python dentro de la carpeta backend utilizando el siguiente comando.

```
python -m venv venv
```

Un entorno virtual permite aislar las dependencias del proyecto para evitar conflictos con otras instalaciones de Python en el sistema.

Luego se activó el entorno virtual y se instalaron las dependencias necesarias para construir la API.

Dependencias instaladas:

- FastAPI
- Uvicorn
- Pydantic
- python-multipart

**FastAPI** es el framework que utilizamos para construir la API.
**Uvicorn** es el servidor que ejecuta la aplicación.
**Pydantic** se utiliza para validar datos en la API.
**python-multipart** permite subir archivos a través de requests HTTP.

Las dependencias se guardaron en el archivo requirements.txt utilizando el comando:

```
pip freeze > requirements.txt
```

Este archivo permite recrear el entorno del proyecto en cualquier máquina.

---

# Archivo .gitignore

Se creó un archivo **.gitignore** en la raíz del proyecto para evitar que ciertos archivos innecesarios o sensibles se suban al repositorio.

Ejemplos de elementos ignorados:

- entorno virtual (venv)
- archivos temporales de Python
- node_modules
- variables de entorno

Esto es una práctica estándar en proyectos de software.

---

# Arquitectura del Backend

El backend se organizó siguiendo una arquitectura común en aplicaciones FastAPI.

La carpeta principal del código es:
```bash
backend/app
```
Dentro de ella se encuentran los distintos componentes del backend.

---

# main.py

Este archivo es el **punto de entrada** de la aplicación.

Cuando el servidor se ejecuta, FastAPI inicia desde este archivo.

Aquí se crea la instancia principal de la aplicación y se registran las rutas del sistema.

Ejemplo simplificado:

```python
from fastapi import FastAPI
from app.api.router import api_router

app = FastAPI(
    title="Kaia Data Validator",
    version="0.1"
)

app.include_router(api_router)
```

---

# Carpeta api

Esta carpeta contiene todos los **endpoints HTTP** del sistema.

Los **endpoints** son las rutas que los usuarios o el frontend utilizan para interactuar con el backend.

Ejemplos de endpoints:
```bash
/health
/validation
```
---

# router.py

Este archivo centraliza todas las **rutas de la API**.

En lugar de registrar endpoints directamente en main.py, se utilizan routers para organizar mejor el código.

Ejemplo:

```python
from fastapi import APIRouter
from app.api.endpoints import health, validation

api_router = APIRouter()

api_router.include_router(health.router, prefix="/health")
api_router.include_router(validation.router, prefix="/validation")
```

Esto permite agregar nuevos módulos de forma organizada.

---

# Carpeta endpoints

Aquí se implementan los **endpoints** reales de la API.

Cada archivo agrupa endpoints relacionados.

En este sprint se crearon dos:
```bash
health.py
validation.py
```
---

# Endpoint Health

El **endpoint health** se utiliza para verificar que el sistema esté funcionando correctamente.

Ruta:

```
GET /health
```

Código simplificado:

```python
from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def health_check():
    return {"status": "ok"}
```

Este endpoint devuelve una respuesta simple que indica que la API está activa.

Este tipo de endpoint se utiliza comúnmente en **sistemas de monitoreo**.

---

# Endpoint Validation

Este endpoint permite *subir archivos al sistema*.

Ruta:

```
POST /validation
```

Código simplificado:

```python
from fastapi import APIRouter, UploadFile, File

router = APIRouter()

@router.post("/")
async def validate_file(file: UploadFile = File(...)):
    return {
        "filename": file.filename
    }
```

Actualmente este endpoint solo recibe el archivo y devuelve su nombre.

En futuros sprints aquí se implementará el motor de validación de datos.

---

# Otras carpetas del backend

Se crearon varias carpetas adicionales para organizar el código a medida que el sistema crezca.

**models**
```bash
Contendrá los modelos de base de datos.
```
**schemas**
```bash
Definirá las estructuras de datos utilizadas por la API.
```
**services**
```bash
Contendrá la lógica principal del sistema, como el motor de validación de archivos.
```
**db**
```bash
Gestionará la conexión con la base de datos.
```
**core**
```bash
Contendrá configuraciones globales del sistema.
```
Aunque estas carpetas todavía no tienen código, se crearon desde el inicio para mantener una arquitectura clara.

---

# Ejecución del Backend

El servidor se ejecuta utilizando el siguiente comando:

```
uvicorn app.main:app --reload
```

**Explicación del comando:**
```bash
app.main: indica el archivo donde está definida la aplicación
app: es la variable que contiene la instancia de FastAPI
--reload: reinicia automáticamente el servidor cuando se modifica el código
```
Una vez iniciado el servidor, la API queda disponible en:

http://localhost:8000

---

# Documentación automática

FastAPI genera **documentación automática para la API**.

Se puede acceder a ella en:
```bash
http://localhost:8000/docs
```

Esta interfaz permite probar los endpoints directamente desde el navegador.

Esto es especialmente útil durante el desarrollo porque permite testear la API sin necesidad de un frontend.

---

# Resultado del Sprint 1

**Al finalizar este sprint se logró:**

* crear la estructura profesional del proyecto
* configurar el entorno de desarrollo
* instalar las dependencias del backend
* crear la aplicación FastAPI
* implementar endpoints iniciales
* habilitar subida de archivos
* generar documentación automática

Esto constituye la base del sistema.

---

# Próximos pasos

En el **Sprint 2** se comenzará a desarrollar la funcionalidad principal del producto.

Se implementará el motor de validación de archivos que permitirá:

- analizar archivos CSV
- validar estructura de columnas
- detectar errores de formato
- identificar valores faltantes
- verificar tipos de datos

Este motor será el núcleo del producto Kaia Data Validator y permitirá resolver uno de los problemas más comunes en proyectos de datos: la carga de archivos incorrectos o inconsistentes.
