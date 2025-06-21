import discord
from discord.ext import commands, tasks
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import asyncio

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

users = {}
LEVEL_UP_XP = 100

def get_user_data(user_id):
    if user_id not in users:
        users[user_id] = {
            "xp": 0,
            "xp_total": 0,
            "level": 1,
            "coins": 0,
            "logros": [],
            "planeta": "🌍"
        }
    return users[user_id]

def actualizar_planeta(user):
    xp_total = user["xp_total"]

    if xp_total < 60:
        user["planeta"] = "🌋"  # En peligro
        user["coins"] = max(0, user["coins"] - 5)
    elif xp_total < 120:
        user["planeta"] = "🌎"  # Contaminado
    elif xp_total < 200:
        user["planeta"] = "🌍"  # En equilibrio
    else:
        user["planeta"] = "🪐"  # Saludable
        user["coins"] += 5

    print(f"[DEBUG] XP total: {xp_total} → Planeta: {user['planeta']}")

@bot.event
async def on_ready():
    print(f'✅ Bot conectado como {bot.user}')
    eco_check.start()

@bot.command(name='hacer')
async def hacer_habito(ctx, *, habito: str):
    user = get_user_data(ctx.author.id)

    xp_ganado = 20
    monedas = 10

    user["xp"] += xp_ganado
    user["xp_total"] += xp_ganado
    user["coins"] += monedas

    if user["xp"] >= LEVEL_UP_XP:
        user["xp"] -= LEVEL_UP_XP
        user["level"] += 1
        await ctx.send(f"🎉 ¡{ctx.author.name} ha subido a nivel {user['level']}!")

    actualizar_planeta(user)

    await ctx.send(
        f"✅ Acción registrada: {habito}\n+{xp_ganado} XP | +{monedas} monedas\n🌐 Estado del planeta: {user['planeta']}"
    )

@bot.command(name='perfil')
async def perfil(ctx):
    user = get_user_data(ctx.author.id)

    estado = {
        "🌋": "🌋 En peligro: ¡haz más acciones ecológicas!",
        "🌎": "🌎 Contaminado: tu planeta necesita ayuda.",
        "🌍": "🌍 En equilibrio: sigue así.",
        "🪐": "🪐 Saludable: ¡felicidades, estás salvando el planeta!"
    }

    embed = discord.Embed(title=f"Perfil de {ctx.author.name}", color=0x34eb8c)
    embed.add_field(name="Nivel", value=user["level"])
    embed.add_field(name="XP", value=f'{user["xp"]}/{LEVEL_UP_XP}')
    embed.add_field(name="XP Total", value=user["xp_total"])
    embed.add_field(name="Monedas", value=user["coins"])
    embed.add_field(name="Logros", value=', '.join(user["logros"]) or "Ninguno")
    embed.add_field(name="Planeta", value=estado.get(user["planeta"], "🌍 Desconocido"), inline=False)

    await ctx.send(embed=embed)

@bot.command(name='logro')
async def agregar_logro(ctx, *, logro: str):
    user = get_user_data(ctx.author.id)
    if logro not in user["logros"]:
        user["logros"].append(logro)
        await ctx.send(f"🏅 Logro agregado: {logro}")
    else:
        await ctx.send("⚠️ Ya tienes este logro.")

@tasks.loop(hours=24)
async def eco_check():
    print("🔁 Revisión ambiental diaria...")

bot.run('')  # reemplaza esto con tu token real
