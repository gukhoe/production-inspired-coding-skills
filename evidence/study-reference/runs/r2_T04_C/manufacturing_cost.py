"""재료비, 직접노무비, 간접비로 제품당 및 총 제조원가를 계산합니다."""
import json
import sys
from decimal import Decimal


EXAMPLE_INPUT = '{"material_per_unit": 12.5, "labor_per_unit": 4.2, "overhead_per_unit": 3.3, "quantity": 1000}'


def calculate_cost(material_per_unit, labor_per_unit, overhead_per_unit, quantity):
    """각 단위 비용의 합과 수량에 따른 총액을 Decimal로 반환합니다."""
    unit_cost = sum(
        (Decimal(str(value)) for value in
         (material_per_unit, labor_per_unit, overhead_per_unit)),
        Decimal('0'),
    )
    return unit_cost, unit_cost * Decimal(str(quantity))


def main():
    # 인수가 없으면 제공된 예제를 사용합니다. JSON을 첫 인수로 전달할 수도 있습니다.
    data = json.loads(sys.argv[1] if len(sys.argv) > 1 else EXAMPLE_INPUT,
                      parse_float=Decimal)
    unit_cost, total_cost = calculate_cost(**data)
    print(f'제품당 제조원가: {unit_cost}')
    print(f'생산 수량: {data["quantity"]}')
    print(f'총 제조원가: {total_cost}')


if __name__ == '__main__':
    main()
