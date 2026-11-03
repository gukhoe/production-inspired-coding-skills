"""일일 생산량과 근무일 수를 이용해 수요 대비 부족량/잉여량을 계산합니다."""


def calculate_production(daily_capacity, working_days, demand):
    """Return total production, shortage, and surplus for the working period."""
    if any(value < 0 for value in (daily_capacity, working_days, demand)):
        raise ValueError("생산량, 근무일 수, 수요는 음수일 수 없습니다.")
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
    print(f"근무일 수: {inputs['working_days']}일")
    print(f"총생산량: {result['total_production']:,}개")
    print(f"수요: {inputs['demand']:,}개")
    if result["shortage"]:
        print(f"생산 부족량: {result['shortage']:,}개")
    elif result["surplus"]:
        print(f"생산 잉여량: {result['surplus']:,}개")
    else:
        print("생산량과 수요가 같습니다. 부족량 및 잉여량: 0개")


if __name__ == "__main__":
    main()
