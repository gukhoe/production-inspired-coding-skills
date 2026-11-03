"""공급사의 항목별 점수에 가중치를 곱해 내림차순으로 정렬한다."""

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
    """큰 점수가 우수하며 동점이면 입력 순서를 유지한다."""
    results = []
    for supplier in data["suppliers"]:
        score = sum(
            (Decimal(str(supplier[key])) * Decimal(str(weight))
             for key, weight in data["weights"].items()),
            Decimal("0"),
        )
        results.append({"name": supplier["name"], "score": score})
    return sorted(results, key=lambda item: item["score"], reverse=True)


def main():
    print("순위 | 공급사 | 가중합 점수")
    previous_score = None
    rank = 0
    for position, supplier in enumerate(rank_suppliers(INPUT), start=1):
        if supplier["score"] != previous_score:
            rank = position
        print(f"{rank} | {supplier['name']} | {supplier['score']:.1f}")
        previous_score = supplier["score"]


if __name__ == "__main__":
    main()
