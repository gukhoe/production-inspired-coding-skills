"""생산량과 불량 수량으로 불량률(%)과 양품 수량을 계산한다.

입력 범위: produced > 0, 0 <= defective <= produced인 정수 수량.
검증 예: produced=2500, defective=75 -> 불량률 3%, 양품 2425개.
파일 입력, 저장, 사용자 인터페이스는 이 프로그램의 범위에 포함하지 않는다.
"""


def calculate_quality(produced: int, defective: int) -> tuple[float, int]:
    """불량률(%)과 양품 수량을 반환한다."""
    defect_rate = defective / produced * 100
    good_quantity = produced - defective
    return defect_rate, good_quantity


def main() -> None:
    inputs = {"produced": 2500, "defective": 75}
    defect_rate, good_quantity = calculate_quality(**inputs)
    print(f"생산량: {inputs['produced']}개")
    print(f"불량 수량: {inputs['defective']}개")
    print(f"불량률: {defect_rate:.2f}%")
    print(f"양품 수량: {good_quantity}개")


if __name__ == "__main__":
    main()
