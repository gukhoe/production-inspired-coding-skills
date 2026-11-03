"""일별 생산량과 근무일, 수요로 생산 부족량과 잉여량을 계산합니다."""


def calculate_production(daily_capacity, working_days, demand):
    total_production = daily_capacity * working_days
    return {
        "total_production": total_production,
        "shortage": max(demand - total_production, 0),
        "surplus": max(total_production - demand, 0),
    }


def main():
    inputs = {"daily_capacity": 450, "working_days": 20, "demand": 9200}
    result = calculate_production(**inputs)
    print(f"총생산량: {result['total_production']:,}")
    print(f"수요: {inputs['demand']:,}")
    print(f"생산 부족량: {result['shortage']:,}")
    print(f"생산 잉여량: {result['surplus']:,}")


if __name__ == "__main__":
    main()
