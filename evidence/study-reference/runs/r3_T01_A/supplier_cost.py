"""Compare annual purchase costs; freight and tooling are annual totals."""
import json
from decimal import Decimal
from pathlib import Path


def compare_costs(data):
    quantity = Decimal(str(data["annual_qty"]))
    totals = []
    for supplier in data["suppliers"]:
        total = (
            quantity * Decimal(str(supplier["unit_price"]))
            + Decimal(str(supplier["freight"]))
            + Decimal(str(supplier["tooling"]))
        )
        totals.append((supplier["name"], total))
    if not totals:
        raise ValueError("공급사가 한 곳 이상 필요합니다.")
    lowest = min(total for _, total in totals)
    winners = [name for name, total in totals if total == lowest]
    return totals, winners, lowest


def main():
    data = json.loads(Path(__file__).with_name("input.json").read_text(encoding="utf-8"))
    totals, winners, lowest = compare_costs(data)
    print("연간 총원가 = 연간 수량 × 단가 + 운송비 + 금형비")
    for name, total in totals:
        print(f"{name}: {total:,.2f}")
    print(f"최저가 공급사: {', '.join(winners)} (연간 총원가: {lowest:,.2f})")


if __name__ == "__main__":
    main()
