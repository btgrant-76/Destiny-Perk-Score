import unittest
from os import listdir
import perk_score.dim_weapon_source as source


class DIMSourceTest(unittest.TestCase):

    def test_something(self):
        print(listdir('.'))
        self.assertTrue(True)
        pass

    def test_config_from_source(self):
        test_source = source.DestinyItemManagerWeaponSource('./perk_score/test/dimTestFile.csv')
        config = test_source.create_config('Test')

        self.assertEqual('Test', config.name)

        perks = config.perks_by_weapon_type
        scout_rifle_perks = perks['Scout Rifle']
        # TODO test that scout_rifle_perks is a map?
        for perk in ['Sights 1', 'Sights 2', 'Perk 1', 'Perk 2', 'Perk 3']:
            self.assertEqual(0, scout_rifle_perks[perk])

        self.assertTrue('Fusion Rifle' not in perks.keys())
