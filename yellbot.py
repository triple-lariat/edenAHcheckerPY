import discord
import asyncio
import requests as r
from datetime import datetime
import json, ast, pytz, platform, time
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

    async def my_background_task(self):
        await self.wait_until_ready()
        # togglable var for logging yells sent
        log_yells = True
        counter = 0
        yell_history = [{} for i in range(31)]

        channel = self.get_channel(727691425688453150) # channel ID goes here
        while not self.is_closed():
            #print(f"[{helper.get_my_timestamp_now()}] cycle started")
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
                await channel.send(yell_message)
            counter += 1
            print('cycle ' + f'{counter}' +  ' complete')
            log.close()
            await asyncio.sleep(30) # task runs every 30 seconds


client = MyClient()
client.run(eden_bot_token)
