import asyncio
import discord
import random
import os
from dotenv import load_dotenv
from discord.ext import commands

# carregar token do arquivo .env deste projeto
load_dotenv()
token = os.getenv("DISCORD_TOKEN")

if not token:
    raise RuntimeError("A variável DISCORD_TOKEN não foi encontrada no arquivo .env")

# intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# criar bot
bot = commands.Bot(command_prefix="$", intents=intents, help_command=None)

partidas_da_velha = set()

from bot_logic import chamar, help_text
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
async def jogodavelha(ctx):

    partida_id = (ctx.guild.id if ctx.guild else "dm", ctx.channel.id, ctx.author.id)
    if partida_id in partidas_da_velha:
        await ctx.send(f"{ctx.author.mention}, você já está em uma partida!")
        return

    partidas_da_velha.add(partida_id)
    tabuleiro = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
    combinacoes_vencedoras = (
        (0, 1, 2), (3, 4, 5), (6, 7, 8),
        (0, 3, 6), (1, 4, 7), (2, 5, 8),
        (0, 4, 8), (2, 4, 6),
    )

    def mostrar_tabuleiro():
        return (
            f" {tabuleiro[0]} | {tabuleiro[1]} | {tabuleiro[2]}\n"
            "---+---+---\n"
            f" {tabuleiro[3]} | {tabuleiro[4]} | {tabuleiro[5]}\n"
            "---+---+---\n"
            f" {tabuleiro[6]} | {tabuleiro[7]} | {tabuleiro[8]}"
        )

    def venceu(simbolo):
        return any(
            all(tabuleiro[posicao] == simbolo for posicao in combinacao)
            for combinacao in combinacoes_vencedoras
        )

    try:
        await ctx.send(
            f"{ctx.author.mention}, vamos jogar! Você é **X** e eu sou **O**.\n"
            "Envie o número da casa onde quer jogar (1 a 9).\n"
            f"```\n{mostrar_tabuleiro()}\n```"
        )

        while True:
            def jogada_valida(message):
                return (
                    message.author == ctx.author
                    and message.channel == ctx.channel
                    and message.content.strip() in {str(numero) for numero in range(1, 10)}
                )

            try:
                mensagem = await bot.wait_for("message", check=jogada_valida, timeout=120)
            except asyncio.TimeoutError:
                await ctx.send("O jogo terminou por falta de resposta.")
                return

            posicao = int(mensagem.content.strip()) - 1
            if tabuleiro[posicao] in ("X", "O"):
                await ctx.send("Essa casa já está ocupada. Escolha outra de 1 a 9.")
                continue

            tabuleiro[posicao] = "X"
            if venceu("X"):
                await ctx.send(f"Você venceu!\n```\n{mostrar_tabuleiro()}\n```")
                return
            if all(casa in ("X", "O") for casa in tabuleiro):
                await ctx.send(f"Deu velha!\n```\n{mostrar_tabuleiro()}\n```")
                return

            casas_livres = [indice for indice, casa in enumerate(tabuleiro) if casa not in ("X", "O")]
            jogada_bot = random.choice(casas_livres)
            tabuleiro[jogada_bot] = "O"
            if venceu("O"):
                await ctx.send(f"Eu venci!\n```\n{mostrar_tabuleiro()}\n```")
                return
            await ctx.send(f"Minha jogada foi **{jogada_bot + 1}**.\n```\n{mostrar_tabuleiro()}\n```")
    finally:
        partidas_da_velha.discard(partida_id)


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


@bot.command()
async def check(ctx):

    if ctx.message.attachments:
        for attachment in ctx.message.attachments:
            file_name = attachment.filename
            file_url = attachment.url
            await ctx.send(f'Arquivo recebido: {file_name}\nURL: {file_url}')
            await ctx.send(f"{ctx.author.mention} seu item é: {file_name}")
    else:
        await ctx.send('Nenhum arquivo foi enviado.')


bot.run(token)