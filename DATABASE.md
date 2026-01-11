# 📊 Guía de Base de Datos

Este documento explica cómo configurar y usar la base de datos Supabase (PostgreSQL) con el bot GUAPA.

## 🗄️ Estructura de la Base de Datos

El bot crea automáticamente la siguiente tabla:

### Tabla: `user_updates`

La base de datos almacena **únicamente** los días en que los usuarios usaron el comando `!actualizar`.

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `id` | SERIAL | ID único del registro (auto-incremento) |
| `user_id` | BIGINT | ID del usuario de Discord |
| `update_date` | DATE | Fecha (día) en que el usuario usó !actualizar |

**Restricciones:**
- `UNIQUE(user_id, update_date)` - Evita duplicados: un usuario solo puede actualizar una vez por día

**Índices:**
- `idx_user_id` en `user_id` (para búsquedas rápidas por usuario)
- `idx_update_date` en `update_date` (para ordenar por fecha)

## 🔧 Configuración con Supabase

### Paso 1: Crear cuenta y proyecto

1. Ve a [Supabase.com](https://supabase.com/)
2. Haz clic en "Start your project" y crea una cuenta gratuita
3. Crea un nuevo proyecto
4. Espera a que se complete la configuración (puede tardar unos minutos)

### Paso 2: Obtener credenciales de conexión

1. En el dashboard de Supabase, ve a **Settings** (⚙️) en el menú lateral
2. Selecciona **Database**
3. Desplázate hasta la sección **Connection string**
4. Selecciona la pestaña **URI** o **Connection parameters**

Verás algo como esto:

**Connection Parameters:**
```
Host: db.xxxxx.supabase.co
Database name: postgres
Port: 5432
User: postgres.xxxxx
Password: [tu contraseña]
```

**O Connection String:**
```
postgresql://postgres.xxxxx:[PASSWORD]@db.xxxxx.supabase.co:5432/postgres
```

### Paso 3: Configurar en el bot

Agrega estas credenciales a tu archivo `.env`:

```env
DB_HOST=db.xxxxx.supabase.co
DB_PORT=5432
DB_NAME=postgres
DB_USER=postgres.xxxxx
DB_PASSWORD=tu_contraseña_aqui
```

**Nota importante:** La contraseña se muestra solo una vez al crear el proyecto. Si la perdiste, puedes resetearla en Settings > Database > Reset database password.

### Paso 4: Verificar conexión

Al iniciar el bot, verás en los logs:

```
INFO - Pool de conexiones PostgreSQL (Supabase) creado exitosamente
INFO - Tabla user_updates verificada/creada exitosamente
INFO - Conexión a la base de datos exitosa
```

Si hay errores, revisa que:
- Las credenciales sean correctas
- El proyecto de Supabase esté activo
- La conexión use SSL (ya está configurado automáticamente)

## 🔒 Seguridad y SSL

Supabase requiere conexiones SSL. El bot está configurado para usar `sslmode=require` automáticamente, por lo que no necesitas configuración adicional.

## 📈 Funcionalidades

### Registro de actualizaciones

El bot registra **únicamente** cuando un usuario usa el comando `!actualizar`:
- Solo se guarda el **día** (fecha), no la hora
- Si un usuario usa `!actualizar` múltiples veces en el mismo día, solo se registra una vez
- Se almacena el `user_id` y la fecha de actualización

### Comandos relacionados

- `!actualizar` - Registra que el usuario actualizó hoy
  - Si ya actualizó hoy, muestra un mensaje informativo
  - Si es la primera vez del día, registra la actualización
  
- `!mystats` - Muestra estadísticas de actualizaciones del usuario
  - Total de días con actualizaciones
  - Primera actualización
  - Última actualización
  - Estado de hoy (si ya actualizó o no)
  - Últimas 5 fechas de actualización

## 🔍 Consultas SQL de ejemplo

Puedes ejecutar estas consultas directamente en el SQL Editor de Supabase:

### Usuarios con más actualizaciones

```sql
SELECT user_id, COUNT(*) as total_updates
FROM user_updates
GROUP BY user_id
ORDER BY total_updates DESC
LIMIT 10;
```

### Actualizaciones por día

```sql
SELECT update_date, COUNT(*) as usuarios_actualizados
FROM user_updates
GROUP BY update_date
ORDER BY update_date DESC
LIMIT 30;
```

### Usuarios que actualizaron hoy

```sql
SELECT user_id, update_date
FROM user_updates
WHERE update_date = CURRENT_DATE
ORDER BY user_id;
```

### Usuarios que nunca han actualizado

```sql
-- Esta consulta requiere conocer todos los user_ids
-- Se puede usar para comparar con una lista de miembros del servidor
SELECT user_id, MIN(update_date) as primera_actualizacion, COUNT(*) as total
FROM user_updates
GROUP BY user_id
ORDER BY primera_actualizacion;
```

### Racha de actualizaciones consecutivas

```sql
-- Usuarios con más días consecutivos de actualización
WITH ranked AS (
    SELECT 
        user_id,
        update_date,
        ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY update_date) as rn,
        update_date - ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY update_date)::int as grp
    FROM user_updates
)
SELECT 
    user_id,
    COUNT(*) as dias_consecutivos,
    MIN(update_date) as inicio_racha,
    MAX(update_date) as fin_racha
FROM ranked
GROUP BY user_id, grp
ORDER BY dias_consecutivos DESC
LIMIT 10;
```

## ⚠️ Notas importantes

- La base de datos es **opcional**. El bot funcionará sin ella
- Si la DB no está configurada, el comando `!actualizar` no guardará registros
- Solo se almacena el **día** (fecha), no la hora exacta
- Un usuario solo puede actualizar **una vez por día** (evita duplicados)
- El pool de conexiones maneja automáticamente las conexiones (máximo 5 simultáneas)
- Los errores de DB no detendrán el bot, solo se registrarán en los logs
- Supabase tiene un plan gratuito generoso (500 MB de base de datos, suficiente para este bot)

## 🛠️ Solución de problemas

### Error: "password authentication failed"

- Verifica que la contraseña sea correcta
- Si olvidaste la contraseña, reseteala en Supabase Dashboard > Settings > Database

### Error: "could not connect to server"

- Verifica que el host sea correcto (formato: `db.xxxxx.supabase.co`)
- Asegúrate de que el proyecto de Supabase esté activo
- Verifica que el puerto 5432 no esté bloqueado por firewall

### Error: "database does not exist"

- El nombre de la base de datos en Supabase siempre es `postgres`
- Verifica que estés usando `DB_NAME=postgres` en tu `.env`

### Error: "SSL connection required"

- El bot ya está configurado para usar SSL automáticamente
- Si ves este error, verifica que estés usando la última versión del código

### La tabla no se crea

- Verifica que el usuario tenga permisos (el usuario `postgres` tiene todos los permisos por defecto)
- Revisa los logs del bot para ver el error específico
- Puedes crear la tabla manualmente desde el SQL Editor de Supabase usando:

```sql
CREATE TABLE IF NOT EXISTS user_updates (
    id SERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL,
    update_date DATE NOT NULL,
    UNIQUE(user_id, update_date)
);

CREATE INDEX IF NOT EXISTS idx_user_id ON user_updates(user_id);
CREATE INDEX IF NOT EXISTS idx_update_date ON user_updates(update_date);
```

## 🎯 Ventajas de Supabase

- **Gratis**: Plan gratuito generoso (500 MB)
- **PostgreSQL**: Base de datos robusta y moderna
- **Dashboard**: Interfaz web para gestionar datos
- **SQL Editor**: Ejecuta consultas directamente desde el navegador
- **API REST**: Acceso adicional vía API REST (opcional)
- **Real-time**: Soporte para suscripciones en tiempo real (futuro)

## 📚 Recursos adicionales

- [Documentación de Supabase](https://supabase.com/docs)
- [Guía de PostgreSQL](https://www.postgresql.org/docs/)
- [SQL Editor de Supabase](https://supabase.com/docs/guides/database/overview)
