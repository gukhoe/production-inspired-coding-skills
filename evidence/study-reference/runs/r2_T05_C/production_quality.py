"""생산량과 불량 수량으로 불량률(%)과 양품 수량을 계산합니다."""

import argparse


def calculate_quality(produced: int, defective: int) -> tuple[float, int]:
    """수량은 정수이며 생산량은 양수, 불량 수량은 0~생산량이어야 합니다."""
    if type(produced) is not int or type(defective) is not int:
        raise ValueError("수량은 정수여야 합니다.")
    if produced <= 0:
        raise ValueError("불량률 계산을 위해 생산량은 0보다 커야 합니다.")
    if not 0 <= defective <= produced:
        raise ValueError("불량 수량은 0 이상, 생산량 이하여야 합니다.")
    return defective / produced * 100, produced - defective


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--produced", type=int, required=True, help="생산량")
    parser.add_argument("--defective", type=int, required=True, help="불량 수량")
    args = parser.parse_args()
    try:
        defect_rate, good_quantity = calculate_quality(args.produced, args.defective)
    except ValueError as exc:
        parser.error(str(exc))
    print(f"불량률: {defect_rate:.2f}%")
    print(f"양품 수량: {good_quantity}개")


if __name__ == "__main__":
    main()
