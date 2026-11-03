"""공급사별 연간 구매 총원가를 비교한다."""
from decimal import Decimal


INPUT = {
    "annual_qty": 10000,
    "suppliers": [
        {"name": "Alpha", "unit_price": 4.8, "freight": 1000, "tooling": 3000},
        {"name": "Beta", "unit_price": 5.0, "freight": 500, "tooling": 0},
        {"name": "Gamma", "unit_price": 4.9, "freight": 800, "tooling": 500},
    ],
}


def compare_suppliers(annual_qty, suppliers):
    """운송비와 금형비는 해당 연도에 각각 한 번 발생하는 비용이다."""
    qty = Decimal(str(annual_qty))
    costs = [
        (
            supplier["name"],
            qty * Decimal(str(supplier["unit_price"]))
            + Decimal(str(supplier["freight"]))
            + Decimal(str(supplier["tooling"])),
        )
        for supplier in suppliers
    ]
    if not costs:
        raise ValueError("공급사가 한 곳 이상 필요합니다.")
    lowest = min(cost for _, cost in costs)
    winners = [name for name, cost in costs if cost == lowest]
    return costs, winners, lowest


def main():
    costs, winners, lowest = compare_suppliers(**INPUT)
    print("연간 총원가 = 연간 구매량 × 단가 + 운송비 + 금형비")
    for name, cost in costs:
        print(f"{name}: {cost:,.2f}")
    print(f"최저가 공급사: {', '.join(winners)} (연간 총원가: {lowest:,.2f})")


if __name__ == "__main__":
    main()
