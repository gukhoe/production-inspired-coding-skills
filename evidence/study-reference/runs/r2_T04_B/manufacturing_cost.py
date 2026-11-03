"""재료비, 직접노무비, 간접비를 합산해 제조원가를 계산합니다."""

from decimal import Decimal


def calculate_cost(material_per_unit, labor_per_unit, overhead_per_unit, quantity):
    """제품당 제조원가와 수량 전체의 제조원가를 반환합니다."""
    per_unit = sum(
        (Decimal(str(value)) for value in
         (material_per_unit, labor_per_unit, overhead_per_unit)),
        Decimal("0"),
    )
    return per_unit, per_unit * quantity


def main():
    inputs = {
        "material_per_unit": 12.5,
        "labor_per_unit": 4.2,
        "overhead_per_unit": 3.3,
        "quantity": 1000,
    }
    per_unit, total = calculate_cost(**inputs)
    print(f"제품당 제조원가: {per_unit:,.2f}")
    print(f"생산 수량: {inputs['quantity']:,}개")
    print(f"총 제조원가: {total:,.2f}")


if __name__ == "__main__":
    main()
