# Author: triple-lariat a.k.a: Tranquille, Desarroi, M.B.
# Any issues you encounter can be posted to https://github.com/triple-lariat/edenAHcheckerPY
# You may also find me on Eden or Eden's discord under the name Tranquille

import discord
from discord.ext import commands, tasks
import asyncio

import sys
import edenAHhelper as helper


class yell_log(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def yells(self, ctx, message: str):
        '''Enables live yell chat log in the channel this command is used in.
               Usage: !yells [on|off]'''
        if message == 'on':
            if ctx.author.permissions_in(ctx.channel).manage_messages:
                helper.add_yell_channel(ctx.channel.id)
                await ctx.channel.send('Yell messages will be sent to this channel.')
            else:
                await ctx.channel.send(f'{ctx.author.mention}' +
                                       ' you must have "manage messages" permissions to use this command!')
            return
        if message == 'off':
            if ctx.author.permissions_in(ctx.channel).manage_messages:
                helper.del_yell_channel(ctx.channel.id)
                await ctx.channel.send('Yell messages have been disabled for this channel.')
            else:
                await ctx.channel.send(f'{ctx.author.mention}' +
                                       ' you must have "manage messages" permissions to use this command!')
            return
