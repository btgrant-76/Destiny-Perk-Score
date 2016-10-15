#!/usr/bin/env python3
from os import listdir

weapon_file_name = 'destinyWeapons.csv'
config_file_identifier = '_perkscore_config.txt'

cur_dir_files = listdir('.')

# if cur_dir_files.index(weapon_file_name) < 0:
if weapon_file_name not in cur_dir_files:
    print('A ' + weapon_file_name + ' must be available in the current directory. ' +
                                    'Please add one and run perkscore again.')
    exit()

# TODO read in existing configs
configs = []


def file_is_config(file_name):
    if file_name.index(config_file_identifier) >= 1:
        config_name = file_name.rstrip(config_file_identifier)
        print('found a config:  ' + config_name)


print(cur_dir_files)

weapon_file = open(weapon_file_name, 'r')
# print(weapon_file)
first_line = weapon_file.readline()
# print('first line is ' + first_line)


# def clean_up_header(header):
#     return header.strip()

headers = [header.strip() for header in first_line.split(',')] # TODO could this split using ', ' instead?
# print(headers)

name_column_index = headers.index('Name')
perk_column_index = headers.index('Nodes')
weapon_type_index = headers.index('Type')
# print(headers[name_column_index] + ' ' + headers[perk_column_index])


def clean_up_perk_name(perk_name):
    # stripped_name = perk_name.strip()
    if perk_name.endswith('*'):
        return perk_name.rstrip('*')
    else:
        return perk_name


def pair_name_and_perks(weapon_file_line):
    split_line = weapon_file_line.split(', ')
    name = split_line[name_column_index]
    weapon_type = split_line[weapon_type_index]
    perks = [clean_up_perk_name(perk) for perk in split_line[perk_column_index: len(split_line) - 1]]
    return name, weapon_type, perks


name_weapon_type_and_perks = [pair_name_and_perks(line) for line in weapon_file.readlines()]

# print(name_weapon_type_and_perks)

# TODO this whole process of writing out configs should be in a separate module
"""
    Begin collecting all of the perks by weapon type.
"""

"""
{config_name: {weapon_type: {perk_name: score}}}
"""

all_weapon_types = ['Auto Rifle', 'Scout Rifle', 'Hand Cannon', 'Pulse Rifle', 'Fusion Rifle', 'Shotgun',
                    'Sniper Rifle', 'Sidearm', 'Rocket Launcher', 'Machine Gun', 'Sword']

perkscore_configs = {'default': {'Auto Rifle': {}, 'Scout Rifle': {}, 'Hand Cannon': {}, 'Pulse Rifle': {},
                                 'Fusion Rifle': {}, 'Shotgun': {}, 'Sniper Rifle': {}, 'Sidearm': {},
                                 'Rocket Launcher': {}, 'Machine Gun': {}, 'Sword': {}}}

perks_by_type_from_weapon_file = {}

for weapon_info in name_weapon_type_and_perks:
    weapon_type = weapon_info[1]
    perks = set(weapon_info[2])
    set_of_perks = perks_by_type_from_weapon_file.get(weapon_type, set())
    perks_by_type_from_weapon_file[weapon_type] = set_of_perks | perks

# print(perks_by_type_from_weapon_file)

default_config = open('Default' + config_file_identifier, 'a')

for weapon_type_and_perks in perks_by_type_from_weapon_file.items():
    weapon_type, perks = weapon_type_and_perks

    default_config.write('--- ' + weapon_type + ' ---\n')
    # print(weapon_type_and_perks)

    perks = list(perks)
    perks.sort()

    for perk in perks:
        default_config.write(perk + ':0\n')


    # print(weapon_type_and_perks[0] + ' ' + [weapon_type_and_perks[1]])


default_config.close()





# for weapon_info in name_weapon_type_and_perks:
#     weapon_type = weapon_info[1]
#     for config_name in perkscore_configs.keys():
#         perks = perkscore_configs[weapon_type]
#         for perk in weapon_info[2]:
#             if perk not in perks:
#                 perks.update({perk: 0})
#                 print('found new perk "{0}" for type {1}'.format(perk, weapon_type))

some_file = open('some_file', 'a')

# TODO collect all of the perks by weapon type
for weapon_info in name_weapon_type_and_perks:
    some_file.write('[{0}]\n'.format(weapon_info[1]))


# something = [header_name.strip() for header_name in headers]
# print(something)

# TODO remove these if they're not useful
# perk_exclusions = []
# perk_match_exclusions = ['Chroma']
# perk_score = {
#     'Scout Rifle': {'Hidden Hand': 9},
#     'Hand Cannon': {'Range Finder': 10, 'Crowd Control': 5, 'Life Support': 7},
#     'Pulse Rifle': {'Counterbalance': 10, 'Surrounded': -1}
# }


# def perk_should_be_filtered(perk_name):
#     # loop through the match values
#
#     if perk_exclusions.index(perk_name) >= 0:
#         return True
#     else:
#         return False

