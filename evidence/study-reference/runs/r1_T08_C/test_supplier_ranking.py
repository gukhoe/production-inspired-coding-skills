import unittest
from decimal import Decimal
from supplier_ranking import INPUT, rank_suppliers


class SupplierRankingTests(unittest.TestCase):
    def test_provided_input(self):
        self.assertEqual(
            rank_suppliers(INPUT),
            [("B", Decimal("88.2")), ("C", Decimal("86.7")), ("A", Decimal("86.0"))],
        )

    def test_quality_only_weights(self):
        data = {
            "weights": {"price": 0, "quality": 1, "delivery": 0},
            "suppliers": INPUT["suppliers"],
        }
        self.assertEqual(
            rank_suppliers(data),
            [("C", Decimal("94")), ("A", Decimal("90")), ("B", Decimal("82"))],
        )


if __name__ == "__main__":
    unittest.main()
