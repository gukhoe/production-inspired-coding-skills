"""Calculate OEE from production time and unit counts using standard Python."""

import math


def calculate_oee(planned_minutes, run_minutes, ideal_cycle_seconds,
                  total_units, good_units):
    """Return Availability, Performance, Quality and OEE as fractions.

    Run time and total production must be positive because they are denominators.
    Performance is not capped: values above 1 can flag an inaccurate ideal cycle.
    """
    for name, value in (
        ("planned_minutes", planned_minutes),
        ("run_minutes", run_minutes),
        ("ideal_cycle_seconds", ideal_cycle_seconds),
    ):
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise ValueError(f"{name} must be a number")
        if not math.isfinite(value) or value <= 0:
            raise ValueError(f"{name} must be finite and greater than zero")
    for name, value in (("total_units", total_units), ("good_units", good_units)):
        if isinstance(value, bool) or not isinstance(value, int):
            raise ValueError(f"{name} must be an integer")
    if run_minutes > planned_minutes:
        raise ValueError("run_minutes cannot exceed planned_minutes")
    if total_units <= 0:
        raise ValueError("total_units must be greater than zero")
    if not 0 <= good_units <= total_units:
        raise ValueError("good_units must be between zero and total_units")

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
    for metric, fraction in calculate_oee(**inputs).items():
        print(f"{metric}: {fraction:.2%}")
