"""Rank suppliers by the weighted sum of their price, quality and delivery scores."""
from decimal import Decimal


EXAMPLE = {
    "weights": {"price": 0.5, "quality": 0.3, "delivery": 0.2},
    "suppliers": [
        {"name": "A", "price": 80, "quality": 90, "delivery": 95},
        {"name": "B", "price": 92, "quality": 82, "delivery": 88},
        {"name": "C", "price": 85, "quality": 94, "delivery": 80},
    ],
}


def rank_suppliers(weights, suppliers):
    """Return (name, score) pairs, highest score first; retain input order on ties."""
    criteria = ("price", "quality", "delivery")
    results = []
    for supplier in suppliers:
        total = sum(
            (Decimal(str(weights[key])) * Decimal(str(supplier[key]))
             for key in criteria),
            Decimal("0"),
        )
        results.append((supplier["name"], total))
    return sorted(results, key=lambda item: item[1], reverse=True)


def main():
    print("순위 | 공급사 | 가중합 점수")
    for position, (name, score) in enumerate(
        rank_suppliers(EXAMPLE["weights"], EXAMPLE["suppliers"]), start=1
    ):
        print(f"{position} | {name} | {score}")


if __name__ == "__main__":
    main()
