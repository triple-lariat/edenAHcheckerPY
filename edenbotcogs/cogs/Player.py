# Author: triple-lariat a.k.a: Tranquille, Desarroi, M.B.
# Any issues you encounter can be posted to https://github.com/triple-lariat/edenAHcheckerPY
# You may also find me on Eden or Eden's discord under the name Tranquille

from discord.ext import commands
from edenbotcogs.coghelpers.Player_helper import *


class Player(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['c'])
    async def check(self, ctx, message: str):
        '''Gets basic player info.
            Usage: !check [player]'''
        player_name = format_player_name(message)
        if check_player_exist(player_name):
            p_info = get_player_info(player_name)
            await ctx.send(embed=build_player_info_embed(player_name, p_info))
        else:
            await ctx.send('Player not found.')

    @commands.command(aliases=['craft'])
    async def crafts(self, ctx, message: str):
        '''Get a player's crafting levels.
            Usage: !crafts [player]'''
        if check_player_exist(message):
            crafts = get_player_crafts(message)
            await ctx.send(embed=build_crafts_embed(message, crafts))
        else:
            await ctx.send('Player not found.')
