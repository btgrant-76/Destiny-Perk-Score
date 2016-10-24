#!/usr/bin/env python3
from os import listdir
import perk_score.configs as configs
import perk_score.dim_weapon_source as weapons

cur_dir_files = listdir('.')
# print(cur_dir_files)

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
config_file_names = configs.config_files(cur_dir_files)

if len(config_file_names) == 0:
    print('No perk score config files were found.')
    # TODO create the default config and write it out

    perks_by_type_from_weapon_file = weapons_source.perks_by_type()

    default_config = configs.Config('Default')
    default_config.perks_by_weapon_type = perks_by_type_from_weapon_file
    default_config.write_config_file()

    print('A default config file called "{0}" has been created. Please update perk scores in this file '
          'and run perk_score again.'.format(default_config.config_file_name()))
    exit()

else:
    print('*** Found config files but we are exiting: {0} ***'.format(config_file_names))
    exit()
