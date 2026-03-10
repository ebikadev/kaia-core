# Sprint 4 — CSV Validation Engine

## Objetivo del Sprint

En este sprint se construirá el **motor real de validación de archivos CSV utilizando los schemas definidos por el usuario**.  
Hasta ahora el sistema permite:

- Crear **schemas de tablas dinámicos**
- Definir **columnas, tipos, campos requeridos y campos únicos**

Sin embargo, el validador todavía **no utiliza esos schemas para validar archivos**.

El objetivo del Sprint 4 es **conectar todo el sistema** para permitir el siguiente flujo:

1. El usuario **crea un schema de tabla** desde la API.
2. El usuario **sube un archivo CSV para validarlo**.
3. El sistema **busca el schema correspondiente**.
4. El sistema **valida el CSV contra ese schema**.
5. El sistema **genera un reporte de errores estructurado**.

Este sprint es fundamental porque transforma el proyecto en **una herramienta de validación de datos dinámica**.

---

# Flujo final del sistema

Una vez completado el Sprint 4, el flujo de uso será:

1. Crear schema

```
POST /schemas
```

2. Subir CSV para validar

```
POST /validation/{table_name}
```

Ejemplo:

```
POST /validation/customers
```

3. El backend ejecuta:

- carga del CSV
- lectura del schema
- validación de reglas
- generación del reporte

---

# Tareas técnicas del Sprint

## Tarea 1 — Implementar servicio para obtener schemas

### Objetivo

El validador debe poder **recuperar el schema de una tabla existente**.

Actualmente los schemas se guardan en memoria, pero aún **no existe una función para consultarlos**.

### Archivo

```
app/services/schema_service.py
```

### Implementar

Una función para obtener el schema por nombre de tabla.

```
get_schema(table_name: str)
```

Esta función deberá:

**1. Buscar el schema en el almacenamiento en memoria:** 
*(diccionario de Python que vive dentro del servidor)*
```
app/services/schema_service.py
```
**2. Devolver el schema correspondiente**
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
**3. Lanzar un error si el schema no existe**
```python
def get_schema(table_name: str):
    if not schemas_db:
        print("El schema no existe, ver en models > table_schema.py")
    else:
        return schemas_db.get(table_name)
```

Esto permitirá que el validador pueda **cargar las reglas de validación dinámicamente**.

---

## Tarea 2 — Crear módulo de validación basado en schemas

### Objetivo

Actualizar el servicio de validación para que **utilice las reglas definidas en el schema**.

Hasta ahora el validador usa columnas esperadas fijas.

Esto debe eliminarse y reemplazarse por **columnas definidas dinámicamente por el usuario**.

### Archivo

```
app/services/csv_validator.py
```

El validador deberá recibir:

- archivo CSV
- schema de la tabla

```
validate_csv(file, schema)
```

El proceso de validación será:

1. Leer el CSV
2. Extraer columnas
3. Comparar contra el schema
4. Aplicar reglas de validación

---

# Tarea 3 — Implementar lectura de CSV con Pandas

### Objetivo

Convertir el archivo CSV en un **DataFrame de Pandas** para facilitar la validación.

### Librería utilizada

```
pandas
```

### Proceso

1. Recibir archivo desde FastAPI
2. Convertir archivo a buffer
3. Leer CSV con pandas

Ejemplo conceptual:

```
df = pandas.read_csv(file)
```

Esto permitirá aplicar validaciones fácilmente:

- columnas
- valores nulos
- duplicados
- tipos

---

# Tarea 4 — Validar estructura de columnas

### Objetivo

Verificar que el CSV contenga **las columnas definidas en el schema**.

El sistema debe detectar:

- columnas faltantes
- columnas inesperadas

### Proceso

1. Obtener columnas del CSV
2. Obtener columnas del schema
3. Comparar ambas listas

Si existen columnas faltantes se debe agregar un error al reporte.

---

# Tarea 5 — Validar campos requeridos

### Objetivo

Verificar que los campos marcados como **required** no contengan valores nulos.

### Regla

Para cada columna del schema:

Si:

```
column.required == True
```

Entonces:

Verificar que el DataFrame **no tenga valores nulos en esa columna**.

Si existen nulos:

Agregar error al reporte.

---

# Tarea 6 — Validar campos únicos

### Objetivo

Verificar que columnas marcadas como **unique** no contengan duplicados.

### Regla

Para cada columna del schema:

```
column.unique == True
```

Validar:

```
df[column].duplicated()
```

Si existen duplicados:

Agregar error al reporte.

---

# Tarea 7 — Validar tipos de datos

### Objetivo

Comparar los tipos definidos en el schema contra los valores del CSV.

### Tipos soportados inicialmente

El sistema soportará tres tipos simples:

```
string
integer
float
```

### Proceso

Para cada columna:

1. Obtener tipo definido en el schema
2. Intentar convertir valores

Ejemplo:

```
astype(int)
```

Si ocurre error:

registrar problema en el reporte.

Esta validación permitirá detectar errores comunes como:

```
"abc" en una columna integer
```

## Código final de csv_validator.py

```
app/services/csv_validator.py
```
**CSV Validation Engine**

Este módulo contiene la lógica principal para validar archivos CSV
utilizando los schemas definidos por el usuario.

El flujo general es:

**1. Recibir archivo CSV**
**2. Leerlo con pandas**
**3. Validar estructura de columnas**
**4. Validar campos requeridos**
**5. Validar campos únicos**
**6. Validar tipos de datos**
**7. Generar reporte de errores**

```python
import pandas as pd
from typing import List, Dict


def validate_csv(file, schema):
    """
    Función principal del validador.

    Recibe:
    - file: archivo CSV subido por el usuario
    - schema: schema de la tabla definido previamente

    Devuelve:
    - reporte de validación estructurado
    """

    errors: List[Dict] = []

    # -----------------------------------------------------------
    # PASO 1 — Leer el archivo CSV utilizando pandas
    # -----------------------------------------------------------

    try:
        # pandas necesita leer el archivo como un buffer
        df = pd.read_csv(file.file)
    except Exception as e:
        return {
            "table": schema.table_name,
            "rows": 0,
            "errors": 1,
            "details": [
                {
                    "column": None,
                    "error": f"Error reading CSV file: {str(e)}"
                }
            ]
        }

    # Cantidad total de filas analizadas
    total_rows = len(df)

    # -----------------------------------------------------------
    # PASO 2 — Obtener columnas del schema
    # -----------------------------------------------------------

    schema_columns = [col.name for col in schema.columns]

    # Columnas presentes en el CSV
    csv_columns = df.columns.tolist()

    # -----------------------------------------------------------
    # PASO 3 — Validar estructura de columnas
    # -----------------------------------------------------------

    # Columnas que deberían existir pero no están
    missing_columns = set(schema_columns) - set(csv_columns)

    for col in missing_columns:
        errors.append({
            "column": col,
            "error": "Missing required column in CSV"
        })

    # Columnas inesperadas
    unexpected_columns = set(csv_columns) - set(schema_columns)

    for col in unexpected_columns:
        errors.append({
            "column": col,
            "error": "Unexpected column found in CSV"
        })

    # Si faltan columnas críticas, continuar validando puede ser peligroso
    # pero lo permitimos para mostrar todos los errores posibles.

    # -----------------------------------------------------------
    # PASO 4 — Validar campos requeridos (required=True)
    # -----------------------------------------------------------

    for column in schema.columns:

        # Solo validar columnas existentes
        if column.name not in df.columns:
            continue

        if column.required:

            # Detectar valores nulos
            null_count = df[column.name].isnull().sum()

            if null_count > 0:
                errors.append({
                    "column": column.name,
                    "error": f"{null_count} missing values in required column"
                })

    # -----------------------------------------------------------
    # PASO 5 — Validar campos únicos (unique=True)
    # -----------------------------------------------------------

    for column in schema.columns:

        if column.name not in df.columns:
            continue

        if column.unique:

            duplicated_count = df[column.name].duplicated().sum()

            if duplicated_count > 0:
                errors.append({
                    "column": column.name,
                    "error": f"{duplicated_count} duplicated values found"
                })

    # -----------------------------------------------------------
    # PASO 6 — Validar tipos de datos
    # -----------------------------------------------------------

    for column in schema.columns:

        if column.name not in df.columns:
            continue

        col_series = df[column.name]

        if column.datatype == "integer":

            # Intentar convertir a entero
            try:
                col_series.astype("Int64")
            except Exception:
                errors.append({
                    "column": column.name,
                    "error": "Invalid integer values detected"
                })

        elif column.datatype == "float":

            try:
                col_series.astype(float)
            except Exception:
                errors.append({
                    "column": column.name,
                    "error": "Invalid float values detected"
                })

        elif column.datatype == "string":

            # Los strings generalmente no fallan
            # pero verificamos que no sean estructuras raras
            if not col_series.map(lambda x: isinstance(x, str) or pd.isna(x)).all():
                errors.append({
                    "column": column.name,
                    "error": "Invalid string values detected"
                })

    # -----------------------------------------------------------
    # PASO 7 — Construir reporte final
    # -----------------------------------------------------------

    result = {
        "table": schema.table_name,
        "rows": total_rows,
        "errors": len(errors),
        "details": errors
    }

    return result
```

---

# Tarea 8 — Crear estructura de reporte de validación

### Objetivo

El resultado de la validación debe ser **un objeto estructurado y consistente**.

Se definirá un schema de respuesta utilizando **Pydantic**.

### Archivo

```
app/schemas/validation_result.py
```

La respuesta incluirá:

- nombre de tabla
- número de filas analizadas
- número de errores
- lista de errores detectados

Cada error debe incluir:

- tipo de error
- columna afectada
- descripción

Esto permite que el frontend o el usuario **interpreten fácilmente los resultados**.

---

# Tarea 9 — Actualizar endpoint de validación

### Objetivo

Actualizar el endpoint existente para que utilice el nuevo validador.

### Archivo

```
app/api/endpoints/validation.py
```

### Endpoint final

```
POST /validation/{table_name}
```

### Flujo interno

El endpoint deberá:

1. recibir archivo CSV
2. obtener el schema de la tabla
3. ejecutar el validador
4. devolver el reporte

Flujo:

```
CSV → Validator → Reporte
```

---

# Tarea 10 — Probar el sistema completo

### Objetivo

Validar que el sistema funciona correctamente desde Swagger.

### Paso 1 — Crear schema

```
POST /schemas
```

Ejemplo:

```
customers
```

con columnas:

```
id
email
name
```

---

### Paso 2 — Crear archivo CSV de prueba

Ejemplo válido:

```
id,email,name
1,test@test.com,John
2,user@mail.com,Ana
```

Ejemplo con errores:

```
id,email,name
1,test@test.com,John
1,test@test.com,Ana
,missing@email.com,Pedro
```

Errores esperados:

- duplicado en id
- valor requerido faltante

---

### Paso 3 — Ejecutar validación

```
POST /validation/customers
```

Subiendo el archivo CSV.

---

# Resultado esperado

El sistema devolverá un reporte similar a:

```
{
  "table": "customers",
  "rows": 3,
  "errors": 2,
  "details": [
    {
      "column": "id",
      "error": "duplicate values detected"
    },
    {
      "column": "id",
      "error": "missing required values"
    }
  ]
}
```

---

# Resultado del Sprint

Al finalizar este sprint el sistema tendrá:

- schemas dinámicos
- carga de CSV
- validación automática
- reglas configurables
- reporte estructurado de errores

Esto convierte el proyecto en **un motor básico de validación de datos basado en schemas**.

En el siguiente sprint se avanzará hacia:

- persistencia de schemas en base de datos
- versionado de schemas
- mejoras en el motor de reglas
- preparación para interfaz de usuario