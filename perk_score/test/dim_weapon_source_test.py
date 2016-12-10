import unittest
import perk_score.dim_weapon_source as source
import perk_score.configs as configs
import os


class DIMSourceTest(unittest.TestCase):

    test_file_name = 'dimFile.csv'
    temp_test_file_name = test_file_name + '.tmp'

    test_config_one = None
    test_config_two = None

    test_source = None

    def setUp(self):
        self.set_up_source_file(self.test_file_name)

        self.test_config_one = configs.Config('Test 1')
        self.test_config_two = configs.Config('Test 2')

        self.test_source = source.DestinyItemManagerWeaponSource(self.test_file_name)

    def tearDown(self):
        self.test_config = None

        if os.path.isfile(self.test_file_name):
            os.remove(self.test_file_name)

        if os.path.isfile(self.temp_test_file_name):
            os.remove(self.temp_test_file_name)

    def test_config_from_source(self):
        test_source = source.DestinyItemManagerWeaponSource('./perk_score/test/dimTestFile.csv')
        config = test_source.create_config('Test')

        self.assertEqual('Test', config.name)

        perks = config.perks_by_weapon_type
        scout_rifle_perks = perks['Scout Rifle']

        self.assertIsInstance(scout_rifle_perks, dict)

        self.assertEqual(8, len(list(scout_rifle_perks.keys())))

        for perk in ['Sights 1', 'Sights 2', 'Sights 3',
                     'Perk 1', 'Perk 2', 'Perk 3', 'Perk 4', 'Perk 5']:
            self.assertEqual(0, scout_rifle_perks[perk])

        pulse_rifle_perks = perks['Pulse Rifle']
        self.assertEqual(7, len(pulse_rifle_perks.keys()))

        for perk in ['Pulse Sight 1', 'Pulse Sight 2', 'Pulse Sight 3',
                     'Pulse Perk 1', 'Pulse Perk 2', 'Pulse Perk 3', 'Pulse Perk 4']:
            self.assertEqual(0, pulse_rifle_perks[perk])

        self.assertTrue('Fusion Rifle' not in perks.keys())

    def test_write_configs_to_source_without_config_data(self):
        self.test_source.update_with_configs([self.test_config_one, self.test_config_two])

        test_file = open(self.test_file_name)
        self.verify_updated_header(test_file)
        self.verify_weapon_count_and_scores(test_file, self.all_zero_scores())

    def test_write_configs_to_source_with_no_applicable_scoring(self):
        self.test_config_one.perks_by_weapon_type = {'Pulse Rifle': {'Scout 1': 2, 'Scout 2': 5},
                                                     'Fusion Rifle': {'Fusion 1': 8, 'Fusion 2': 100}}
        self.test_config_two.perks_by_weapon_type = {'Scout Rifle': {'Scout 1': 2, 'Scout 2': 5},
                                                     'Fusion Rifle': {'Fusion 1': 8, 'Fusion 2': 100}}

        self.test_source.update_with_configs([self.test_config_one, self.test_config_two])

        test_file = open(self.test_file_name)
        self.verify_updated_header(test_file)
        self.verify_weapon_count_and_scores(test_file, self.all_zero_scores())

    def all_zero_scores(self):
        return {'Scout Rifle 1': (' 0', ' 0'),
                'Scout Rifle 2': (' 0', ' 0'),
                'Hand Cannon 1': (' 0', ' 0'),
                'Hand Cannon 2': (' 0', ' 0'),
                'Hand Cannon 3': (' 0', ' 0'),
                'Machine Gun':   (' 0', ' 0'),
                'Pulse Rifle 1': (' 0', ' 0'),
                'Pulse Rifle 2': (' 0', ' 0')}

    def verify_updated_header(self, test_file):
        header_line = test_file.readline()
        self.assertTrue(', Notes, Test 1, Test 2, Nodes' in header_line, header_line)

    def verify_weapon_count_and_scores(self, test_file, weapon_scores):
        number_of_weapons_found = 0

        for weapon_line in test_file:
            split_line = weapon_line.split(',')
            scores = weapon_scores[split_line[0]]
            self.assertEqual(scores[0], split_line[20])
            self.assertEqual(scores[1], split_line[21])
            number_of_weapons_found += 1

        self.assertEqual(8, number_of_weapons_found)

    def set_up_source_file(self, file_name):
        test_file = open(file_name, 'w')
        test_file.write("Name, Tag, Tier, Type, Light, Dmg, Owner, % Leveled, Locked, Equipped, Year,AA, Impact, Range, Stability, ROF, Reload, Mag, Equip, Notes, Nodes\n")

        test_file.write("Scout Rifle 1, , Rare, Scout Rifle, 340, Kinetic, Hunter(345), 0, false, false, "
                        "2, 48, 35, 45, 56, 52, 52, 20, 63, , "
                        "SLO-12*, SPO-26, Outlaw, Quickdraw, Hammer Forged, \n")
        test_file.write("Hand Cannon 1, , Rare, Hand Cannon, 340, Kinetic, Hunter(345), 0, false, false, "
                        "2, 67, 81, 32, 27, 22, 49, 5, 31, , "
                        "QuickDraw IS*, TrueSight IS, SureShot IS, Partial Refund, Hand Loaded, Reinforced Barrel, \n")
        test_file.write("Machine Gun, , Rare, Machine Gun, 340, Arc, Hunter(345), 0, false, false, "
                        "2, 48, 53, 16, 46, 66, 28, 56, 30, , "
                        "CQB Ballistics*, Accurized Ballistics, Smooth Ballistics, Surrounded, Perfect Balance, Rifled Barrel, \n")
        test_file.write("Pulse Rifle 1, , Legendary, Pulse Rifle, 349, Kinetic, Hunter(345), 100, true, false, "
                        "2, 60, 7, 36, 90, 73, 73, 24, 89, , "
                        "SLO-12, SPO-28*, SRO-41, Fitted Stock*, Casket Mag, Outlaw*, Single Point Sling, Smallbore*, \n")
        test_file.write("Hand Cannon 2, , Legendary, Hand Cannon, 350, Kinetic, Hunter(345), 100, true, false, "
                        "3, 70, 81, 62, 44, 22, 31, 9, 46, , "
                        "TrueSight IS*, FastDraw IS, QuickDraw IS, Mulligan, Spray and Play*, Rifled Barrel*, Casket Mag, Rangefinder*, \n")
        test_file.write("Pulse Rifle 2, , Legendary, Pulse Rifle, 335, Kinetic, Hunter(345), 100, true, false, "
                        "2, 60, 7, 36, 90, 73, 73, 24, 89, , "
                        "SLO-19, SPO-28*, SPO-57, Fitted Stock*, Oiled Frame, Counterbalance*, Single Point Sling, Smallbore*, \n")
        test_file.write("Hand Cannon 3, , Legendary, Hand Cannon, 340, Kinetic, Hunter(345), 100, true, false, "
                        "2, 50, 81, 62, 35, 22, 46, 12, 60, , "
                        "SteadyHand IS, FastDraw IS*, QuickDraw IS, Outlaw*, Lightweight, Reinforced Barrel*, Oiled Frame, Life Support*, \n")
        test_file.write("Scout Rifle 2, , Exotic, Scout Rifle, 340, Kinetic, Hunter(345), 100, true, false, "
                        "2, 90, 38, 52, 59, 42, 100, 21, 100, , "
                        "Soft Ballistics, CQB Ballistics, Smart Drift Control*, Third Eye*, Lightweight*, Quickdraw, Field Scout, MIDA Multi-Tool*, Special Ops, Arctic Survivalist, \n")

        test_file.close()


        #  TODO it would be good to have some tests where there's a perk with the same name across multiple
        #  weapon types to demonstrate that scoring is applied appropriately

        # self.set_up_source_file(self.test_file_name)
        #
        # test_config_one = configs.Config('Test 1')
        # # test_config_one.perks_by_weapon_type = {'Pulse Rifle': {'Oiled Frame': 2, 'Scout 2': 5},
        # #                                         'Fusion Rifle': {'Fusion 1': 8, 'Fusion 2': 100}}
        #
        # test_config_two = configs.Config('Test 2')
        # # test_config_two.perks_by_weapon_type = {'Scout Rifle': {'Scout 1': 2, 'Scout 2': 5},
        # #                                         'Fusion Rifle': {'Fusion 1': 8, 'Fusion 2': 100}}
        #
        # # Scout Rifle, Sights 1*, Sights 2, Perk 1, Perk 2, Perk 3,
        # # Pulse Rifle, Pulse Sight 1, Pulse Sight 2*, Pulse Sight 3, Pulse Perk 1, Pulse Perk 2*, Pulse Perk 3, Pulse Perk 4*,
        # # Scout Rifle, Sights 1, Sights 3*, Perk 1*, Perk 5, Perk 4,
        #
        # test_source = source.DestinyItemManagerWeaponSource(self.test_file_name)
        # test_source.update_with_configs([test_config_one, test_config_two])
