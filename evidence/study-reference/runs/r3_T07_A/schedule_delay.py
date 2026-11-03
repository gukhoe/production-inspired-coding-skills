"""완료일을 비교해 달력 기준 지연일을 계산합니다."""

from datetime import date


def calculate_delay(planned_finish: str, actual_finish: str) -> int:
    """YYYY-MM-DD 날짜를 비교합니다. 조기 완료 또는 당일 완료는 0일입니다."""
    planned = date.fromisoformat(planned_finish)
    actual = date.fromisoformat(actual_finish)
    return max(0, (actual - planned).days)


if __name__ == "__main__":
    inputs = {"planned_finish": "2026-11-10", "actual_finish": "2026-11-14"}
    print(f"일정 지연일: {calculate_delay(**inputs)}일")
