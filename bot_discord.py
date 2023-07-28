import discord
import requests
import asyncio

DISCORD_TOKEN = ""
CHATPDF_API_KEY = ""
SOURCE_ID = ""

def get_chatpdf_response(question):
    url = "https://api.chatpdf.com/v1/chats/message"
    headers = {
        "x-api-key": CHATPDF_API_KEY,
        "Content-Type": "application/json",
    }
    data = {
        "sourceId": SOURCE_ID,
        "messages": [
            {
                "role": "user",
                "content": question,
            }
        ]
    }

    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()
    return response.json()["content"]

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Bot conectado como {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!pergunta'):
        def support_check(m):
            return m.author == message.author and m.channel == support_channel

        category_id = "858001239999250462"  # Substitua pelo ID da categoria "chamados - bot"

        await message.channel.send("Você será encaminhado para o chat suporte.")

        try:
            await asyncio.sleep(1)  # Pequeno atraso antes de criar o novo canal
            support_channel = await message.guild.create_text_channel("chat-suporte", category=message.guild.get_channel(int(category_id)))
            await support_channel.send("Qual sua dúvida? Você tem 5 minutos para fazer sua pergunta.")


            question_message = await client.wait_for('message', check=support_check, timeout=300)
            question = "Responda em português, de uma maneira simplificada como se fosse um funcionário de suporte: " + question_message.content.strip()

            # Adicionar a linha abaixo aqui
            chatpdf_response = get_chatpdf_response(question)

            while True:
                # Obter a resposta do ChatPDF
                chatpdf_response = get_chatpdf_response(question)

                # Enviar a resposta no mesmo canal "chat-suporte"
                await support_channel.send(chatpdf_response)

                # Esperar pela próxima mensagem do usuário no canal "chat-suporte"
                question_message = await client.wait_for('message', check=support_check, timeout=300)
                question = "Responda em português, de uma maneira simplificada como se fosse um funcionário de suporte, pode ser bem simplista rapido e direto, se der para não se exceder muito, à menos que seja um duvida que exija mais especifidade: " + question_message.content.strip()

                # Verificar se a mensagem começa com "!encerrar"
                if question_message.content.startswith('!encerrar'):
                    await message.channel.send("O chat-suporte foi encerrado a pedido do usuário.")
                    await asyncio.sleep(1)  # Pequeno atraso antes de excluir o canal
                    await support_channel.delete()
                    break

        except asyncio.TimeoutError:
            await message.channel.send("Tempo limite excedido. O chat-suporte foi encerrado.")
            await asyncio.sleep(1)  # Pequeno atraso antes de excluir o canal
            await support_channel.delete()

client.run(DISCORD_TOKEN)
