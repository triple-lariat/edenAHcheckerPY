# Author: triple-lariat a.k.a: Tranquille, Desarroi, M.B.
# Any issues you encounter can be posted to https://github.com/triple-lariat/edenAHcheckerPY
# You may also find me on Eden or Eden's discord under the name Tranquille

import platform
import logging
import discord
from discord.ext import commands
from edenbotcogs.cogs import *

# Set up logging
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='edenAHbot.log', encoding='utf-8', mode='a')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


# debug var
track_exceptions = True

# import bot token from separate file 'eden_bot_token.py'
try:
    from eden_bot_token import eden_bot_token
except ImportError:
    new_instance = open('eden_bot_token.py', 'w')
    new_instance.write('eden_bot_token = "YoUrBotTokEn"')
    raise ImportError('Please enter your bot token in eden_bot_token.py' +
                      '\nThis file has been created for you.')

description = ''
bot = commands.Bot(command_prefix='!', description=description)


@bot.event
async def on_ready():
    print('edenAHbot Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    await bot.change_presence(activity=discord.Activity(name=platform.system(),
                                                        type=discord.ActivityType.playing))


@bot.event
async def on_command_error(ctx, exception):
    if track_exceptions:
        if isinstance(exception, commands.CommandNotFound):
            pass
        elif isinstance(exception, discord.Forbidden):
            pass
        elif isinstance(exception, commands.MissingRequiredArgument):
            await ctx.send(f'Arguments must be provided to use this command {ctx.author.mention}!\n' +
                           'Use !help [command] for more info.')
        print(f'Exception of {ctx.command} in {ctx.guild}: {exception}')


@bot.command(hidden=True)
async def ping(ctx):
    await ctx.send('pong')


@bot.command(hidden=True)
async def args(ctx, *, message: str):
    message = message.split(' ')
    for item in enumerate(message):
        await ctx.send(message[item[0]])

# add created cogs
bot.add_cog(Check_settings.settings(bot))
bot.add_cog(Player.Player(bot))
bot.add_cog(Market.Market(bot))
bot.add_cog(Misc.Misc(bot))
bot.add_cog(math_commands.Math(bot))
bot.add_cog(yellbot.yell_log(bot))
bot.add_cog(Timers.Timers(bot))

try:
    bot.run(eden_bot_token)
except discord.LoginFailure:
    print('There was an error logging in. Please ensure you have the right login token set in eden_bot_token.py')
