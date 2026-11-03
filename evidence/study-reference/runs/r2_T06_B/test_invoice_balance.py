import unittest
from decimal import Decimal

from invoice_balance import calculate_balance


class InvoiceBalanceTests(unittest.TestCase):
    def test_provided_payments(self):
        self.assertEqual(calculate_balance(12500, [2000, 3500, 1000]), (6500, 6000))

    def test_no_payments(self):
        self.assertEqual(calculate_balance(12500, []), (0, 12500))

    def test_decimal_payments_exactly_settle_invoice(self):
        self.assertEqual(calculate_balance("0.30", ["0.10", "0.20"]),
                         (Decimal("0.30"), Decimal("0.00")))

    def test_overpayment_is_credit(self):
        self.assertEqual(calculate_balance(100, [120]), (120, -20))


if __name__ == "__main__":
    unittest.main()
