"""입출고 기록을 이용해 최종 재고를 계산합니다."""


def calculate_inventory(opening, receipts, issues):
    """기초 재고 + 총 입고 - 총 출고를 반환합니다."""
    return opening + sum(receipts) - sum(issues)


if __name__ == "__main__":
    data = {"opening": 120, "receipts": [30, 20], "issues": [45, 25]}
    final_inventory = calculate_inventory(**data)
    print(f"최종 재고: {final_inventory}")
