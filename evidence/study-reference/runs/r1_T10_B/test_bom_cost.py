from decimal import Decimal
import unittest

from bom_cost import INPUT_DATA, bom_cost, part_cost


class BomCostTests(unittest.TestCase):
    def test_provided_input(self):
        self.assertEqual(
            [part_cost(part) for part in INPUT_DATA["parts"]],
            [Decimal("14.50"), Decimal("2.10"), Decimal("2.50")],
        )
        self.assertEqual(bom_cost(INPUT_DATA), Decimal("19.10"))

    def test_decimal_precision(self):
        data = {"parts": [{"part": "A", "qty": 3, "unit_price": 0.1}]}
        self.assertEqual(bom_cost(data), Decimal("0.3"))

    def test_empty_bom(self):
        self.assertEqual(bom_cost({"parts": []}), Decimal("0"))


if __name__ == "__main__":
    unittest.main()
