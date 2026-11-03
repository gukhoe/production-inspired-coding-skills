"""설비 OEE 계산: 비율은 0~1 기준으로 반환하고 출력은 백분율로 표시한다."""

import math


def calculate_oee(planned_minutes, run_minutes, ideal_cycle_seconds,
                  total_units, good_units):
    """A = 가동/계획, P = 이상 생산시간/가동시간, Q = 양품/총생산.

    분모가 0이면 비율을 정의할 수 없으므로 ValueError를 발생시킨다.
    Performance가 100%를 넘어도 입력값을 그대로 반영하며 자르지 않는다.
    """
    for name, value in (("planned_minutes", planned_minutes),
                        ("run_minutes", run_minutes),
                        ("ideal_cycle_seconds", ideal_cycle_seconds)):
        if (isinstance(value, bool) or not isinstance(value, (int, float))
                or not math.isfinite(value) or value <= 0):
            raise ValueError(f"{name} must be a positive finite number")
    for name, value in (("total_units", total_units), ("good_units", good_units)):
        if isinstance(value, bool) or not isinstance(value, int) or value < 0:
            raise ValueError(f"{name} must be a nonnegative integer")
    if total_units == 0:
        raise ValueError("total_units must be greater than zero")
    if run_minutes > planned_minutes:
        raise ValueError("run_minutes cannot exceed planned_minutes")
    if good_units > total_units:
        raise ValueError("good_units cannot exceed total_units")

    availability = run_minutes / planned_minutes
    performance = ideal_cycle_seconds * total_units / (run_minutes * 60)
    quality = good_units / total_units
    return {
        "availability": availability,
        "performance": performance,
        "quality": quality,
        "oee": availability * performance * quality,
    }


if __name__ == "__main__":
    inputs = {
        "planned_minutes": 480,
        "run_minutes": 420,
        "ideal_cycle_seconds": 30,
        "total_units": 760,
        "good_units": 735,
    }
    result = calculate_oee(**inputs)
    for key, label in (("availability", "Availability (가동률)"),
                       ("performance", "Performance (성능률)"),
                       ("quality", "Quality (양품률)"),
                       ("oee", "OEE (설비종합효율)")):
        print(f"{label}: {result[key]:.2%}")
