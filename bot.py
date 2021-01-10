import os
import boto3
import random
import datetime
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

bot = commands.Bot(command_prefix='!')

# AWS Credentials
AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_PROFILE_NAME = os.getenv('PROFILE_NAME')
AWS_REGION_NAME = os.getenv('REGION_NAME')

session = boto3.Session(
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    profile_name=AWS_PROFILE_NAME,
    region_name=AWS_REGION_NAME
)

db_client = session.resource('dynamodb')
bot = commands.Bot(command_prefix="!")


# respond to ping message
@bot.command(name='ping', help='Responds to ping for testing purposes')
async def ping(ctx):
    response = f'Pong! 🏓 Response time: {round(bot.latency, 3)}ms'
    await ctx.send(response)


# repeat text given
@bot.command(name='echo', help='Repeats your message')
async def echo(ctx, message):
    response = f'You said: {message}, echo!'
    await ctx.send(response)


# add assignment
@bot.command(name="add", help="""Adds an assignment to the database
        Params: assignment_name, assignment_body, day, date
""")
async def add_assignment_command(ctx, assignment_name, assignment_body, day, date):

    created_time = datetime.datetime.now()

    body = {
        "id": random.randint(0, 1500),
        "assignment_name": assignment_name,
        "assignment_body": assignment_body,
        "date_created": created_time.strftime("%c"),
        "due_date": f"{day} {date}"
    }

    table = db_client.Table("CirrusBotMessages")

    db_response = table.put_item(Item=body)['HTTPStatusCode']

    await ctx.send(f"HTTP Response: {db_response}")


@bot.command(name='list', help='List all assignments added')
async def list_assignments(ctx):

    table = db_client.Table("CirrusBotMessages")
    response = table.scan()['Items']

    for i in response:
        string = f"ID: {i['id']}\nDate Created: {i['date_created']}\nName: {i['assignment_name']}\n" \
                 f"Description: {i['assignment_body']}"

        await ctx.send(f'{string}')


@bot.command(name='delete', help='Delete indicated assignment by ID and assignment name')
async def delete_assignments(ctx, assignment_id, assignment_name):

    table = db_client.Table("CirrusBotMessages")
    response = table.delete_item(Key={'id': int(assignment_id), 'assignment_name': assignment_name},)    

    await ctx.send(response)

@bot.command(name='get', help='Delete indicated assignment by ID and assignment name')
async def delete_assignments(ctx, assignment_id, assignment_name):

    table = db_client.Table("CirrusBotMessages")
    response = table.get_item(Key={'id': int(assignment_id), 'assignment_name': assignment_name},)['Item']    

    string = f"ID: {response['id']}\nDate Created: {response['date_created']}\nName: {response['assignment_name']}\n" \
                 f"Description: {response['assignment_body']}"

    await ctx.send(f'{string}')


bot.run(TOKEN)
