import os
import boto3
import random

from datetime import datetime

import discord
from discord.ext import commands
from dotenv import load_dotenv

import helper_functions.create_embed as create_embed

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

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


<<<<<<< HEAD
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Sorry! This function requires more parameters. Run !help <command> to see what parameters are needed")
=======
# error handling
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Sorry! This function requires more parameters. "
                       "Run !help <command> to see what parameters are needed")
    elif isinstance(error, commands.CommandInvokeError):
        print(type(error.__cause__))
        if isinstance(error.__cause__, KeyError):
            await ctx.send("Uh oh! Something was wrong with your input! "
                           "Check to see if you're passing in the correct values!")
        elif isinstance(error.__cause__, ValueError):
            print(type(error.__cause__))
            await ctx.send("Command cancelled.")
    else:
        await ctx.send("Something went wrong here!")

>>>>>>> 7032ba850afd37fc2c186a31b1eca7ce717258d5

# respond to ping message
@bot.command(name='ping', help='Responds to ping for testing purposes')
async def ping(ctx):
    response = f"Pong! 🏓 Response time: {round(bot.latency, 3)}ms"
    await ctx.send(response)


# repeat text given
@bot.command(name='echo', help='Repeats your message')
async def echo(ctx, message):
    response = f"You said: {message}, echo!"
    await ctx.send(response)


# add assignment
@bot.command(name="add", help="""
    Adds an assignment to the database
    Params: assignment_name, assignment_body, day, date
    """)
async def add_assignment_command(ctx, assignment_name, assignment_body, due_month, due_day):
        
    created_time = datetime.now()
    assignment_id = random.randint(0, 1500)

    body = {
        "id": assignment_id,
        "assignment_name": assignment_name,
        "assignment_body": assignment_body,
        "date_created": created_time.strftime("%c"),
        "due_month": int(due_month),
        "due_day": int(due_day)
    }

    try:
        table = db_client.Table("CirrusBotMessages")
        db_response = table.put_item(Item=body)['ResponseMetadata']['HTTPStatusCode']
        print(f"HTTP Response: {db_response}")
    except ConnectionAbortedError:
        raise commands.CommandInvokeError

    # todo: separate file for db manipulation functions
    try:
        table = db_client.Table("CirrusBotMessages")
        response = table.get_item(Key={'id': int(assignment_id), 'assignment_name': assignment_name})['Item']
    except Exception as e:
        raise e

    em = create_embed.create_assignment_embed(response, 'Assignment created!', create_embed.PASTEL_YELLOW)

    await ctx.send(embed=em)


# lists all assignments
@bot.command(name='list', help='List all assignments added')
async def list_assignments(ctx):
    try:
        table = db_client.Table("CirrusBotMessages")
        response = table.scan()['Items']
    except ConnectionAbortedError:
        raise commands.CommandInvokeError

    em = create_embed.create_assignment_embed(response, 'Your current assignments:', create_embed.PASTEL_GREEN)

    await ctx.send(embed=em)


# deletes an assignment by id and assignment name
@bot.command(name='delete', help='Delete indicated assignment by ID and assignment name')
async def delete_assignments(ctx, assignment_id, assignment_name):
    try:
        table = db_client.Table("CirrusBotMessages")
        response = table.delete_item(
            Key={
                'id': int(assignment_id),
                'assignment_name': assignment_name
            }
        )['ResponseMetadata']['HTTPStatusCode']
        await ctx.send(f"HTTP Response: {response}")
    except ConnectionAbortedError:
        raise commands.CommandInvokeError


# clear all assignments
@bot.command(name='clear', help='Clears ALL assignments from the list')
async def clear_assignments(ctx):
    await ctx.send("Are you sure you want to clear all assignments? Type `y` to confirm or anything else to cancel.")

    def check(m):
        if not (m.content == "y" and m.channel == ctx.channel):
            raise ValueError("Cancelled")
        else:
            return True

    msg = await bot.wait_for("message", check=check)
    try:
        await ctx.send(f"ok, deleting... this is {msg.author}'s fault!")

        try:
            table = db_client.Table("CirrusBotMessages")
            response = table.scan()['Items']
        except Exception:
            raise commands.CommandInvokeError

        deleted_items = []
        for i in response:
            deleted_items.append({
                'DeleteRequest': {
                    'Key': {
                        'id': int(i['id']),
                        'assignment_name': i['assignment_name']
                    }
                }
            })
        print(deleted_items)

        try:
            db_client.batch_write_item(RequestItems={
                'CirrusBotMessages': deleted_items
            })
        except Exception:
            raise commands.CommandInvokeError

        await ctx.send(f"Deletion Successful!")
    except ValueError:
        raise ValueError


# gets an assignment by id and assignment name
@bot.command(name='get', help='Get indicated assignment by ID and assignment name')
async def get_assignments(ctx, assignment_id, assignment_name):
    try:
        table = db_client.Table("CirrusBotMessages")
        response = table.get_item(Key={'id': int(assignment_id), 'assignment_name': assignment_name})['Item']
    except Exception as e:
        raise e

    em = create_embed.create_assignment_embed(response, 'Found assignment:', create_embed.PASTEL_PURPLE)

    await ctx.send(embed=em)


bot.run(TOKEN)
