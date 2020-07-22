# Author: triple-lariat a.k.a: Tranquille, Desarroi, M.B.
# Any issues you encounter can be posted to https://github.com/triple-lariat/edenAHcheckerPY
# You may also find me on Eden or Eden's discord under the name Tranquille

from discord.ext import commands

class Market(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ah(self, ctx, *, message: str):
        '''Gets the AH entries for an item from the website.
            Usage: !ah [item name] [y for stack]'''
        # split the arguments given with command into an array
        message = helper.format_item_string(message)
        separator = '_'
        # check whether to look up a stack or single of given item
        stack_flag = 'false'
        if message[-1] == 'y':
            stack_flag = 'true'
            item_name = separator.join(message[:-1])
        else:
            item_name = separator.join(message)

        # check if the item given actually exists, pass recursive flag as false
        page_exist = helper.check_item(item_name, False)
        prefix = page_exist[2]

        # concat item name and prefix if one was not given by command args
        item_name = prefix + item_name

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
        message = helper.format_item_string(message)
        separator = '_'
        item_name = separator.join(message)

        page_exist = helper.check_item(item_name, False)

        prefix = page_exist[2]

        # concat item name and prefix if one was not given by command args
        item_name = prefix + item_name

        await ctx.send(embed=helper.build_bazaar_embed(item_name, page_exist))