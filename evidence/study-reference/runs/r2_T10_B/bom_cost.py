"""Calculate per-product BOM cost from a JSON parts list."""

import json
import sys
from decimal import Decimal
from pathlib import Path


def calculate_bom(parts):
    """Return (part, quantity, unit price, subtotal) rows and their total."""
    rows = []
    total = Decimal("0")
    for part in parts:
        qty = Decimal(str(part["qty"]))
        price = Decimal(str(part["unit_price"]))
        if not qty.is_finite() or not price.is_finite() or qty < 0 or price < 0:
            raise ValueError("수량과 단가는 유한한 0 이상의 숫자여야 합니다.")
        subtotal = qty * price
        rows.append((part["part"], qty, price, subtotal))
        total += subtotal
    return rows, total


def main():
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).with_name("input.json")
    data = json.loads(path.read_text(encoding="utf-8"), parse_float=Decimal)
    rows, total = calculate_bom(data["parts"])
    for name, qty, price, subtotal in rows:
        print(f"{name}: {qty} × {price:.2f} = {subtotal:.2f}")
    print(f"제품 1대당 BOM 원가: {total:.2f}")


if __name__ == "__main__":
    main()
