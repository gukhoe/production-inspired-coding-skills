"""Calculate an invoice's remaining balance using exact decimal amounts."""
from decimal import Decimal


def calculate_balance(invoice_total, payments):
    """Return total paid and remaining balance; a negative balance is a credit."""
    total = Decimal(str(invoice_total))
    total_paid = sum((Decimal(str(payment)) for payment in payments), Decimal('0'))
    return total_paid, total - total_paid


def main():
    invoice = {"invoice_total": 12500, "payments": [2000, 3500, 1000]}
    paid, balance = calculate_balance(invoice["invoice_total"], invoice["payments"])
    print(f"청구액: {invoice['invoice_total']:,}")
    print(f"총 지급액: {paid:,}")
    print(f"미지급 잔액: {balance:,}")


if __name__ == '__main__':
    main()
