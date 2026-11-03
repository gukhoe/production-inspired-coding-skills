"""일별 생산량과 작업일 수로 총생산량 및 수요 차이를 계산합니다."""
import argparse
import json


def calculate_production(daily_capacity, working_days, demand):
    total_production = daily_capacity * working_days
    difference = total_production - demand
    return {
        "total_production": total_production,
        "demand": demand,
        "shortage": max(-difference, 0),
        "surplus": max(difference, 0),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "input_json", nargs="?",
        default='{"daily_capacity": 450, "working_days": 20, "demand": 9200}',
        help="daily_capacity, working_days, demand를 포함하는 JSON",
    )
    inputs = json.loads(parser.parse_args().input_json)
    result = calculate_production(**inputs)
    print(f"총생산량: {result['total_production']:,}개")
    print(f"수요: {result['demand']:,}개")
    print(f"생산 부족량: {result['shortage']:,}개")
    print(f"생산 잉여량: {result['surplus']:,}개")


if __name__ == "__main__":
    main()
