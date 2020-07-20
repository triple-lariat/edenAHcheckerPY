# Author: triple-lariat a.k.a: Tranquille, Desarroi, M.B.
# Any issues you encounter can be posted to https://github.com/triple-lariat/edenAHcheckerPY
# You may also find me on Eden or Eden's discord under the name Tranquille

from discord.ext import commands


class Math(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['addition'])
    async def add(self, ctx, *, message: str):
        '''Adds numbers
        Usage: !add [num] [num] ...'''
        args = message.split(' ')
        try:
            add_sum = 0
            for num in args:
                add_sum += float(num)
            await ctx.send(add_sum)
        except ValueError:
            await ctx.send('Invalid operand(s).')

    @commands.command(aliases=['subtract', 'subtraction'])
    async def sub(self, ctx, *, message: str):
        '''Subtracts numbers
        Usage: !sub [num] [num] ...'''
        args = message.split()
        try:
            difference = float(args[0])
            for num in args[1:]:
                difference -= float(num)
            await ctx.send(difference)
        except ValueError:
            await ctx.send('Invalid operand(s).')

    @commands.command(aliases=['divide', 'division'])
    async def div(self, ctx, *, message: str):
        '''Divides numbers
        Usage: !div [num] [num] ...'''
        args = message.split()
        try:
            quotient = float(args[0])
            for num in args[1:]:
                quotient /= float(num)
            await ctx.send(quotient)
        except ValueError:
            await ctx.send('Invalid operand(s).')
        except ZeroDivisionError:
            await ctx.send('You cannot divide by zero.')

    @commands.command(aliases=['multiply', 'multiplication', 'times'])
    async def mult(self, ctx, *, message: str):
        '''Multiplies numbers
        Usage: !mult [num] [num] ...'''
        args = message.split()
        try:
            product = float(args[0])
            for num in args[1:]:
                product *= float(num)
            await ctx.send(product)
        except ValueError:
            await ctx.send('Invalid operand(s).')
