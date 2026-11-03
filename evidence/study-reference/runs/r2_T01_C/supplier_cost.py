"""Compare annual purchase costs, including the given freight and tooling once."""
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
    """Return each supplier's total and the cheapest supplier's name and total."""
    quantity = Decimal(str(data["annual_qty"]))
    totals = [
        (supplier["name"],
         quantity * Decimal(str(supplier["unit_price"]))
         + Decimal(str(supplier["freight"]))
         + Decimal(str(supplier["tooling"])))
        for supplier in data["suppliers"]
    ]
    return totals, min(totals, key=lambda item: item[1])


def main():
    totals, cheapest = compare_suppliers(INPUT)
    print("연간 총원가 = 연간 구매수량 × 단가 + 운송비 + 금형비")
    for name, total in totals:
        print(f"{name}: {total:,.2f}")
    print(f"최저가 공급사: {cheapest[0]} (연간 총원가: {cheapest[1]:,.2f})")


if __name__ == "__main__":
    main()
