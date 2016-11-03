import unittest
import perk_score.dim_weapon_source as source


class DIMSourceTest(unittest.TestCase):

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