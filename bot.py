import discord
from discord.ext import commands
import requests as r
from datetime import datetime
import json, ast, pytz, platform
import edenAHhelper as helper

# import bot token from separate file 'eden_bot_token.py'
try:
        from eden_bot_token import eden_bot_token
except ImportError:
        raise ImportError('You must create a file "eden_bot_token.py" with' +
                          ' variable eden_bot_token = "your.bot.token"')

description = ''
bot = commands.Bot(command_prefix='!', description=description)

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    await bot.change_presence(activity=discord.Activity(name=platform.system(),
                                                        type=discord.ActivityType.playing))

@bot.command()
async def add(ctx, left: int, right: int):
    """Adds two numbers together."""
    await ctx.send(left + right)

@bot.command()
async def ping(ctx):
        await ctx.send('pong')

@bot.command()
async def args(ctx, *, message:str):
        message = message.split(' ')
        for item in enumerate(message):
                await ctx.send(message[item[0]])

@bot.command()
async def ah(ctx, *, message:str):
        # split the arguments given with command into an array
        message = message.split(' ')
        separator = '_'
        # check whether to look up a stack or single of given item
        stack_flag = 'false'
        if message[-1] == 'y':
                stack_flag = 'true'
                item_name = separator.join(message[:-1])
        else:
                item_name = separator.join(message)

        # check if the item given actually exists
        page_exist = helper.check_item(item_name)
        
        await ctx.send(embed=helper.build_AH_embed(item_name, page_exist, stack_flag))

@bot.command(aliases =['bazaar'])
async def b(ctx, *, message:str):
        # split the arguments given with command into an array
        message = message.split(' ')
        separator = '_'
        item_name = separator.join(message)

        page_exist = helper.check_item(item_name)

        await ctx.send(embed=helper.build_bazaar_embed(item_name, page_exist))

@bot.command(aliases=['y'])
async def yells(ctx):
        await ctx.send(embed=helper.build_yell_embed())

bot.run(eden_bot_token)
