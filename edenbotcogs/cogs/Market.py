# Author: triple-lariat a.k.a: Tranquille, Desarroi, M.B.
# Any issues you encounter can be posted to https://github.com/triple-lariat/edenAHcheckerPY
# You may also find me on Eden or Eden's discord under the name Tranquille

from discord.ext import commands
from edenbotcogs.coghelpers.Market_helper import *
from edenbotcogs.coghelpers.settings_helper import check_channel

ID = 4004


class Market(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @check_channel(ID)
    @commands.command()
    async def ah(self, ctx, *, message: str):
        '''Gets the AH entries for an item from the website.
            Usage: !ah [item name] [y for stack]'''
        # split the arguments given with command into an array
        message = format_item_string(message)

        server_id = ctx.message.guild.id

        separator = '_'
        # check whether to look up a stack or single of given item
        stack_flag = 'false'
        if message[-1] == 'y':
            stack_flag = 'true'
            item_name = separator.join(message[:-1])
        else:
            item_name = separator.join(message)

        # check if the item given actually exists
        item_info = check_item(item_name)

        item_name = item_info[0]
        additional_results = item_info[2]

        if item_info[1] == 'false':
            stack_flag = item_info[1]

        if item_name:
            await ctx.send(embed=build_AH_embed(item_name, stack_flag, server_id))
        elif additional_results:
            await ctx.send('No results found, did you mean one of these items?\n')
            results = ''
            for item in additional_results[:20]:
                results += format_name(item) + '\n'
            await ctx.send(results)
        else:
            await ctx.send("I couldn't find any matches for that item, " + ctx.author.mention + '!')

    @check_channel(ID)
    @commands.command(aliases=['bazaar'], category="Market")
    async def b(self, ctx, *, message: str):
        '''Gets the bazaar entries for an item. May take a while...
           Usage: !b [item name]
           Note: the "x2" or other number beside an entry shows how many
           individual item slots, not the actual amount.'''
        # split the arguments given with command into an array
        message = format_item_string(message)
        separator = '_'
        item_name = separator.join(message)

        # check if the item given actually exists
        item_info = check_item(item_name)

        item_name = item_info[0]
        additional_results = item_info[2]

        if item_name:
            await ctx.send(embed=build_bazaar_embed(item_name))
        elif additional_results:
            await ctx.send('No results found, did you mean one of these items?\n')
            results = ''
            for item in additional_results[:20]:
                results += format_name(item) + '\n'
            await ctx.send(results)
        else:
            await ctx.send("I couldn't find any matches for that item, " + ctx.author.mention + '!')

    @check_channel(ID)
    @commands.command(hidden=True)
    async def search(self, ctx, *, message: str):
        await ctx.send(search_item(message))
