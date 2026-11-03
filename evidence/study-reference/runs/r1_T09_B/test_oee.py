import unittest

from oee import calculate_oee


class OeeTests(unittest.TestCase):
    def test_provided_input(self):
        result = calculate_oee(480, 420, 30, 760, 735)
        self.assertAlmostEqual(result["Availability"], 0.875)
        self.assertAlmostEqual(result["Performance"], 19 / 21)
        self.assertAlmostEqual(result["Quality"], 147 / 152)
        self.assertAlmostEqual(result["OEE"], 0.765625)
        # Independent identity: good production's ideal time / planned time.
        self.assertAlmostEqual(result["OEE"], (735 * 30) / (480 * 60))

    def test_perfect_production(self):
        self.assertEqual(calculate_oee(60, 60, 60, 60, 60), {
            "Availability": 1, "Performance": 1, "Quality": 1, "OEE": 1,
        })

    def test_all_units_rejected(self):
        result = calculate_oee(60, 30, 60, 30, 0)
        self.assertEqual(result["Quality"], 0)
        self.assertEqual(result["OEE"], 0)

    def test_invalid_inputs(self):
        for args in (
            (0, 30, 60, 30, 30),
            (60, 0, 60, 30, 30),
            (60, 30, 60, 0, 0),
            (60, 70, 60, 30, 30),
            (60, 30, 60, 30, 31),
            (60, 30, float("nan"), 30, 30),
        ):
            with self.subTest(args=args), self.assertRaises(ValueError):
                calculate_oee(*args)


if __name__ == "__main__":
    unittest.main()
