"""Compare annual purchase costs; freight and tooling are annual total charges."""

from decimal import Decimal


INPUT = {
    "annual_qty": 10000,
    "suppliers": [
        {"name": "Alpha", "unit_price": 4.8, "freight": 1000, "tooling": 3000},
        {"name": "Beta", "unit_price": 5.0, "freight": 500, "tooling": 0},
        {"name": "Gamma", "unit_price": 4.9, "freight": 800, "tooling": 500},
    ],
}


def compare_costs(data):
    """Return costs in input order and all suppliers tied for the lowest cost."""
    quantity = Decimal(str(data["annual_qty"]))
    costs = []
    for supplier in data["suppliers"]:
        total = (
            quantity * Decimal(str(supplier["unit_price"]))
            + Decimal(str(supplier["freight"]))
            + Decimal(str(supplier["tooling"]))
        )
        costs.append((supplier["name"], total))
    if not costs:
        raise ValueError("공급사가 한 곳 이상 필요합니다.")
    minimum = min(total for _, total in costs)
    winners = [name for name, total in costs if total == minimum]
    return costs, winners, minimum


def main():
    costs, winners, minimum = compare_costs(INPUT)
    print("연간 총원가 = 연간 수량 × 단가 + 운송비 + 금형비")
    for name, total in costs:
        print(f"{name}: {total:,.2f}")
    print(f"최저가 공급사: {', '.join(winners)} (연간 총원가: {minimum:,.2f})")


if __name__ == "__main__":
    main()
