"""인보이스 청구액에서 부분 지급액 합계를 빼서 미지급 잔액을 계산한다."""


def unpaid_balance(invoice_total, payments):
    """청구액과 지급액 목록을 받아 잔액을 반환한다."""
    return invoice_total - sum(payments)


def main():
    invoice_total = 12500
    payments = [2000, 3500, 1000]
    print(f"인보이스 청구액: {invoice_total}")
    print(f"총 지급액: {sum(payments)}")
    print(f"미지급 잔액: {unpaid_balance(invoice_total, payments)}")


if __name__ == "__main__":
    main()
