"""청구액에서 지급액 합계를 빼서 미지급 잔액을 계산한다.

입력: 청구액과 지급액 목록. 출력: Decimal 잔액.
범위: 단순 잔액 계산만 수행하며 세금, 이자, 환율은 계산하지 않는다.
"""
from decimal import Decimal


def unpaid_balance(invoice_total, payments):
    """금액을 십진수로 계산해 소수 금액의 이진 부동소수점 오차를 피한다."""
    total = Decimal(str(invoice_total))
    paid = sum((Decimal(str(payment)) for payment in payments), Decimal("0"))
    return total - paid


def main():
    data = {"invoice_total": 12500, "payments": [2000, 3500, 1000]}
    balance = unpaid_balance(data["invoice_total"], data["payments"])
    print(f"청구액: {data['invoice_total']:,}원")
    print(f"총 지급액: {sum(data['payments']):,}원")
    print(f"미지급 잔액: {balance:,}원")


if __name__ == "__main__":
    main()
