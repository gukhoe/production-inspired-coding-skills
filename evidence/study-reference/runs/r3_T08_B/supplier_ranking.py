"""공급사의 가격·품질·납기 점수를 가중합하여 내림차순으로 정렬한다."""

INPUT = {
    "weights": {"price": 0.5, "quality": 0.3, "delivery": 0.2},
    "suppliers": [
        {"name": "A", "price": 80, "quality": 90, "delivery": 95},
        {"name": "B", "price": 92, "quality": 82, "delivery": 88},
        {"name": "C", "price": 85, "quality": 94, "delivery": 80},
    ],
}


def rank_suppliers(data):
    """점수는 높을수록 좋으며, 동점인 공급사는 입력 순서를 유지한다."""
    weights = data["weights"]
    results = [
        {
            "name": supplier["name"],
            "score": sum(
                supplier[criterion] * weights[criterion]
                for criterion in ("price", "quality", "delivery")
            ),
        }
        for supplier in data["suppliers"]
    ]
    return sorted(results, key=lambda result: result["score"], reverse=True)


def main():
    print("순위 | 공급사 | 가중합 점수")
    for position, result in enumerate(rank_suppliers(INPUT), start=1):
        print(f"{position} | {result['name']} | {result['score']:.1f}")


if __name__ == "__main__":
    main()
