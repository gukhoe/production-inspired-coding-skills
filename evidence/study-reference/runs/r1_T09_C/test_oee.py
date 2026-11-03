import unittest

from oee import calculate_oee


class OEETests(unittest.TestCase):
    def test_requested_example(self):
        result = calculate_oee(480, 420, 30, 760, 735)
        self.assertAlmostEqual(result["availability"], 0.875)
        self.assertAlmostEqual(result["performance"], 19 / 21)
        self.assertAlmostEqual(result["quality"], 147 / 152)
        self.assertAlmostEqual(result["oee"], 0.765625)

    def test_perfect_production_and_seconds_conversion(self):
        self.assertEqual(calculate_oee(60, 60, 30, 120, 120),
                         dict(availability=1, performance=1, quality=1, oee=1))

    def test_no_good_units(self):
        self.assertEqual(calculate_oee(60, 60, 30, 120, 0)["oee"], 0)

    def test_invalid_inputs(self):
        for inputs in ((0, 420, 30, 760, 735), (480, 0, 30, 760, 735),
                       (480, 420, 30, 0, 0), (480, 420, 30, 760, 761),
                       (480, 481, 30, 760, 735),
                       (480, 420, float("nan"), 760, 735)):
            with self.subTest(inputs=inputs):
                with self.assertRaises(ValueError):
                    calculate_oee(*inputs)


if __name__ == "__main__":
    unittest.main()
