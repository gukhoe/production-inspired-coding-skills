"""일별 생산량과 근무일 수를 이용해 수요 대비 부족·잉여량을 계산한다."""


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
    print(f"일별 생산량: {inputs['daily_capacity']:,}개")
    print(f"근무일 수: {inputs['working_days']}일")
    print(f"총생산량: {result['total_production']:,}개")
    print(f"수요: {inputs['demand']:,}개")
    print(f"부족량: {result['shortage']:,}개")
    print(f"잉여량: {result['surplus']:,}개")
    if result["shortage"]:
        print(f"결과: 생산량이 {result['shortage']:,}개 부족합니다.")
    elif result["surplus"]:
        print(f"결과: 생산량이 {result['surplus']:,}개 남습니다.")
    else:
        print("결과: 생산량과 수요가 일치합니다.")


if __name__ == "__main__":
    main()
