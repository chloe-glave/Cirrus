import boto3
import discord
import os
import random

from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

db_client = boto3.resource('dynamodb')
bot = commands.Bot(command_prefix="!")

@bot.command(name="add")
async def add_assignment_command(ctx):
    info = message.content.split()
    body = {"id": random.randint(), "assignment_name": info[1]}

    table = db_client.Table("CirrusBotMessages")

    table.put_item =(Item=body)

bot.run(TOKEN)