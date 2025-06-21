import discord
from discord.ext import commands, tasks
import random
import asyncio

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Base de datos en memoria (usa un JSON o base real en producción)
users = {}

# Nivel y experiencia
LEVEL_UP_XP = 100

# Misiones base
MISIONES_BASE = [
    {"nombre": "Reciclar", "accion": "reciclar", "objetivo": 2, "recompensa": {"xp": 30, "coins": 20}},
    {"nombre": "Ahorrar agua", "accion": "agua", "objetivo": 2, "recompensa": {"xp": 25, "coins": 15}},
    {"nombre": "Apagar luces", "accion": "luces", "objetivo": 1, "recompensa": {"xp": 20, "coins": 10}},
    {"nombre": "Evitar plásticos", "accion": "plástico", "objetivo": 2, "recompensa": {"xp": 30, "coins": 25}},
    {"nombre": "Reutilizar bolsas", "accion": "bolsa", "objetivo": 2, "recompensa": {"xp": 20, "coins": 10}}
]

def get_user_data(user_id):
    if user_id not in users:
        users[user_id] = {
            "xp": 0,
            "level": 1,
            "coins": 0,
            "logros": [],
            "planeta": "🌍",
            "misiones": asignar_misiones()
        }
    return users[user_id]

def actualizar_planeta(user):
    xp = user["xp"]
    if xp < 50:
        user["planeta"] = "🌋"
        user["coins"] = max(0, user["coins"] - 5)
    elif xp < 100:
        user["planeta"] = "🌎"
    elif xp < 200:
        user["planeta"] = "🌍"
    else:
        user["planeta"] = "🪐"
        user["coins"] += 5

def asignar_misiones():
    return [
        {**m, "progreso": 0, "completada": False} 
        for m in random.sample(MISIONES_BASE, 3)
    ]

def verificar_misiones(user, habito):
    for m in user["misiones"]:
        if not m["completada"] and m["accion"] in habito.lower():
            m["progreso"] += 1
            if m["progreso"] >= m["objetivo"]:
                m["completada"] = True
                user["xp"] += m["recompensa"]["xp"]
                user["coins"] += m["recompensa"]["coins"]
    if all(m["completada"] for m in user["misiones"]):
        user["misiones"] = asignar_misiones()

@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user}')
    eco_check.start()

@bot.command(name='hacer')
async def hacer_habito(ctx, *, habito: str):
    user = get_user_data(ctx.author.id)

    xp_ganado = 20
    monedas = 10

    user["xp"] += xp_ganado
    user["coins"] += monedas

    verificar_misiones(user, habito)
    actualizar_planeta(user)

    if user["xp"] >= LEVEL_UP_XP:
        user["xp"] -= LEVEL_UP_XP
        user["level"] += 1
        await ctx.send(f"🎉 ¡{ctx.author.name} ha subido a nivel {user['level']}!")

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
    embed.add_field(name="XP", value=user["xp"])
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

@bot.command(name='misiones')
async def misiones(ctx):
    user = get_user_data(ctx.author.id)
    mensaje = f"📋 Misiones de {ctx.author.name}\n"
    for m in user["misiones"]:
        if m["completada"]:
            mensaje += f"✅ {m['nombre']}: Completada\n"
        else:
            mensaje += f"🔹 {m['nombre']}: {m['progreso']}/{m['objetivo']}\n"
    await ctx.send(mensaje)

@tasks.loop(hours=24)
async def eco_check():
    print("🔁 Revisión ambiental diaria...")

# Token de tu bot aquí (NO lo compartas)
bot.run('MTI4OTYzMjg1NTAzMDQ5NzM3MQ.GfpSNN.J8nIhg5OtfUzMs7sK9tKGc2hG_PDs-lHQCeyGs')


