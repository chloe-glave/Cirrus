import os

from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

bot = commands.Bot(command_prefix='!')


# respond to ping message
@bot.command(name='ping', help='Responds to ping for testing purposes')
async def ping(ctx):
    response = f'pong! {bot.latency}'
    await ctx.send(response)

bot.run(TOKEN)
