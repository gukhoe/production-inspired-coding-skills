"""공급사 평가 점수의 가중합을 계산하고 내림차순으로 정렬합니다."""
from decimal import Decimal


EXAMPLE = {
    "weights": {"price": 0.5, "quality": 0.3, "delivery": 0.2},
    "suppliers": [
        {"name": "A", "price": 80, "quality": 90, "delivery": 95},
        {"name": "B", "price": 92, "quality": 82, "delivery": 88},
        {"name": "C", "price": 85, "quality": 94, "delivery": 80},
    ],
}


def rank_suppliers(data):
    """가격·품질·납기는 모두 평가 점수이며 높을수록 좋습니다.

    동점인 공급사는 입력 순서를 유지합니다. Decimal로 소수 가중치를
    계산하여 이진 부동소수점 반올림 오차를 피합니다.
    """
    weights = {key: Decimal(str(value)) for key, value in data["weights"].items()}
    results = []
    for supplier in data["suppliers"]:
        score = sum(
            (Decimal(str(supplier[key])) * weight for key, weight in weights.items()),
            Decimal("0"),
        )
        results.append({"name": supplier["name"], "score": score})
    return sorted(results, key=lambda item: item["score"], reverse=True)


def main():
    print("가중합 = 가격 점수 × 0.5 + 품질 점수 × 0.3 + 납기 점수 × 0.2")
    for position, supplier in enumerate(rank_suppliers(EXAMPLE), start=1):
        print(f"{position}위: {supplier['name']} — {supplier['score']:.1f}점")


if __name__ == "__main__":
    main()
