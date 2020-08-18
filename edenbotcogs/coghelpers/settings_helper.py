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

command_options = {
    'misc': MISC_COMMANDS,
    'player': PLAYER_COMMANDS,
    'math': MATH_COMMANDS,
    'market': MARKET_COMMANDS,
    'timers': TIMER_COMMANDS
}


def initialize_channel_dict():
    try:
        channel_file = open('./data/disabled_channels.txt', 'rb')
        return pickle.load(channel_file)
    except FileNotFoundError:
        return {}
    except EOFError:
        return {}


disabled_channels = initialize_channel_dict()


def save_dict():  # called when any changes are made to the disabled channels dict
    channel_file = open('./data/disabled_channels.txt', 'wb')
    pickle.dump(disabled_channels, channel_file)
    print('Current disabled channel dictionary written to file!')


def disable_all_commands(channel_id):
    disabled_channels[channel_id] = [
        MISC_COMMANDS,
        PLAYER_COMMANDS,
        MATH_COMMANDS,
        MARKET_COMMANDS,
        TIMER_COMMANDS
    ]

    save_dict()


def enable_all_commands(channel_id):
    try:
        del disabled_channels[channel_id]
        save_dict()
    except KeyError:
        pass


def disable_command(channel_id, command_flag):
    try:
        if command_flag not in disabled_channels[channel_id]:
            disabled_channels[channel_id].append(command_flag)
            save_dict()
    except KeyError:
        disabled_channels[channel_id] = [command_flag]
        save_dict()


def enable_command(channel_id, command_flag):
    try:
        if command_flag in disabled_channels[channel_id]:
            disabled_channels[channel_id].remove(command_flag)
            save_dict()
    except KeyError:
        pass
