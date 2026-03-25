import random
import asyncio

chamar = [
    "Ei {mention}, você foi convocado! 🔔",
    "ei, {mention}, venha aqui!! 😎",
    "Marcando {mention} para uma aventura! 🚀",
    "{mention}, prepare-se para o caos! 😈",
    "Chamando {mention}! Hora de brilhar! ✨"
]

help_text = (
    '**olá! aqui está uma lista de comandos para você usar!**\n'
    ' \n'
    '"$help" - eu mostro essa mensagem, se você não soubesse isso, não estaria lendo!\n'
    '"$hello" - eu respondo com um Hello!\n'
    '"$bye" - eu mando um emoji sorridente!\n'
    '"$coin" - eu jogo uma moeda para você (cara ou coroa)!!\n'
    '@[usuário] - eu chamo o usuário junto com você!\n'
    '$checkDM - eu mando uma mensagem a sua DM para testar se está funcionando!\n'
    '$historia - começo a contar histórias!'
)



def gen_pass(pass_length):
    elements = "+-/*!&$#?=@<>"
    password = ""
    for i in range(pass_length):
        password += random.choice(elements)
    return password
    
