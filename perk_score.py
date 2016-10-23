#!/usr/bin/env python3
from os import listdir
import perk_score.configs as configs
import perk_score.dim_weapon_source as weapons

cur_dir_files = listdir('.')
print(cur_dir_files)

weapon_file = None
potential_sources = weapons.source_file(cur_dir_files)
if len(potential_sources) != 1:
    # raise AssertionError('could not find a source file')
    print('A ' + weapons.file_name + ' must be available in the current directory. ' +
          'Please add one and run perk score again.')
    exit()
else:
    weapon_file = potential_sources[0]


weapons_source = weapons.DestinyItemManagerWeaponSource(weapon_file)

# TODO read in existing configs
configs = configs.config_files(cur_dir_files)
print('found config files: {0}'.format(configs))

# TODO this whole process of writing out configs should be in a separate module
"""
    Begin collecting all of the perks by weapon type.
"""

"""
{config_name: {weapon_type: {perk_name: score}}}
"""


perks_by_type_from_weapon_file = weapons_source.perks_by_type()

config_file_identifier = '_perk_score_config.txt'  # FIXME remove this when Config handles all of this logic

default_config = open('Default' + config_file_identifier, 'a')

all_weapon_types = ['Auto Rifle', 'Scout Rifle', 'Hand Cannon', 'Pulse Rifle', 'Fusion Rifle', 'Shotgun',
                    'Sniper Rifle', 'Sidearm', 'Rocket Launcher', 'Machine Gun', 'Sword']
all_weapon_types.sort()

for weapon_type in all_weapon_types:
    default_config.write('--- ' + weapon_type + ' ---\n')

    perks = perks_by_type_from_weapon_file.get(weapon_type, {})
    perks = list(perks)
    # TODO move this into the config or into the file handling?
    perks.sort()

    for perk in perks:
        default_config.write(perk + ':0\n')


default_config.close()
