# Author: triple-lariat a.k.a: Tranquille, Desarroi, M.B.
# Any issues you encounter can be posted to https://github.com/triple-lariat/edenAHcheckerPY
# You may also find me on Eden or Eden's discord under the name Tranquille

from discord.ext import commands
from edenbotcogs.coghelpers.Timers_helper import *


class Timers(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def clock(self, ctx):
        '''Gives the current Vana'diel time, day, and moon phase.
        Usage: !clock'''
        await ctx.send(embed=build_clock_embed())

    @commands.command()
    async def calendar(self, ctx):
        await ctx.send(embed=build_calendar())
