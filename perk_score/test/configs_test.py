import unittest
import os
import os.path
import perk_score.configs as configs


class ConfigTest(unittest.TestCase):

    weapon_types = sorted(['Auto Rifle', 'Scout Rifle', 'Hand Cannon', 'Pulse Rifle', 'Fusion Rifle', 'Shotgun',
                           'Sniper Rifle', 'Sidearm', 'Rocket Launcher', 'Machine Gun', 'Sword'])
    file_name = 'test_perk_score_config.txt'
    test_config = None
    config_file = None

    def setUp(self):
        self.test_config = configs.Config('test')

    def tearDown(self):
        if self.config_file:
            self.config_file.close()
            self.config_file = None

        if os.path.isfile(self.file_name):
            os.remove(self.file_name)

    def open_config_file(self):
        self.config_file = open(self.file_name)
        return self.config_file

    def test_names_that_are_config_names(self):
        confirmed_config_names = configs.config_files(['first_perk_score_config.txt', 'not_a_config.txt',
                                                       'second_perk_score_config.txt'])
        self.assertEqual(2, len(confirmed_config_names))
        self.assertEqual(['first_perk_score_config.txt', 'second_perk_score_config.txt'], confirmed_config_names)

    def test_an_empty_config_will_write_only_weapon_types(self):
        self.test_config.write_config_file()

        config_file = self.open_config_file()
        for weapon_type in self.weapon_types:
            line = config_file.readline()
            self.assertEqual(line, '--- ' + weapon_type + ' ---\n')

    def test_a_config_with_a_mix_of_perks(self):
        self.test_config.perks_by_weapon_type = {'Scout Rifle': {'Scout 1': 2, 'Scout 2': 5},
                                                 'Fusion Rifle': {'Fusion 1': 8, 'Fusion 2': 100}}
        self.test_config.write_config_file()

        config_file = self.open_config_file()

        for weapon_type in self.weapon_types:
            line = config_file.readline()
            self.assertEqual(line, '--- ' + weapon_type + ' ---\n')

            if weapon_type == 'Scout Rifle':
                self.assertEqual('Scout 1:2\n', config_file.readline())
                self.assertEqual('Scout 2:5\n', config_file.readline())
            elif weapon_type == 'Fusion Rifle':
                self.assertEqual('Fusion 1:8\n', config_file.readline())
                self.assertEqual('Fusion 2:100\n', config_file.readline())

    def test_perks_are_written_in_alpha_order(self):
        self.test_config.perks_by_weapon_type = {'Scout Rifle': {'Z Scout 1': 2, 'A Scout 2': 5},
                                                 'Fusion Rifle': {'Fusion Z': 8, 'Fusion A': 100}}
        self.test_config.write_config_file()

        config_file = self.open_config_file()

        for weapon_type in self.weapon_types:
            line = config_file.readline()
            self.assertEqual(line, '--- ' + weapon_type + ' ---\n')

            if weapon_type == 'Scout Rifle':
                self.assertEqual('A Scout 2:5\n', config_file.readline())
                self.assertEqual('Z Scout 1:2\n', config_file.readline())
            elif weapon_type == 'Fusion Rifle':
                self.assertEqual('Fusion A:100\n', config_file.readline())
                self.assertEqual('Fusion Z:8\n', config_file.readline())

    def test_only_real_weapon_types_are_written_out(self):
        fake_weapon_type = 'VOOP Nation'
        self.test_config.perks_by_weapon_type = {fake_weapon_type: {'Fusion 1': 8, 'Fusion 2': 100}}

        self.test_config.write_config_file()

        config_file = self.open_config_file()

        for line in config_file:
            self.assertEqual(-1, line.find(fake_weapon_type))

    def test_no_perks_are_change_when_all_perks_already_exist(self):
        self.test_config.perks_by_weapon_type = {'Scout Rifle': {'Scout 1': 2, 'Scout 2': 5},
                                                 'Fusion Rifle': {'Fusion 1': 8, 'Fusion 2': 100}}
        another_config = configs.Config('Another Config')
        another_config.perks_by_weapon_type = {'Scout Rifle': {'Scout 1': 4, 'Scout 2': 10},
                                               'Fusion Rifle': {'Fusion 1': 16, 'Fusion 2': 200}}

        perks_were_added = self.test_config.add_missing_perks(another_config)
        self.assertFalse(perks_were_added)

        self.assertEqual({'Scout 1': 2, 'Scout 2': 5}, self.test_config.perks_by_weapon_type['Scout Rifle'])
        self.assertEqual({'Fusion 1': 8, 'Fusion 2': 100}, self.test_config.perks_by_weapon_type['Fusion Rifle'])

    def test_addition_of_missing_perks(self):
        self.test_config.perks_by_weapon_type = {'Scout Rifle': {'Scout 1': 2, 'Scout 2': 5},
                                                 'Fusion Rifle': {'Fusion 1': 8, 'Fusion 2': 100}}
        another_config = configs.Config('Another Config')
        another_config.perks_by_weapon_type = {'Scout Rifle': {'Scout 3': 4, 'Scout 4': 10},
                                               'Shotgun': {'Shotgun 1': 16, 'Shotgun 2': 200}}

        perks_were_added = self.test_config.add_missing_perks(another_config)
        self.assertTrue(perks_were_added)

        self.assertEqual({'Scout 1': 2, 'Scout 2': 5, 'Scout 3': 4, 'Scout 4': 10},
                         self.test_config.perks_by_weapon_type['Scout Rifle'])
        self.assertEqual({'Fusion 1': 8, 'Fusion 2': 100}, self.test_config.perks_by_weapon_type['Fusion Rifle'])
        self.assertEqual({'Shotgun 1': 16, 'Shotgun 2': 200}, self.test_config.perks_by_weapon_type['Shotgun'])

