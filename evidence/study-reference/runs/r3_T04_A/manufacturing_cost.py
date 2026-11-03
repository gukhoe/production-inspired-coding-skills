"""재료비, 직접노무비, 간접비로 제품당 및 총 제조원가를 계산한다."""

from decimal import Decimal


def calculate_cost(material_per_unit, labor_per_unit, overhead_per_unit, quantity):
    """제품당 제조원가와 생산 수량 전체의 제조원가를 반환한다."""
    unit_cost = sum(
        (Decimal(str(cost)) for cost in
         (material_per_unit, labor_per_unit, overhead_per_unit)),
        Decimal('0'),
    )
    total_cost = unit_cost * Decimal(str(quantity))
    return unit_cost, total_cost


def main():
    inputs = {
        'material_per_unit': 12.5,
        'labor_per_unit': 4.2,
        'overhead_per_unit': 3.3,
        'quantity': 1000,
    }
    unit_cost, total_cost = calculate_cost(**inputs)
    print(f"생산 수량: {inputs['quantity']:,}개")
    print(f'제품당 제조원가: {unit_cost:,.2f}')
    print(f'총 제조원가: {total_cost:,.2f}')


if __name__ == '__main__':
    main()
