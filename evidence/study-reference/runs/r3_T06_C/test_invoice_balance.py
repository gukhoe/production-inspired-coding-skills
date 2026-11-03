import unittest
from decimal import Decimal

from invoice_balance import calculate_balance


class InvoiceBalanceTests(unittest.TestCase):
    def test_provided_input(self):
        self.assertEqual(calculate_balance(12500, [2000, 3500, 1000]), Decimal("6000"))

    def test_no_payments(self):
        self.assertEqual(calculate_balance(12500, []), Decimal("12500"))

    def test_fully_paid(self):
        self.assertEqual(calculate_balance(12500, [5000, 7500]), Decimal("0"))

    def test_decimal_amounts(self):
        self.assertEqual(calculate_balance(0.3, [0.1, 0.2]), Decimal("0"))


if __name__ == "__main__":
    unittest.main()
