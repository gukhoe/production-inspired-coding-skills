"""입출고 기록으로 최종 재고를 계산합니다."""


def final_inventory(opening, receipts, issues):
    """기초 재고 + 입고 합계 - 출고 합계를 반환합니다."""
    return opening + sum(receipts) - sum(issues)


def main():
    records = {"opening": 120, "receipts": [30, 20], "issues": [45, 25]}
    result = final_inventory(**records)
    print(f"기초 재고: {records['opening']}")
    print(f"입고 합계: {sum(records['receipts'])}")
    print(f"출고 합계: {sum(records['issues'])}")
    print(f"최종 재고: {result}")


if __name__ == "__main__":
    main()
