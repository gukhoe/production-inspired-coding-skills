"""Calculate equipment OEE; time inputs are minutes except cycle time (seconds)."""


def calculate_oee(planned_minutes, run_minutes, ideal_cycle_seconds,
                  total_units, good_units):
    """Return Availability, Performance, Quality, and OEE as fractions.

    Run time and production count must be positive because Performance and
    Quality are undefined when their respective denominators are zero.
    """
    if planned_minutes <= 0 or not 0 < run_minutes <= planned_minutes:
        raise ValueError("Require 0 < run_minutes <= planned_minutes.")
    if ideal_cycle_seconds <= 0:
        raise ValueError("ideal_cycle_seconds must be positive.")
    if total_units <= 0 or not 0 <= good_units <= total_units:
        raise ValueError("Require total_units > 0 and 0 <= good_units <= total_units.")

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
    for name, fraction in calculate_oee(**inputs).items():
        print(f"{name}: {fraction:.4%}")
