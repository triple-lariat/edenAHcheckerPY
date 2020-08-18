# Author: triple-lariat a.k.a: Tranquille, Desarroi, M.B.
# Any issues you encounter can be posted to https://github.com/triple-lariat/edenAHcheckerPY
# You may also find me on Eden or Eden's discord under the name Tranquille

from discord.ext import commands
from edenbotcogs.coghelpers.Timers_helper import *
from edenbotcogs.coghelpers.settings_helper import check_channel

ID = 5005


class Timers(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @check_channel(ID)
    @commands.command()
    async def clock(self, ctx):
        '''Gives the current Vana'diel time, day, and moon phase.
        Usage: !clock'''
        await ctx.send(embed=build_clock_embed())

    @check_channel(ID)
    @commands.command()
    async def calendar(self, ctx):
        '''Gives info about the next 25 Vana'diel days.
        Usage: !calendar'''
        await ctx.send(embed=build_calendar())

    @check_channel(ID)
    @commands.command()
    async def rse(self, ctx, race: str = ''):
        '''Gives RSE start time, location, and end time if a race is provided.
        Usage: !rse [humem|humef|elvaanm|elvaanf|tarum|taruf|mithra|galka]
        !rse with no arguments gives the next few RSE weeks'''
        race = race.lower()
        await ctx.send(embed=build_rse_embed(race))
