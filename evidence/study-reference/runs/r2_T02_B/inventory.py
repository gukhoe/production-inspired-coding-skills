"""입출고 기록으로 최종 재고를 계산합니다."""


def calculate_inventory(opening, receipts, issues):
    """기초 재고 + 총 입고량 - 총 출고량을 반환합니다."""
    return opening + sum(receipts) - sum(issues)


if __name__ == "__main__":
    records = {"opening": 120, "receipts": [30, 20], "issues": [45, 25]}
    result = calculate_inventory(**records)
    print(f"최종 재고: {result}")
