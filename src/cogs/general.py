# cogs/general.py
import discord
from discord.ext import commands
from database import log_user_update, get_user_update_stats, get_user_update_dates, has_updated_today

class General(commands.Cog, name="General"):
    """Comandos generales del bot."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='ping', help='Responde con el tiempo de latencia del bot')
    async def ping(self, ctx):
        latency = round(self.bot.latency * 1000)
        await ctx.send(f'🏓 Pong! Latencia: {latency}ms')

    @commands.command(name='info', help='Muestra información sobre el bot')
    async def info(self, ctx):
        embed = discord.Embed(
            title="🤖 Información del Bot",
            description="Bot desarrollado para GUAPA",
            color=discord.Color.green()
        )
        embed.add_field(name="Servidores", value=len(self.bot.guilds), inline=True)
        embed.add_field(name="Latencia", value=f"{round(self.bot.latency * 1000)}ms", inline=True)
        embed.add_field(name="Comandos", value=len(self.bot.commands), inline=True)
        await ctx.send(embed=embed)
        

async def setup(bot):
    await bot.add_cog(General(bot))