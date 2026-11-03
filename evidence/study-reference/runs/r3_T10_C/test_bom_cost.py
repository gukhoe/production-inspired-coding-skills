import json
import unittest
from decimal import Decimal

from bom_cost import EXAMPLE_INPUT, calculate_bom


class BomCostTests(unittest.TestCase):
    def test_provided_input(self):
        rows, total = calculate_bom(json.loads(EXAMPLE_INPUT, parse_float=Decimal))
        self.assertEqual([row[3] for row in rows],
                         [Decimal("14.50"), Decimal("2.10"), Decimal("2.50")])
        self.assertEqual(total, Decimal("19.10"))

    def test_decimal_arithmetic(self):
        _, total = calculate_bom({"parts": [
            {"part": "A", "qty": 3, "unit_price": 0.1},
            {"part": "B", "qty": 7, "unit_price": 0.2},
        ]})
        self.assertEqual(total, Decimal("1.7"))


if __name__ == "__main__":
    unittest.main()
