# Schema Creation - Debugging & Fixes

## Problemas Encontrados

### 1. **Tipo de dato `bool` no soportado** ❌
- **Problema**: El frontend permitía seleccionar `bool` como tipo de dato, pero el validador backend solo aceptaba `string`, `integer`, y `float`
- **Resultado**: La validación fallaba silenciosamente cuando se creaba un schema con columnas de tipo `bool`
- **Solución**: Agregué `bool` a `ALLOWED_TYPES` en `validator_schema.py`

```python
# Antes:
ALLOWED_TYPES = {"string", "integer", "float"}

# Después:
ALLOWED_TYPES = {"string", "integer", "float", "bool"}
```

---

### 2. **Sin manejo de errores en el frontend** ❌
- **Problema**: El código frontend no validaba si la respuesta fue exitosa
- **Resultado**: Si la creación fallaba (error 422, 500, etc.), el alert seguía diciendo "Schema created!"
- **Solución**: Agregué validación de `response.ok` antes de procesar la respuesta

```javascript
// Ahora el frontend valida la respuesta:
if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || "Failed to create schema");
}
```

---

### 3. **Sin verificación de que el schema se guardó** ❌
- **Problema**: El frontend creaba el schema pero nunca verificaba que realmente se guardó
- **Resultado**: El usuario no sabía si el schema se guardó correctamente
- **Solución**: Agregué una función `getSchemasAPI()` y la llamo después de crear el schema

```javascript
// Nuevo flujo:
1. Crear schema
2. Si es exitoso, obtener lista de schemas
3. Mostrar en consola para verificación
```

---

### 4. **Sin validación de campos vacíos** ❌
- **Problema**: El frontend permitía enviar un schema sin nombre de tabla o columnas sin nombre
- **Resultado**: Errores confusos al usuario
- **Solución**: Agregué validaciones locales en el frontend antes de enviar

```javascript
if (!tableName.trim()) {
    alert("Table name is required");
    return;
}
```

---

## Cambios Realizados

### Backend
- **Archivo**: `backend/app/validator/validator_schema.py`
  - ✅ Agregué `"bool"` a `ALLOWED_TYPES`

### Frontend
- **Archivo**: `frontend/api.js`
  - ✅ Mejoré `createSchemaAPI()` con validación de respuesta
  - ✅ Agregué función `getSchemasAPI()` para obtener lista de schemas
  - ✅ Mejoré `createSchema()` con try-catch y validaciones locales

---

## Flujo Correcto (Ahora)

```
Usuario completa formulario
        ↓
Frontend valida campos locales (table_name, column_names)
        ↓
Frontend envía POST /schemas con payload
        ↓
Backend recibe y valida en validator_schema.py
        ↓
Si la validación falla → Backend devuelve error 422
        ↓
Si la validación es exitosa → Se guarda en schemas_db
        ↓
Backend devuelve el schema creado
        ↓
Frontend obtiene lista de schemas con GET /schemas
        ↓
Usuario ve confirmación y consola muestra todos los schemas
```

---

## Cómo Verificar que Funciona

1. **Inicia el servidor backend**:
   ```bash
   cd backend
   uvicorn app.main:app --reload
   ```

2. **Abre el frontend** en `http://localhost:8000/create_schema.html` (o donde esté almacenado)

3. **Crea un schema**:
   - Nombre de tabla: `customers`
   - Añade columnas: `id` (integer), `email` (string), `name` (string)
   - Haz click en "Create Schema"

4. **Verifica en la consola del navegador** (F12):
   - Deberías ver: `Stored schemas: ["customers"]`
   - Si hay error, verás el mensaje de error específico

5. **Verifica en la consola del servidor**:
   - Deberías ver: `Stored schemas: {'customers': TableSchema(...)}`

---

## Notas Importantes

- Los schemas se almacenan en **memoria** (`schemas_db`), **NO en base de datos**
- Si reinician el servidor, **SE PIERDEN TODOS LOS SCHEMAS**
- En sprints futuros, esto debe migrarse a BigQuery, PostgreSQL o Firestore
- El diccionario `schemas_db` está en `backend/app/services/services_schema.py`

---

## Testing Recomendado

- [ ] Crear schema con tipo `bool`
- [ ] Crear schema sin nombre de tabla (debe rechazar)
- [ ] Crear schema sin columnas (backend rechaza)
- [ ] Crear schema con columnas duplicadas (backend rechaza)
- [ ] Crear múltiples schemas y verificar que aparecen en GET /schemas
