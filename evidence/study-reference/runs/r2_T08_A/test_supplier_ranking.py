import unittest
from decimal import Decimal
from supplier_ranking import INPUT, rank_suppliers


class RankingTests(unittest.TestCase):
    def test_provided_input(self):
        self.assertEqual(rank_suppliers(INPUT), [
            {"name": "B", "score": Decimal("88.2")},
            {"name": "C", "score": Decimal("86.7")},
            {"name": "A", "score": Decimal("86.0")},
        ])

    def test_quality_only(self):
        data = {"weights": {"price": 0, "quality": 1, "delivery": 0},
                "suppliers": INPUT["suppliers"]}
        self.assertEqual(rank_suppliers(data), [
            {"name": "C", "score": Decimal("94")},
            {"name": "A", "score": Decimal("90")},
            {"name": "B", "score": Decimal("82")},
        ])


if __name__ == "__main__":
    unittest.main()
