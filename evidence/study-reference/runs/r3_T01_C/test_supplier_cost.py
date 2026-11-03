import unittest
from decimal import Decimal

from supplier_cost import INPUT, compare_suppliers


class SupplierCostTests(unittest.TestCase):
    def test_provided_input(self):
        totals, winners = compare_suppliers(INPUT)
        self.assertEqual(totals, [
            ("Alpha", Decimal("52000")),
            ("Beta", Decimal("50500")),
            ("Gamma", Decimal("50300")),
        ])
        self.assertEqual(winners, ["Gamma"])

    def test_fees_can_outweigh_unit_price(self):
        totals, winners = compare_suppliers({
            "annual_qty": 10,
            "suppliers": [
                {"name": "A", "unit_price": 1, "freight": 5, "tooling": 10},
                {"name": "B", "unit_price": 2, "freight": 0, "tooling": 0},
            ],
        })
        self.assertEqual(totals, [("A", Decimal("25")), ("B", Decimal("20"))])
        self.assertEqual(winners, ["B"])

    def test_decimal_tie(self):
        _, winners = compare_suppliers({
            "annual_qty": 3,
            "suppliers": [
                {"name": "A", "unit_price": 0.1, "freight": 0.2, "tooling": 0},
                {"name": "B", "unit_price": 0, "freight": 0, "tooling": 0.5},
            ],
        })
        self.assertEqual(winners, ["A", "B"])


if __name__ == "__main__":
    unittest.main()
