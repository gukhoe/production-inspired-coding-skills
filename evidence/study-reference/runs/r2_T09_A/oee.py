"""설비의 Availability, Performance, Quality와 OEE를 계산합니다."""

import math


def calculate_oee(planned_minutes, run_minutes, ideal_cycle_seconds,
                  total_units, good_units):
    """Return unrounded ratios; minutes are converted to seconds for performance.

    A zero denominator makes the corresponding ratio undefined, so this function
    raises ValueError instead of inventing a percentage. Performance is not capped.
    """
    for name, value in (
        ("planned_minutes", planned_minutes),
        ("run_minutes", run_minutes),
        ("ideal_cycle_seconds", ideal_cycle_seconds),
    ):
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise ValueError(f"{name} must be a finite positive number")
        if not math.isfinite(value) or value <= 0:
            raise ValueError(f"{name} must be a finite positive number")
    for name, value in (("total_units", total_units), ("good_units", good_units)):
        if isinstance(value, bool) or not isinstance(value, int) or value < 0:
            raise ValueError(f"{name} must be a nonnegative integer")
    if run_minutes > planned_minutes:
        raise ValueError("run_minutes must not exceed planned_minutes")
    if total_units == 0:
        raise ValueError("total_units must be positive to calculate quality")
    if good_units > total_units:
        raise ValueError("good_units must not exceed total_units")

    availability = run_minutes / planned_minutes
    performance = ideal_cycle_seconds * total_units / (run_minutes * 60)
    quality = good_units / total_units
    return {
        "Availability": availability,
        "Performance": performance,
        "Quality": quality,
        "OEE": availability * performance * quality,
    }


if __name__ == "__main__":
    inputs = {
        "planned_minutes": 480,
        "run_minutes": 420,
        "ideal_cycle_seconds": 30,
        "total_units": 760,
        "good_units": 735,
    }
    for name, ratio in calculate_oee(**inputs).items():
        print(f"{name}: {ratio:.2%}")
