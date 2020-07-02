import platform

import discord
from discord.ext import commands

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
    print('edenAHbot Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    await bot.change_presence(activity=discord.Activity(name=platform.system(),
                                                        type=discord.ActivityType.playing))


@bot.command()
async def getid(ctx, *, message: str):
    '''Get the item ID and homepointxi link for any item
                (filtered out some OOE items)'''
    message = message.split(' ')
    separator = '_'
    item_name = separator.join(message)
    csv = open('item_names_and_ids.csv', 'r')
    item_info = []
    for line in csv:
        item_info.append(line.split(','))
    i = 0
    try:
        while not (item_info[i][1].rstrip() == item_name):
            i += 1
        await ctx.channel.send(item_info[i])
        await ctx.channel.send(f'http://homepointxi.com/db/items/{item_info[i][0]}/{item_name}')
    except IndexError:
        await ctx.channel.send('No item found')
    csv.close()


@bot.command()
async def ping(ctx):
    await ctx.send('pong')


@bot.command()
async def args(ctx, *, message: str):
    message = message.split(' ')
    for item in enumerate(message):
        await ctx.send(message[item[0]])


@bot.command()
async def ah(ctx, *, message: str):
    '''Gets the AH entries for an item from the website.
            Usage: !ah [item name] [y for stack]'''
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
    stack_flag = page_exist[1]

    await ctx.send(embed=helper.build_AH_embed(item_name, page_exist[0], stack_flag))


@bot.command(aliases=['bazaar'])
async def b(ctx, *, message: str):
    '''Gets the bazaar entries for an item. May take a while...
           Usage: !b [item name]
           Note: the "x2" or other number beside an entry shows how many
           individual item slots, not the actual amount.'''
    # split the arguments given with command into an array
    message = message.split(' ')
    separator = '_'
    item_name = separator.join(message)

    page_exist = helper.check_item(item_name)

    await ctx.send(embed=helper.build_bazaar_embed(item_name, page_exist))


# @bot.command(aliases=['y'])
# async def yells(ctx):
#        await ctx.send(embed=helper.build_yell_embed())

# Add help details for yellbot.py commands.
@bot.command()
async def yells(ctx):
    '''Enables live yell chat log in the channel this command is used in.
           Usage: !yells [on|off]'''
    return


bot.run(eden_bot_token)
