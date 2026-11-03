"""Calculate the BOM cost of one product from part quantities and prices."""
from decimal import Decimal


EXAMPLE_INPUT = {
    "parts": [
        {"part": "Housing", "qty": 1, "unit_price": 14.5},
        {"part": "Clip", "qty": 6, "unit_price": 0.35},
        {"part": "Seal", "qty": 2, "unit_price": 1.25},
    ]
}


def calculate_bom_cost(data):
    """Return each part's extended cost and their exact decimal sum."""
    lines = []
    for part in data["parts"]:
        quantity = Decimal(str(part["qty"]))
        unit_price = Decimal(str(part["unit_price"]))
        lines.append((part["part"], quantity, unit_price, quantity * unit_price))
    total = sum((line[3] for line in lines), Decimal("0"))
    return lines, total


def main():
    lines, total = calculate_bom_cost(EXAMPLE_INPUT)
    for name, quantity, unit_price, cost in lines:
        print(f"{name}: {quantity} × {unit_price:.2f} = {cost:.2f}")
    print(f"제품 1대당 BOM 원가: {total:.2f}")


if __name__ == "__main__":
    main()
