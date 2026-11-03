"""공급사별 점수의 가중합을 계산하고 내림차순으로 정렬한다."""
from decimal import Decimal


INPUT = {
    "weights": {"price": 0.5, "quality": 0.3, "delivery": 0.2},
    "suppliers": [
        {"name": "A", "price": 80, "quality": 90, "delivery": 95},
        {"name": "B", "price": 92, "quality": 82, "delivery": 88},
        {"name": "C", "price": 85, "quality": 94, "delivery": 80},
    ],
}


def rank_suppliers(data):
    """모든 항목은 높을수록 좋은 점수다. 동점이면 입력 순서를 유지한다."""
    scores = [
        {
            "name": supplier["name"],
            "score": sum(
                (Decimal(str(supplier[key])) * Decimal(str(weight))
                 for key, weight in data["weights"].items()),
                Decimal("0"),
            ),
        }
        for supplier in data["suppliers"]
    ]
    return sorted(scores, key=lambda row: row["score"], reverse=True)


def main():
    for position, row in enumerate(rank_suppliers(INPUT), start=1):
        print(f"{position}위: {row['name']} — {row['score']:.1f}점")


if __name__ == "__main__":
    main()
