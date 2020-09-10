# Author: triple-lariat a.k.a: Tranquille, Desarroi, M.B.
# Any issues you encounter can be posted to https://github.com/triple-lariat/edenAHcheckerPY
# You may also find me on Eden or Eden's discord under the name Tranquille

from datetime import datetime
import pytz
import ast
import re
import aiohttp
from edenbotcogs.coghelpers.Timers_helper import get_timezone, server_timezones

yell_url = 'http://classicffxi.com/api/v1/misc/yells'


async def get_new_yells(yell_history):
    async with aiohttp.ClientSession() as s:
        async with s.get(yell_url) as resp:
            yell_info = await resp.text()

    yell_info = ast.literal_eval(yell_info)

    displace = -1
    for yell in enumerate(yell_info):
        if yell[1] == yell_history[0]:
            displace = yell[0]

    if displace == -1:
        return list(reversed(yell_info)), yell_info
    return list(reversed(yell_info[:displace])), yell_info


def yell_formatter(yell, server_id=None):
    f_yell = yell_date_formatter(yell, server_id)
    name = f_yell['speaker']
    message = f_yell['message']
    # replace unparseable character if given by site
    message = message.replace('\x85', '')
    message = escape_markdown(message)
    date = f_yell['date']

    return f'[{date}] **{name}**: {message}'


# For now this only removes characters that Discord would think is formatting
# In the long-term will want to find a way to escape special characters
def escape_markdown(text):
    escaped = re.sub(r'(\*|_|`|~|\||\\)', '', text)  # escape *, _, `, ~, \, |
    return escaped


def yell_date_formatter(yell, server_id=None):
    formatted = yell.copy()
    formatted['date'] = get_timestamp(yell['date'] / 1000, server_id)
    return formatted


def get_yell_channels():
    ch_list = open('./data/yell_channels.csv', 'r')
    channel_ids = []
    for ch_id in ch_list:
        channel_ids.append(int(ch_id.rstrip()))

    ch_list.close()
    return channel_ids


def add_yell_channel(channel_id):
    ch_list = open('./data/yell_channels.csv', 'r+')
    id_exists = False
    for ch_id in ch_list:
        if ch_id.rstrip() == f'{channel_id}':
            id_exists = True

    if not id_exists:
        ch_list.write(f'{channel_id}\n')

    ch_list.close()


def del_yell_channel(channel_id):
    ch_list = open('./data/yell_channels.csv', 'r+')
    lines = ch_list.readlines()
    ch_list.seek(0)
    for i in lines:
        if i.rstrip() != f'{channel_id}':
            ch_list.write(i)
    ch_list.truncate()
    ch_list.close()


# check if yell channels is empty
def check_channels_exist():
    try:
        existent = get_yell_channels()
    except FileNotFoundError:
        create_yell_channels = open('./data/yell_channels.csv', 'w')
        create_yell_channels.close()
        existent = []

    if not existent:
        return False
    return True


async def check_connection(url):
    valid_connection = False
    try:
        async with aiohttp.ClientSession() as s:
            async with s.get(url) as resp:
                if resp.status == 200:
                    valid_connection = True
    except Exception:
        # something went horribly wrong and the url is probably invalid in some way
        pass

    return valid_connection


def get_timestamp(unix_ts, server_id=None):
    if server_id:
        tz = get_timezone(server_id)
    else:
        tz = 'US/Eastern'
    tz = pytz.timezone(tz)
    human_time = datetime.fromtimestamp(unix_ts, tz)
    return human_time.strftime('%Y-%m-%d %H:%M:%S')


def get_my_timestamp_now():
    now = datetime.now()
    now = now.strftime("%H:%M:%S")
    return now
