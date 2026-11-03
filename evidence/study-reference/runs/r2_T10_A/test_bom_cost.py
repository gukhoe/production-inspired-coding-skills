import unittest
from decimal import Decimal

from bom_cost import calculate_bom


class BomCostTests(unittest.TestCase):
    def test_provided_input(self):
        rows, total = calculate_bom([
            {"part": "Housing", "qty": 1, "unit_price": 14.5},
            {"part": "Clip", "qty": 6, "unit_price": 0.35},
            {"part": "Seal", "qty": 2, "unit_price": 1.25},
        ])
        self.assertEqual([row[3] for row in rows],
                         [Decimal("14.50"), Decimal("2.10"), Decimal("2.50")])
        self.assertEqual(total, Decimal("19.10"))

    def test_decimal_precision(self):
        _, total = calculate_bom([{"part": "A", "qty": 3, "unit_price": 0.1}])
        self.assertEqual(total, Decimal("0.3"))

    def test_empty_bom(self):
        self.assertEqual(calculate_bom([]), ([], Decimal("0")))

    def test_invalid_amounts(self):
        for field in ("qty", "unit_price"):
            for value in (-1, "NaN", "Infinity"):
                part = {"part": "A", "qty": 1, "unit_price": 1}
                part[field] = value
                with self.subTest(field=field, value=value):
                    with self.assertRaises(ValueError):
                        calculate_bom([part])


if __name__ == "__main__":
    unittest.main()
