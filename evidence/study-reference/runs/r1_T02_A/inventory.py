"""입출고 기록으로 최종 재고를 계산합니다."""


def final_inventory(opening, receipts, issues):
    """기초 재고에 총 입고를 더하고 총 출고를 뺍니다."""
    return opening + sum(receipts) - sum(issues)


def main():
    data = {"opening": 120, "receipts": [30, 20], "issues": [45, 25]}
    result = final_inventory(**data)
    print(f"기초 재고: {data['opening']}")
    print(f"총 입고: {sum(data['receipts'])}")
    print(f"총 출고: {sum(data['issues'])}")
    print(f"최종 재고: {result}")


if __name__ == "__main__":
    main()
