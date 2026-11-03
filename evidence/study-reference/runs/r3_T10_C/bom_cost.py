"""Calculate the BOM cost of one product from part quantities and unit prices."""

import json
from decimal import Decimal


EXAMPLE_INPUT = '''{"parts": [{"part": "Housing", "qty": 1, "unit_price": 14.5}, {"part": "Clip", "qty": 6, "unit_price": 0.35}, {"part": "Seal", "qty": 2, "unit_price": 1.25}]}'''


def calculate_bom(data):
    """Return each part's extended cost and the total cost for one product."""
    rows = []
    total = Decimal("0")
    for part in data["parts"]:
        quantity = Decimal(str(part["qty"]))
        price = Decimal(str(part["unit_price"]))
        cost = quantity * price
        rows.append((part["part"], quantity, price, cost))
        total += cost
    return rows, total


def main():
    data = json.loads(EXAMPLE_INPUT, parse_float=Decimal)
    rows, total = calculate_bom(data)
    for name, quantity, price, cost in rows:
        print(f"{name}: {quantity} × {price:.2f} = {cost:.2f}")
    print(f"제품 1대당 BOM 원가: {total:.2f}")


if __name__ == "__main__":
    main()
