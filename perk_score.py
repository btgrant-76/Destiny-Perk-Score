#!/usr/bin/env python3
from os import listdir
import perk_score.configs as configs
import perk_score.dim_weapon_source as weapons

cur_dir_files = listdir('.')

weapon_file = None
potential_sources = weapons.source_file(cur_dir_files)
if len(potential_sources) != 1:
    print('A ' + weapons.file_name + ' must be available in the current directory. ' +
          'Please add one and run perk score again.')
    exit()
else:
    weapon_file = potential_sources[0]


weapons_source = weapons.DestinyItemManagerWeaponSource(weapon_file)

# TODO read in existing configs
config_file_names = configs.config_files(cur_dir_files)

default_config = weapons_source.create_config('Default')

perks_by_type_from_weapon_file = weapons_source.perks_by_type()

def log_and_return(name, value):
    print('got "{0}" for "{1}"'.format(value, name))
    return value

if len(config_file_names) == 0:
    print('No perk score config files were found.')

    default_config.write_config_file()

    print('A default config file called "{0}" has been created. Please update perk scores in this file '
          'and run perk_score again.'.format(default_config.config_file_name()))
    exit()
else:
    config_names = [configs.config_name(file_name) for file_name in config_file_names]
    configs_from_files = {name: configs.Config(name) for name in config_names}
    [configuration.read_file() for configuration in configs_from_files.values()]
    configs_with_new_perks = list(filter(lambda conf: conf.add_missing_perks(default_config),
                                         configs_from_files.values()))

    if len(configs_with_new_perks) > 0:
        [conf.write_config_file() for conf in configs_with_new_perks]

        names_of_updated_configs = '{0}'.format([config.name for config in configs_with_new_perks]).strip('[]')

        print('New perks have been discovered in the weapon source file and were added to the following configs:  {0}. '
              'Please update the configs and run perk_score again.'.format(names_of_updated_configs))
    else:
        print('No new perks were found. Now we need to update the source with perk values...')
    exit()
