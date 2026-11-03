"""Calculate an invoice's unpaid balance after partial payments."""

from decimal import Decimal


def unpaid_balance(invoice_total, payments):
    """Subtract payments exactly; a negative balance represents overpayment."""
    total = Decimal(str(invoice_total))
    paid = sum((Decimal(str(payment)) for payment in payments), Decimal("0"))
    return total - paid


if __name__ == "__main__":
    data = {"invoice_total": 12500, "payments": [2000, 3500, 1000]}
    balance = unpaid_balance(data["invoice_total"], data["payments"])
    print(f"미지급 잔액: {balance}")
