"""Calculate the BOM cost of one product using decimal arithmetic."""
import json
from decimal import Decimal

EXAMPLE_JSON = '''{"parts": [{"part": "Housing", "qty": 1, "unit_price": 14.5}, {"part": "Clip", "qty": 6, "unit_price": 0.35}, {"part": "Seal", "qty": 2, "unit_price": 1.25}]}'''


def calculate_bom(parts):
    """Return (part, extended cost) rows and their total."""
    rows = []
    for part in parts:
        quantity = Decimal(str(part["qty"]))
        unit_price = Decimal(str(part["unit_price"]))
        rows.append((part["part"], quantity * unit_price))
    total = sum((cost for _, cost in rows), Decimal("0"))
    return rows, total


def main():
    data = json.loads(EXAMPLE_JSON, parse_float=Decimal)
    rows, total = calculate_bom(data["parts"])
    for name, cost in rows:
        print(f"{name}: {cost:.2f}")
    print(f"제품 1대당 BOM 원가: {total:.2f}")


if __name__ == "__main__":
    main()
