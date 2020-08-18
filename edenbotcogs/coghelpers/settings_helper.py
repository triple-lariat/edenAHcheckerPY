# Author: triple-lariat a.k.a: Tranquille, Desarroi, M.B.
# Any issues you encounter can be posted to https://github.com/triple-lariat/edenAHcheckerPY
# You may also find me on Eden or Eden's discord under the name Tranquille

import pickle

# command disable flags
MISC_COMMANDS = 1001
PLAYER_COMMANDS = 2002
MATH_COMMANDS = 3003
MARKET_COMMANDS = 4004
TIMER_COMMANDS = 5005


def initialize_channel_dict():
    try:
        channel_file = open('./data/disabled_channels.txt', 'rb')
        return pickle.load(channel_file)
    except FileNotFoundError:
        return {}


disabled_channels = initialize_channel_dict()


def disable_all_commands(channel_id):
    disabled_channels[channel_id] = [
        MISC_COMMANDS,
        PLAYER_COMMANDS,
        MATH_COMMANDS,
        MARKET_COMMANDS,
        TIMER_COMMANDS
    ]


def disable_command(channel_id, command_flag):
    try:
        if command_flag not in disabled_channels[channel_id]:
            disabled_channels[channel_id].append(command_flag)
    except KeyError:
        disabled_channels[channel_id] = [command_flag]
