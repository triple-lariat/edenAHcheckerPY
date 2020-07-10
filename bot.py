# Author: triple-lariat a.k.a: Tranquille, Desarroi, M.B.
# Any issues you encounter can be posted to https://github.com/triple-lariat/edenAHcheckerPY
# You may also find me on Eden or Eden's discord under the name Tranquille

import platform

import discord
from discord.ext import commands

import edenAHhelper as helper

# import bot token from separate file 'eden_bot_token.py'
try:
    from eden_bot_token import eden_bot_token
except ImportError:
    new_instance = open('eden_bot_token.py', 'w')
    new_instance.write('eden_bot_token = "YoUrBotTokEn"')
    raise ImportError('Please enter your bot token in eden_bot_token.py' +
                      '\nThis file has been created for you.')

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


@bot.command(hidden=True)
async def ping(ctx):
    await ctx.send('pong')


@bot.command(hidden=True)
async def args(ctx, *, message: str):
    message = message.split(' ')
    for item in enumerate(message):
        await ctx.send(message[item[0]])


class Player(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['c'])
    async def check(self, ctx, message: str):
        '''Gets basic player info.
            Usage: !check [player]'''
        player_name = helper.format_player_name(message)
        if helper.check_player_exist(player_name):
            p_info = helper.get_player_info(player_name)
            await ctx.send(embed=helper.build_player_info_embed(player_name, p_info))
        else:
            await ctx.send('Player not found.')

    @commands.command(aliases=['craft'])
    async def crafts(self, ctx, message: str):
        '''Get a player's crafting levels.
            Usage: !crafts [player]'''
        if helper.check_player_exist(message):
            crafts = helper.get_player_crafts(message)
            await ctx.send(embed=helper.build_crafts_embed(message, crafts))
        else:
            await ctx.send('Player not found.')


class Market(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ah(self, ctx, *, message: str):
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
        if page_exist[1] == 'false':
            stack_flag = page_exist[1]

        await ctx.send(embed=helper.build_AH_embed(item_name, page_exist[0], stack_flag))

    @commands.command(aliases=['bazaar'], category="Market")
    async def b(self, ctx, *, message: str):
        '''Gets the bazaar entries for an item. May take a while...
           Usage: !b [item name]
           Note: the "x2" or other number beside an entry shows how many
           individual item slots, not the actual amount.'''
        # split the arguments given with command into an array
        message = message.split(' ')
        separator = '_'
        item_name = separator.join(message)

        page_exist = helper.check_item(item_name)[1]

        await ctx.send(embed=helper.build_bazaar_embed(item_name, page_exist))


# Add help details for yellbot.py commands.
@bot.command()
async def yells(ctx):
    '''Enables live yell chat log in the channel this command is used in.
           Usage: !yells [on|off]'''
    return

# add created cogs
bot.add_cog(Player(bot))
bot.add_cog(Market(bot))

try:
    bot.run(eden_bot_token)
except discord.LoginFailure:
    print('There was an error logging in. Please ensure you have the right login token set in eden_bot_token.py')
