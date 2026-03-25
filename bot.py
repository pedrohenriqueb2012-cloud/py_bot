import discord
import random
import asyncio

import os
from dotenv import load_dotenv
from discord.ext import commands

# carregar token
load_dotenv(dotenv_path="c:/Users/rbert/Documents/codigos_kodland/bot_1/token")

# intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# criar bot
bot = commands.Bot(command_prefix="$", intents=intents, help_command=None)

from bot_logic import gen_pass, chamar, help_text
from historias import historia_menu, historia_pybot
from historia_reac import menu_historia


@bot.event
async def on_ready():
    print(f'Fizemos login como {bot.user}')


@bot.event
async def on_message(message):

    if message.author == bot.user:
        return

    # sistema de menções
    if message.mentions:
        for mention in message.mentions:
            frase = random.choice(chamar).format(mention=mention.mention)
            await message.channel.send(frase)
        return

    # repetir mensagem se não for comando
    if not message.content.startswith("$"):
        await message.channel.send(message.content)

    # importante para comandos funcionarem
    await bot.process_commands(message)

@bot.command()
async def hello(ctx):
    await ctx.send("Hello!")


@bot.command()
async def bye(ctx):
    await ctx.send("\U0001f642")


@bot.command()
async def help(ctx):
    await ctx.send(help_text)


@bot.command()
async def coin(ctx):

    await ctx.message.delete()

    moeda = random.choice(['Cara', 'Coroa'])

    await ctx.send(
        f"{ctx.author.mention} jogou uma moeda e deu **{moeda}**!"
    )


@bot.command()
async def checkDM(ctx):

    try:
        DM = await ctx.author.send(
            "Teste: este é um DM do py_bot.\n"
            "Se você recebeu, reaja com ✅ para confirmar!"
        )

        await DM.add_reaction("✅")

        await ctx.send(
            f"{ctx.author.mention}, enviei um DM de teste para você — confira sua caixa de entrada!"
        )

        def check(reaction, user):
            return (
                user == ctx.author
                and str(reaction.emoji) == "✅"
                and reaction.message.id == DM.id
            )

        reaction, user = await bot.wait_for("reaction_add", check=check)

        await ctx.author.send("Perfeito! Sua DM está funcionando corretamente!")

    except discord.Forbidden:

        await ctx.send(
            f"{ctx.author.mention}, não consegui enviar DM. Verifique suas configurações de privacidade."
        )


@bot.command()
async def historia(ctx):

    try:

        dm = await ctx.author.create_dm()

        await ctx.send(
            f"{ctx.author.mention} 📜 Verifique sua DM!"
        )

        class FakeMessage:
            def __init__(self, author, channel):
                self.author = author
                self.channel = channel

        fake_message = FakeMessage(ctx.author, dm)

        await menu_historia(bot, fake_message, historia_menu, historia_pybot)

    except discord.Forbidden:

        await ctx.send(
            f"{ctx.author.mention} ❌ ERRO ❌ use $checkDM para verificar se seu DM está ativado!"
        )


print(gen_pass(10))

bot.run(os.getenv("DISCORD_TOKEN"))