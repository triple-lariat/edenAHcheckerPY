# Author: triple-lariat a.k.a: Tranquille, Desarroi, M.B.
# Any issues you encounter can be posted to https://github.com/triple-lariat/edenAHcheckerPY
# You may also find me on Eden or Eden's discord under the name Tranquille
import ast
from datetime import datetime
import re
import pandas as pd
import pytz
import requests as r
import discord.embeds

item_prefixes = [
    'piece_of_',
    'scroll_of_',
    'square_of_',
    'chunk_of_',
    'pot_of_',
    'flask_of_',
    'pinch_of_',
    'bottle_of_',
    'vial_of_',
    'sprig_of_',
    'handful_of_',
    'lump_of_',
    'clump_of_',
    'bottle_of_',
    'loop_of_',
    'block_of_',
    'jar_of_',
    'bag_of_',
    'bunch_of_',
    'remnant_of_a_'
]


def init_item_names():
    csv = open('./data/market_items.csv', 'r')
    item_info = []
    for line in csv:
        item_info.append(line.rstrip())

    csv.close()
    return item_info


item_names = init_item_names()


def format_item_string(item):
    item = item.lower()
    item = item.split(' ')
    i = 0
    while i < len(item):
        item[i] = re.sub(r"[!@#$%^&*']+", '', item[i])
        i += 1
    print(item)
    return item


def format_name(item_name):
    return item_name.replace('_', ' ').title()


def get_ET_timestamp(unix_ts):
    tz = pytz.timezone('America/New_York')
    ET_time = datetime.fromtimestamp(unix_ts, tz)
    return ET_time.strftime('%Y-%m-%d %H:%M:%S')


def check_item(item_name):
    # returns (name, stack_flag, additional_results)
    stack_flag = 'false'

    matches = [x for x in item_names if item_name in x]
    if len(matches) == 1:
        item_name = matches[0]
    elif item_name not in matches:
        item_name = check_prefixes(item_name)

    if item_name:
        stack_flag = check_stack_flag(item_name)

    return item_name, stack_flag, matches


def check_prefixes(item_stub):
    overall_matches = []
    for prefix in item_prefixes:
        matches = search_item(prefix + item_stub)
        if len(matches) == 1:
            overall_matches.append(matches[0])
    if len(overall_matches) == 1:
        return overall_matches[0]
    return ''


def check_stack_flag(item_name):
    check_url = f'http://www.classicffxi.com/api/v1/items/{item_name}'
    check_page = r.get(check_url).text
    is_stack = check_page.split(',')[1][11:]
    return is_stack


def search_item(item_stub):
    matches = [x for x in item_names if item_stub in x]
    return matches


def condense(info_list):
    df = pd.DataFrame(info_list)
    # gets number of entries
    dupes = pd.DataFrame(info_list, columns=['0', '1'])
    dupes = dupes.pivot_table(index=['0', '1'], aggfunc='size')
    dupes = dupes.tolist()

    # gets rid of duplicate entries
    df = df.drop_duplicates()
    df = df.values.tolist()

    # adds number of occurrences to list
    for i in range(len(df)):
        df[i].append(dupes[i])
    return df


def build_AH_embed(item_name, stack_flag):
    embed_title = format_name(item_name)

    url = f'http://www.classicffxi.com/api/v1/items/{item_name}/ah?stack={stack_flag}'
    ah_info = r.get(url).text

    if ah_info == '[]':
        return discord.Embed(title=embed_title, description='No entries found.')

    ah_info = ast.literal_eval(ah_info)
    embed = discord.Embed(title=embed_title, description='', color=0x00ff00)
    for entry in ah_info:
        # convert given unix timestamp to initialized timezone
        sell_time = get_ET_timestamp(entry['sell_date'])
        embed.add_field(name=sell_time,
                        value=entry['seller_name'] + ' -> ' +
                              entry['buyer_name'] + f"\n**{entry['sale']:,}g**",
                        inline=True)
    return embed


def build_bazaar_embed(item_name):
    embed_title = format_name(item_name)

    url = f'http://www.classicffxi.com/api/v1/items/{item_name}/bazaar'
    ah_info = r.get(url).text

    ah_info = ast.literal_eval(ah_info)
    b_info = []

    for entry in ah_info:
        if not (entry['bazaar'] == 99999999):
            b_info.append([entry['charname'], entry['bazaar']])

    if not b_info:
        return discord.Embed(title=embed_title, description='No entries found.')
    b_info = condense(b_info)

    embed = discord.Embed(title=embed_title, description='', color=0x00dd00)
    for entry in b_info:
        embed.add_field(name=entry[0],
                        value=f"\n**{entry[1]:,}g** x{entry[2]}",
                        inline=True)
    return embed
