# Author: triple-lariat a.k.a: Tranquille, Desarroi, M.B.
# Any issues you encounter can be posted to https://github.com/triple-lariat/edenAHcheckerPY
# You may also find me on Eden or Eden's discord under the name Tranquille

# The functions for calculating time are derived from Pyogenes' timers
# Extra special thanks to them for working out the math for all of this!
# Source: http://www.pyogenes.com/ffxi/timer/v2.html

import discord.embeds
from time import time
from math import floor

base_datetime = 1024844400000.0  # 1022166000000.0
base_moon_datetime = 1074997872000.0
base_week_datetime = 1075281264000.0
phase_name = (
    'Full Moon',
    'Waning Gibbous',
    'Last Quarter',
    'Waning Crescent',
    'New Moon',
    'Waxing Crescent',
    'First Quarter',
    'Waxing Gibbous'
)
emote_moon = (
    ':full_moon:',
    ':waning_gibbous_moon:',
    ':last_quarter_moon:',
    ':waning_crescent_moon:',
    ':new_moon:',
    ':waxing_crescent_moon:',
    ':first_quarter_moon:',
    ':waxing_gibbous_moon:'
)
week_day = (
    'Firesday',
    'Earthsday',
    'Watersday',
    'Windsday',
    'Iceday',
    'Lightningday',
    'Lightsday',
    'Darksday'
)
day_color = (
    0xDD000,
    0xAAAA00,
    0x0000DD,
    0x00AA22,
    0x7799FF,
    0xAA00AA,
    0xAAAAAA,
    0x333333
)

game_day_ms = (24 * 60 * 60 * 1000 / 25.0)  # milliseconds in a game day
real_day_ms = (24 * 60 * 60 * 1000.0)  # milliseconds in a real day


def get_vana_time(now = None):
    if now is None:
        now = time() * 1000  # current time in ms
    vana_date = (((898 * 360) + 30) * real_day_ms) + (now - base_datetime) * 25
    return vana_date


def get_moon_phase(now = None):
    if now is None:
        now = time() * 1000  # current time in ms
    moon_days = (floor((now - base_moon_datetime) / game_day_ms)) % 84
    moon_percent = - round((42 - moon_days) / 42 * 100)

    if moon_percent <= -94 or moon_percent >= 90:
        return phase_name[0], abs(moon_percent), emote_moon[0]
    elif -93 <= moon_percent <= -62:
        return phase_name[1], abs(moon_percent), emote_moon[1]
    elif -61 <= moon_percent <= -41:
        return phase_name[2], abs(moon_percent), emote_moon[2]
    elif -40 <= moon_percent <= -11:
        return phase_name[3], abs(moon_percent), emote_moon[3]
    elif -10 <= moon_percent <= 6:
        return phase_name[4], abs(moon_percent), emote_moon[4]
    elif 7 <= moon_percent <= 36:
        return phase_name[5], abs(moon_percent), emote_moon[5]
    elif 37 <= moon_percent <= 56:
        return phase_name[6], abs(moon_percent), emote_moon[6]
    else:
        return phase_name[7], abs(moon_percent), emote_moon[7]


def get_vana_ymd(vana_date):
    vana_year = floor(vana_date / (360 * real_day_ms))
    vana_mon = floor((vana_date % (360 * real_day_ms)) / (30 * real_day_ms)) + 1
    vana_day = floor((vana_date % (30 * real_day_ms)) / real_day_ms) + 1

    if vana_year < 1000:
        vana_year = '0' + str(vana_year)
    else:
        vana_year = str(vana_year)

    if vana_mon < 10:
        vana_mon = '0' + str(vana_mon)
    else:
        vana_mon = str(vana_mon)

    if vana_day < 10:
        vana_day = '0' + str(vana_day)
    else:
        vana_day = str(vana_day)

    return vana_year, vana_mon, vana_day


def get_vana_hms(vana_date):
    vana_hour = floor((vana_date % real_day_ms) / (60 * 60 * 1000))
    vana_min = floor((vana_date % (60 * 60 * 1000)) / (60 * 1000))
    vana_sec = floor((vana_date % (60 * 1000)) / 1000)

    if vana_hour < 10:
        vana_hour = '0' + str(vana_hour)
    else:
        vana_hour = str(vana_hour)

    if vana_min < 10:
        vana_min = '0' + str(vana_min)
    else:
        vana_min = str(vana_min)

    if vana_sec < 10:
        vana_sec = '0' + str(vana_sec)
    else:
        vana_sec = str(vana_sec)

    return vana_hour, vana_min, vana_sec


def get_vana_week_day(vana_date):
    vana_week_day = floor((vana_date % (8 * real_day_ms)) / real_day_ms)
    return week_day[vana_week_day], day_color[vana_week_day]


def build_clock_embed():
    moon = get_moon_phase()
    vana_date = get_vana_time()
    ymd = get_vana_ymd(vana_date)
    hms = get_vana_hms(vana_date)
    day = get_vana_week_day(vana_date)

    clock_embed = discord.Embed(title=f'{ymd[0]}-{ymd[1]}-{ymd[2]}', color=day[1])
    clock_embed.add_field(name='Time(HMS)', value=f'{hms[0]}:{hms[1]}:{hms[2]}')
    clock_embed.add_field(name='Day', value=day[0])
    clock_embed.add_field(name=f'Moon {moon[2]}', value=f'{moon[0]} {moon[1]}%')
    return clock_embed


def build_calendar():
    offset = time() * 1000
    days = []
    for day in range(26):
        offset_vana_time = get_vana_time(offset)
        moon = get_moon_phase(offset)
        day_info = [get_vana_ymd(offset_vana_time)[1:], moon, get_vana_week_day(offset_vana_time)]
        days.append(day_info)
        offset += game_day_ms
    calendar_embed = discord.Embed(title='placeholder')
    for day in days:
        calendar_embed.add_field(name=f'{day[0][0]}/{day[0][1]}', value=f'{day[1][2]} {day[1][1]}%\n{day[2]}')
    return calendar_embed
