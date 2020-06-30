import discord
from discord.ext import commands
import requests as r
from datetime import datetime
import json, ast, re, pytz

def check_item(item_name):
    check_url = f'http://www.classicffxi.com/api/v1/items/{item_name}'
    check_page = r.get(check_url).text
    if check_page == '':
            page_exist = False
    else:
            page_exist = True
    return page_exist

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
        embed = discord.Embed(title=embed_title, description='', color=0x00dd00)
        for entry in ah_info:
                embed.add_field(name=entry['charname'],
                                value=f"\n**{entry['bazaar']}g**",
                                inline=True)
        return embed

def get_ET_timestamp(unix_ts):
    tz = pytz.timezone('America/New_York')
    ET_time = datetime.fromtimestamp(unix_ts, tz)
    return ET_time.strftime('%Y-%m-%d %H:%M:%S')

def format_name(item_name):
    return item_name.replace('_',' ').title()
