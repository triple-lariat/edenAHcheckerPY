# Author: triple-lariat a.k.a: Tranquille, Desarroi, M.B.
# Any issues you encounter can be posted to https://github.com/triple-lariat/edenAHcheckerPY
# You may also find me on Eden or Eden's discord under the name Tranquille

from edenbotcogs.coghelpers.settings_helper import *


class settings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def disableall(self, ctx):
        '''Disables usage of all commands by anyone without "Manage messages" permissions in the current channel.'''
        disable_all_commands(ctx.channel.id)
        await ctx.message.add_reaction('✅')

    @commands.command(aliases=['disable'])
    @commands.has_permissions(manage_messages=True)
    async def disablecommand(self, ctx, message: str):
        try:
            message = message.lower()
            flag = command_options[message]
            disable_command(ctx.channel.id, flag)
            await ctx.message.add_reaction('✅')
        except KeyError:
            await ctx.send('Invalid command category given.')

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def enableall(self, ctx):
        '''Enables all disabled commands, if any, in the current channel.'''
        enable_all_commands(ctx.channel.id)
        await ctx.message.add_reaction('✅')

    @commands.command(aliases=['enable'])
    @commands.has_permissions(manage_messages=True)
    async def enablecommand(self, ctx, message: str):
        try:
            message = message.lower()
            flag = command_options[message]
            enable_command(ctx.channel.id, flag)
            await ctx.message.add_reaction('✅')
        except KeyError:
            await ctx.send('Invalid command category given.')

    @commands.command(hidden=True, aliases=['disablelist', 'disabledlist'])
    @commands.has_permissions(administrator=True)
    async def listdisabled(self, ctx):
        await ctx.send(disabled_channels)

    @commands.command()
    async def credit(self, ctx):
        cred = "Hello! This bot was created by Tranquille/Triple Lariat/M.B.! You can find the source code at " + \
               "https://github.com/triple-lariat/edenAHcheckerPY\n" + \
               "Thank you so much for using this bot and I hope you enjoy!~"
        await ctx.send(cred)
