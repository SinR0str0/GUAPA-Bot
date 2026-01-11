"""
Módulo para manejar las funcionalidades relacionadas con el clima.
"""
import discord
import aiohttp
from typing import Optional, Dict, Any
from utils import get_weather_api_key


WEATHER_API_URL = "http://api.openweathermap.org/data/2.5/weather"


async def obtener_clima(ciudad: str) -> Optional[Dict[str, Any]]:
    """
    Obtiene los datos del clima de una ciudad usando la API de OpenWeatherMap.
    
    Args:
        ciudad: Nombre de la ciudad
        
    Returns:
        Dict con los datos del clima o None si hay error
    """
    try:
        api_key = get_weather_api_key()
        
        async with aiohttp.ClientSession() as session:
            params = {
                'q': ciudad,
                'appid': api_key,
                'units': 'metric',
                'lang': 'es'
            }
            
            async with session.get(WEATHER_API_URL, params=params) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    return None
                    
    except Exception as e:
        print(f"Error al obtener clima: {e}")
        return None


def crear_embed_clima(data: Dict[str, Any]) -> discord.Embed:
    """
    Crea un embed de Discord con la información del clima.
    
    Args:
        data: Diccionario con los datos del clima de la API
        
    Returns:
        Embed de Discord con la información del clima
    """
    # Extraer información relevante
    temperatura = data['main']['temp']
    sensacion = data['main']['feels_like']
    humedad = data['main']['humidity']
    descripcion = data['weather'][0]['description'].title()
    viento = data['wind']['speed']
    ciudad_nombre = data['name']
    pais = data['sys']['country']
    
    # Crear embed con la información
    embed = discord.Embed(
        title=f"🌤️ Clima en {ciudad_nombre}, {pais}",
        color=discord.Color.blue()
    )
    embed.add_field(name="🌡️ Temperatura", value=f"{temperatura}°C", inline=True)
    embed.add_field(name="😌 Sensación", value=f"{sensacion}°C", inline=True)
    embed.add_field(name="💧 Humedad", value=f"{humedad}%", inline=True)
    embed.add_field(name="🌬️ Viento", value=f"{viento} m/s", inline=True)
    embed.add_field(name="☁️ Condición", value=descripcion, inline=False)
    
    return embed


async def procesar_comando_clima(ctx, ciudad: str) -> None:
    """
    Procesa el comando de clima y envía la respuesta al usuario.
    
    Args:
        ctx: Contexto del comando de Discord
        ciudad: Nombre de la ciudad
    """
    try:
        data = await obtener_clima(ciudad)
        
        if data is None:
            await ctx.send(f"❌ No se encontró la ciudad '{ciudad}'. Intenta con otro nombre.")
            return
        
        embed = crear_embed_clima(data)
        await ctx.send(embed=embed)
        
    except KeyError as e:
        await ctx.send(f"❌ Error al procesar los datos del clima: {str(e)}")
    except Exception as e:
        await ctx.send(f"❌ Ocurrió un error inesperado: {str(e)}")

