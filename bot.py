import os
import random

import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client()


@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )


# respond to ping message
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content == 'ping':
        response = 'pong!'
        await message.channel.send(response)

client.run(TOKEN)
