"""Calculate invoice total minus the sum of partial payments.

Inputs are numeric amounts; output is the signed remaining balance as Decimal.
Acceptance example: 12500 - (2000 + 3500 + 1000) == 6000.
Currency conversion, interest, fees, and payment persistence are out of scope.
"""

from decimal import Decimal


def calculate_balance(invoice_total, payments):
    """Return the unpaid balance using decimal monetary arithmetic."""
    total = Decimal(str(invoice_total))
    paid = sum((Decimal(str(payment)) for payment in payments), Decimal("0"))
    return total - paid


def main():
    data = {"invoice_total": 12500, "payments": [2000, 3500, 1000]}
    balance = calculate_balance(data["invoice_total"], data["payments"])
    paid = Decimal(str(data["invoice_total"])) - balance
    print(f"인보이스 청구액: {data['invoice_total']:,}")
    print(f"총 지급액: {paid:,}")
    print(f"미지급 잔액: {balance:,}")


if __name__ == "__main__":
    main()
