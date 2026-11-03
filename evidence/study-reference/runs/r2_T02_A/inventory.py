"""입출고 기록으로 최종 재고를 계산합니다."""


def final_inventory(opening, receipts, issues):
    """기초 재고 + 총 입고 - 총 출고를 반환합니다."""
    return opening + sum(receipts) - sum(issues)


if __name__ == "__main__":
    data = {"opening": 120, "receipts": [30, 20], "issues": [45, 25]}
    result = final_inventory(**data)
    print(f"최종 재고: {result}")
