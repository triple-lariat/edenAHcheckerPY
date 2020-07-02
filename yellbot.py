import discord
import asyncio
import requests as r
from discord.ext import commands
from datetime import datetime
import json, ast, pytz, platform, time, sys
import edenAHhelper as helper

try:
        from eden_bot_token import eden_bot_token
except ImportError:
        raise ImportError('You must create a file "eden_bot_token.py" with' +
                          ' variable eden_bot_token = "your.bot.token"')

class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # create the background task and run it in the background
        self.bg_task = self.loop.create_task(self.my_background_task())

    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')

    async def on_message(self, message):
            if message.author == self.user:
                    return
            if message.content.startswith('!yells on'):
                    helper.add_yell_channel(message.channel.id)
                    await message.channel.send('Yell messages will be sent to this channel.')
                    return
            if message.content.startswith('!yells off'):
                    helper.del_yell_channel(message.channel.id)
                    await message.channel.send('Yell messages have been disabled for this channel.')
                    return
            if message.content.startswith('!error'):
                    a = self.get_channel(728081585441603615)
                    await a.send('task failed successfully')

    async def my_background_task(self):
        await self.wait_until_ready()
        # togglable var for logging yells sent
        log_yells = True
        counter = 0
        yell_history = [{} for i in range(31)]

        #channel = self.get_channel(727691425688453150) # channel ID goes here
        try:
                while not self.is_closed():
                    #print(f"[{helper.get_my_timestamp_now()}] cycle started")
                    channel_ids = helper.get_yell_channels()
                    if log_yells:
                        log = open('eden_yell_log.txt','a')
                    yell_tuple = helper.yell_helper(yell_history)
                    yell_history = yell_tuple[1]
                    for yell in yell_tuple[0]:
                        f_yell = helper.yell_formatter(yell)
                        name = f_yell['speaker']
                        message = f_yell['message']
                        date = f_yell['date']

                        yell_message = f'[{date}] **{name}**: {message}'

                        if log_yells:
                            log.write(yell_message + '\n')

                        for channel in channel_ids:
                                try:
                                        to_send = self.get_channel(channel)
                                        await to_send.send(yell_message)
                                except AttributeError:
                                        print(sys.exc_info())
                                        helper.del_yell_channel(channel)
                                        print(f'Purged invalid channel {channel}')
                    counter += 1
                    print('cycle ' + f'{counter}' +  ' complete')
                    log.close()
                    await asyncio.sleep(30) # task runs every 30 seconds
        except Exception:
                print('Background task raised exception')
                print(sys.exc_info())
                raise
        finally:
                print('yell loop exited')


client = MyClient()
client.run(eden_bot_token)
