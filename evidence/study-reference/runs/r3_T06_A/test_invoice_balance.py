import unittest
from decimal import Decimal

from invoice_balance import outstanding_balance


class InvoiceBalanceTests(unittest.TestCase):
    def test_provided_input(self):
        self.assertEqual(outstanding_balance(12500, [2000, 3500, 1000]), Decimal("6000"))

    def test_no_payments(self):
        self.assertEqual(outstanding_balance(12500, []), Decimal("12500"))

    def test_fully_paid(self):
        self.assertEqual(outstanding_balance(100, [40, 60]), Decimal("0"))

    def test_decimal_amounts(self):
        self.assertEqual(outstanding_balance("0.30", ["0.10", "0.20"]), Decimal("0"))

    def test_overpayment(self):
        self.assertEqual(outstanding_balance(100, [120]), Decimal("-20"))


if __name__ == "__main__":
    unittest.main()
