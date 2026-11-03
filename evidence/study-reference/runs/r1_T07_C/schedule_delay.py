"""Calculate actual minus planned completion dates in calendar days.

Inputs: ISO dates (YYYY-MM-DD). Output: integer day difference.
Acceptance example: 2026-11-10 to 2026-11-14 yields 4 days.
A negative difference means early completion. Business-day calendars and
holiday adjustments are outside this program's scope.
"""

from datetime import date


def schedule_delay(planned_finish: str, actual_finish: str) -> int:
    """Return the signed number of days between the completion dates."""
    planned = date.fromisoformat(planned_finish)
    actual = date.fromisoformat(actual_finish)
    return (actual - planned).days


def main() -> None:
    inputs = {"planned_finish": "2026-11-10", "actual_finish": "2026-11-14"}
    delay = schedule_delay(**inputs)
    print(f"계획 완료일: {inputs['planned_finish']}")
    print(f"실제 완료일: {inputs['actual_finish']}")
    print(f"일정 지연일: {delay}일")


if __name__ == "__main__":
    main()
