const { Client, Intents } = require('discord.js');
const axios = require('axios');

const DISCORD_TOKEN = "MTEzMTU3MDcxOTk2OTUyMTY5NA.GbGg0E.iEg5iDhkYsuyGmADP4NXTwHv0b4S0l4GKqBE2Q";
const CHATPDF_API_KEY = "sec_MREH39JMvKwBuEg1zmKvkTkErqbvFYTa";
const SOURCE_ID = "share/m0ZVtQHsZ5AfAuLYjVaJF";

const intents = new Intents([
  Intents.FLAGS.GUILDS,
  Intents.FLAGS.GUILD_MESSAGES,
  Intents.FLAGS.DIRECT_MESSAGES,
]);

const client = new Client({ intents });

client.once('ready', () => {
  console.log('Bot conectado como ' + client.user.tag);
});

client.on('messageCreate', async (message) => {
  if (message.author.bot) return;

  if (message.content.startsWith('!pdf')) {
    await message.channel.send("Por favor, envie a pergunta que deseja fazer.");

    const filter = (m) => m.author.id === message.author.id;
    const questionMessage = await message.channel.awaitMessages({
      filter,
      max: 1,
      time: 60000,
      errors: ['time']
    });

    const question = questionMessage.first().content.trim();
    const response = await chatPdf(question, SOURCE_ID);

    await message.channel.send(response);
  }
});

async function chatPdf(question, sourceId) {
  const url = "https://api.chatpdf.com/v1/chats/message";
  const headers = {
    "x-api-key": CHATPDF_API_KEY,
    "Content-Type": "application/json",
  };
  const data = {
    "sourceId": sourceId,
    "messages": [
      {
        "role": "user",
        "content": question,
      }
    ]
  };

  try {
    const response = await axios.post(url, data, { headers });
    if (response.status === 200) {
      return response.data.content;
    } else {
      return "Desculpe, não consegui obter uma resposta.";
    }
  } catch (error) {
    console.error(error);
    return "Ocorreu um erro ao obter a resposta.";
  }
}

client.login(DISCORD_TOKEN);
