import discord
import asyncio

from historias import py_bot_cap1, py_bot_cap2, cap_3_aviso, py_bot_cap3

async def escrever_historia(channel, texto, delay=1.5):
    msg = await channel.send("...")
    linhas = []

    for linha in texto:

        if linha.startswith("REPLACE:"):
            linhas[-1] = linha.replace("REPLACE:", "").strip()

        else:
            linhas.append(linha)

        conteudo = "\n".join(linhas)
        await msg.edit(content=conteudo)

        await asyncio.sleep(delay)


async def menu_historia(bot, message, historia_menu, historia_pybot):

    historia = await message.channel.send(historia_menu)

    await historia.add_reaction("🤖")
    await historia.add_reaction("🔐")

    def check(reaction, user):
        return (
            user == message.author
            and reaction.message.id == historia.id
        )

    reaction, user = await bot.wait_for("reaction_add", check=check)

    await historia.delete()

    if str(reaction.emoji) == "🤖":

        capitulo = await message.channel.send(historia_pybot)

        await capitulo.add_reaction("🧪")
        await capitulo.add_reaction("🛡️")
        await capitulo.add_reaction("🚨")
        await capitulo.add_reaction("⬅️")

        def check(reaction, user):
            return (
                user == message.author
                and reaction.message.id == capitulo.id
            )

        reaction, user = await bot.wait_for("reaction_add", check=check)

        await capitulo.delete()



        if str(reaction.emoji) == "🧪":

            texto = py_bot_cap1

            async with message.channel.typing():
                await asyncio.sleep(2)

            await escrever_historia(message.channel, texto)



        elif str(reaction.emoji) == "🛡️":

            texto = py_bot_cap2

            async with message.channel.typing():
                await asyncio.sleep(2)

            await escrever_historia(message.channel, texto)

        elif str(reaction.emoji) == "🚨":

            aviso = await message.channel.send("\n".join(cap_3_aviso))

            await aviso.add_reaction("✅")
            await aviso.add_reaction("❌")

            def check_aviso(reaction, user):
                return (
                    user == message.author
                    and reaction.message.id == aviso.id
                )

            reaction, user = await bot.wait_for("reaction_add", check=check_aviso)

            await aviso.delete()

            if str(reaction.emoji) == "✅":

                texto = [
                    linha.replace("{nome}", message.author.display_name)
                    for linha in py_bot_cap3['parte_1']
                ]

                async with message.channel.typing():
                    await asyncio.sleep(2)

                await escrever_historia(message.channel, texto)

                escolha = await message.channel.send(
                ' \n'
                '✅ = "ok, vamos"\n'
                '❌ = "melhor outra hora"'
                )

                await escolha.add_reaction("✅")
                await escolha.add_reaction("❌")

                def check(reaction, user):
                    return (
                        user == message.author
                        and reaction.message.id == escolha.id
                    )

                reaction, user = await bot.wait_for("reaction_add", check=check)

                await escolha.delete()
                if str(reaction.emoji) == "✅":

                    texto = [
                        linha.replace("{nome}", message.author.display_name)
                        for linha in py_bot_cap3['parte_2']
                    ]

                    async with message.channel.typing():
                        await asyncio.sleep(2)

                    await escrever_historia(message.channel, texto)

                    escolha = await message.channel.send(
                        '🛏️ - ir para o quarto do py_bot\n'
                        '💻 - ir para a sala de programação'
                    )

                    await escolha.add_reaction("🛏️")
                    await escolha.add_reaction("💻")

                    def check(reaction, user):
                        return (
                            user == message.author
                            and reaction.message.id == escolha.id
                        )

                    reaction, user = await bot.wait_for("reaction_add", check=check)

                    await escolha.delete()


                elif str(reaction.emoji) == "❌":
                    await message.channel.send(
                        'Pedrão: "isso não é uma escolha"\n'
                        '"vamos logo"'
                    )
                    
                    texto = [
                        linha.replace("{nome}", message.author.display_name)
                        for linha in py_bot_cap3['parte_2']
                    ]

                    async with message.channel.typing():
                        await asyncio.sleep(2)

                    await escrever_historia(message.channel, texto)

                    escolha = await message.channel.send(
                        '🛏️ - ir para o quarto do py_bot\n'
                        '💻 - ir para a sala de programação'
                    )

                    await escolha.add_reaction("🛏️")
                    await escolha.add_reaction("💻")

                    def check(reaction, user):
                        return (
                            user == message.author
                            and reaction.message.id == escolha.id
                        )

                    reaction, user = await bot.wait_for("reaction_add", check=check)
                    
                    await escolha.delete()

        elif str(reaction.emoji) == "⬅️":
            await menu_historia(bot, message, historia_menu, historia_pybot)