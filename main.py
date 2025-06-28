import discord
from discord.ext import commands
from discord.ext import tasks
import os

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Variables
dinero = 0
nivel = 0
xp = 0
needed_xp = 100
puntuacion_planeta = 0
estado_planeta = "Critico"
max_puntuacion_planeta = 100
dias_racha_bici = 0
racha_bici_necesaria = 7
recuperar_racha_costo = 100
recompensas_racha_xp = 160
recompensas_racha_dinero = 120
reclamar_racha = "false"
meta_multiplicador = 1
ultima_recompensa_planeta = 0


# Siempre se va a ejecutar
@tasks.loop(seconds=0.1)
async def process_loop():
    global xp
    global nivel
    global needed_xp

    if xp >= needed_xp:
        nivel += 1
        xp -= needed_xp
        needed_xp *= 2

    # Recompensas por cuidar el planeta
    global dinero
    global puntuacion_planeta
    global ultima_recompensa_planeta
    metas = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]

    for meta in metas:
        if puntuacion_planeta >= meta and ultima_recompensa_planeta < meta:
            reward_dinero = meta * 15
            reward_xp = meta * 25
            dinero += reward_dinero
            xp += reward_xp
            ultima_recompensa_planeta = meta
            break


# Incio del bot
@bot.event
async def on_ready():
    process_loop.start()
    print(f"Bot conectado como {bot.user}")


# Prueba
@bot.command()
async def hola(ctx):
    await ctx.send("hola")


#Ayuda


#informacion
@bot.command()
async def info(ctx):
    embed = discord.Embed(
        title="Bot del Medio Ambiente",
        description=
        "Soy un bot ecologico que te ayuda a gamificar tus acciones ambientales y crear habitos sostenibles.",
        color=0x00ff00)
    embed.add_field(
        name="Como funciona:",
        value=
        "Realiza acciones ecologicas para ganar XP, dinero virtual y mejorar tu planeta virtual.",
        inline=False)
    embed.add_field(
        name="Sistema de Rachas:",
        value=
        "Usa la bicicleta diariamente para crear rachas. Cada 7 dias de racha obtienes recompensas especiales que aumentan infinitamente.",
        inline=False)
    embed.add_field(
        name="Economia Virtual:",
        value=
        "Gana dinero virtual realizando acciones ecologicas y gastalo en la tienda para recompensas personales.",
        inline=False)
    embed.add_field(
        name="Planeta Virtual:",
        value=
        "Cada accion ecologica mejora tu planeta virtual. Observa como cambia su estado segun tus acciones.",
        inline=False)
    embed.add_field(
        name="Recompensas del Planeta:",
        value=
        "Cada 10 puntos de planeta desbloqueas recompensas especiales. Usa !reclamar_planeta para obtenerlas.",
        inline=False)
    embed.add_field(
        name="Comandos principales:",
        value=
        "!acciones - Ver acciones disponibles\n!tienda - Ver tienda\n!bici_dia - Usar bicicleta\n!stats - Ver estadisticas\n!planeta - Ver tu planeta\n!reclamar_planeta - Obtener recompensas",
        inline=False)
    embed.set_footer(
        text="Juntos podemos hacer la diferencia por el medio ambiente")

    await ctx.send(embed=embed)


# Ayuda accioones
@bot.command()
async def accion(ctx):
    await ctx.send(
        "Que accion haz completado??, Indica la accion que hiciste con accion_(la accion que realizaste), si quieres ver las acciones disponibles usa el comando !acciones"
    )


@bot.command()
async def acciones(ctx):
    embed = discord.Embed(
        title="Acciones Ecologicas Disponibles",
        description=
        "Estas son todas las acciones que puedes realizar para ayudar al planeta:",
        color=0x00ff00)
    embed.add_field(name="Reciclaje",
                    value="!accion_reciclar - Recicla materiales",
                    inline=False)
    embed.add_field(
        name="Evitar Plasticos",
        value=
        "!evitar_plastico_1dia\n!evitar_plastico_3dias\n!evitar_plastico_5dias\n!evitar_plastico_7dias",
        inline=False)
    embed.add_field(
        name="Bicicleta",
        value="!bici_dia - Usar bici por un dia\n!no_bici - Perdiste tu racha",
        inline=False)
    embed.add_field(name="Recuperar Racha",
                    value="!recuperar_racha - Recupera tu racha de bici",
                    inline=False)
    embed.add_field(
        name="Estado",
        value=
        "!planeta - Ver tu planeta virtual\n!reclamar_planeta - Reclamar recompensas del planeta",
        inline=False)
    embed.add_field(
        name="Recompensas del Planeta",
        value="Cada 10 puntos del planeta desbloquea recompensas especiales",
        inline=False)
    embed.set_footer(
        text="Cada accion cuenta para mejorar el planeta y obtener recompensas"
    )

    await ctx.send(embed=embed)


# Tienda
@bot.command()
async def tienda(ctx):
    global dinero

    embed = discord.Embed(
        title="Bienvenido a la Tienda",
        description="Aqui puedes comprar recompensas propias",
        color=0x339fff)
    embed.add_field(name="Pedir Comida o Salir a Comer:",
                    value="280$ - !pedir_comida",
                    inline=False)
    embed.add_field(name="Ir al Cine:", value="350$ - !ir_cine", inline=False)
    embed.add_field(name="Comprar un Libro:",
                    value="200$ - !comprar_libro",
                    inline=False)
    embed.add_field(name="Jugar Videojuegos (2 horas):",
                    value="150$ - !jugar_videojuegos",
                    inline=False)

    embed.add_field(name="Streaming Premium (1 mes):",
                    value="500$ - !streaming_premium",
                    inline=False)
    embed.set_footer(
        text=
        f"Dinero disponible: {dinero}$ - Gasta sabiamente tu dinero que no es infinito"
    )

    await ctx.send(embed=embed)


# Cosas de la tienda


#pedir comida a domicilio o ir a comer
@bot.command()
async def pedir_comida(ctx):
    global dinero
    precio = 280

    if dinero >= precio:
        dinero -= precio
        embed = discord.Embed(
            title="Compraste Pedir Comida o Salir a Comer",
            description="Puedes pedir 1 vez comida a casa o Salir a Comer",
            color=0x00ff00)
        embed.add_field(name="Precio:", value=f"{precio}$", inline=False)
        embed.add_field(name="Dinero restante:",
                        value=f"{dinero}$",
                        inline=False)
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title="No tienes el dinero necesario",
                              description="No te alcanza para comprar esto",
                              color=0xff0000)
        embed.add_field(name="Precio:", value=f"{precio}$", inline=False)
        embed.add_field(name="Tu dinero:", value=f"{dinero}$", inline=False)
        await ctx.send(embed=embed)


#ir al cine
@bot.command()
async def ir_cine(ctx):
    global dinero
    precio = 350

    if dinero >= precio:
        dinero -= precio
        embed = discord.Embed(
            title="Compraste Ir al Cine",
            description="Disfruta de una película en el cine",
            color=0x00ff00)
        embed.add_field(name="Precio:", value=f"{precio}$", inline=False)
        embed.add_field(name="Dinero restante:",
                        value=f"{dinero}$",
                        inline=False)
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title="No tienes el dinero necesario",
                              description="No te alcanza para comprar esto",
                              color=0xff0000)
        embed.add_field(name="Precio:", value=f"{precio}$", inline=False)
        embed.add_field(name="Tu dinero:", value=f"{dinero}$", inline=False)
        await ctx.send(embed=embed)


#comprar un libro
@bot.command()
async def comprar_libro(ctx):
    global dinero
    precio = 200

    if dinero >= precio:
        dinero -= precio
        embed = discord.Embed(title="Compraste un Libro",
                              description="Disfruta de una buena lectura",
                              color=0x00ff00)
        embed.add_field(name="Precio:", value=f"{precio}$", inline=False)
        embed.add_field(name="Dinero restante:",
                        value=f"{dinero}$",
                        inline=False)
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title="No tienes el dinero necesario",
                              description="No te alcanza para comprar esto",
                              color=0xff0000)
        embed.add_field(name="Precio:", value=f"{precio}$", inline=False)
        embed.add_field(name="Tu dinero:", value=f"{dinero}$", inline=False)
        await ctx.send(embed=embed)


#jugar videojuegos por un tiempo
@bot.command()
async def jugar_videojuegos(ctx):
    global dinero
    precio = 150

    if dinero >= precio:
        dinero -= precio
        embed = discord.Embed(title="Compraste Jugar Videojuegos",
                              description="Disfruta de 2 horas de videojuegos",
                              color=0x00ff00)
        embed.add_field(name="Precio:", value=f"{precio}$", inline=False)
        embed.add_field(name="Dinero restante:",
                        value=f"{dinero}$",
                        inline=False)
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title="No tienes el dinero necesario",
                              description="No te alcanza para comprar esto",
                              color=0xff0000)
        embed.add_field(name="Precio:", value=f"{precio}$", inline=False)
        embed.add_field(name="Tu dinero:", value=f"{dinero}$", inline=False)
        await ctx.send(embed=embed)


# contratar streaming premuim por un mes
@bot.command()
async def streaming_premium(ctx):
    global dinero
    precio = 500

    if dinero >= precio:
        dinero -= precio
        embed = discord.Embed(
            title="Compraste Streaming Premium",
            description="Disfruta de un mes de streaming premium",
            color=0x00ff00)
        embed.add_field(name="Precio:", value=f"{precio}$", inline=False)
        embed.add_field(name="Dinero restante:",
                        value=f"{dinero}$",
                        inline=False)
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title="No tienes el dinero necesario",
                              description="No te alcanza para comprar esto",
                              color=0xff0000)
        embed.add_field(name="Precio:", value=f"{precio}$", inline=False)
        embed.add_field(name="Tu dinero:", value=f"{dinero}$", inline=False)
        await ctx.send(embed=embed)


# Acciones


#reciclar
@bot.command()
async def accion_reciclar(ctx):
    global dinero
    global xp
    global puntuacion_planeta

    puntuacion_planeta += 1
    dinero += 20
    xp += 5

    embed = discord.Embed(
        title="Accion: Reciclar",
        description="Gracias por reciclar! Aquí tienes tus recompensas",
        color=0x00ff00)
    embed.add_field(name="Recompensas",
                    value="XP: +5\nMonedas: +20",
                    inline=False)
    embed.add_field(name="Puntuación del planeta:",
                    value=f"+1 (Total: {puntuacion_planeta})",
                    inline=False)
    embed.set_footer(text="¡Sigue así para mejorar el planeta!")

    await ctx.send(embed=embed)


# Evitar plasticos


#1 dia
@bot.command()
async def evitar_plastico_1dia(ctx):
    global dinero
    global xp
    global puntuacion_planeta

    puntuacion_planeta += 1
    recompensa_dinero = 10
    recompensa_xp = 20

    dinero += recompensa_dinero
    xp += recompensa_xp

    embed = discord.Embed(
        title="Accion: Evitar plásticos durante un día!",
        description=
        "Gracias por ayudar al planeta! Aquí tienes tus recompensas",
        color=0x00ff00)
    embed.add_field(
        name="Recompensa",
        value=f"XP: +{recompensa_xp}\nMonedas: +{recompensa_dinero}",
        inline=False)
    embed.add_field(name="Puntuación del planeta:",
                    value=f"+1 (Total: {puntuacion_planeta})",
                    inline=False)
    embed.set_footer(text="¡Has mejorado un poco tu planeta, sigue así!")

    await ctx.send(embed=embed)


#3 dias
@bot.command()
async def evitar_plastico_3dias(ctx):
    global dinero
    global xp
    global puntuacion_planeta

    puntuacion_planeta += 2
    recompensa_dinero = 40
    recompensa_xp = 80

    dinero += recompensa_dinero
    xp += recompensa_xp

    embed = discord.Embed(
        title="Accion: Evitar plásticos durante tres días!!",
        description=
        "Gracias por ayudar al planeta! Aquí tienes tus recompensas",
        color=0x00ff00)
    embed.add_field(
        name="Recompensa",
        value=f"XP: +{recompensa_xp}\nMonedas: +{recompensa_dinero}",
        inline=False)
    embed.add_field(name="Puntuación del planeta:",
                    value=f"+2 (Total: {puntuacion_planeta})",
                    inline=False)
    embed.set_footer(text="¡Has ayudado al planeta!")

    await ctx.send(embed=embed)


#5dias
@bot.command()
async def evitar_plastico_5dias(ctx):
    global dinero
    global xp
    global puntuacion_planeta

    puntuacion_planeta += 3
    recompensa_dinero = 95
    recompensa_xp = 175

    dinero += recompensa_dinero
    xp += recompensa_xp

    embed = discord.Embed(
        title="Accion: Evitar plásticos durante cinco días!!!",
        description=
        "Gracias por ayudar al planeta! Aquí tienes tus recompensas",
        color=0x00ff00)
    embed.add_field(
        name="Recompensa",
        value=f"XP: +{recompensa_xp}\nMonedas: +{recompensa_dinero}",
        inline=False)
    embed.add_field(name="Puntuación del planeta:",
                    value=f"+3 (Total: {puntuacion_planeta})",
                    inline=False)
    embed.set_footer(text="¡Has ayudado al planeta y lo estás mejorando!")

    await ctx.send(embed=embed)


#7 dias
@bot.command()
async def evitar_plastico_7dias(ctx):
    global dinero
    global xp
    global puntuacion_planeta

    puntuacion_planeta += 4
    recompensa_dinero = 140
    recompensa_xp = 260

    dinero += recompensa_dinero
    xp += recompensa_xp

    embed = discord.Embed(
        title="Accion: Evitar plásticos durante una semana!!!!",
        description=
        "Gracias por ayudar al planeta! Aquí tienes tus recompensas",
        color=0x00ff00)
    embed.add_field(
        name="Recompensa",
        value=f"XP: +{recompensa_xp}\nMonedas: +{recompensa_dinero}",
        inline=False)
    embed.add_field(name="Puntuación del planeta:",
                    value=f"+4 (Total: {puntuacion_planeta})",
                    inline=False)
    embed.set_footer(text="¡Gracias, has ayudado al planeta!")

    await ctx.send(embed=embed)


# Racha de bici diaria
@bot.command()
async def bici_dia(ctx):
    global dinero
    global xp
    global puntuacion_planeta
    global dias_racha_bici
    global recompensas_racha_xp
    global recompensas_racha_dinero
    global meta_multiplicador

    puntuacion_planeta += 1
    recompensa_dinero_base = 10
    recompensa_xp_base = 20

    dinero += recompensa_dinero_base
    xp += recompensa_xp_base
    dias_racha_bici += 1

    meta_alcanzada = False
    bonus_xp = 0
    bonus_dinero = 0
    meta_siguiente = 7

    if dias_racha_bici % 7 == 0:

        meta_alcanzada = True
        meta_multiplicador = (dias_racha_bici // 7)
        bonus_xp = recompensas_racha_xp * meta_multiplicador
        bonus_dinero = recompensas_racha_dinero * meta_multiplicador

        dinero += bonus_dinero
        xp += bonus_xp
        meta_siguiente = dias_racha_bici + 7

    embed = discord.Embed(
        title="Dia de bicicleta completado",
        description="Has usado la bicicleta hoy en lugar de vehículos.",
        color=0x75ad39)

    embed.add_field(
        name="Recompensa Diaria",
        value=f"XP: +{recompensa_xp_base}\nMonedas: +{recompensa_dinero_base}",
        inline=False)
    embed.add_field(name="Racha Actual",
                    value=f" {dias_racha_bici} días consecutivos",
                    inline=False)

    if meta_alcanzada:
        embed.add_field(
            name="Meta alcanzada!",
            value=f"Bonus XP: +{bonus_xp}\nBonus Dinero: +{bonus_dinero}",
            inline=False)
        embed.add_field(name="Próxima Meta",
                        value=f" {meta_siguiente} días",
                        inline=False)
        embed.set_footer(text="Has alcanzado un nuevo objetivo. ¡Sigue así!")
    else:
        dias_hasta_siguiente = 7 - (dias_racha_bici % 7)
        embed.add_field(
            name="Próxima Meta",
            value=f" {dias_hasta_siguiente} días para la siguiente meta",
            inline=False)
        embed.set_footer(
            text="Sigue usando la bici para alcanzar la siguiente meta")

    embed.add_field(name="Puntuación del planeta:",
                    value=f"+1 (Total: {puntuacion_planeta})",
                    inline=False)

    await ctx.send(embed=embed)


@bot.command()
async def no_bici(ctx):
    global dias_racha_bici
    global puntuacion_planeta

    racha_perdida = dias_racha_bici

    dias_racha_bici = 0

    embed = discord.Embed(
        title="Has perdido tu racha de bicicleta",
        description=
        "No usaste la bicicleta hoy y has perdido tu racha. ¡Pero ser honesto también cuenta!",
        color=0xff6b6b)
    embed.add_field(name="Racha Perdida",
                    value=f" {racha_perdida} días perdidos",
                    inline=False)
    embed.add_field(name="Racha Actual", value=" 0 días", inline=False)
    embed.add_field(
        name="Recuperación",
        value="Usa !recuperar_racha para recuperar tu racha (cuesta dinero)",
        inline=False)
    embed.add_field(name="Puntuación del planeta:",
                    value=f"+1 (Total: {puntuacion_planeta}) por ser honesto",
                    inline=False)
    embed.set_footer(
        text="¡No te desanimes! Puedes empezar una nueva racha mañana.")

    await ctx.send(embed=embed)


@bot.command()
async def recuperar_racha(ctx):
    global dinero
    global dias_racha_bici
    global recuperar_racha_costo

    costo = max(recuperar_racha_costo, dias_racha_bici * 10)

    if dinero >= costo:
        dinero -= costo

        dias_racha_bici = 7

        embed = discord.Embed(
            title="🔄 ¡Racha Recuperada!",
            description="Has pagado para recuperar tu racha de bicicleta.",
            color=0x00ff00)
        embed.add_field(name="Costo:", value=f"-{costo}$", inline=False)
        embed.add_field(name="Racha Restaurada:",
                        value=f" {dias_racha_bici} días",
                        inline=False)
        embed.add_field(name="Dinero restante:",
                        value=f"{dinero}$",
                        inline=False)
        embed.set_footer(text="¡Aprovecha esta segunda oportunidad!")

        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(
            title="💸 No tienes suficiente dinero",
            description="No puedes permitirte recuperar tu racha.",
            color=0xff0000)
        embed.add_field(name="Costo:", value=f"{costo}$", inline=False)
        embed.add_field(name="Tu dinero:", value=f"{dinero}$", inline=False)
        embed.set_footer(
            text=
            "Gana más dinero con acciones ecológicas para recuperar tu racha.")

        await ctx.send(embed=embed)


@bot.command()
async def racha_info(ctx):
    global dias_racha_bici
    global meta_multiplicador

    meta_siguiente = 7
    if dias_racha_bici > 0:
        meta_siguiente = ((dias_racha_bici // 7) + 1) * 7

    dias_hasta_siguiente = meta_siguiente - dias_racha_bici
    current_multiplicador = max(1, dias_racha_bici // 7)
    next_multiplicador = current_multiplicador + 1

    embed = discord.Embed(
        title="Información de Racha de Bicicleta",
        description="Aquí está el estado de tu racha de bicicleta:",
        color=0x75ad39)
    embed.add_field(name="Racha Actual",
                    value=f" {dias_racha_bici} días consecutivos",
                    inline=False)
    embed.add_field(
        name="Próxima meta",
        value=f" {meta_siguiente} días ({dias_hasta_siguiente} días restantes)",
        inline=False)
    embed.add_field(name="Multiplicador Actual",
                    value=f"x{current_multiplicador}",
                    inline=True)
    embed.add_field(name="Próximo Multiplicador",
                    value=f" x{next_multiplicador}",
                    inline=True)
    embed.add_field(
        name="Recompensa Base meta",
        value=f"XP: {recompensas_racha_xp}\nDinero: {recompensas_racha_dinero}",
        inline=False)
    embed.set_footer(text="¡Usa !bici_dia cada día para mantener tu racha!")

    await ctx.send(embed=embed)


# Player stats
@bot.command()
async def stats(ctx):
    global dinero, nivel, xp, needed_xp, puntuacion_planeta, dias_racha_bici

    embed = discord.Embed(title="Tus Estadísticas",
                          description="Aquí están todas tus estadísticas:",
                          color=0x3498db)
    embed.add_field(name=" Dinero", value=f"{dinero}$", inline=True)
    embed.add_field(name=" Nivel", value=str(nivel), inline=True)
    embed.add_field(name=" XP", value=f"{xp}/{needed_xp}", inline=True)
    embed.add_field(name=" Puntuación Planeta",
                    value=f"{puntuacion_planeta}/{max_puntuacion_planeta}",
                    inline=True)
    embed.add_field(name="Racha Bici",
                    value=f"{dias_racha_bici} días",
                    inline=True)
    embed.add_field(name="Estado Planeta", value=estado_planeta, inline=True)
    embed.set_footer(text="¡Sigue mejorando con acciones ecológicas!")

    await ctx.send(embed=embed)


# Planeta virtual
@bot.command()
async def planeta(ctx):
    global puntuacion_planeta
    global max_puntuacion_planeta
    global estado_planeta

    if puntuacion_planeta >= 0 and puntuacion_planeta <= 9:
        estado_planeta = "Crítico"
        color = 0x9c0000
        footer_text = "Necesitas urgentemente mejorar el planeta virtual"
    elif puntuacion_planeta >= 10 and puntuacion_planeta <= 19:
        estado_planeta = "Muy Grave"
        color = 0x9c0000
        footer_text = "Necesitas urgentemente mejorar el planeta virtual"
    elif puntuacion_planeta >= 20 and puntuacion_planeta <= 29:
        estado_planeta = "Grave"
        color = 0x9c0000
        footer_text = "Necesitas urgentemente mejorar el planeta virtual"
    elif puntuacion_planeta >= 30 and puntuacion_planeta <= 39:
        estado_planeta = "Medianamente Grave"
        color = 0x9c0000
        footer_text = "El estado de tu planeta es Medianamente Grave necesitas mejorarlo"
    elif puntuacion_planeta >= 40 and puntuacion_planeta <= 49:
        estado_planeta = "Muy Malo"
        color = 0x9c5c00
        footer_text = "Necesitas mejorar el planeta virtual"
    elif puntuacion_planeta >= 50 and puntuacion_planeta <= 59:
        estado_planeta = "Malo"
        color = 0xcfa30d
        footer_text = "Necesitas mejorar el planeta virtual"
    elif puntuacion_planeta >= 60 and puntuacion_planeta <= 69:
        estado_planeta = "Decente"
        color = 0xd29812
        footer_text = "Mejora el planeta virtual para que sea mejor"
    elif puntuacion_planeta >= 70 and puntuacion_planeta <= 79:
        estado_planeta = "Bueno"
        color = 0x75ad39
        footer_text = "¡Bien! Tu planeta está mejorando"
    elif puntuacion_planeta >= 80 and puntuacion_planeta <= 89:
        estado_planeta = "Muy Bueno"
        color = 0x5cb85c
        footer_text = "¡Excelente! Tu planeta está en muy buen estado"
    elif puntuacion_planeta >= 90 and puntuacion_planeta <= 99:
        estado_planeta = "Excelente"
        color = 0x2e7d32
        footer_text = "¡Increíble! Tu planeta está casi perfecto"
    else:
        estado_planeta = "Perfecto"
        color = 0x1b5e20
        footer_text = "Has alcanzado el máximo nivel del planeta!"

    embed = discord.Embed(
        title=" Este es tu planeta virtual",
        description=
        "Realiza acciones ecológicas para mejorarlo y recibir recompensas",
        color=color)
    embed.add_field(name="Estado del planeta",
                    value=estado_planeta,
                    inline=False)
    embed.add_field(name="Puntuación del planeta",
                    value=f"{puntuacion_planeta}/{max_puntuacion_planeta}",
                    inline=False)

    meta_siguiente = None
    for meta in [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]:
        if puntuacion_planeta < meta:
            meta_siguiente = meta
            break

    if meta_siguiente:
        puntos_necesarios = meta_siguiente - puntuacion_planeta
        reward_dinero = meta_siguiente * 15
        reward_xp = meta_siguiente * 25
        embed.add_field(
            name="Proxima Recompensa",
            value=
            f"En {puntos_necesarios} puntos: {reward_dinero}$ + {reward_xp} XP",
            inline=False)

    if ultima_recompensa_planeta < puntuacion_planeta:
        for meta in [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]:
            if puntuacion_planeta >= meta and ultima_recompensa_planeta < meta:
                reward_dinero = meta * 15
                reward_xp = meta * 25
                embed.add_field(
                    name="Recompensa Disponible",
                    value=
                    f"Usa !reclamar_planeta para obtener {reward_dinero}$ + {reward_xp} XP",
                    inline=False)
                break

    embed.set_footer(text=footer_text)

    await ctx.send(embed=embed)


# Reclamar recompenass del planeta
@bot.command()
async def reclamar_planeta(ctx):
    global dinero, xp, puntuacion_planeta, ultima_recompensa_planeta

    recompensas_reclamadas = False
    total_dinero = 0
    total_xp = 0
    metas_claimed = []

    metas = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]

    for meta in metas:
        if puntuacion_planeta >= meta and ultima_recompensa_planeta < meta:
            reward_dinero = meta * 15
            reward_xp = meta * 25

            dinero += reward_dinero
            xp += reward_xp
            total_dinero += reward_dinero
            total_xp += reward_xp
            metas_claimed.append(meta)
            ultima_recompensa_planeta = meta
            recompensas_reclamadas = True

    if recompensas_reclamadas:
        embed = discord.Embed(
            title="Recompensas del Planeta Reclamadas",
            description="Has reclamado tus recompensas por mejorar el planeta",
            color=0x00ff00)
        embed.add_field(
            name="metas Alcanzados",
            value=f"Puntuacion: {', '.join(map(str, metas_claimed))}",
            inline=False)
        embed.add_field(name="Recompensas Obtenidas",
                        value=f"Dinero: +{total_dinero}$\nXP: +{total_xp}",
                        inline=False)
        embed.add_field(
            name="Tu Estado Actual",
            value=
            f"Dinero Total: {dinero}$\nPuntuacion Planeta: {puntuacion_planeta}/100",
            inline=False)
        embed.set_footer(
            text=
            "Sigue realizando acciones ecologicas para obtener mas recompensas"
        )
    else:
        embed = discord.Embed(
            title="No hay recompensas disponibles",
            description=
            "No tienes recompensas del planeta pendientes por reclamar",
            color=0xff6b6b)
        embed.add_field(name="Tu Puntuacion Actual",
                        value=f"{puntuacion_planeta}/100",
                        inline=False)

        meta_siguiente = None
        for meta in metas:
            if puntuacion_planeta < meta:
                meta_siguiente = meta
                break

        if meta_siguiente:
            puntos_necesarios = meta_siguiente - puntuacion_planeta
            embed.add_field(
                name="Proxima Recompensa",
                value=
                f"Necesitas {puntos_necesarios} puntos mas para alcanzar {meta_siguiente} puntos",
                inline=False)

        embed.set_footer(
            text="Realiza mas acciones ecologicas para ganar puntos del planeta"
        )

    await ctx.send(embed=embed)


# Para ejecutar el bot
bot.run('Token')
