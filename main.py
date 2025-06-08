import discord
from discord.ext import commands

# Intenciones necesarias (por ejemplo, para poder ver mensajes y miembros)
intents = discord.Intents.default()
intents.message_content = True  # Necesario para recibir el contenido de los mensajes

# Prefijo de comandos
bot = commands.Bot(command_prefix='!', intents=intents)

# Mensaje cuando el bot esté listo
@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user.name}')

# Comando básico
@bot.command()
async def ping(ctx):
    await ctx.send('Hola')

# Inicia el bot
bot.run('TU_TOKEN_AQUI')
