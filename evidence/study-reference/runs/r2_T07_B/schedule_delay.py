"""Calculate schedule delay in calendar days from ISO dates."""

from datetime import date


def calculate_delay(planned_finish: str, actual_finish: str) -> int:
    """Return overdue calendar days; early/on-time completion has no delay."""
    planned = date.fromisoformat(planned_finish)
    actual = date.fromisoformat(actual_finish)
    return max(0, (actual - planned).days)


if __name__ == "__main__":
    inputs = {"planned_finish": "2026-11-10", "actual_finish": "2026-11-14"}
    delay = calculate_delay(**inputs)
    print(f"계획 완료일: {inputs['planned_finish']}")
    print(f"실제 완료일: {inputs['actual_finish']}")
    print(f"일정 지연일: {delay}일")
