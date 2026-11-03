"""Calculate the BOM cost of one product using decimal arithmetic."""
from decimal import Decimal


INPUT_DATA = {
    "parts": [
        {"part": "Housing", "qty": 1, "unit_price": 14.5},
        {"part": "Clip", "qty": 6, "unit_price": 0.35},
        {"part": "Seal", "qty": 2, "unit_price": 1.25},
    ]
}


def part_cost(part):
    return Decimal(str(part["qty"])) * Decimal(str(part["unit_price"]))


def bom_cost(data):
    return sum((part_cost(part) for part in data["parts"]), Decimal("0"))


def main():
    for part in INPUT_DATA["parts"]:
        print(
            f'{part["part"]}: {part["qty"]} × '
            f'{Decimal(str(part["unit_price"])):.2f} = {part_cost(part):.2f}'
        )
    print(f"제품 1대당 BOM 원가: {bom_cost(INPUT_DATA):.2f}")


if __name__ == "__main__":
    main()
