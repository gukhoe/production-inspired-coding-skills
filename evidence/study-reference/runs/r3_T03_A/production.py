"""일별 생산량과 작업일수로 수요 대비 부족량 또는 잉여량을 계산한다."""


def calculate_production(daily_capacity, working_days, demand):
    """총생산량, 부족량, 잉여량을 반환한다. 입력값은 음수가 아닌 정수다."""
    for name, value in (
        ("daily_capacity", daily_capacity),
        ("working_days", working_days),
        ("demand", demand),
    ):
        if type(value) is not int or value < 0:
            raise ValueError(f"{name}은 음수가 아닌 정수여야 합니다.")

    total_production = daily_capacity * working_days
    return {
        "total_production": total_production,
        "shortage": max(demand - total_production, 0),
        "surplus": max(total_production - demand, 0),
    }


def main():
    inputs = {"daily_capacity": 450, "working_days": 20, "demand": 9200}
    result = calculate_production(**inputs)
    print(f"일일 생산량: {inputs['daily_capacity']:,}개")
    print(f"작업일수: {inputs['working_days']}일")
    print(f"총생산량: {result['total_production']:,}개")
    print(f"수요: {inputs['demand']:,}개")
    if result["shortage"]:
        print(f"생산 부족량: {result['shortage']:,}개")
    elif result["surplus"]:
        print(f"생산 잉여량: {result['surplus']:,}개")
    else:
        print("생산량과 수요가 일치합니다.")


if __name__ == "__main__":
    main()
