"""생산량과 불량 수량으로 불량률과 양품 수량을 계산합니다."""


def calculate_quality(produced: int, defective: int) -> tuple[float, int]:
    if type(produced) is not int or type(defective) is not int:
        raise TypeError("수량은 정수여야 합니다.")
    if produced <= 0:
        raise ValueError("생산량은 0보다 커야 합니다.")
    if not 0 <= defective <= produced:
        raise ValueError("불량 수량은 0 이상 생산량 이하여야 합니다.")
    return defective / produced * 100, produced - defective


def main() -> None:
    inputs = {"produced": 2500, "defective": 75}
    defect_rate, good_quantity = calculate_quality(**inputs)
    print(f"생산량: {inputs['produced']}개")
    print(f"불량 수량: {inputs['defective']}개")
    print(f"불량률: {defect_rate:.2f}%")
    print(f"양품 수량: {good_quantity}개")


if __name__ == "__main__":
    main()
