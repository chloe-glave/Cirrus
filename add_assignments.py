import boto3
import discord
import os
import random

from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

# AWS Credentials
AWS_ACCESS_KEY = os.getenv('ACCESS_KEY')
AWS_SECRET_KEY = os.getenv('SECRET_KEY')
AWS_PROFILE_NAME = os.getenv('PROFILE_NAME')

session = boto3.Session(
    aws_access_key_id=AWS_ACCESS_KEY
    aws_secret_access_key=AWS_SECRET_KEY
    profile_name=AWS_PROFILE_NAME
)

db_client = session.resource('dynamodb')
bot = commands.Bot(command_prefix="!")

@bot.command(name="add")
async def add_assignment_command(ctx, assignment_name, help="adds an assignment to the database"):
    info = message.content.split()
    body = {"id": random.randint(), "assignment_name": assignment_name}

    table = db_client.Table("CirrusBotMessages")

    table.put_item =(Item=body)

bot.run(TOKEN)