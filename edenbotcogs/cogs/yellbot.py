# Author: triple-lariat a.k.a: Tranquille, Desarroi, M.B.
# Any issues you encounter can be posted to https://github.com/triple-lariat/edenAHcheckerPY
# You may also find me on Eden or Eden's discord under the name Tranquille

import asyncio
import sys
from edenbotcogs.coghelpers.yellbot_helper import *
from discord.ext import commands, tasks


class yell_log(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.yellbot_task.start()
        # toggleable var for logging yells sent
        self.log_yells = True
        self.counter = 0
        self.yell_history = [{} for i in range(31)]

    @commands.command()
    @commands.guild_only()
    async def yells(self, ctx, message: str):
        '''Enables live yell chat log in the channel this command is used in.
               Usage: !yells [on|off]'''
        if message == 'on':
            if ctx.author.permissions_in(ctx.channel).manage_messages:
                add_yell_channel(ctx.channel.id)
                await ctx.send('Yell messages will be sent to this channel.')
            else:
                await ctx.send(f'{ctx.author.mention}' +
                               ' you must have "manage messages" permissions to use this command!')
            return
        if message == 'off':
            if ctx.author.permissions_in(ctx.channel).manage_messages:
                del_yell_channel(ctx.channel.id)
                await ctx.send('Yell messages have been disabled for this channel.')
            else:
                await ctx.send(f'{ctx.author.mention}' +
                               ' you must have "manage messages" permissions to use this command!')
            return

    @yells.error
    async def yells_error(self, ctx, error):
        if isinstance(error, commands.NoPrivateMessage):
            await ctx.send("Yell logs can't be sent over DMs!")

    @tasks.loop(seconds=40)
    async def yellbot_task(self):
        await self.bot.wait_until_ready()
        try:
            if check_channels_exist() and await check_connection(yell_url):
                print(f"[{get_my_timestamp_now()}] cycle started.")
                channel_ids = get_yell_channels()
                if self.log_yells:
                    log = open('eden_yell_log.txt', 'a')

                yell_tuple = await get_new_yells(self.yell_history)
                self.yell_history = yell_tuple[1]
                for yell in yell_tuple[0]:
                    yell_message = yell_formatter(yell)

                    if self.log_yells:
                        log.write(yell_message + '\n')

                    for channel in channel_ids:
                        try:
                            to_send = self.bot.get_channel(channel)
                            guild_id = to_send.guild.id
                            yell_message = yell_formatter(yell, guild_id)
                            await to_send.send(yell_message)
                        except AttributeError:
                            print(sys.exc_info())
                            del_yell_channel(channel)
                            print(f'Purged invalid channel {channel}')
                self.counter += 1
                print(f'[{get_my_timestamp_now()}] cycle {self.counter} complete.')
                log.close()
            else:
                print(f'[{get_my_timestamp_now()}] cycle skipped.' +
                      ' Either no channels are registered or the site is down.')
                # wait an addition 30 sec when server is possibly down
                await asyncio.sleep(30)
        except Exception:
            print('Background task raised exception')
            print(sys.exc_info())
            self.yell_history = [{} for i in range(31)]
