import unittest
from decimal import Decimal
from manufacturing_cost import calculate_cost


class ManufacturingCostTests(unittest.TestCase):
    def test_provided_input(self):
        self.assertEqual(
            calculate_cost(12.5, 4.2, 3.3, 1000),
            (Decimal("20.0"), Decimal("20000.0")),
        )

    def test_decimal_precision(self):
        self.assertEqual(
            calculate_cost(0.1, 0.2, 0.3, 3),
            (Decimal("0.6"), Decimal("1.8")),
        )

    def test_zero_quantity_preserves_unit_cost(self):
        self.assertEqual(
            calculate_cost(12.5, 4.2, 3.3, 0),
            (Decimal("20.0"), Decimal("0")),
        )


if __name__ == "__main__":
    unittest.main()
