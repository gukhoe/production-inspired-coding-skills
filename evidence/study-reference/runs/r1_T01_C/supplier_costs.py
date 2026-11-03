"""Compare annual purchasing costs; freight and tooling are included once."""
from decimal import Decimal

INPUT_DATA = {
    "annual_qty": 10000,
    "suppliers": [
        {"name": "Alpha", "unit_price": 4.8, "freight": 1000, "tooling": 3000},
        {"name": "Beta", "unit_price": 5.0, "freight": 500, "tooling": 0},
        {"name": "Gamma", "unit_price": 4.9, "freight": 800, "tooling": 500},
    ],
}


def compare_suppliers(data):
    """Return each annual total and all suppliers sharing the lowest total."""
    quantity = Decimal(str(data["annual_qty"]))
    totals = []
    for supplier in data["suppliers"]:
        total = (
            quantity * Decimal(str(supplier["unit_price"]))
            + Decimal(str(supplier["freight"]))
            + Decimal(str(supplier["tooling"]))
        )
        totals.append((supplier["name"], total))
    minimum = min(total for _, total in totals)
    winners = [name for name, total in totals if total == minimum]
    return totals, winners


def main():
    totals, winners = compare_suppliers(INPUT_DATA)
    print("연간 구매 총원가 = 연간 구매 수량 × 단가 + 운송비 + 금형비")
    for name, total in totals:
        print(f"{name}: {total:,.2f}")
    print(f"최저가 공급사: {', '.join(winners)}")


if __name__ == "__main__":
    main()
