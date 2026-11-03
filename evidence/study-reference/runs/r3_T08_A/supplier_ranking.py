"""공급사의 가격·품질·납기 점수를 가중합산하여 순위를 출력합니다."""

INPUT_DATA = {
    "weights": {"price": 0.5, "quality": 0.3, "delivery": 0.2},
    "suppliers": [
        {"name": "A", "price": 80, "quality": 90, "delivery": 95},
        {"name": "B", "price": 92, "quality": 82, "delivery": 88},
        {"name": "C", "price": 85, "quality": 94, "delivery": 80},
    ],
}


def rank_suppliers(data):
    """높을수록 좋은 점수로 계산합니다. 동점은 입력 순서를 유지합니다."""
    weights = data["weights"]
    results = [
        {
            "name": supplier["name"],
            "score": sum(supplier[criterion] * weight
                         for criterion, weight in weights.items()),
        }
        for supplier in data["suppliers"]
    ]
    return sorted(results, key=lambda result: result["score"], reverse=True)


def main():
    print("순위 | 공급사 | 가중합 점수")
    for rank, supplier in enumerate(rank_suppliers(INPUT_DATA), start=1):
        print(f"{rank} | {supplier['name']} | {supplier['score']:.2f}")


if __name__ == "__main__":
    main()
