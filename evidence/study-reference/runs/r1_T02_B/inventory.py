"""입출고 기록으로 최종 재고를 계산한다."""


def calculate_inventory(opening, receipts, issues):
    """기초 재고 + 총 입고량 - 총 출고량을 반환한다."""
    return opening + sum(receipts) - sum(issues)


def main():
    records = {"opening": 120, "receipts": [30, 20], "issues": [45, 25]}
    final_inventory = calculate_inventory(**records)
    print(f"최종 재고: {final_inventory}")


if __name__ == "__main__":
    main()
