"""
Módulo para crear configuraciones personalizadas para cada servidor.
"""
import logging
import json
from typing import Optional, Dict, Any
from database import get_pool

logger = logging.getLogger(__name__)


DEFAULT_CONFIG = {
    "prefix": "!",
    "levels": 0,
    "level_roles": {},
    "problems_id": {},
    "verification_enabled": False,
    "codeforces_channel": 0,
    "leetcode_channel": 0,
    "atcoder_channel": 0,
    "codechef_channel": 0,
    "topcoder_channel": 0,
    "hackerearth_channel": 0,
    "hackerrank_channel": 0,
    "guini_channel": 0
}

JSON_FIELDS = {"level_roles", "problems_id"}

COLUMNS = ["guild_id"] + list(DEFAULT_CONFIG.keys())
COLUMN_STR = ", ".join(COLUMNS)


async def ensure_guild_config(guild_id: int) -> bool:
    """
    Asegura que un servidor tenga una fila en la tabla.
    """
    try:
        pool = get_pool()
        values = [guild_id]
        for key, val in DEFAULT_CONFIG.items():
            if isinstance(val, (dict, list)):
                values.append(json.dumps(val))
            else:
                values.append(val)

        placeholders = ", ".join([f"${i+1}" for i in range(len(values))])
        query = f"""
            INSERT INTO guild_config ({COLUMN_STR})
            VALUES ({placeholders})
            ON CONFLICT (guild_id) DO NOTHING;
        """

        await pool.execute(query, *values)
        logger.info(f"Configuración asegurada para guild_id={guild_id}")
        return True

    except Exception as e:
        logger.error(f"Error al asegurar config para guild {guild_id}: {e}")
        return False


async def update_guild_field(guild_id: int, field: str, value: Any) -> bool:
    if field not in DEFAULT_CONFIG:
        logger.error(f"Campo inválido: {field}")
        return False

    # Serializar si es JSONB
    final_value = json.dumps(value) if field in JSON_FIELDS else value

    try:
        pool = get_pool()
        # Inserta o actualiza en una sola operación
        query = f"""
            INSERT INTO guild_config (guild_id, {field})
            VALUES ($1, $2)
            ON CONFLICT (guild_id)
            DO UPDATE SET {field} = $2;
        """
        await pool.execute(query, guild_id, final_value)
        logger.info(f"Guild {guild_id}: {field} = {value}")
        return True

    except Exception as e:
        logger.error(f"Error al actualizar {field} para guild {guild_id}: {e}")
        return False


async def get_guild_config(guild_id: int) -> Optional[Dict[str, Any]]:
    """Obtiene la configuración completa de un guild."""
    try:
        pool = get_pool()
        query = f"SELECT {COLUMN_STR} FROM guild_config WHERE guild_id = $1"
        row = await pool.fetchrow(query, guild_id)
        
        if not row:
            return None

        config = {}
        for col, val in zip(COLUMNS, row):
            if col in JSON_FIELDS and isinstance(val, str):
                config[col] = json.loads(val)
            else:
                config[col] = val

        return config

    except Exception as e:
        logger.error(f"Error al obtener config para guild {guild_id}: {e}")
        return None


async def get_prefix_for_guild(guild_id: int) -> str:
    """Obtiene el prefijo de un guild, con fallback seguro."""
    if guild_id is None:
        return "!"
    try:
        config = await get_guild_config(guild_id)
        if config is None:
            # Crear configuración por defecto si no existe
            await ensure_guild_config(guild_id)
            return DEFAULT_CONFIG["prefix"]
        return config["prefix"]
    except Exception as e:
        logger.warning(f"Error al obtener prefijo para {guild_id}: {e}")
        return "!"