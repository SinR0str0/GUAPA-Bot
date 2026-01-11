"""
Utilidades y funciones auxiliares para el bot.
"""
import os
from dotenv import load_dotenv
from pathlib import Path


# Cargar variables de entorno
load_dotenv(dotenv_path=Path(".env"))


def get_token() -> str:
    """
    Obtiene el token de Discord desde las variables de entorno.
    """
    token = os.getenv('DISCORD_TOKEN')
    if not token:
        raise ValueError(
            "DISCORD_TOKEN no está configurado. "
            "Por favor, crea un archivo .env con tu token."
        )
    return token


def get_weather_api_key() -> str:
    """
    Obtiene la API key de OpenWeatherMap desde las variables de entorno.
    """
    api_key = os.getenv('WEATHER_API_KEY')
    if not api_key:
        raise ValueError(
            "WEATHER_API_KEY no está configurada. "
            "Por favor, crea un archivo .env con tu API key."
        )
    return api_key


def get_db_config() -> dict:
    """
    Obtiene la configuración de la base de datos Supabase desde las variables de entorno.
    """
    # Supabase usa PostgreSQL, puerto por defecto 5432
    host = os.getenv('DB_HOST')
    port = os.getenv('DB_PORT', '5432')
    database = os.getenv('DB_NAME')
    user = os.getenv('DB_USER')
    password = os.getenv('DB_PASSWORD')
    
    if not all([host, database, user, password]):
        raise ValueError(
            "Variables de base de datos no configuradas. "
            "Por favor, configura DB_HOST, DB_NAME, DB_USER y DB_PASSWORD en .env"
        )
    
    return {
        'host': host,
        'port': int(port),
        'database': database,
        'user': user,
        'password': password
    }


def validate_env() -> bool:
    """
    Valida que todas las variables de entorno necesarias estén configuradas.
    """
    try:
        get_token()
        get_db_config()
        return True
    except ValueError:
        return False

