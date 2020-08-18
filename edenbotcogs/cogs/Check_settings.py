# Author: triple-lariat a.k.a: Tranquille, Desarroi, M.B.
# Any issues you encounter can be posted to https://github.com/triple-lariat/edenAHcheckerPY
# You may also find me on Eden or Eden's discord under the name Tranquille

from discord.ext import commands
from edenbotcogs.coghelpers.settings_helper import *


class settings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def disableall(self, ctx):
        '''Disables usage of all commands by anyone without "Manage messages" permissions in the current channel.'''
        disable_all_commands(ctx.channel.id)
        await ctx.send('All commands have been disabled for this channel!')

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def disablecommand(self, ctx, message: str):
        try:
            message = message.lower()
            flag = command_options[message]
            disable_command(ctx.channel.id, flag)
        except KeyError:
            await ctx.send('Invalid command category given.')

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def enableall(self, ctx):
        '''Enables all disabled commands, if any, in the current channel.'''
        enable_all_commands(ctx.channel.id)
        await ctx.send('All commands have been enabled for this channel!')

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def enablecommand(self, ctx, message: str):
        try:
            message = message.lower()
            flag = command_options[message]
            enable_command(ctx.channel.id, flag)
        except KeyError:
            await ctx.send('Invalid command category given.')

    @commands.command(hidden=True)
    @commands.has_permissions(administrator=True)
    async def listdisabled(self, ctx):
        await ctx.send(disabled_channels)

