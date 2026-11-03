"""공급사 점수의 가중합을 계산해 높은 점수부터 정렬합니다."""
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
    """Return (name, weighted score) pairs; equal scores retain input order.

    All criteria are scores where higher is better, including price.
    Weights are used as supplied, without automatic normalization.
    Decimal avoids binary floating-point artifacts in the weighted sum.
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
    return sorted(results, key=lambda result: result[1], reverse=True)


def main():
    print("순위 | 공급사 | 가중합 점수")
    for rank, (name, score) in enumerate(rank_suppliers(INPUT), start=1):
        print(f"{rank} | {name} | {score:.2f}")


if __name__ == "__main__":
    main()
