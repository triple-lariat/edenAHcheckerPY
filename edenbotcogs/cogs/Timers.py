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
        v = get_vana_time()
        await ctx.send(f'{get_vana_ymd(v)} - {get_vana_hms(v)} - {get_vana_week_day(v)} ... moon:{get_moon_phase()}')
