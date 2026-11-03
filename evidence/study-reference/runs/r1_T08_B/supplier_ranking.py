"""공급사 점수에 가중치를 적용해 높은 점수부터 순위를 출력합니다."""
import json
import sys
from decimal import Decimal
from pathlib import Path


CRITERIA = ("price", "quality", "delivery")


def rank_suppliers(data):
    """가격을 포함한 모든 항목은 높을수록 좋은 점수입니다.

    동점인 공급사는 입력 순서를 유지합니다. 입력 데이터는 변경하지 않습니다.
    """
    weights = {key: Decimal(str(data["weights"][key])) for key in CRITERIA}
    results = []
    for supplier in data["suppliers"]:
        score = sum(
            (Decimal(str(supplier[key])) * weights[key] for key in CRITERIA),
            Decimal("0"),
        )
        results.append({"name": supplier["name"], "score": score})
    return sorted(results, key=lambda item: item["score"], reverse=True)


def main():
    input_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).with_name("input.json")
    with input_path.open(encoding="utf-8") as handle:
        data = json.load(handle, parse_float=Decimal)
    print("순위 | 공급사 | 가중합 점수")
    for rank, supplier in enumerate(rank_suppliers(data), start=1):
        print(f"{rank} | {supplier['name']} | {supplier['score']:f}")


if __name__ == "__main__":
    main()
