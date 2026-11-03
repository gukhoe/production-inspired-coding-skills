"""Calculate OEE; run with no arguments for the supplied example."""

import json
import math
import sys


EXAMPLE = {
    "planned_minutes": 480,
    "run_minutes": 420,
    "ideal_cycle_seconds": 30,
    "total_units": 760,
    "good_units": 735,
}


def calculate_oee(planned_minutes, run_minutes, ideal_cycle_seconds,
                  total_units, good_units):
    """Return fractional A/P/Q/OEE values (multiply by 100 for percent).

    Run time and total production must be positive because otherwise the
    individual Performance or Quality ratios are undefined. Performance is
    not capped at 100%, so an inconsistent ideal cycle remains visible.
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
    if run_minutes > planned_minutes:
        raise ValueError("run_minutes must not exceed planned_minutes")
    if total_units == 0:
        raise ValueError("total_units must be positive to calculate Quality")
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


def main():
    if len(sys.argv) > 2:
        raise ValueError("Usage: python3 oee.py [JSON-input]")
    inputs = json.loads(sys.argv[1]) if len(sys.argv) == 2 else EXAMPLE
    for name, ratio in calculate_oee(**inputs).items():
        print(f"{name}: {ratio * 100:.4f}%")


if __name__ == "__main__":
    main()
