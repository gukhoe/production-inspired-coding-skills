"""인보이스 청구액에서 부분 지급액 합계를 차감한다."""

from decimal import Decimal


def calculate_balance(invoice_total, payments):
    """(지급액 합계, 잔액)를 반환한다. 음수 잔액은 초과 지급액이다."""
    total = Decimal(str(invoice_total))
    paid = sum((Decimal(str(payment)) for payment in payments), Decimal("0"))
    return paid, total - paid


def main():
    data = {"invoice_total": 12500, "payments": [2000, 3500, 1000]}
    paid, balance = calculate_balance(data["invoice_total"], data["payments"])
    print(f"인보이스 청구액: {data['invoice_total']:,}")
    print(f"지급액 합계: {paid:,}")
    print(f"미지급 잔액: {balance:,}")


if __name__ == "__main__":
    main()
