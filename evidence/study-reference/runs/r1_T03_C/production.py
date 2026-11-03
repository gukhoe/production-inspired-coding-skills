"""Calculate production shortage or surplus for a working period."""


def production_balance(daily_capacity, working_days, demand):
    """Return total production and nonnegative shortage/surplus amounts."""
    total_production = daily_capacity * working_days
    difference = total_production - demand
    return {
        "total_production": total_production,
        "shortage": max(-difference, 0),
        "surplus": max(difference, 0),
    }


def main():
    inputs = {"daily_capacity": 450, "working_days": 20, "demand": 9200}
    result = production_balance(**inputs)
    print(f"일별 생산량: {inputs['daily_capacity']:,}")
    print(f"작업 일수: {inputs['working_days']:,}")
    print(f"총생산량: {result['total_production']:,}")
    print(f"수요량: {inputs['demand']:,}")
    if result["shortage"]:
        print(f"생산 부족량: {result['shortage']:,}")
    elif result["surplus"]:
        print(f"생산 잉여량: {result['surplus']:,}")
    else:
        print("생산량과 수요량이 일치합니다.")


if __name__ == "__main__":
    main()
