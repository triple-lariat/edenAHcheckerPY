# edenAHcheckerPY
Dependencies:
discord.py, platform, logging, pickle, ast, re, pandas, pytz, math, time, datetime, Pillow, aiohttp
<br><br>
This bot is designed to pull info from classicffxi.com and post it in a discord channel.<br>
In other words, it's designed for Eden private server.<br><br>
In order to use this bot you MUST create your own eden_bot_token.py with a variable of the same name containing your bot's token.
<br><br>
Usage: Running bot.py will enable the use of several commands (use !help to see them all). This includes a yell logging tool. If you don't
wish to use that, you should comment out the line ```bot.add_cog(yellbot.yell_log(bot))``` from bot.py
<br><br>
As of right now, I have only tested the bot with python3.7.4 and python3.6.8<br>
it should, however, be able to work with python3.6.2+<br><br>
If, for any reason, you would like to mess around with a bot like this but refuse to use Python<br>
I have written a more rough and somewhat defunct implementation of bot.py in node.js
<br>Please contact me if you wish to view it.
