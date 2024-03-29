# Author: triple-lariat a.k.a: Tranquille, Desarroi, M.B.
# Any issues you encounter can be posted to https://github.com/triple-lariat/edenAHcheckerPY
# You may also find me on Eden or Eden's discord under the name Tranquille

import re
from datetime import datetime

import discord.embeds
import pytz
import ast
from edenbotcogs.coghelpers.Timers_helper import get_timezone
from PIL import Image
from io import BytesIO
from edenbotcogs.coghelpers.Market_helper import format_name
import aiohttp
from random import randint


char_url = 'https://144.217.79.186/api/v1/chars/'
avatars = dict(ef1a='https://vignette.wikia.nocookie.net/ffxi/images/d/d7/Ef1a.jpg',
               ef2a='https://vignette.wikia.nocookie.net/ffxi/images/c/c1/Ef2a.jpg',
               ef3a='https://vignette.wikia.nocookie.net/ffxi/images/a/a4/Ef3a.jpg',
               ef4a='https://vignette.wikia.nocookie.net/ffxi/images/6/67/Ef4a.jpg',
               ef5a='https://vignette.wikia.nocookie.net/ffxi/images/6/62/Ef5a.jpg',
               ef6a='https://vignette.wikia.nocookie.net/ffxi/images/f/f9/Ef6a.jpg',
               ef7a='https://vignette.wikia.nocookie.net/ffxi/images/c/c6/Ef7a.jpg',
               ef8a='https://vignette.wikia.nocookie.net/ffxi/images/6/60/Ef8a.jpg',
               ef1b='https://vignette.wikia.nocookie.net/ffxi/images/c/cf/Ef1b.jpg',
               ef2b='https://vignette.wikia.nocookie.net/ffxi/images/5/5a/Ef2b.jpg',
               ef3b='https://vignette.wikia.nocookie.net/ffxi/images/d/d5/Ef3b.jpg',
               ef4b='https://vignette.wikia.nocookie.net/ffxi/images/1/19/Ef4b.jpg',
               ef5b='https://vignette.wikia.nocookie.net/ffxi/images/4/45/Ef5b.jpg',
               ef6b='https://vignette.wikia.nocookie.net/ffxi/images/a/a2/Ef6b.jpg',
               ef7b='https://vignette.wikia.nocookie.net/ffxi/images/2/2d/Ef7b.jpg',
               ef8b='https://vignette.wikia.nocookie.net/ffxi/images/9/95/Ef8b.jpg',
               em8b='https://vignette.wikia.nocookie.net/ffxi/images/a/a4/Em8b.jpg',
               em7b='https://vignette.wikia.nocookie.net/ffxi/images/7/76/Em7b.jpg',
               em6b='https://vignette.wikia.nocookie.net/ffxi/images/f/f1/Em6b.jpg',
               em5b='https://vignette.wikia.nocookie.net/ffxi/images/3/3f/Em5b.jpg',
               em4b='https://vignette.wikia.nocookie.net/ffxi/images/2/2c/Em4b.jpg',
               em3b='https://vignette.wikia.nocookie.net/ffxi/images/9/9c/Em3b.jpg',
               em2b='https://vignette.wikia.nocookie.net/ffxi/images/4/41/Em2b.jpg',
               em1b='https://vignette.wikia.nocookie.net/ffxi/images/a/a7/Em1b.jpg',
               em8a='https://vignette.wikia.nocookie.net/ffxi/images/a/a6/Em8a.jpg',
               em7a='https://vignette.wikia.nocookie.net/ffxi/images/3/32/Em7a.jpg',
               em6a='https://vignette.wikia.nocookie.net/ffxi/images/a/ae/Em6a.jpg',
               em5a='https://vignette.wikia.nocookie.net/ffxi/images/1/19/Em5a.jpg',
               em4a='https://vignette.wikia.nocookie.net/ffxi/images/a/a4/Em4a.jpg',
               em3a='https://vignette.wikia.nocookie.net/ffxi/images/9/90/Em3a.jpg',
               em2a='https://vignette.wikia.nocookie.net/ffxi/images/6/63/Em2a.jpg',
               em1a='https://vignette.wikia.nocookie.net/ffxi/images/9/98/Em1a.jpg',
               gm1a='https://vignette.wikia.nocookie.net/ffxi/images/4/4c/G1a.jpg',
               gm2a='https://vignette.wikia.nocookie.net/ffxi/images/6/6a/G2a.jpg',
               gm3a='https://vignette.wikia.nocookie.net/ffxi/images/4/4d/G3a.jpg',
               gm4a='https://vignette.wikia.nocookie.net/ffxi/images/0/02/G4a.jpg',
               gm5a='https://vignette.wikia.nocookie.net/ffxi/images/6/6c/G5a.jpg',
               gm6a='https://vignette.wikia.nocookie.net/ffxi/images/d/d7/G6a.jpg',
               gm7a='https://vignette.wikia.nocookie.net/ffxi/images/7/71/G7a.jpg',
               gm8a='https://vignette.wikia.nocookie.net/ffxi/images/2/22/G8a.jpg',
               gm1b='https://vignette.wikia.nocookie.net/ffxi/images/a/af/G1b.jpg',
               gm2b='https://vignette.wikia.nocookie.net/ffxi/images/3/30/G2b.jpg',
               gm3b='https://vignette.wikia.nocookie.net/ffxi/images/8/8b/G3b.jpg',
               gm4b='https://vignette.wikia.nocookie.net/ffxi/images/a/a1/G4b.jpg',
               gm5b='https://vignette.wikia.nocookie.net/ffxi/images/2/21/G5b.jpg',
               gm6b='https://vignette.wikia.nocookie.net/ffxi/images/b/b6/G6b.jpg',
               gm7b='https://vignette.wikia.nocookie.net/ffxi/images/6/6e/G7b.jpg',
               gm8b='https://vignette.wikia.nocookie.net/ffxi/images/f/fd/G8b.jpg',
               hf1a='https://vignette.wikia.nocookie.net/ffxi/images/1/12/Hf1a.jpg',
               hf2a='https://vignette.wikia.nocookie.net/ffxi/images/4/45/Hf2a.jpg',
               hf3a='https://vignette.wikia.nocookie.net/ffxi/images/2/25/Hf3a.jpg',
               hf4a='https://vignette.wikia.nocookie.net/ffxi/images/1/19/Hf4a.jpg',
               hf5a='https://vignette.wikia.nocookie.net/ffxi/images/e/e5/Hf5a.jpg',
               hf6a='https://vignette.wikia.nocookie.net/ffxi/images/5/5a/Hf6a.jpg',
               hf7a='https://vignette.wikia.nocookie.net/ffxi/images/0/08/Hf7a.jpg',
               hf8a='https://vignette.wikia.nocookie.net/ffxi/images/8/89/Hf8a.jpg',
               hf1b='https://vignette.wikia.nocookie.net/ffxi/images/3/3c/Hf1b.jpg',
               hf2b='https://vignette.wikia.nocookie.net/ffxi/images/3/37/Hf2b.jpg',
               hf3b='https://vignette.wikia.nocookie.net/ffxi/images/b/b0/Hf3b.jpg',
               hf4b='https://vignette.wikia.nocookie.net/ffxi/images/6/6c/Hf4b.jpg',
               hf5b='https://vignette.wikia.nocookie.net/ffxi/images/5/5d/Hf5b.jpg',
               hf6b='https://vignette.wikia.nocookie.net/ffxi/images/a/aa/Hf6b.jpg',
               hf7b='https://vignette.wikia.nocookie.net/ffxi/images/2/28/Hf7b.jpg',
               hf8b='https://vignette.wikia.nocookie.net/ffxi/images/b/bf/Hf8b.jpg',
               hm8b='https://vignette.wikia.nocookie.net/ffxi/images/8/84/Hm8b.jpg',
               hm7b='https://vignette.wikia.nocookie.net/ffxi/images/4/43/Hm7b.jpg',
               hm6b='https://vignette.wikia.nocookie.net/ffxi/images/2/28/Hm6b.jpg',
               hm5b='https://vignette.wikia.nocookie.net/ffxi/images/8/86/Hm5b.jpg',
               hm4b='https://vignette.wikia.nocookie.net/ffxi/images/4/45/Hm4b.jpg',
               hm3b='https://vignette.wikia.nocookie.net/ffxi/images/d/df/Hm3b.jpg',
               hm2b='https://vignette.wikia.nocookie.net/ffxi/images/3/33/Hm2b.jpg',
               hm1b='https://vignette.wikia.nocookie.net/ffxi/images/f/f5/Hm1b.jpg',
               hm8a='https://vignette.wikia.nocookie.net/ffxi/images/d/d0/Hm8a.jpg',
               hm7a='https://vignette.wikia.nocookie.net/ffxi/images/0/04/Hm7a.jpg',
               hm6a='https://vignette.wikia.nocookie.net/ffxi/images/a/a4/Hm6a.jpg',
               hm5a='https://vignette.wikia.nocookie.net/ffxi/images/c/c7/Hm5a.jpg',
               hm4a='https://vignette.wikia.nocookie.net/ffxi/images/9/9d/Hm4a.jpg',
               hm3a='https://vignette.wikia.nocookie.net/ffxi/images/4/49/Hm3a.jpg',
               hm2a='https://vignette.wikia.nocookie.net/ffxi/images/6/61/Hm2a.jpg',
               hm1a='https://vignette.wikia.nocookie.net/ffxi/images/b/b3/Hm1a.jpg',
               mf1a='https://vignette.wikia.nocookie.net/ffxi/images/d/d1/M1a.jpg',
               mf2a='https://vignette.wikia.nocookie.net/ffxi/images/1/19/M2a.jpg',
               mf3a='https://vignette.wikia.nocookie.net/ffxi/images/3/37/M3a.jpg',
               mf4a='https://vignette.wikia.nocookie.net/ffxi/images/e/e3/M4a.jpg',
               mf5a='https://vignette.wikia.nocookie.net/ffxi/images/0/03/M5a.jpg',
               mf6a='https://vignette.wikia.nocookie.net/ffxi/images/7/7f/M6a.jpg',
               mf7a='https://vignette.wikia.nocookie.net/ffxi/images/c/cc/M7a.jpg',
               mf8a='https://vignette.wikia.nocookie.net/ffxi/images/8/82/M8a.jpg',
               mf1b='https://vignette.wikia.nocookie.net/ffxi/images/2/24/M1b.jpg',
               mf2b='https://vignette.wikia.nocookie.net/ffxi/images/d/d2/M2b.jpg',
               mf3b='https://vignette.wikia.nocookie.net/ffxi/images/6/63/M3b.jpg',
               mf4b='https://vignette.wikia.nocookie.net/ffxi/images/e/ee/M4b.jpg',
               mf5b='https://vignette.wikia.nocookie.net/ffxi/images/c/c9/M5b.jpg',
               mf6b='https://vignette.wikia.nocookie.net/ffxi/images/f/ff/M6b.jpg',
               mf7b='https://vignette.wikia.nocookie.net/ffxi/images/9/90/M7b.jpg',
               mf8b='https://vignette.wikia.nocookie.net/ffxi/images/9/9f/M8b.jpg',
               tf1a='https://vignette.wikia.nocookie.net/ffxi/images/a/ab/Tf1a.jpg',
               tf2a='https://vignette.wikia.nocookie.net/ffxi/images/b/bf/Tf2a.jpg',
               tf3a='https://vignette.wikia.nocookie.net/ffxi/images/6/66/Tf3a.jpg',
               tf4a='https://vignette.wikia.nocookie.net/ffxi/images/0/09/Tf4a.jpg',
               tf5a='https://vignette.wikia.nocookie.net/ffxi/images/5/5c/Tf5a.jpg',
               tf6a='https://vignette.wikia.nocookie.net/ffxi/images/1/1c/Tf6a.jpg',
               tf7a='https://vignette.wikia.nocookie.net/ffxi/images/2/2a/Tf7a.jpg',
               tf8a='https://vignette.wikia.nocookie.net/ffxi/images/6/69/Tf8a.jpg',
               tf1b='https://vignette.wikia.nocookie.net/ffxi/images/a/a0/Tf1b.jpg',
               tf2b='https://vignette.wikia.nocookie.net/ffxi/images/d/d0/Tf2b.jpg',
               tf3b='https://vignette.wikia.nocookie.net/ffxi/images/f/fe/Tf3b.jpg',
               tf4b='https://vignette.wikia.nocookie.net/ffxi/images/1/18/Tf4b.jpg',
               tf5b='https://vignette.wikia.nocookie.net/ffxi/images/d/da/Tf5b.jpg',
               tf6b='https://vignette.wikia.nocookie.net/ffxi/images/3/38/Tf6b.jpg',
               tf7b='https://vignette.wikia.nocookie.net/ffxi/images/5/5f/Tf7b.jpg',
               tf8b='https://vignette.wikia.nocookie.net/ffxi/images/3/37/Tf8b.jpg',
               tm8b='https://vignette.wikia.nocookie.net/ffxi/images/2/27/Tm8b.jpg',
               tm7b='https://vignette.wikia.nocookie.net/ffxi/images/5/55/Tm7b.jpg',
               tm6b='https://vignette.wikia.nocookie.net/ffxi/images/7/7d/Tm6b.jpg',
               tm5b='https://vignette.wikia.nocookie.net/ffxi/images/4/4b/Tm5b.jpg',
               tm4b='https://vignette.wikia.nocookie.net/ffxi/images/5/59/Tm4b.jpg',
               tm3b='https://vignette.wikia.nocookie.net/ffxi/images/2/21/Tm3b.jpg',
               tm2b='https://vignette.wikia.nocookie.net/ffxi/images/4/48/Tm2b.jpg',
               tm1b='https://vignette.wikia.nocookie.net/ffxi/images/f/f5/Tm1b.jpg',
               tm8a='https://vignette.wikia.nocookie.net/ffxi/images/b/bb/Tm8a.jpg',
               tm7a='https://vignette.wikia.nocookie.net/ffxi/images/3/34/Tm7a.jpg',
               tm6a='https://vignette.wikia.nocookie.net/ffxi/images/3/33/Tm6a.jpg',
               tm5a='https://vignette.wikia.nocookie.net/ffxi/images/9/97/Tm5a.jpg',
               tm4a='https://vignette.wikia.nocookie.net/ffxi/images/c/c6/Tm4a.jpg',
               tm3a='https://vignette.wikia.nocookie.net/ffxi/images/d/d9/Tm3a.jpg',
               tm2a='https://vignette.wikia.nocookie.net/ffxi/images/f/f0/Tm2a.jpg',
               tm1a='https://vignette.wikia.nocookie.net/ffxi/images/d/d8/Tm1a.jpg')
base_url = 'https://static.ffxiah.com/images/icon/'
base_ah_url = 'https://www.144.217.79.186/tools/item/'
user_ah_url = 'https://edenxi.com/tools/item/'
equip_background = 'https://www.ffxiah.com/images/equip_box.gif'


def format_player_name(name):
    return re.sub(r'\W+', '', name)


def format_name(name):
    return name.replace('_', ' ').title()


async def check_player_exist(player):
    url = char_url + player
    async with aiohttp.ClientSession() as s:
        async with s.get(url, ssl=False) as resp:
            player_data = await resp.text()
    if player_data:
        return True
    return False


async def get_player_info(player):
    url = char_url + player
    async with aiohttp.ClientSession() as s:
        async with s.get(url, ssl=False) as resp:
            p_info = await resp.text()
    p_info = ast.literal_eval(p_info)
    return p_info


def get_nation(nation_id):
    if nation_id == 1:
        return "Bastok"
    elif nation_id == 2:
        return "Windurst"
    else:
        return "San d'Oria"


def get_avatar_img(avatar_id):
    return avatars[avatar_id]


async def get_player_crafts(player):
    url = char_url + player + '/crafts'
    async with aiohttp.ClientSession() as s:
        async with s.get(url, ssl=False) as resp:
            craft_info = await resp.text()
    craft_info = ast.literal_eval(craft_info)
    return craft_info


async def get_player_jobs(player):
    url = char_url + player
    async with aiohttp.ClientSession() as s:
        async with s.get(url, ssl=False) as resp:
            p_info = await resp.text()
    p_info = ast.literal_eval(p_info)
    return p_info['jobs']


async def get_player_equip(player):
    url = char_url + player + '/equip'
    async with aiohttp.ClientSession() as s:
        async with s.get(url, ssl=False) as resp:
            equip_info = await resp.text()
    equip_info = ast.literal_eval(equip_info)
    return equip_info


def get_equip_ids(equip):
    ids = []
    for slot in equip:
        if 'itemid' in equip[slot]:
            ids.append(equip[slot]['itemid'])
        else:
            ids.append(0)
    return ids


def order_equip_ids(equip_ids):
    # Order used for in-game equipment menu
    order = (0, 1, 2, 3, 4, 9, 11, 12, 5, 6, 13, 14, 15, 10, 7, 8)
    ordered_ids = []
    for index in order:
        ordered_ids.append(equip_ids[index])

    return ordered_ids


async def build_equip_visual(ordered_ids):
    imgs = []
    for equip_id in ordered_ids:
        if not equip_id:
            imgs.append(0)
        url = base_url + str(equip_id) + '.png'
        async with aiohttp.ClientSession() as s:
            async with s.get(url, ssl=False) as resp:
                img_bytes = await resp.read()
        img_bytes = BytesIO(img_bytes)
        imgs.append(Image.open(img_bytes))
    widths, heights = zip(*(i.size for i in imgs if i))
    total_width = max(widths) * 4
    max_height = max(heights) * 4

    new_im = Image.new('RGB', (total_width, max_height))
    x_offset = 0
    y_offset = 0
    x_size = 32
    y_size = 32
    counter = 0
    async with aiohttp.ClientSession() as s:
        async with s.get(equip_background) as resp:
            img_bytes = await resp.read()
    img_bytes = BytesIO(img_bytes)
    bg_img = Image.open(img_bytes)
    for im in imgs:
        # background image needs to exist regardless of if the slot if full or not
        new_im.paste(bg_img, (x_offset, y_offset))

        # only bother adding a top layer item image if an item is equipped
        if im:
            new_im.paste(im, (x_offset, y_offset), mask=im)
            x_offset += x_size

        # move down every 4 slots
        counter += 1
        if x_offset == x_size * 4:
            y_offset += y_size
            x_offset = 0

    buffer = BytesIO()
    new_im.save(buffer, 'png')
    buffer.seek(0)

    return buffer


async def build_equip_embed(name):
    color = randint(0, 0xFFFFFF)
    equip = await get_player_equip(name)
    equip_ids = get_equip_ids(equip)
    ordered_ids = order_equip_ids(equip_ids)
    image = await build_equip_visual(ordered_ids)

    file = discord.File(fp=image, filename="player_equip.png")
    equip_embed = discord.Embed(title=format_name(name), color=color)
    equip_embed.set_image(url='attachment://player_equip.png')

    for slot in equip:
        if 'itemid' in equip[slot]:
            name = equip[slot]["name"]
            formatted_name = format_name(name)
            equip_embed.add_field(name=slot, value=f'[{formatted_name}]({user_ah_url + name})')
        elif 'ls' not in slot:
            equip_embed.add_field(name=slot, value='None')

    return equip_embed, file


def build_player_info_embed(player, p_info, last_online, server_id):
    embed = discord.Embed(title=format_name(player))
    ranks = f"San d'Oria: {p_info['ranks']['sandoria']}\n" \
            + f"Bastok:     {p_info['ranks']['bastok']}\n" \
            + f"Windurst:   {p_info['ranks']['windurst']}\n"

    embed.set_thumbnail(url=get_avatar_img(p_info['avatar']))
    embed.add_field(name='Title', value=p_info['title'], inline=True)
    embed.add_field(name='Job', value=p_info['jobString'], inline=True)
    if bool(p_info['online']):
        embed.color = 0x00ff00
        embed.add_field(name='Online?', value=bool(p_info['online']), inline=False)
    else:
        embed.color = 0x8B0000
        embed.add_field(name='Offline since:', value=last_online, inline=False)
    embed.add_field(name='Nation', value=get_nation(p_info['nation']))
    embed.add_field(name='Ranks', value=ranks)
    embed.set_footer(text=f'Time given in {get_timezone(server_id)}')

    return embed


def build_crafts_embed(player, craft_info):
    embed = discord.Embed(title=player)
    for craft in craft_info:
        embed.add_field(name=craft, value=craft_info[craft])
    return embed


async def build_jobs_embed(player):
    color = randint(0, 0xFFFFFF)
    jobs = await get_player_jobs(player)

    embed = discord.Embed(title=format_name(player), color=color)

    for job in jobs:
        if jobs[job]:
            embed.add_field(name=job, value=jobs[job], inline=True)

    return embed


def get_readable_timestamp(unix_ts, server_id):
    if server_id:
        tz = get_timezone(server_id)
    else:
        tz = 'US/Eastern'
    tz = pytz.timezone(tz)
    human_time = datetime.fromtimestamp(unix_ts, tz)
    return human_time.strftime('%Y-%m-%d %H:%M:%S')
