"""입출고 기록을 합산해 최종 재고를 계산합니다."""


def final_inventory(opening, receipts, issues):
    """기초 재고 + 총입고 - 총출고를 반환합니다."""
    return opening + sum(receipts) - sum(issues)


if __name__ == '__main__':
    records = {"opening": 120, "receipts": [30, 20], "issues": [45, 25]}
    print(f"최종 재고: {final_inventory(**records)}")
