import json
import unittest
from decimal import Decimal
from pathlib import Path
from supplier_cost import compare_costs


class CostTests(unittest.TestCase):
    def test_provided_example(self):
        data = json.loads(Path(__file__).with_name("input.json").read_text())
        totals, winners, lowest = compare_costs(data)
        self.assertEqual(dict(totals), {"Alpha": Decimal("52000"), "Beta": Decimal("50500"), "Gamma": Decimal("50300")})
        self.assertEqual(winners, ["Gamma"])
        self.assertEqual(lowest, Decimal("50300"))

    def test_tie_and_decimal_arithmetic(self):
        data = {"annual_qty": 3, "suppliers": [
            {"name": "A", "unit_price": 0.1, "freight": 0, "tooling": 0},
            {"name": "B", "unit_price": 0, "freight": 0.3, "tooling": 0},
        ]}
        _, winners, lowest = compare_costs(data)
        self.assertEqual(winners, ["A", "B"])
        self.assertEqual(lowest, Decimal("0.3"))

    def test_zero_quantity_retains_fixed_costs(self):
        totals, _, _ = compare_costs({"annual_qty": 0, "suppliers": [
            {"name": "A", "unit_price": 5, "freight": 100, "tooling": 200}
        ]})
        self.assertEqual(totals, [("A", Decimal("300"))])


if __name__ == "__main__":
    unittest.main()
