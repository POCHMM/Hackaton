import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True  # Necesario para leer mensajes

bot = commands.Bot(command_prefix="!", intents=intents)

# Evento al iniciar el bot
@bot.event
async def on_ready():
    print(f"Bot conectado como {bot.user}")

# Comando base para registrar una acción ecológica
@bot.command()
async def accion(ctx, *, descripcion):
    await ctx.send(f"✅ Acción registrada: **{descripcion}**.\n¡Gracias por cuidar el planeta !")
    # Aquí puedes añadir XP, monedas, logros, etc.

# Comando para ver el estado básico del usuario (placeholder)
@bot.command()
async def perfil(ctx):
    await ctx.send(f"🎮 Perfil de {ctx.author.display_name}:\nNivel: 1 | XP: 0 | Monedas: 0")
    # Sustituye por datos reales cuando los implementes

# Comando para ver el estado del planeta virtual
@bot.command()
async def planeta(ctx):
    await ctx.send(" Planeta Virtual: Salud 100%, Contaminación 0%")
    # Sustituye por variables reales cuando las tengas

# Inicia el bot con tu token
bot.run("MTI4OTYyODI2ODM1MzI5NDMzNg.Gor6_N.AfE5mU8R8qpJQXfriM4fz-U_iS7aA6anPXfLeY")

#Ves esto??
