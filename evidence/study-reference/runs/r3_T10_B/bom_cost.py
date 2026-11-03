"""제품 1대당 BOM 원가 계산. JSON 파일을 인자로 주거나 기본 예제를 실행한다."""
import json
import sys
from decimal import Decimal

EXAMPLE_JSON = '''{"parts": [{"part": "Housing", "qty": 1, "unit_price": 14.5}, {"part": "Clip", "qty": 6, "unit_price": 0.35}, {"part": "Seal", "qty": 2, "unit_price": 1.25}]}'''


def calculate_bom(data):
    """부품별 원가 목록과 제품 1대당 합계(Decimal)를 반환한다."""
    rows = []
    total = Decimal('0')
    for item in data['parts']:
        qty = Decimal(str(item['qty']))
        unit_price = Decimal(str(item['unit_price']))
        if not qty.is_finite() or not unit_price.is_finite() or qty < 0 or unit_price < 0:
            raise ValueError('수량과 단가는 유한한 0 이상의 값이어야 합니다.')
        cost = qty * unit_price
        rows.append((item['part'], qty, unit_price, cost))
        total += cost
    return rows, total


def main():
    if len(sys.argv) > 2:
        raise SystemExit('사용법: python3 bom_cost.py [input.json]')
    if len(sys.argv) == 2:
        with open(sys.argv[1], encoding='utf-8') as source:
            data = json.load(source, parse_float=Decimal)
    else:
        data = json.loads(EXAMPLE_JSON, parse_float=Decimal)
    rows, total = calculate_bom(data)
    for part, qty, unit_price, cost in rows:
        print(f'{part}: {qty} × {unit_price:.2f} = {cost:.2f}')
    print(f'제품 1대당 BOM 원가: {total:.2f}')


if __name__ == '__main__':
    main()
