# Author: triple-lariat a.k.a: Tranquille, Desarroi, M.B.
# Any issues you encounter can be posted to https://github.com/triple-lariat/edenAHcheckerPY
# You may also find me on Eden or Eden's discord under the name Tranquille

from time import time
from discord.ext import commands, tasks
from edenbotcogs.coghelpers.Player_helper import *
import pickle
from edenbotcogs.coghelpers.settings_helper import check_channel

ID = 2002


class Player(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.track_activity.start()
        self.most_recent_activity = {}

    @check_channel(ID)
    @commands.command(aliases=['c'])
    async def check(self, ctx, message: str):
        '''Gets basic player info.
            Usage: !check [player]'''
        server_id = ctx.message.guild.id
        player_name = format_player_name(message)
        if await check_player_exist(player_name):
            p_info = await get_player_info(player_name)
            try:
                last_online = self.most_recent_activity[format_name(player_name)]
                last_online = get_readable_timestamp(last_online, server_id)
            except KeyError:
                last_online = 'At least 7/31'
            await ctx.send(embed=build_player_info_embed(player_name, p_info, last_online, server_id))
        else:
            await ctx.send('Player not found.')

    @check_channel(ID)
    @commands.command(aliases=['craft'])
    async def crafts(self, ctx, message: str):
        '''Get a player's crafting levels.
            Usage: !crafts [player]'''
        player_name = format_player_name(message)
        if await check_player_exist(player_name):
            crafts = await get_player_crafts(player_name)
            await ctx.send(embed=build_crafts_embed(player_name, crafts))
        else:
            await ctx.send('Player not found.')

    @check_channel(ID)
    @commands.command()
    async def equip(self, ctx, name: str):
        '''Displays a player's equipment.
            Usage: !equip [player]'''
        player_name = format_player_name(name)
        if await check_player_exist(player_name):
            embed = await build_equip_embed(player_name)
            await ctx.send(file=embed[1], embed=embed[0])

    @check_channel(ID)
    @commands.command()
    async def jobs(self, ctx, name: str):
        player_name = format_player_name(name)
        if await check_player_exist(player_name):
            embed = await build_jobs_embed(player_name)
            await ctx.send(embed=embed)
        else:
            await ctx.send('Player not found.')

    @tasks.loop(seconds=1800)
    async def track_activity(self):
        await self.bot.wait_until_ready()

        try:
            activity_read = open('eden_player_activity.txt', 'rb')
            activity_dict = pickle.load(activity_read)
            activity_read.close()
        except FileNotFoundError:
            activity_dict = {}

        async with aiohttp.ClientSession() as s:
            async with s.get('https://144.217.79.186/api/v1/chars?online=true&limit=28000') as resp:
                current_online = await resp.text()
        current_online = ast.literal_eval(current_online)['chars']
        log_time = int(time())

        for player in current_online:
            activity_dict[player['charname']] = log_time

        activity_write = open('eden_player_activity.txt', 'wb')
        pickle.dump(activity_dict, activity_write)
        activity_write.close()

        self.most_recent_activity = activity_dict
        print('Successfully logged player activity.')
