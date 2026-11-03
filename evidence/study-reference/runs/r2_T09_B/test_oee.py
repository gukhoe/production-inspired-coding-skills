import unittest

from oee import calculate_oee


class OEETests(unittest.TestCase):
    def test_provided_input(self):
        result = calculate_oee(480, 420, 30, 760, 735)
        self.assertAlmostEqual(result["Availability"], 0.875)
        self.assertAlmostEqual(result["Performance"], 19 / 21)
        self.assertAlmostEqual(result["Quality"], 147 / 152)
        self.assertAlmostEqual(result["OEE"], 0.765625)
        # Independent identity: ideal time for good units / planned time.
        self.assertAlmostEqual(result["OEE"], 735 * 30 / (480 * 60))

    def test_perfect_production(self):
        self.assertEqual(calculate_oee(60, 60, 30, 120, 120),
                         dict(Availability=1, Performance=1, Quality=1, OEE=1))

    def test_all_rejected(self):
        self.assertEqual(calculate_oee(60, 60, 30, 120, 0)["OEE"], 0)

    def test_invalid_denominators_and_counts(self):
        for args in [(0, 0, 30, 10, 10), (60, 0, 30, 10, 10),
                     (60, 61, 30, 10, 10), (60, 60, 0, 10, 10),
                     (60, 60, 30, 0, 0), (60, 60, 30, 10, 11),
                     (60, 60, 30, 10, -1)]:
            with self.subTest(args=args), self.assertRaises(ValueError):
                calculate_oee(*args)


if __name__ == "__main__":
    unittest.main()
