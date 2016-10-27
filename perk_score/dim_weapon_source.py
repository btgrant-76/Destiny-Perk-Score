import perk_score.configs as configs


file_name = 'destinyWeapons.csv'


def source_file(file_names):
    return list(filter(lambda fn: fn == file_name, file_names))


class DestinyItemManagerWeaponSource:
    _source_file = None
    _name_index = -1
    _type_index = -1
    _perk_index = -1

    def __init__(self, dim_file_name):

        self._source_file = dim_file_name

        # TODO move the rest of these lines out of the init
        file = open(dim_file_name, 'r')
        headers = [header.strip() for header in file.readline().split(',')]

        self._name_index = headers.index('Name')
        self._perk_index = headers.index('Nodes')
        self._type_index = headers.index('Type')

        file.close()

    def pair_name_and_perks(self, weapon_file_line):
        split_line = weapon_file_line.split(', ')
        weapon_type = split_line[self._type_index]
        perks = [self.clean_up_perk_name(perk) for perk in split_line[self._perk_index: len(split_line)]]
        return weapon_type, perks

    def perks_by_type(self):
        file = open(self._source_file, 'r')
        file.readline()  # ignore the header

        weapon_type_and_perks = [self.pair_name_and_perks(line) for line in file.readlines()]

        perks_by_type = {}

        # TODO try a map comprehension
        for weapon_info in weapon_type_and_perks:
            weapon_type = weapon_info[0]
            perks = set(weapon_info[1])
            set_of_perks = perks_by_type.get(weapon_type, set())
            perks_by_type[weapon_type] = set_of_perks | perks

        for weapon_type in perks_by_type.keys():
            perk_set = perks_by_type[weapon_type]
            perks_by_type[weapon_type] = dict(zip(perk_set, [0] * len(perk_set)))

        return perks_by_type

    def create_config(self, name):
        config = configs.Config(name)
        config.perks_by_weapon_type = self.perks_by_type()
        return config

    @staticmethod
    def clean_up_perk_name(perk_name):

        perk_name = perk_name.strip()

        if perk_name.endswith(','):
            perk_name = perk_name.rstrip(',')

        if perk_name.endswith('*'):
            perk_name = perk_name.rstrip('*')

        return perk_name

