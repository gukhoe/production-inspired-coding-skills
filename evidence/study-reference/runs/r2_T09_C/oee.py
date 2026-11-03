"""Calculate OEE ratios and print percentages for the supplied production data.

Inputs: planned/run minutes, ideal cycle seconds, total/good unit counts.
Acceptance example: 480, 420, 30, 760, 735 yields OEE 76.5625%.
Scope: calculation and console output only; no storage or external services.
"""


def calculate_oee(planned_minutes, run_minutes, ideal_cycle_seconds,
                  total_units, good_units):
    """Return Availability, Performance, Quality and OEE as fractions."""
    if planned_minutes <= 0 or run_minutes <= 0 or total_units <= 0:
        raise ValueError("계획시간, 가동시간, 전체 생산수는 0보다 커야 합니다.")
    if run_minutes > planned_minutes:
        raise ValueError("가동시간은 계획시간을 초과할 수 없습니다.")
    if ideal_cycle_seconds <= 0 or not 0 <= good_units <= total_units:
        raise ValueError("이상 사이클은 양수, 양품수는 0 이상 전체 생산수 이하여야 합니다.")
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
        print(f"{name}: {ratio:.4%}")
