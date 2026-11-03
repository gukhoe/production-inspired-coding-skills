import unittest

from oee import EXAMPLE, calculate_oee


class OeeTests(unittest.TestCase):
    def test_supplied_input(self):
        actual = calculate_oee(**EXAMPLE)
        expected = {
            "Availability": 0.875,
            "Performance": 19 / 21,
            "Quality": 147 / 152,
            "OEE": 0.765625,
        }
        for name, value in expected.items():
            self.assertAlmostEqual(actual[name], value)

    def test_perfect_production(self):
        result = calculate_oee(60, 60, 30, 120, 120)
        self.assertEqual(result, dict.fromkeys(result, 1.0))

    def test_units_and_combined_loss(self):
        result = calculate_oee(120, 60, 15, 120, 60)
        self.assertEqual(result, {
            "Availability": 0.5, "Performance": 0.5,
            "Quality": 0.5, "OEE": 0.125,
        })

    def test_no_good_units(self):
        result = calculate_oee(**{**EXAMPLE, "good_units": 0})
        self.assertEqual(result["Quality"], 0)
        self.assertEqual(result["OEE"], 0)

    def test_invalid_inputs(self):
        for override in (
            {"planned_minutes": 0}, {"run_minutes": 0},
            {"total_units": 0}, {"good_units": 761},
            {"good_units": -1}, {"total_units": 1.5},
            {"run_minutes": 481}, {"ideal_cycle_seconds": -1},
            {"planned_minutes": float("nan")},
            {"run_minutes": float("inf")}, {"good_units": True},
        ):
            with self.subTest(override=override):
                with self.assertRaises(ValueError):
                    calculate_oee(**{**EXAMPLE, **override})


if __name__ == "__main__":
    unittest.main()
