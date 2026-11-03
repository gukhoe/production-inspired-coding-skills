"""재료비, 직접노무비, 간접비를 합산하여 제조원가를 계산한다."""
from decimal import Decimal


def calculate_cost(material_per_unit, labor_per_unit, overhead_per_unit, quantity):
    """금액과 수량으로 제품당 제조원가 및 총 제조원가를 반환한다."""
    if isinstance(quantity, bool) or not isinstance(quantity, int) or quantity < 0:
        raise ValueError("생산수량은 0 이상의 정수여야 합니다.")
    costs = [Decimal(str(value)) for value in
             (material_per_unit, labor_per_unit, overhead_per_unit)]
    if any(not cost.is_finite() or cost < 0 for cost in costs):
        raise ValueError("비용은 유한한 0 이상의 수여야 합니다.")
    per_unit = sum(costs, Decimal("0"))
    return per_unit, per_unit * quantity


def main():
    inputs = {"material_per_unit": 12.5, "labor_per_unit": 4.2,
              "overhead_per_unit": 3.3, "quantity": 1000}
    per_unit, total = calculate_cost(**inputs)
    print(f"제품당 제조원가: {per_unit:,.2f}")
    print(f"생산수량: {inputs['quantity']:,}개")
    print(f"총 제조원가: {total:,.2f}")


if __name__ == "__main__":
    main()
