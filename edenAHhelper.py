import ast
import pytz
from datetime import datetime

import discord
import pandas as pd
import requests as r


def check_item(item_name):
    check_url = f'http://www.classicffxi.com/api/v1/items/{item_name}'
    check_page = r.get(check_url).text
    print(check_page)
    if check_page == '':
        page_exist = False
        is_stackable = 'false'
    else:
        page_exist = True
        is_stackable = check_page.split(',')[1][12:]
        print(is_stackable)
    return (page_exist, is_stackable)


def build_AH_embed(item_name, exist_flag, stack_flag):
    embed_title = format_name(item_name)
    if not exist_flag:
        return discord.Embed(title='Invalid item name given.')
    url = f'http://www.classicffxi.com/api/v1/items/{item_name}/ah?stack={stack_flag}'
    ah_info = r.get(url).text
    ah_info = ast.literal_eval(ah_info)
    embed = discord.Embed(title=embed_title, description='', color=0x00ff00)
    for entry in ah_info:
        # convert given unix timestamp to initialized timezone
        sell_time = get_ET_timestamp(entry['sell_date'])
        embed.add_field(name=sell_time,
                        value=entry['seller_name'] + ' -> ' +
                        entry['buyer_name'] + f"\n**{entry['sale']}g**",
                        inline=True)
    return embed


def build_bazaar_embed(item_name, exist_flag):
    embed_title = format_name(item_name)
    if not exist_flag:
        return discord.Embed(title='Invalid item name given.')
    url = f'http://www.classicffxi.com/api/v1/items/{item_name}/bazaar'
    ah_info = r.get(url).text
    ah_info = ast.literal_eval(ah_info)
    b_info = []
    embed = discord.Embed(title=embed_title, description='', color=0x00dd00)
    for entry in ah_info:
        if not (entry['bazaar'] == 99999999):
            b_info.append([entry['charname'], entry['bazaar']])

    b_info = condense(b_info)

    for entry in b_info:
        embed.add_field(name=entry[0],
                        value=f"\n**{entry[1]}g** x{entry[2]}",
                        inline=True)
    return embed


def build_yell_embed():
    url = 'http://classicffxi.com/api/v1/misc/yells'
    yell_info = r.get(url).text
    yell_info = ast.literal_eval(yell_info)

    embed = discord.Embed(title='yells')
    for entry in yell_info:
        embed.add_field(name='placeholder', value=entry)
    print(len(yell_info))
    return embed


def get_ET_timestamp(unix_ts):
    tz = pytz.timezone('America/New_York')
    ET_time = datetime.fromtimestamp(unix_ts, tz)
    return ET_time.strftime('%Y-%m-%d %H:%M:%S')


def get_my_timestamp_now():
    now = datetime.now()
    now = now.strftime("%H:%M:%S")
    return now


def format_name(item_name):
    return item_name.replace('_', ' ').title()


def condense(info_list):
    df = pd.DataFrame(info_list)
    # gets number of entries 
    dupes = pd.DataFrame(info_list, columns=['0', '1'])
    dupes = dupes.pivot_table(index=['0', '1'], aggfunc='size')
    dupes = dupes.tolist()

    # gets rid of duplicate entries
    df = df.drop_duplicates()
    df = df.values.tolist()

    # adds number of occurences to list
    for i in range(len(df)):
        df[i].append(dupes[i])
    return df


################## for use with yellbot.py #################
def get_new_yells(yell_history):
    url = 'http://classicffxi.com/api/v1/misc/yells'
    yell_info = r.get(url).text
    yell_info = ast.literal_eval(yell_info)

    displace = -1
    for yell in enumerate(yell_info):
        if yell[1] == yell_history[0]:
            displace = yell[0]

    if displace == -1:
        return (list(reversed(yell_info)), yell_info)
    return (list(reversed(yell_info[:displace])), yell_info)


def yell_formatter(yell):
    f_yell = yell_date_formatter(yell)
    name = f_yell['speaker']
    message = f_yell['message']
    date = f_yell['date']

    return f'[{date}] **{name}**: {message}'


def yell_date_formatter(yell):
    formatted = yell.copy()
    formatted['date'] = get_ET_timestamp(yell['date'] / 1000)
    return formatted


def get_yell_channels():
    ch_list = open('yell_channels.csv', 'r')
    channel_ids = []
    for ch_id in ch_list:
        channel_ids.append(int(ch_id.rstrip()))

    ch_list.close()
    return channel_ids


def add_yell_channel(channel_id):
    ch_list = open('yell_channels.csv', 'r+')
    id_exists = False
    for ch_id in ch_list:
        if ch_id.rstrip() == f'{channel_id}':
            id_exists = True

    if not id_exists:
        ch_list.write(f'{channel_id}\n')

    ch_list.close()


def del_yell_channel(channel_id):
    ch_list = open('yell_channels.csv', 'r+')
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
        create_yell_channels = open('yell_channels.csv', 'w')
        create_yell_channels.close()
        existent = []

    if not existent:
        return False
    return True
