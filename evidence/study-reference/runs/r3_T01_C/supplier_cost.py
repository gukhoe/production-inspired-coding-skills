"""공급사별 연간 구매 총원가 비교 (운송비와 금형비는 각 1회 합산)."""

from decimal import Decimal


INPUT = {
    "annual_qty": 10000,
    "suppliers": [
        {"name": "Alpha", "unit_price": 4.8, "freight": 1000, "tooling": 3000},
        {"name": "Beta", "unit_price": 5.0, "freight": 500, "tooling": 0},
        {"name": "Gamma", "unit_price": 4.9, "freight": 800, "tooling": 500},
    ],
}


def compare_suppliers(data):
    """Return (name, total) pairs and all suppliers with the lowest total."""
    qty = Decimal(str(data["annual_qty"]))
    totals = [
        (
            supplier["name"],
            qty * Decimal(str(supplier["unit_price"]))
            + Decimal(str(supplier["freight"]))
            + Decimal(str(supplier["tooling"])),
        )
        for supplier in data["suppliers"]
    ]
    if not totals:
        raise ValueError("비교할 공급사가 필요합니다.")
    lowest = min(total for _, total in totals)
    winners = [name for name, total in totals if total == lowest]
    return totals, winners


def main():
    totals, winners = compare_suppliers(INPUT)
    print("연간 총원가 = 연간 구매수량 × 단가 + 운송비 + 금형비")
    for name, total in totals:
        print(f"{name}: {total:,.2f}")
    print(f"최저가 공급사: {', '.join(winners)}")


if __name__ == "__main__":
    main()
