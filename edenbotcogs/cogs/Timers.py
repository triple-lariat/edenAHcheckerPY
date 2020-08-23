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

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def timezone(self, ctx, message: str):
        '''Sets the time zone for printed times.
        Usage: !timezone [time zone]
        Valid US timezones: Central, Arizona, Eastern, Pacific, Mountain'''
        tz = f'US/{message}'
        server_id = ctx.message.guild.id
        if set_timezone(tz, server_id):
            await ctx.message.add_reaction('✅')
        else:
            await ctx.send('Timezone change failed! Did you enter a valid timezone?')


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
    async def fullmoon(self, ctx):
        '''Gives the time to next full moon.
        Usage: !fullmoon'''
        next_full = get_next_end_moon(True, ctx.message.guild.id)
        await ctx.send(f'Next full moon at: {next_full}')

    @check_channel(ID)
    @commands.command()
    async def newmoon(self, ctx):
        '''Gives the time to next new moon
        Usage: !newmoon'''
        next_new = get_next_end_moon(False, ctx.message.guild.id)
        await ctx.send(f'Next new moon at: {next_new}')

    @check_channel(ID)
    @commands.command()
    async def rse(self, ctx, race: str = ''):
        '''Gives RSE start time, location, and end time if a race is provided.
        Usage: !rse [humem|humef|elvaanm|elvaanf|tarum|taruf|mithra|galka]
        !rse with no arguments gives the next few RSE weeks'''
        race = race.lower()
        await ctx.send(embed=build_rse_embed(race, ctx.message.guild.id))
