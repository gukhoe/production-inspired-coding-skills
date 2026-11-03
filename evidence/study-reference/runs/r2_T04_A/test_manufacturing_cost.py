import unittest
from decimal import Decimal
from manufacturing_cost import calculate_cost


class ManufacturingCostTests(unittest.TestCase):
    def test_provided_inputs(self):
        self.assertEqual(calculate_cost(12.5, 4.2, 3.3, 1000),
                         (Decimal("20.0"), Decimal("20000.0")))

    def test_decimal_precision(self):
        self.assertEqual(calculate_cost(0.1, 0.2, 0, 3),
                         (Decimal("0.3"), Decimal("0.9")))

    def test_zero_quantity(self):
        self.assertEqual(calculate_cost(12.5, 4.2, 3.3, 0),
                         (Decimal("20.0"), Decimal("0")))

    def test_invalid_quantity(self):
        for quantity in (-1, 1.5, True):
            with self.subTest(quantity=quantity), self.assertRaises(ValueError):
                calculate_cost(1, 2, 3, quantity)

    def test_invalid_cost(self):
        for cost in (-1, "NaN", "Infinity"):
            with self.subTest(cost=cost), self.assertRaises(ValueError):
                calculate_cost(cost, 2, 3, 1)


if __name__ == "__main__":
    unittest.main()
