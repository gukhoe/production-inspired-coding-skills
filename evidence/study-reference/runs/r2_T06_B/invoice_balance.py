"""Calculate the signed unpaid balance of an invoice using decimal arithmetic."""

import json
import sys
from decimal import Decimal


def calculate_balance(invoice_total, payments):
    """Return total paid and balance; a negative balance denotes overpayment."""
    total_paid = sum((Decimal(str(payment)) for payment in payments), Decimal("0"))
    return total_paid, Decimal(str(invoice_total)) - total_paid


def main():
    raw = sys.argv[1] if len(sys.argv) > 1 else '{"invoice_total":12500,"payments":[2000,3500,1000]}'
    data = json.loads(raw, parse_float=Decimal)
    paid, balance = calculate_balance(data["invoice_total"], data["payments"])
    print(f"청구액: {data['invoice_total']:f}" if isinstance(data['invoice_total'], Decimal)
          else f"청구액: {data['invoice_total']}")
    print(f"지급액 합계: {paid:f}")
    print(f"미지급 잔액: {balance:f}")


if __name__ == "__main__":
    main()
