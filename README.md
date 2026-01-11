# GUAPA-Bot

Bot desarrollado para el Grupo Universitario de Algoritmia y Programación Avanzada (GUAPA) de la FES Acatlán.

## 🚀 Características

- Bot de Discord con comandos básicos
- Integración con API de clima (OpenWeatherMap)
- Base de datos MySQL para registro de usuarios y logs
- Sistema de comandos con prefijo personalizable
- Manejo de errores integrado
- Estadísticas de uso por usuario

## 📋 Requisitos

- Python 3.8 o superior
- Cuenta de Discord Developer
- Base de datos Supabase (opcional pero recomendado, plan gratuito disponible)

## 🔧 Instalación

1. Clona o descarga este repositorio

2. Instala las dependencias:
```bash
pip install -r requirements.txt
```

3. Configura las variables de entorno:
   - Copia el archivo `env.example` y renómbralo a `.env`
   - **IMPORTANTE**: El archivo `.env` está en `.gitignore` y nunca debe subirse a Git
   - Edita `.env` y agrega tus credenciales:
     - `DISCORD_TOKEN`: Token de tu bot de Discord
     - `WEATHER_API_KEY`: API Key de OpenWeatherMap
     - Variables de base de datos MySQL (opcional pero recomendado)

## 🔒 Seguridad

**NUNCA compartas o subas a Git:**
- El archivo `.env` (ya está en `.gitignore`)
- Tokens o API keys en el código
- Credenciales en commits o mensajes

Si necesitas compartir el proyecto, usa `env.example` como plantilla sin valores reales.

## 🔑 Obtener Credenciales

### Token de Discord:
1. Ve a [Discord Developer Portal](https://discord.com/developers/applications)
2. Crea una nueva aplicación
3. Ve a la sección "Bot" y crea un bot
4. Copia el token y guárdalo en `.env`

### Base de Datos Supabase:
1. Ve a [Supabase](https://supabase.com/) y crea una cuenta gratuita
2. Crea un nuevo proyecto
3. Ve a **Settings** > **Database** en el dashboard
4. En la sección **Connection string**, copia los parámetros:
   - **Host**: `db.xxxxx.supabase.co`
   - **Puerto**: `5432`
   - **Database**: `postgres`
   - **User**: `postgres.xxxxx`
   - **Password**: Tu contraseña (se muestra solo una vez)
5. Agrega estas credenciales a tu archivo `.env`:
   ```
   DB_HOST=db.xxxxx.supabase.co
   DB_PORT=5432
   DB_NAME=postgres
   DB_USER=postgres.xxxxx
   DB_PASSWORD=tu_contraseña_supabase
   ```

**Nota**: La base de datos es opcional. El bot funcionará sin ella, pero el comando `!actualizar` no guardará registros. Para más detalles, consulta [DATABASE.md](DATABASE.md).

## 🎮 Comandos Disponibles

- `!ping` - Muestra la latencia del bot
- `!info` - Muestra información sobre el bot
- `!clima <ciudad>` - Obtiene el clima de una ciudad
- `!actualizar` - Registra tu actualización del día (requiere DB configurada)
- `!mystats` - Muestra tus estadísticas de actualizaciones (requiere DB configurada)
- `!help` - Lista todos los comandos disponibles

## ▶️ Ejecutar el Bot

```bash
python main.py
```

## 📁 Estructura del Proyecto

```
GUAPA Bot/
├── src/
│   ├── __init__.py      # Inicialización del paquete
│   ├── main.py          # Configuración y creación del bot
│   ├── commands.py      # Comandos generales (ping, info, mystats)
│   ├── clima.py         # Lógica del clima y API
│   ├── database.py      # Manejo de base de datos MySQL
│   └── utils.py         # Utilidades y manejo de variables de entorno
├── main.py              # Punto de entrada principal
├── requirements.txt     # Dependencias del proyecto
├── env.example          # Plantilla de variables de entorno
├── .gitignore          # Archivos ignorados por Git
└── README.md           # Documentación
```

## 📝 Notas

- Asegúrate de que el bot tenga los permisos necesarios en tu servidor de Discord
- El prefijo de comandos está configurado como `!` pero puede modificarse en `src/main.py`
- La base de datos Supabase es opcional. Si no está configurada, el comando `!actualizar` no guardará registros
- El bot solo registra cuando un usuario usa `!actualizar`, almacenando únicamente el día (fecha), no la hora
- Un usuario solo puede actualizar una vez por día (evita duplicados)
- La tabla `user_updates` se crea automáticamente al iniciar el bot por primera vez
- Supabase usa PostgreSQL y requiere conexión SSL (ya configurado automáticamente)

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Siéntete libre de mejorar este bot.
