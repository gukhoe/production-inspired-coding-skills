"""계획 완료일과 실제 완료일 사이의 달력 날짜 차이를 계산합니다."""

from datetime import date


def calculate_delay(planned_finish: str, actual_finish: str) -> int:
    """실제 완료일 - 계획 완료일을 반환합니다. 음수는 조기 완료입니다."""
    planned = date.fromisoformat(planned_finish)
    actual = date.fromisoformat(actual_finish)
    return (actual - planned).days


def main() -> None:
    inputs = {
        "planned_finish": "2026-11-10",
        "actual_finish": "2026-11-14",
    }
    delay = calculate_delay(**inputs)
    print(f"계획 완료일: {inputs['planned_finish']}")
    print(f"실제 완료일: {inputs['actual_finish']}")
    print(f"일정 지연일: {delay}일")


if __name__ == "__main__":
    main()
