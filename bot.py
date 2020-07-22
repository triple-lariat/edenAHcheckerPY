# Author: triple-lariat a.k.a: Tranquille, Desarroi, M.B.
# Any issues you encounter can be posted to https://github.com/triple-lariat/edenAHcheckerPY
# You may also find me on Eden or Eden's discord under the name Tranquille

import platform

import discord
from discord.ext import commands

import edenbotcogs

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


@bot.command(hidden=True)
async def ping(ctx):
    await ctx.send('pong')


@bot.command(hidden=True)
async def args(ctx, *, message: str):
    message = message.split(' ')
    for item in enumerate(message):
        await ctx.send(message[item[0]])

# add created cogs
bot.add_cog(edenbotcogs.Player(bot))
bot.add_cog(edenbotcogs.Market(bot))
bot.add_cog(edenbotcogs.Misc(bot))
bot.add_cog(edenbotcogs.math_commands.Math(bot))
bot.add_cog(edenbotcogs.yellbot.yell_log(bot))

try:
    bot.run(eden_bot_token)
except discord.LoginFailure:
    print('There was an error logging in. Please ensure you have the right login token set in eden_bot_token.py')
