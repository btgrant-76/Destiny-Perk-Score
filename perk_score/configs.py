from os.path import isfile
import os

config_file_identifier = '_perk_score_config.txt'  # TODO make this private?


def config_files(file_names):
    return list(filter(lambda n: n.endswith(config_file_identifier), file_names))


class Config:
    _all_weapon_types = sorted(['Auto Rifle', 'Scout Rifle', 'Hand Cannon', 'Pulse Rifle', 'Fusion Rifle', 'Shotgun',
                               'Sniper Rifle', 'Sidearm', 'Rocket Launcher', 'Machine Gun', 'Sword'])
    name = None
    perks_by_weapon_type = {}

    def __init__(self, name):
        self.name = name

    def config_file_name(self):
        return self.name + config_file_identifier

    def backup_file_name(self):
        return self.name + '_backup_' + config_file_identifier

    def write_config_file(self):
        self.create_backup_config()

        config_file = open(self.config_file_name(), 'a')  # TODO is there a way to truncate and then write?

        for weapon_type in self._all_weapon_types:
            config_file.write('--- ' + weapon_type + ' ---\n')

            perks = self.perks_by_weapon_type.get(weapon_type, {})
            perk_names = sorted(perks.keys())

            for perk_name in perk_names:
                config_file.write('{0}:{1}\n'.format(perk_name, perks[perk_name]))

        config_file.close()
        self.delete_backup_file()
        pass

    def create_backup_config(self):
        if isfile(self.config_file_name()):
            backup_file_name = self.backup_file_name()
            if isfile(backup_file_name):  # TODO do something a bit more constructive
                raise AssertionError('a backup file was found:  ' + backup_file_name)

            os.rename(self.config_file_name(), backup_file_name)

    def delete_backup_file(self):
        if isfile(self.backup_file_name()):
            os.remove(self.backup_file_name())

    def add_missing_perks(self, config):
        for weapon_type in config.perks_by_weapon_type.keys():
            incoming_perks = config.perks_by_weapon_type[weapon_type]

            if weapon_type in self.perks_by_weapon_type.keys():
                my_perks = self.perks_by_weapon_type[weapon_type]

                for incoming_perk in incoming_perks.keys():
                    if incoming_perk not in my_perks.keys():
                        my_perks[incoming_perk] = incoming_perks[incoming_perk]
            else:
                self.perks_by_weapon_type[weapon_type] = incoming_perks

