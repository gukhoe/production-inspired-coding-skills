import unittest
from decimal import Decimal

from invoice_balance import unpaid_balance


class InvoiceBalanceTests(unittest.TestCase):
    def test_provided_input(self):
        self.assertEqual(unpaid_balance(12500, [2000, 3500, 1000]), Decimal("6000"))

    def test_no_payments(self):
        self.assertEqual(unpaid_balance(12500, []), Decimal("12500"))

    def test_paid_in_full(self):
        self.assertEqual(unpaid_balance(100, [40, 60]), Decimal("0"))

    def test_overpayment_is_credit(self):
        self.assertEqual(unpaid_balance(100, [110]), Decimal("-10"))

    def test_decimal_amounts(self):
        self.assertEqual(unpaid_balance("0.30", ["0.10", "0.20"]), Decimal("0.00"))


if __name__ == "__main__":
    unittest.main()
