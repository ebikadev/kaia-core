"""
¿Qué valida este código?
1- Columnas faltantes
        Si el schema dice:
            id
            email
            name
        
        y el CSV tiene: id,name
        
        El sistema devuelve: Missing column: email

2- Columnas inesperadas
        Si el CSV tiene: id,email,name,age
        pero el schema no define age.

        Se detecta: Unexpected column: age

3- Columnas obligatorias
        Si una columna tiene:
            required = true
        y no aparece en el CSV, se genera error.

4- Columnas únicas
        Si el schema dice: email -> unique
        y el CSV contiene:
            email
            test@mail.com
            test@mail.com

        Se detecta: Column 'email' contains duplicate values

5- Valores nulos
        Ejemplo CSV:
            id,email
            1,test@mail.com
            2,

        Resultado:
            null_values = {
                "email": 1
            }
"""

"""
app/services/csv_validator.py

CSV Validation Engine

Este módulo contiene la lógica principal para validar archivos CSV
utilizando los schemas definidos por el usuario.

El flujo general es:

1. Recibir archivo CSV
2. Leerlo con pandas
3. Validar estructura de columnas
4. Validar campos requeridos
5. Validar campos únicos
6. Validar tipos de datos
7. Generar reporte de errores
"""

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