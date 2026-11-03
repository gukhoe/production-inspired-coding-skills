"""인보이스 총액에서 부분 지급액의 합계를 빼 미지급 잔액을 계산한다."""

from decimal import Decimal


def outstanding_balance(invoice_total, payments):
    """금액을 십진수로 계산하며, 초과 지급은 음수 잔액으로 표시한다."""
    total = Decimal(str(invoice_total))
    paid = sum((Decimal(str(payment)) for payment in payments), Decimal("0"))
    return total - paid


def main():
    data = {"invoice_total": 12500, "payments": [2000, 3500, 1000]}
    balance = outstanding_balance(data["invoice_total"], data["payments"])
    total = Decimal(str(data["invoice_total"]))
    print(f"인보이스 청구액: {total:,.0f}")
    print(f"지급액 합계: {total - balance:,.0f}")
    print(f"미지급 잔액: {balance:,.0f}")


if __name__ == "__main__":
    main()
