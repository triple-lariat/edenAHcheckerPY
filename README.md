# edenAHcheckerPY
Dependencies:
discord.py,
requests,
datetime,
json,
ast,
re,
pytz,
pandas<br><br>
This bot is designed to pull info from classicffxi.com and post it in a discord channel.<br>
In other words, it's designed for Eden private server.<br><br>
In order to use this bot you MUST create your own eden_bot_token.py with a variable of the same name containing your bot's token.
<br><br>
Usage: the main bot.py contains the !ah and !b commands to check bazaar and auction entries from the Eden website.<br><br>
yellbot.py pings the website's yell info every 30 seconds and posts new yells to certain channels. Channels can be added using the !yells command.
<br><br>
With the way that Discord bots work, you can run both scripts simulateously to get both functionalities.
<br>In Windows, this is as easy as just opening both scripts.<br>
On my Raspbian system I generally run both using the following command:<br><br>
sudo python3.6 yellbot.py &<br>
sudo python3.6 bot.py<br><br><br>
As of right now, I have only tested the bot with python3.7.4 and python3.6.8<br>
it should, however, be able to work with python3.6.1+<br><br>
If, for any reason, you would like to mess around with a bot like this but refuse to use Python<br>
I have written a more rough and somewhat defunct implementation of bot.py in node.js
<br>Please contact me if you wish to view it.
