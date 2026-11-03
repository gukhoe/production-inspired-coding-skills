"""입출고 기록으로 최종 재고를 계산합니다."""


def calculate_inventory(opening, receipts, issues):
    """최종 재고 = 기초 재고 + 입고 합계 - 출고 합계."""
    return opening + sum(receipts) - sum(issues)


def main():
    records = {"opening": 120, "receipts": [30, 20], "issues": [45, 25]}
    final_inventory = calculate_inventory(**records)
    print(f"최종 재고: {final_inventory}")


if __name__ == "__main__":
    main()
