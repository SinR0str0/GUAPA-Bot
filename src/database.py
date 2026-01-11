"""
Módulo para manejar la conexión y creaciones de bases con la base de datos Supabase (PostgreSQL).
"""
import logging
import asyncpg

from utils import get_db_config


logger = logging.getLogger(__name__)
_pool: asyncpg.Pool = None


async def init_db() -> bool:
    """
    Inicializa el pool de conexiones y crea las tablas necesarias si no existen.
    """
    global _pool
    
    try:
        db_config = get_db_config()
        dsn = f"postgresql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}?sslmode=require"
        
        
        # Crear pool de conexiones
        _pool = await asyncpg.create_pool(
            dsn,
            min_size=1,
            max_size=5,
            command_timeout=60
        )
        logger.info("Pool de asyncpg creado exitosamente")
        
        # Crear tablas si no existe
        await create_users_table()
        await create_guild_config_table()
        
        return True
        
    except Exception as e:
        logger.error(f"Error al inicializar la base de datos: {e}")
        return False


def get_pool() -> asyncpg.Pool:
    if _pool is None:
        raise RuntimeError("Base de datos no inicializada. Llama a init_db() primero.")
    return _pool


async def create_guild_config_table() -> bool:
    query = """
    CREATE TABLE IF NOT EXISTS guild_config (
        guild_id BIGINT PRIMARY KEY,
        prefix VARCHAR(10) NOT NULL,
        levels INTEGER NOT NULL,
        level_roles JSONB NOT NULL,
        problems_id JSONB NOT NULL,
        verification_enabled BOOLEAN NOT NULL,
        codeforces_channel BIGINT NOT NULL,
        leetcode_channel BIGINT NOT NULL,
        atcoder_channel BIGINT NOT NULL,
        codechef_channel BIGINT NOT NULL,
        topcoder_channel BIGINT NOT NULL,
        hackerearth_channel BIGINT NOT NULL,
        hackerrank_channel BIGINT NOT NULL,
        guini_channel BIGINT NOT NULL
    );
    """
    try:
        await get_pool().execute(query)
        logger.info("Tabla guild_config creada/verificada")
        return True
    except Exception as e:
        logger.error(f"Error al crear guild_config: {e}")
        return False


async def create_users_table() -> bool:
    query = """
    CREATE TABLE IF NOT EXISTS user_updates (
        user_id BIGINT PRIMARY KEY,
        problems_id JSONB NOT NULL,
        codeforces_nickname VARCHAR(100),
        leetcode_nickname VARCHAR(100),
        atcoder_nickname VARCHAR(100),
        codechef_nickname VARCHAR(100),
        topcoder_nickname VARCHAR(100),
        hackerearth_nickname VARCHAR(100),
        hackerrank_nickname VARCHAR(100),
        guini_nickname VARCHAR(100)
    );
    """
    try:
        await get_pool().execute(query)
        logger.info("Tabla user_updates creada/verificada")
        return True
    except Exception as e:
        logger.error(f"Error al crear user_updates: {e}")
        return False
