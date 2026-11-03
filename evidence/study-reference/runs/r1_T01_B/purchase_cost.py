"""공급사별 연간 구매 총원가를 계산한다."""
import json
import sys
from decimal import Decimal
from pathlib import Path


def compare_costs(data):
    """운송비와 금형비는 연간 총액에 각각 한 번 더한다."""
    quantity = Decimal(str(data['annual_qty']))
    costs = []
    for supplier in data['suppliers']:
        total = (quantity * Decimal(str(supplier['unit_price']))
                 + Decimal(str(supplier['freight']))
                 + Decimal(str(supplier['tooling'])))
        costs.append((supplier['name'], total))
    if not costs:
        raise ValueError('비교할 공급사가 필요합니다.')
    minimum = min(total for _, total in costs)
    winners = [name for name, total in costs if total == minimum]
    return costs, winners, minimum


def main():
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).with_name('input.json')
    data = json.loads(path.read_text(encoding='utf-8'), parse_float=Decimal)
    costs, winners, minimum = compare_costs(data)
    print('연간 구매 총원가 (구매수량 × 단가 + 운송비 + 금형비)')
    for name, total in costs:
        print(f'{name}: {total:,.2f}')
    print(f'최저가 공급사: {", ".join(winners)}')
    print(f'최저 총원가: {minimum:,.2f}')


if __name__ == '__main__':
    main()
