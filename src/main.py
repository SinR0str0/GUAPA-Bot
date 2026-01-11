"""
Función principal del bot de Discord.
"""
import logging
import asyncio
from utils import get_token, validate_env
from database import init_db, get_pool
from db.guilds import get_prefix_for_guild, ensure_guild_config
try:
    import discord
    from discord.ext import commands
except ModuleNotFoundError as e:
    raise SystemExit(
        f"{e.name} not found.\n  pip install [--user] {e.name}"
    ) from e

""" Configuración del logging """
logger = logging.getLogger(__name__)
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.INFO
    )
logger.info("Inicializando GUAPA Bot.")

async def determine_prefix(bot, message):
    """Determina el prefijo de un servidor."""
    if message.guild is None:
        return commands.when_mentioned_or('!')(bot, message)
    
    prefix = await get_prefix_for_guild(message.guild.id)
    
    return commands.when_mentioned_or(prefix)(bot, message)

async   def create_bot() -> commands.Bot:
    """Crea y configura la instancia del bot."""
    # Configuración del bot
    intents = discord.Intents.default()
    intents.message_content = True
        
    bot = commands.Bot(command_prefix=determine_prefix, intents=intents)
    
    @bot.event
    async def on_ready():
        """Evento que se ejecuta cuando el bot se conecta a Discord."""
        await bot.tree.sync()
        logger.info(f'{bot.user} se ha conectado a Discord! | Bot ID: {bot.user.id}')
        for guild in bot.guilds:
            await ensure_guild_config(guild.id)
        logger.info("✅ Configuraciones iniciales aseguradas")
    
    @bot.event
    async def on_command_error(ctx, error):
        """Maneja los errores de comandos."""
        try:
            if ctx.guild:
                prefix = await get_prefix_for_guild(ctx.guild.id)
            else:
                prefix = "!"
        except Exception:
            prefix = "!"          

        if isinstance(error, commands.CommandNotFound):
            await ctx.send(f"❌ Comando no encontrado. Usa `{prefix}help` para ver los comandos disponibles.")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("❌ Faltan argumentos requeridos. Revisa la sintaxis del comando.")
        else:
            await ctx.send(f"❌ Ocurrió un error: {str(error)}")
            logger.error(f"Error no manejado en comando: {error}")
    
    @bot.event
    async def on_guild_join(guild):
        logger.info(f"🆕 ¡Añadido a {guild.name}!")
        await ensure_guild_config(guild.id)
    
    # Configurar comandos
    await bot.load_extension("cogs.general")
    
    return bot


async def main():
    """Función principal para ejecutar el bot."""
    # Validar variables de entorno
    if not validate_env():
        print("❌ Error: Variables de entorno no configuradas correctamente.")
        print("Por favor, crea un archivo .env con tus API keys.")
        return
    
    # Inicializar base de datos
    try:
        db_ready = await init_db()
        if db_ready:
            logger.info("✅ Base de datos inicializada y lista")
        else:
            logger.critical("❌ Base de datos no disponible. Deteniendo el bot.")
            return
    except Exception as e:
        logger.error(f"❌ Error al inicializar la base de datos: {e}")
        logger.info("El bot continuará sin funcionalidad de base de datos")
    
    # Verificar credenciales del bot
    try:
        token = get_token()
        bot = await create_bot()
        await bot.start(token)

        logger.info("Bot iniciado correctamente.")
    except ValueError as e:
        logger.error(f"Error de configuración: {e}")
    except Exception as e:
        logger.error(f"Error inesperado: {e}")
    finally:
        # Cerrar pool de DB siempre
        pool = get_pool()
        if pool:
            await pool.close()
            logger.info("🔌 Pool de base de datos cerrado.")


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("🛑 Bot detenido manualmente.")
