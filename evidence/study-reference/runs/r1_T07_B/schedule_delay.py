"""Calculate calendar-day schedule delay from ISO-format completion dates."""
import argparse
from datetime import date


def delay_days(planned_finish: str, actual_finish: str) -> int:
    """Return days late; early or on-time completion has zero delay."""
    planned = date.fromisoformat(planned_finish)
    actual = date.fromisoformat(actual_finish)
    return max(0, (actual - planned).days)


def main() -> None:
    parser = argparse.ArgumentParser(description="계획 완료일과 실제 완료일로 일정 지연일을 계산합니다.")
    parser.add_argument("--planned-finish", default="2026-11-10", help="계획 완료일 (YYYY-MM-DD)")
    parser.add_argument("--actual-finish", default="2026-11-14", help="실제 완료일 (YYYY-MM-DD)")
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
