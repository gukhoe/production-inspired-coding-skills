"""Compare annual purchase costs, adding freight and tooling once per year."""
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
    """Return supplier totals and all suppliers tied for the minimum."""
    quantity = Decimal(str(data["annual_qty"]))
    totals = []
    for supplier in data["suppliers"]:
        total = (
            quantity * Decimal(str(supplier["unit_price"]))
            + Decimal(str(supplier["freight"]))
            + Decimal(str(supplier["tooling"]))
        )
        totals.append((supplier["name"], total))
    if not totals:
        raise ValueError("공급사가 최소 한 곳 필요합니다.")
    minimum = min(total for _, total in totals)
    winners = [name for name, total in totals if total == minimum]
    return totals, winners, minimum


def main():
    totals, winners, minimum = compare_costs(INPUT)
    print(f"연간 구매 수량: {INPUT['annual_qty']:,}")
    print("계산식: 연간 구매 수량 × 단가 + 운송비 + 금형비")
    for name, total in totals:
        print(f"{name} 연간 총원가: {total:,.2f}")
    print(f"최저가 공급사: {', '.join(winners)}")
    print(f"최저 연간 총원가: {minimum:,.2f}")


if __name__ == "__main__":
    main()
