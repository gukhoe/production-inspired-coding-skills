"""제품 1대당 BOM 원가 계산. 인수로 JSON 파일 경로를 주면 해당 입력을 사용한다."""
import json
import sys
from decimal import Decimal

EXAMPLE = {
    "parts": [
        {"part": "Housing", "qty": 1, "unit_price": "14.5"},
        {"part": "Clip", "qty": 6, "unit_price": "0.35"},
        {"part": "Seal", "qty": 2, "unit_price": "1.25"},
    ]
}


def calculate_bom_cost(data):
    """각 부품의 수량 × 단가 및 총원가를 Decimal로 반환한다."""
    items = []
    for part in data["parts"]:
        qty = Decimal(str(part["qty"]))
        unit_price = Decimal(str(part["unit_price"]))
        items.append({"part": part["part"], "qty": qty,
                      "unit_price": unit_price, "cost": qty * unit_price})
    total = sum((item["cost"] for item in items), Decimal("0"))
    return items, total


def main():
    if len(sys.argv) > 1:
        with open(sys.argv[1], encoding="utf-8") as source:
            data = json.load(source, parse_float=Decimal)
    else:
        data = EXAMPLE
    items, total = calculate_bom_cost(data)
    for item in items:
        print(f'{item["part"]}: {item["qty"]} × {item["unit_price"]:.2f} = {item["cost"]:.2f}')
    print(f"제품 1대당 BOM 원가: {total:.2f}")


if __name__ == "__main__":
    main()
