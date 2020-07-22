# Author: triple-lariat a.k.a: Tranquille, Desarroi, M.B.
# Any issues you encounter can be posted to https://github.com/triple-lariat/edenAHcheckerPY
# You may also find me on Eden or Eden's discord under the name Tranquille

from discord.ext import commands


class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['exp'])
    async def tnl(self, ctx, *, message: str):
        '''Get the exp from the beginning of a certain level to the end of another.
        Usage: !tnl [initial level] [target level]'''
        lvls = message.split(' ')
        lvls.append('75')
        print(lvls)
        try:
            initial_level = int(lvls[0])
            target_level = int(lvls[1])
            exp_msg = helper.get_tnl(initial_level, target_level)

            await ctx.send(exp_msg)

        except ValueError:
            await ctx.send('Levels must be provided as numbers (like 1 or 30)')
        except IndexError:
            await ctx.send('Must provide two levels.')

    @commands.command()
    async def getid(self, ctx, *, message: str):
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
