"""설비의 Availability, Performance, Quality 및 OEE를 계산한다.

시간 입력은 분, 이상 사이클 시간은 초, 수량은 개 단위이다.
반환값은 0~1 비율이며 표시할 때만 백분율로 변환한다.
성능률이 100%를 초과하는 입력도 임의로 보정하지 않는다.
"""
import math


def calculate_oee(planned_minutes, run_minutes, ideal_cycle_seconds,
                  total_units, good_units):
    for name, value in (("planned_minutes", planned_minutes),
                        ("run_minutes", run_minutes),
                        ("ideal_cycle_seconds", ideal_cycle_seconds)):
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise ValueError(f"{name} must be a finite positive number")
        if not math.isfinite(value) or value <= 0:
            raise ValueError(f"{name} must be a finite positive number")
    for name, value in (("total_units", total_units), ("good_units", good_units)):
        if isinstance(value, bool) or not isinstance(value, int) or value < 0:
            raise ValueError(f"{name} must be a nonnegative integer")
    if run_minutes > planned_minutes:
        raise ValueError("run_minutes cannot exceed planned_minutes")
    if total_units == 0:
        raise ValueError("total_units must be positive to calculate quality")
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


def main():
    inputs = {
        "planned_minutes": 480,
        "run_minutes": 420,
        "ideal_cycle_seconds": 30,
        "total_units": 760,
        "good_units": 735,
    }
    result = calculate_oee(**inputs)
    for label, key in (("Availability (가동률)", "availability"),
                       ("Performance (성능률)", "performance"),
                       ("Quality (양품률)", "quality"),
                       ("OEE (설비종합효율)", "oee")):
        print(f"{label}: {result[key]:.2%}")


if __name__ == "__main__":
    main()
