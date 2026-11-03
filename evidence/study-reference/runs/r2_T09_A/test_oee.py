import unittest

from oee import calculate_oee


class OeeTests(unittest.TestCase):
    def test_provided_example(self):
        result = calculate_oee(480, 420, 30, 760, 735)
        self.assertAlmostEqual(result["Availability"], 0.875)
        self.assertAlmostEqual(result["Performance"], 0.9047619047619048)
        self.assertAlmostEqual(result["Quality"], 0.9671052631578947)
        self.assertAlmostEqual(result["OEE"], 0.765625)

    def test_perfect_production(self):
        self.assertEqual(calculate_oee(60, 60, 30, 120, 120), {
            "Availability": 1, "Performance": 1, "Quality": 1, "OEE": 1,
        })

    def test_no_good_units(self):
        result = calculate_oee(60, 60, 30, 120, 0)
        self.assertEqual(result["Quality"], 0)
        self.assertEqual(result["OEE"], 0)

    def test_invalid_inputs(self):
        for values in [
            (0, 420, 30, 760, 735),
            (480, 0, 30, 760, 735),
            (480, 420, 30, 0, 0),
            (480, 481, 30, 760, 735),
            (480, 420, -30, 760, 735),
            (480, 420, 30, 760, 761),
            (480, 420, 30, 760, -1),
            (480, float("nan"), 30, 760, 735),
        ]:
            with self.subTest(values=values):
                with self.assertRaises(ValueError):
                    calculate_oee(*values)


if __name__ == "__main__":
    unittest.main()
