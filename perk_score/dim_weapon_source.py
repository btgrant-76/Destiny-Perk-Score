import perk_score.configs as configs
import os


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

            if '' in perks:
                # Empty perks only seem to be show up when I use the 'real' file from DIM.
                # If I try to introduce the same end-of-line characters, they end up being stripped out.
                # I'm not interested in investigating the source of the different behavior now so just
                # remove an empty perk.
                perks.remove('')

            set_of_perks = perks_by_type.get(weapon_type, set())
            perks_by_type[weapon_type] = set_of_perks | perks

        for weapon_type in perks_by_type.keys():
            perk_set = perks_by_type[weapon_type]
            perks_by_type[weapon_type] = dict(zip(perk_set, [0] * len(perk_set)))

        file.close()
        return perks_by_type

    def create_config(self, name):
        config = configs.Config(name)
        config.perks_by_weapon_type = self.perks_by_type()
        return config

    def update_with_configs(self, configurations):
        # TODO weapon rows, populate the appropriate config column with the score for that weapon type's scores
        input_file = open(self._source_file)
        output_file = open(self._source_file + '.tmp', 'x')

        header_row = input_file.readline()

        output_file.writelines(self.update_header_with_config_names(header_row, configurations))

        for weapon in input_file:
            output_file.write(self.add_score_to_weapon_line(weapon, configurations))

        input_file.close()
        output_file.close()

        os.remove(input_file.name)
        os.rename(output_file.name, input_file.name)

    @staticmethod
    def update_header_with_config_names(header_row, configurations):
        notes_header = 'Notes, '

        partitioned_header = header_row.split(notes_header)
        header_with_configs = partitioned_header[0] + notes_header

        for config in configurations:
            header_with_configs = header_with_configs + '{0}, '.format(config.name)

        header_with_configs += partitioned_header[1]
        return header_with_configs

    def add_score_to_weapon_line(self, weapon_line, configurations):
        split_weapon = weapon_line.split(',')

        first_half = split_weapon[0:self._perk_index]
        perks = split_weapon[self._perk_index:len(split_weapon)]

        first_half = first_half + [' {0}'.format(self.score_perks(first_half[self._type_index].strip(), perks, configuration)) for configuration in configurations]

        return ','.join(first_half + perks)

    @staticmethod
    def score_perks(weapon_type, perks, configuration):
        if weapon_type not in configuration.perks_by_weapon_type.keys():
            return 0

        total_score = 0
        perk_scores = configuration.perks_by_weapon_type[weapon_type]

        for perk in perks:
            perk_name = DestinyItemManagerWeaponSource.clean_up_perk_name(perk)
            if perk_name in perk_scores.keys():
                total_score += perk_scores[perk_name]

        return total_score

    @staticmethod
    def clean_up_perk_name(perk_name):

        perk_name = perk_name.strip()

        if perk_name.endswith(','):
            perk_name = perk_name.rstrip(',')

        if perk_name.endswith('*'):
            perk_name = perk_name.rstrip('*')

        return perk_name

