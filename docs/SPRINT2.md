# Kaia Data Validator

## Sprint 2 — Data Validation Engine (Core Feature)

### Introducción

Durante el Sprint 1 se construyó la base técnica del proyecto. Se creó la estructura del backend, se configuró el entorno de desarrollo y se implementó una API inicial utilizando FastAPI. El sistema ya puede ejecutarse localmente, tiene endpoints organizados y permite subir archivos mediante una API.

El **Sprint 2** marca el *inicio del desarrollo de la funcionalidad principal del producto*. En este sprint se comenzará a construir el **motor de validación de archivos**, que será el núcleo del sistema. Este motor analizará archivos cargados por el usuario y verificará si cumplen ciertas reglas estructurales.

El problema que se busca resolver es común en muchos proyectos de datos. Las organizaciones suelen cargar información mediante archivos Excel o CSV que pueden contener errores humanos, como nombres de columnas incorrectos, columnas faltantes, datos vacíos o tipos de datos inconsistentes. Estos errores terminan rompiendo pipelines de datos, dashboards o procesos de transformación.

El objetivo del motor de validación es detectar estos problemas antes de que los archivos ingresen a un sistema analítico o pipeline de datos.

---

# Objetivo del Sprint 2

El objetivo principal del Sprint 2 es implementar la primera versión funcional del motor de validación de archivos.

Al finalizar este sprint el sistema deberá poder:

- recibir un archivo CSV mediante la API
- leer el contenido del archivo
- analizar su estructura
- verificar si las columnas cumplen un esquema esperado
- identificar errores básicos de calidad de datos
- devolver un reporte de validación en formato JSON

Este motor será la primera pieza real de valor del producto.

---

# Alcance funcional del Sprint 2

La primera versión del validador no será compleja. Se enfocará en validaciones estructurales básicas.

Las validaciones que se implementarán son:

- validación de nombres de columnas
- validación de columnas obligatorias
- detección de columnas faltantes
- detección de columnas inesperadas
- detección de valores nulos
- conteo de registros

El objetivo no es cubrir todos los casos posibles, sino crear una base sobre la cual se puedan agregar nuevas reglas de validación en el futuro.

---

# Arquitectura del motor de validación

Para mantener una arquitectura clara, el motor de validación no se implementará directamente dentro del endpoint de la API. En su lugar se creará un módulo dentro de la carpeta services.

La **carpeta services** contendrá la lógica principal del sistema.

El flujo de ejecución será el siguiente.

- El usuario envía un archivo CSV mediante el endpoint de validación.
- El endpoint recibe el archivo y lo envía al servicio de validación.
- El servicio analiza el archivo y ejecuta distintas reglas.
- El servicio genera un resultado de validación.
- La API devuelve el resultado al usuario.

Este diseño permite separar claramente la capa de API de la lógica de negocio.

---

# Cambios en la estructura del proyecto

Durante este sprint se agregará el primer servicio dentro de la carpeta **services**.

La estructura del backend quedará de la siguiente forma.

```id="ejx4o1"
backend/
  app/
    api/
      endpoints/
        health.py
        validation.py

    services/
      csv_validator.py

    schemas/
      validation_schema.py
```

Se crearán dos nuevos componentes.
- Un *servicio* encargado de validar archivos CSV.
- Un *esquema* que definirá la estructura del resultado de validación.

---

# Diseño del motor de validación

El **motor de validación** funcionará en tres etapas.

- Primero se leerá el archivo CSV utilizando una librería de Python.

- Luego se extraerá la estructura del archivo, es decir los nombres de las columnas y el número de registros.

- Finalmente se ejecutarán distintas reglas de validación.

Cada regla evaluará un aspecto específico del archivo y generará un resultado.

Por ejemplo, una regla puede verificar si todas las columnas obligatorias están presentes.

Otra regla puede verificar si existen valores nulos en columnas críticas.

El resultado final será un objeto que contenga información sobre si el archivo es válido y qué errores fueron encontrados.

---

# Estructura del resultado de validación

El sistema devolverá un **objeto JSON** con información sobre el análisis del archivo.

Ejemplo conceptual del resultado:

```json
{
  "valid": false,
  "row_count": 150,
  "columns_detected": ["id", "name", "email"],
  "missing_columns": ["created_at"],
  "unexpected_columns": [],
  "null_values": {
    "email": 3
  }
}
```

Este resultado permitirá al usuario entender rápidamente si el archivo cumple con los requisitos esperados.

---

# Tareas técnicas del Sprint 2

1) La primera tarea consiste en **crear el archivo del servicio de validación** dentro de la carpeta **services**.
El archivo se llamará **csv_validator.py** y contendrá la lógica para analizar archivos CSV.
Dentro de este archivo se implementará una función principal encargada de ejecutar el proceso de validación.

Esta función recibirá el archivo cargado por el usuario y devolverá un resultado estructurado.

### Pasos:
El primer paso consiste en crear el archivo que contendrá la lógica principal de validación de archivos.

Este archivo se ubicará en la carpeta services del backend.

**Ruta del archivo:**
```
backend/app/services/csv_validator.py
```
Si la carpeta services todavía está vacía, simplemente crea el archivo dentro de ella.

Este archivo será responsable de ejecutar todo el proceso de validación.

Primero crea el archivo **csv_validator.py** y agrega el siguiente código base.

```python
import pandas as pd
from typing import Dict, Any

def validate_csv(file) -> Dict[str, Any]:

    result = {
        "valid": True,
        "row_count": 0,
        "columns_detected": [],
        "missing_columns": [],
        "unexpected_columns": [],
        "null_values": {}
    }

    return result
```

Este código crea una función llamada **validate_csv** que recibirá el archivo enviado por el usuario y devolverá un resultado estructurado en formato diccionario.

Este diccionario será el reporte de validación que luego devolverá la API.

En este momento el código todavía no analiza el archivo. Eso se implementará en las siguientes tareas.

---

2) La segunda tarea será definir el **esquema de respuesta de validación** dentro de la carpeta **schemas**.
Este esquema utilizará **Pydantic** para definir la estructura del resultado de validación.

Esto permitirá que FastAPI valide automáticamente las respuestas del sistema.

### Pasos:
Ahora se debe definir formalmente la estructura de respuesta de la API.

Esto se hace utilizando Pydantic, que es la librería que utiliza FastAPI para validar estructuras de datos.

**Primero crea el archivo:**
```
backend/app/schemas/validation_schema.py
```
Dentro de este archivo define el modelo de respuesta.

```python
from pydantic import BaseModel
from typing import List, Dict


class ValidationResult(BaseModel):

    valid: bool
    row_count: int
    columns_detected: List[str]
    missing_columns: List[str]
    unexpected_columns: List[str]
    null_values: Dict[str, int]
```

Este modelo define exactamente qué campos devolverá el sistema cuando se valide un archivo.

FastAPI utilizará este modelo para garantizar que todas las respuestas tengan el formato correcto.

Esto también mejora la documentación automática de la API.

---

3) La tercera tarea será **modificar el endpoint de validación** para utilizar el servicio de validación.
Actualmente el endpoint solo devuelve el nombre del archivo.

En este sprint el endpoint deberá enviar el archivo al servicio y devolver el resultado generado por el validador.

### Pasos:

Ahora se debe modificar el endpoint que recibe archivos para que utilice el motor de validación.

Abre el archivo:
```
backend/app/api/endpoints/validation.py
```
El código actual probablemente se vea similar a esto.

```python
from fastapi import APIRouter, UploadFile, File

router = APIRouter()

@router.post("/")
async def validate_file(file: UploadFile = File(...)):
    return {
        "filename": file.filename
    }
```

Este endpoint actualmente solo devuelve el nombre del archivo.

Ahora se debe modificar para utilizar el servicio de validación.

Primero importa el servicio y el esquema.

```python
from fastapi import APIRouter, UploadFile, File
from app.services.csv_validator import validate_csv
from app.schemas.validation_schema import ValidationResult
```

Luego modifica el endpoint para que utilice el motor de validación.

```python
@router.post("/", response_model=ValidationResult)
async def validate_file(file: UploadFile = File(...)):

    result = await validate_csv(file)

    return result
```

Con esto el endpoint ahora ejecutará el servicio de validación y devolverá el resultado.

---

4) La cuarta tarea será implementar la **lectura de archivos CSV** utilizando una librería de Python.
La opción más simple es utilizar la librería estándar **csv** o la librería **pandas**.

Para la primera versión del sistema se recomienda utilizar pandas porque facilita el análisis de datos tabulares.

### Pasos:

Ahora se implementará la lógica para leer el archivo utilizando pandas.

Abre nuevamente el archivo:
```
backend/app/services/csv_validator.py
```
Primero importa pandas si todavía no está importado.

```python
import pandas as pd
```

Ahora modifica la función validate_csv para que lea el archivo.

```python
async def validate_csv(file):

    df = pd.read_csv(file.file)

    result = {
        "valid": True,
        "row_count": len(df),
        "columns_detected": list(df.columns),
        "missing_columns": [],
        "unexpected_columns": [],
        "null_values": {}
    }

    return result
```

Aquí se utiliza pandas para leer el archivo CSV.

- **pandas** convierte automáticamente el archivo en una estructura llamada **DataFrame** que permite analizar fácilmente filas y columnas.

El sistema ahora detecta automáticamente:
- cantidad de registros
- nombres de columnas

Esto ya representa el primer análisis real del archivo.

Si pandas todavía no está instalado debes agregarlo a las dependencias.

Ejecuta dentro del entorno virtual:

```
pip install pandas
```

Luego actualiza requirements.txt:

```
pip freeze > requirements.txt
```

---

5) La quinta tarea será implementar las **primeras reglas de validación**.
Estas reglas *analizarán la estructura del archivo* y *generarán un reporte de errores*.

Cada regla debe ser lo suficientemente simple como para extenderse en el futuro.

### Pasos:

Ahora se implementarán las primeras reglas de validación.

Dentro del archivo **csv_validator.py** agrega una lista de columnas esperadas.

```python
EXPECTED_COLUMNS = [
    "id",
    "name",
    "email",
    "created_at"
]
```

Ahora agrega lógica para detectar columnas faltantes.

```python
missing_columns = []

for column in EXPECTED_COLUMNS:
    if column not in df.columns:
        missing_columns.append(column)
```

Luego agrega detección de columnas inesperadas.

```python
unexpected_columns = []

for column in df.columns:
    if column not in EXPECTED_COLUMNS:
        unexpected_columns.append(column)
```

Luego agrega detección de valores nulos.

```python
null_values = {}

for column in df.columns:
    null_count = df[column].isnull().sum()

    if null_count > 0:
        null_values[column] = int(null_count)
```

Finalmente integra estos resultados dentro del reporte.

```python
result = {
    "valid": len(missing_columns) == 0,
    "row_count": len(df),
    "columns_detected": list(df.columns),
    "missing_columns": missing_columns,
    "unexpected_columns": unexpected_columns,
    "null_values": null_values
}
```

Esto completa la primera versión del motor de validación.

---

6) La sexta tarea será **probar el sistema** utilizando la *interfaz de documentación automática de FastAPI*.

Se cargarán archivos de prueba para verificar que el sistema detecta correctamente errores estructurales.

### Pasos:

Ahora se debe probar el sistema utilizando la documentación automática de FastAPI.

Primero levanta el servidor desde la carpeta backend.

```
uvicorn app.main:app --reload
```

Luego abre el navegador y accede a:

http://localhost:8000/docs

Esta página mostrará la interfaz de Swagger generada automáticamente por FastAPI.

Busca el endpoint:
```
POST /validation
```
Haz clic en el botón "Try it out".

Carga un archivo CSV de prueba.

Un ejemplo simple de archivo puede ser:

```
id,name,email
1,Ana,ana@email.com
2,Carlos,
3,Laura,laura@email.com
```

Cuando envíes el archivo, el sistema analizará su estructura y devolverá un reporte de validación.

Ejemplo de respuesta:

```json
{
  "valid": false,
  "row_count": 3,
  "columns_detected": ["id", "name", "email"],
  "missing_columns": ["created_at"],
  "unexpected_columns": [],
  "null_values": {
    "email": 1
  }
}
```

Esto significa que el sistema detectó que falta una columna esperada y que existe un valor nulo en la columna email.

Esto es simplemente para:

- entender la arquitectura
- probar lectura de archivos
- probar reglas de validación
- probar endpoints

No es el producto final.

---

# Resultado esperado del Sprint 2

Al finalizar este sprint el sistema tendrá por primera vez una funcionalidad completa.

Un usuario podrá subir un archivo CSV mediante la API y recibir un reporte automático de validación.

Este reporte indicará si el archivo cumple o no con el esquema esperado.

Esto representa el primer paso hacia un sistema de validación de datos que puede integrarse en pipelines de datos o procesos de ingestión.

---

# Valor del producto en esta etapa

Aunque el sistema todavía estará en una fase temprana, el motor de validación ya podrá demostrar el valor del producto.

Muchas organizaciones enfrentan problemas causados por archivos mal estructurados.

Un sistema como Kaia Data Validator permite detectar estos problemas antes de que afecten dashboards, pipelines o procesos analíticos.

Este tipo de herramientas forma parte de la categoría conocida como Data Quality Tools.

---

# Próximos pasos futuros

Una vez que el motor básico esté funcionando, se podrán agregar nuevas capacidades.

Entre ellas se encuentran:

- validaciones de tipo de dato
- validaciones de formato
- comparación contra esquemas guardados
- historial de validaciones
- interfaz web para cargar archivos
- integración con almacenamiento en la nube

Estos componentes permitirán transformar el proyecto en una herramienta más completa para equipos de datos.

El Sprint 2 representa el primer paso hacia ese objetivo.
