import json
import unittest
from decimal import Decimal
from bom_cost import EXAMPLE_JSON, calculate_bom


class BomCostTests(unittest.TestCase):
    def test_provided_input(self):
        rows, total = calculate_bom(json.loads(EXAMPLE_JSON))
        self.assertEqual([row[3] for row in rows],
                         [Decimal('14.5'), Decimal('2.10'), Decimal('2.50')])
        self.assertEqual(total, Decimal('19.10'))

    def test_empty_bom(self):
        self.assertEqual(calculate_bom({'parts': []}), ([], Decimal('0')))

    def test_decimal_precision(self):
        _, total = calculate_bom({'parts': [{'part': 'A', 'qty': 3, 'unit_price': 0.1}]})
        self.assertEqual(total, Decimal('0.3'))

    def test_negative_value_rejected(self):
        with self.assertRaises(ValueError):
            calculate_bom({'parts': [{'part': 'A', 'qty': -1, 'unit_price': 1}]})


if __name__ == '__main__':
    unittest.main()
