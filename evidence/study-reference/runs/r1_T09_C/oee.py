"""Calculate Availability, Performance, Quality and OEE as ratios.

Inputs: planned/run minutes, ideal seconds per unit, total/good unit counts.
The executable example uses the requested inputs and prints percentages.
Expected example OEE: 0.765625 (76.5625%). No external dependencies or I/O
services are needed. Zero denominators are rejected as undefined ratios.
"""

import math


def calculate_oee(planned_minutes, run_minutes, ideal_cycle_seconds,
                  total_units, good_units):
    """Return unrounded ratios; performance is not capped at 100%."""
    for name, value in (("planned_minutes", planned_minutes),
                        ("run_minutes", run_minutes),
                        ("ideal_cycle_seconds", ideal_cycle_seconds)):
        if (isinstance(value, bool) or not isinstance(value, (int, float))
                or not math.isfinite(value) or value <= 0):
            raise ValueError(f"{name} must be a finite positive number")
    for name, value in (("total_units", total_units), ("good_units", good_units)):
        if isinstance(value, bool) or not isinstance(value, int):
            raise ValueError(f"{name} must be an integer")
    if run_minutes > planned_minutes:
        raise ValueError("run_minutes cannot exceed planned_minutes")
    if total_units <= 0 or not 0 <= good_units <= total_units:
        raise ValueError("require total_units > 0 and 0 <= good_units <= total_units")

    availability = run_minutes / planned_minutes
    performance = (ideal_cycle_seconds * total_units) / (run_minutes * 60)
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
    print(f"Availability (가동률): {result['availability']:.4%}")
    print(f"Performance (성능): {result['performance']:.4%}")
    print(f"Quality (양품률): {result['quality']:.4%}")
    print(f"OEE (설비종합효율): {result['oee']:.4%}")
