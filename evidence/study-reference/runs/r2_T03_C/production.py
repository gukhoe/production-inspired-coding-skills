"""일별 생산량과 근무일수로 총생산량 및 수요 대비 차이를 계산한다."""


def calculate_production(daily_capacity, working_days, demand):
    """생산량, 부족량, 잉여량을 반환한다. 입력값은 음수가 아닌 수량이다."""
    total_production = daily_capacity * working_days
    balance = total_production - demand
    return {
        "total_production": total_production,
        "shortage": max(-balance, 0),
        "surplus": max(balance, 0),
    }


def main():
    inputs = {"daily_capacity": 450, "working_days": 20, "demand": 9200}
    result = calculate_production(**inputs)
    print(f"총생산량: {result['total_production']:,}개")
    print(f"수요: {inputs['demand']:,}개")
    if result['shortage'] > 0:
        print(f"생산 부족량: {result['shortage']:,}개")
    elif result['surplus'] > 0:
        print(f"생산 잉여량: {result['surplus']:,}개")
    else:
        print("생산량과 수요가 일치합니다.")


if __name__ == "__main__":
    main()
