import unittest

from oee import calculate_oee


class OeeTests(unittest.TestCase):
    def test_supplied_example(self):
        result = calculate_oee(480, 420, 30, 760, 735)
        expected = {
            "Availability": 0.875,
            "Performance": 19 / 21,
            "Quality": 147 / 152,
            "OEE": 0.765625,
        }
        for key, value in expected.items():
            with self.subTest(metric=key):
                self.assertAlmostEqual(result[key], value)

    def test_perfect_production(self):
        self.assertEqual(calculate_oee(60, 60, 60, 60, 60), {
            "Availability": 1, "Performance": 1, "Quality": 1, "OEE": 1,
        })

    def test_no_good_units(self):
        self.assertEqual(calculate_oee(60, 60, 60, 60, 0)["OEE"], 0)

    def test_undefined_denominator(self):
        with self.assertRaises(ValueError):
            calculate_oee(480, 0, 30, 760, 735)


if __name__ == "__main__":
    unittest.main()
