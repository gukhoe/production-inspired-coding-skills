import unittest

from oee import calculate_oee


class OeeTests(unittest.TestCase):
    def test_given_inputs_and_unit_conversion(self):
        result = calculate_oee(480, 420, 30, 760, 735)
        self.assertAlmostEqual(result["availability"], 0.875)
        self.assertAlmostEqual(result["performance"], 19 / 21)
        self.assertAlmostEqual(result["quality"], 147 / 152)
        self.assertAlmostEqual(result["oee"], 0.765625)
        # Independently calculate ideal time for good units / planned time.
        self.assertAlmostEqual(result["oee"], (735 * 30) / (480 * 60))

    def test_perfect_production(self):
        self.assertEqual(calculate_oee(60, 60, 60, 60, 60),
                         dict(availability=1, performance=1, quality=1, oee=1))

    def test_no_good_units(self):
        result = calculate_oee(60, 30, 60, 30, 0)
        self.assertEqual(result["quality"], 0)
        self.assertEqual(result["oee"], 0)

    def test_invalid_inputs(self):
        cases = [
            (0, 10, 30, 10, 9), (60, 0, 30, 10, 9),
            (60, 10, 30, 0, 0), (60, 61, 30, 10, 9),
            (60, 10, 30, 10, 11), (60, 10, -30, 10, 9),
            (60, 10, 30, 10, -1), (60, 10, 30, 10.5, 9),
            (float("nan"), 10, 30, 10, 9),
        ]
        for args in cases:
            with self.subTest(args=args), self.assertRaises(ValueError):
                calculate_oee(*args)


if __name__ == "__main__":
    unittest.main()
