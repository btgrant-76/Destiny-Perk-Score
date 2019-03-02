#!/usr/bin/env python3
from os import listdir
import perk_score.configs as configs
import perk_score.dim_weapon_source as weapons


# TODO testing
# test a workflow where there are existing perk configs & new perks are detected in the weapon source to verify
# that we inform the user that new perks were detected.


cur_dir_files = listdir('.')

weapon_file = None
potential_sources = weapons.source_file(cur_dir_files)
if len(potential_sources) != 1:
    # TODO update this message to include the source from which the file should originate. This information should come from the weapon source.
    print('A ' + weapons.file_name + ' must be available in the current directory. ' +
          'Please add one and run perk score again.')
    exit()
else:
    weapon_file = potential_sources[0]

weapons_source = weapons.DestinyItemManagerWeaponSource(weapon_file)

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
    config_file_names = [configs.config_name(file_name) for file_name in config_file_names]
    configs_from_files = {file_name: configs.Config(file_name) for file_name in config_file_names}
    [configuration.read_file() for configuration in configs_from_files.values()]
    configs_with_new_perks = list(filter(lambda conf: conf.add_missing_perks(default_config),
                                         configs_from_files.values()))

    if len(configs_with_new_perks) > 0:
        [conf.write_config_file() for conf in configs_with_new_perks]

        names_of_updated_configs = '{0}'.format([config.name for config in configs_with_new_perks]).strip('[]')

        print('New perks have been discovered in the weapon source file and were added to the following configs:  {0}. '
              'Please update the configs and run perk_score again.'.format(names_of_updated_configs))
    else:
        weapons_source.update_with_configs(configs_from_files.values())

        configs = '{0}'.format(config_file_names).strip('[]')

        print('Scores from configs have been added:  {0}'.format(configs))
    exit()
