"""계획 완료일과 실제 완료일의 달력 날짜 차이를 계산한다.

입력 형식: YYYY-MM-DD. 양수는 지연, 0은 정시, 음수는 조기 완료.
주말·공휴일을 제외하는 영업일 계산은 수행하지 않는다.
"""

from datetime import date


def calculate_delay(planned_finish: str, actual_finish: str) -> int:
    """실제 완료일에서 계획 완료일을 뺀 일수를 반환한다."""
    planned = date.fromisoformat(planned_finish)
    actual = date.fromisoformat(actual_finish)
    return (actual - planned).days


if __name__ == "__main__":
    inputs = {
        "planned_finish": "2026-11-10",
        "actual_finish": "2026-11-14",
    }
    delay_days = calculate_delay(**inputs)
    print(f"일정 지연일: {delay_days}일")
