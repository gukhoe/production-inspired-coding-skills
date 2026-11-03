import unittest
from decimal import Decimal
from supplier_costs import INPUT, compare_suppliers


class SupplierCostTests(unittest.TestCase):
    def test_provided_input(self):
        costs, winners, lowest = compare_suppliers(**INPUT)
        self.assertEqual(costs, [
            ("Alpha", Decimal("52000")),
            ("Beta", Decimal("50500")),
            ("Gamma", Decimal("50300")),
        ])
        self.assertEqual(winners, ["Gamma"])
        self.assertEqual(lowest, Decimal("50300"))

    def test_fixed_costs_change_winner_at_small_quantity(self):
        _, winners, lowest = compare_suppliers(100, INPUT["suppliers"])
        self.assertEqual(winners, ["Beta"])
        self.assertEqual(lowest, Decimal("1000"))

    def test_exact_decimal_tie(self):
        costs, winners, lowest = compare_suppliers(3, [
            {"name": "A", "unit_price": 0.1, "freight": 0.2, "tooling": 0},
            {"name": "B", "unit_price": 0, "freight": 0, "tooling": 0.5},
        ])
        self.assertEqual(winners, ["A", "B"])
        self.assertEqual(lowest, Decimal("0.5"))

    def test_empty_suppliers(self):
        with self.assertRaises(ValueError):
            compare_suppliers(100, [])


if __name__ == "__main__":
    unittest.main()
