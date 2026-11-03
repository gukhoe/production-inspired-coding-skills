"""계획 완료일과 실제 완료일로 일정 지연일을 계산합니다."""

import argparse
from datetime import date


def delay_days(planned_finish: str, actual_finish: str) -> int:
    """달력 기준 지연일을 반환합니다. 조기/당일 완료는 0일입니다."""
    planned = date.fromisoformat(planned_finish)
    actual = date.fromisoformat(actual_finish)
    return max(0, (actual - planned).days)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("planned_finish", help="계획 완료일 (YYYY-MM-DD)")
    parser.add_argument("actual_finish", help="실제 완료일 (YYYY-MM-DD)")
    args = parser.parse_args()
    try:
        days = delay_days(args.planned_finish, args.actual_finish)
    except ValueError:
        parser.error("유효한 날짜를 YYYY-MM-DD 형식으로 입력하세요.")
    print(f"계획 완료일: {args.planned_finish}")
    print(f"실제 완료일: {args.actual_finish}")
    print(f"일정 지연일: {days}일")


if __name__ == "__main__":
    main()
