"""Calculate schedule delay in calendar days (early completion is zero delay)."""

import argparse
from datetime import date


def delay_days(planned_finish: str, actual_finish: str) -> int:
    """Return nonnegative calendar days after the planned finish date."""
    planned = date.fromisoformat(planned_finish)
    actual = date.fromisoformat(actual_finish)
    return max(0, (actual - planned).days)


def main() -> None:
    parser = argparse.ArgumentParser(description="일정 지연일 계산")
    parser.add_argument("planned_finish", help="계획 완료일 (YYYY-MM-DD)")
    parser.add_argument("actual_finish", help="실제 완료일 (YYYY-MM-DD)")
    args = parser.parse_args()
    try:
        days = delay_days(args.planned_finish, args.actual_finish)
    except ValueError as exc:
        parser.error(f"유효한 날짜를 입력하세요: {exc}")
    print(f"계획 완료일: {args.planned_finish}")
    print(f"실제 완료일: {args.actual_finish}")
    print(f"일정 지연일: {days}일")


if __name__ == "__main__":
    main()
