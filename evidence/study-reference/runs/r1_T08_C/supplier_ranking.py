"""Rank supplier scores by their weighted sum (higher is better)."""
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
    """Return (name, score) pairs in descending score order.

    Price is already a score, not a monetary cost. Weights are used as
    supplied. Equal totals preserve the input order.
    """
    weights = {key: Decimal(str(value)) for key, value in data["weights"].items()}
    results = [
        (
            supplier["name"],
            sum(
                (Decimal(str(supplier[key])) * weight for key, weight in weights.items()),
                Decimal("0"),
            ),
        )
        for supplier in data["suppliers"]
    ]
    return sorted(results, key=lambda item: item[1], reverse=True)


def main():
    print("순위 | 공급사 | 가중합 점수")
    for rank, (name, score) in enumerate(rank_suppliers(INPUT), start=1):
        print(f"{rank} | {name} | {score:.1f}")


if __name__ == "__main__":
    main()
