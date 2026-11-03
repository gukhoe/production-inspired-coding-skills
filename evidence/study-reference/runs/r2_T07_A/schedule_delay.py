"""완료일을 비교하여 달력 기준 지연일을 계산합니다."""

import json
from datetime import date


def delay_days(planned_finish: str, actual_finish: str) -> int:
    """YYYY-MM-DD 날짜를 받아 지연일을 반환합니다. 조기 완료는 0일입니다."""
    planned = date.fromisoformat(planned_finish)
    actual = date.fromisoformat(actual_finish)
    return max(0, (actual - planned).days)


if __name__ == "__main__":
    inputs = {"planned_finish": "2026-11-10", "actual_finish": "2026-11-14"}
    result = {**inputs, "delay_days": delay_days(**inputs)}
    print(json.dumps(result, ensure_ascii=False))
