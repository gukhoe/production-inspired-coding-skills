"""Calculate a product's BOM cost with exact decimal arithmetic."""

from decimal import Decimal


def calculate_bom(parts):
    """Return each part's extended cost and the total cost for one product."""
    rows = []
    for part in parts:
        quantity = Decimal(str(part["qty"]))
        unit_price = Decimal(str(part["unit_price"]))
        if not quantity.is_finite() or not unit_price.is_finite():
            raise ValueError("Quantity and unit price must be finite.")
        if quantity < 0 or unit_price < 0:
            raise ValueError("Quantity and unit price must be nonnegative.")
        rows.append((part["part"], quantity, unit_price, quantity * unit_price))
    return rows, sum((row[3] for row in rows), Decimal("0"))


def main():
    data = {"parts": [
        {"part": "Housing", "qty": 1, "unit_price": 14.5},
        {"part": "Clip", "qty": 6, "unit_price": 0.35},
        {"part": "Seal", "qty": 2, "unit_price": 1.25},
    ]}
    rows, total = calculate_bom(data["parts"])
    for name, quantity, unit_price, cost in rows:
        print(f"{name}: {quantity} × {unit_price:.2f} = {cost:.2f}")
    print(f"제품 1대당 BOM 원가: {total:.2f}")


if __name__ == "__main__":
    main()
