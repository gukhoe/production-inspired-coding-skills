"""Compare annual purchasing costs, including annual freight and tooling."""
import json
from decimal import Decimal
from pathlib import Path


def compare_costs(data):
    """Return supplier totals and all suppliers tied for the lowest total."""
    quantity = Decimal(str(data['annual_qty']))
    totals = [
        (supplier['name'],
         quantity * Decimal(str(supplier['unit_price']))
         + Decimal(str(supplier['freight']))
         + Decimal(str(supplier['tooling'])))
        for supplier in data['suppliers']
    ]
    lowest = min(cost for _, cost in totals)
    winners = [name for name, cost in totals if cost == lowest]
    return totals, winners


def main():
    data = json.loads(Path(__file__).with_name('input.json').read_text(),
                      parse_float=Decimal)
    totals, winners = compare_costs(data)
    print(f"연간 구매 수량: {data['annual_qty']:,}")
    print('총원가 = 연간 수량 × 단가 + 운송비 + 금형비')
    for name, cost in totals:
        print(f'{name}: {cost:,.2f}')
    print(f"최저가 공급사: {', '.join(winners)}")
    print(f'최저 연간 총원가: {min(cost for _, cost in totals):,.2f}')


if __name__ == '__main__':
    main()
