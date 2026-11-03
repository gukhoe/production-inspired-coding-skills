import unittest

from production import calculate_production


class ProductionTests(unittest.TestCase):
    def test_provided_shortage_example(self):
        self.assertEqual(
            calculate_production(450, 20, 9200),
            {"total_production": 9000, "shortage": 200, "surplus": 0},
        )

    def test_surplus(self):
        self.assertEqual(
            calculate_production(450, 20, 8800),
            {"total_production": 9000, "shortage": 0, "surplus": 200},
        )

    def test_matching_demand(self):
        self.assertEqual(
            calculate_production(450, 20, 9000),
            {"total_production": 9000, "shortage": 0, "surplus": 0},
        )

    def test_no_working_days(self):
        self.assertEqual(
            calculate_production(450, 0, 9200),
            {"total_production": 0, "shortage": 9200, "surplus": 0},
        )


if __name__ == "__main__":
    unittest.main()
