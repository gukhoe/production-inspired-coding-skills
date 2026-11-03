"""Calculate the BOM cost of one product using decimal arithmetic."""
import json
import sys
from decimal import Decimal
from pathlib import Path


def calculate_bom(parts):
    """Return (part name, extended cost) rows and their total, without rounding."""
    rows = [
        (part["part"], Decimal(str(part["qty"])) * Decimal(str(part["unit_price"])))
        for part in parts
    ]
    return rows, sum((cost for _, cost in rows), Decimal("0"))


def main():
    input_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).with_name("input.json")
    data = json.loads(input_path.read_text(encoding="utf-8"), parse_float=Decimal)
    rows, total = calculate_bom(data["parts"])
    for name, cost in rows:
        print(f"{name}: {cost:.2f}")
    print(f"제품 1대당 BOM 원가: {total:.2f}")


if __name__ == "__main__":
    main()
