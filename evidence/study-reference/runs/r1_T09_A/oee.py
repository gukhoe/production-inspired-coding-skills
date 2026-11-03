"""설비의 Availability, Performance, Quality 및 OEE 계산."""


def calculate_oee(planned_minutes, run_minutes, ideal_cycle_seconds,
                  total_units, good_units):
    """각 지표를 0~1 비율로 반환한다. 분과 초의 단위를 맞춰 계산한다."""
    if planned_minutes <= 0 or run_minutes <= 0 or total_units <= 0:
        raise ValueError("계획 시간, 가동 시간, 총 생산 수량은 양수여야 합니다.")
    if run_minutes > planned_minutes:
        raise ValueError("가동 시간은 계획 시간을 초과할 수 없습니다.")
    if ideal_cycle_seconds <= 0 or not 0 <= good_units <= total_units:
        raise ValueError("이상 사이클은 양수이고 양품 수량은 0~총 생산 수량이어야 합니다.")

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
    for name, value in calculate_oee(**inputs).items():
        print(f"{name}: {value:.2%}")
