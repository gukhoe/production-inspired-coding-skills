def evaluate(quotes, quantity):
    results = []
    for q in quotes:
        total = (q['unit_price'] * quantity + q.get('freight', 0)) * (1 + q.get('duty_rate', 0)) + q.get('tooling', 0)
        results.append({'supplier': q['supplier'], 'total': round(total, 2)})
    return min(results, key=lambda x: x['total'])
