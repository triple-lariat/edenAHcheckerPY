# Author: triple-lariat a.k.a: Tranquille, Desarroi, M.B.
# Any issues you encounter can be posted to https://github.com/triple-lariat/edenAHcheckerPY
# You may also find me on Eden or Eden's discord under the name Tranquille

import discord
import asyncio

import sys
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
        print('yellbot_legacy.py logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')

    async def on_message(self, message):
        if message.author == self.user:
            return
        if message.content.startswith('!yells on'):
            if message.author.permissions_in(message.channel).manage_messages:
                helper.add_yell_channel(message.channel.id)
                await message.channel.send('Yell messages will be sent to this channel.')
            else:
                await message.channel.send(f'{message.author.mention}' +
                                           ' you must have "manage messages" permissions to use this command!')
            return
        if message.content.startswith('!yells off'):
            if message.author.permissions_in(message.channel).manage_messages:
                helper.del_yell_channel(message.channel.id)
                await message.channel.send('Yell messages have been disabled for this channel.')
            else:
                await message.channel.send(f'{message.author.mention}' +
                                           ' you must have "manage messages" permissions to use this command!')
            return

    async def my_background_task(self):
        await self.wait_until_ready()
        # toggleable var for logging yells sent
        log_yells = True
        counter = 0
        yell_history = [{} for i in range(31)]

        try:
            while not self.is_closed():
                if helper.check_channels_exist() and helper.check_connection(helper.yell_url):
                    print(f"[{helper.get_my_timestamp_now()}] cycle started.")
                    channel_ids = helper.get_yell_channels()
                    if log_yells:
                        log = open('eden_yell_log.txt', 'a')

                    yell_tuple = helper.get_new_yells(yell_history)
                    yell_history = yell_tuple[1]
                    for yell in yell_tuple[0]:
                        yell_message = helper.yell_formatter(yell)

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
                    print(f'[{helper.get_my_timestamp_now()}] cycle {counter} complete.')
                    log.close()
                else:
                    print(f'[{helper.get_my_timestamp_now()}] cycle skipped.' +
                          ' Either no channels are registered or the site is down.')
                    # wait an addition 30 sec when server is possibly down
                    await asyncio.sleep(30)
                await asyncio.sleep(30)  # task runs every 30 seconds
        except Exception:
            print('Background task raised exception')
            print(sys.exc_info())
            raise
        finally:
            print('yell loop exited')


client = MyClient()
client.run(eden_bot_token)
