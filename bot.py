import os
import boto3
import random

from datetime import datetime, timedelta
import calendar

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

bot = commands.Bot(command_prefix='!')

# AWS Credentials
AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_REGION_NAME = os.getenv('REGION_NAME')

session = boto3.Session(
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=AWS_REGION_NAME
)

db_client = session.resource('dynamodb')
bot = commands.Bot(command_prefix="!")

# error handling
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Sorry! This function requires more parameters. Run !help <command> to see what parameters are needed")
    elif isinstance(error, commands.CommandInvokeError):
        print(type(error.__cause__))
        if isinstance(error.__cause__, KeyError):
            await ctx.send("Uh oh! Something was wrong with your input! Check to see if you're passing in the correct values!")
        else:
            await ctx.send("Something went wrong here!")

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
async def add_assignment_command(ctx, assignment_name, assignment_body, due_month, due_day):
    created_time = datetime.now()

    body = {
        "id": random.randint(0, 1500),
        "assignment_name": assignment_name,
        "assignment_body": assignment_body,
        "date_created": created_time.strftime("%c"),
        "due_month": int(due_month),
        "due_day": int(due_day)
    }

    try:
        table = db_client.Table("CirrusBotMessages")
        db_response = table.put_item(Item=body)['ResponseMetadata']['HTTPStatusCode']
        await ctx.send(f"HTTP Response: {db_response}")
    except ConnectionAbortedError:
        raise commands.CommandInvokeError

# lists all assignments
@bot.command(name='list', help='List all assignments added')
async def list_assignments(ctx):
    try:
        table = db_client.Table("CirrusBotMessages")
        response = table.scan()['Items']
    except ConnectionAbortedError:
        raise commands.CommandInvokeError

    em = discord.Embed(
        title='Your current assignments:',
        color=0x77dd77,  # green
    )

    for i in response:
        assignment_description = \
            f'''
                `📌 Desc:` {i['assignment_body']}
                `📆 Due:` {i['due_month']}/{i['due_day']}
                `🔑 ID:` {i['id']}
            '''

        em.add_field(
            name=i['assignment_name'],
            value=assignment_description,
            inline=False
        )

    await ctx.send(embed=em)

# deletes an assignment by id and assignment name
@bot.command(name='delete', help='Delete indicated assignment by ID and assignment name')
async def delete_assignments(ctx, assignment_id, assignment_name):
    try:
        table = db_client.Table("CirrusBotMessages")
        response = table.delete_item(Key={'id': int(assignment_id), 'assignment_name': assignment_name},)['ResponseMetadata']['HTTPStatusCode']
        await ctx.send(f"HTTP Response: {response}")
    except ConnectionAbortedError:
        raise commands.CommandInvokeError
    

# gets an assignment by id and assignment name
@bot.command(name='get', help='Get indicated assignment by ID and assignment name')
async def get_assignments(ctx, assignment_id, assignment_name):
    try:
        table = db_client.Table("CirrusBotMessages")
        response = table.get_item(Key={'id': int(assignment_id), 'assignment_name': assignment_name}, )['Item']
    except Exception as e:
        raise e

    em = discord.Embed(
        title=response['assignment_name'],
        description=response['assignment_body'],
        color=0x77dd77,  # green
        timestamp=datetime.strptime(
            f"{calendar.month_name[int(response['due_month'])]} {int(response['due_day'])} {datetime.now().year}",
            '%B %d %Y'
        ) + timedelta(days=1)  # add one cuz it subtracts one for unknown reason
    )
    em.set_footer(text=f"ID: {response['id']}")

    await ctx.send(embed=em)


bot.run(TOKEN)
