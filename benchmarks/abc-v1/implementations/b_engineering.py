from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

def money(v):
    if isinstance(v, bool): raise ValueError('boolean is not a number')
    try: d = Decimal(str(v))
    except (InvalidOperation, TypeError, ValueError): raise ValueError('invalid number')
    if not d.is_finite(): raise ValueError('nonfinite number')
    return d

def evaluate(quotes, quantity):
    qty = money(quantity)
    if qty <= 0 or qty != qty.to_integral_value(): raise ValueError('quantity must be positive integer')
    if not quotes: raise ValueError('quotes required')
    results = []
    for q in quotes:
        supplier = q['supplier']
        if not isinstance(supplier, str) or not supplier.strip(): raise ValueError('supplier required')
        unit = money(q['unit_price']); freight = money(q.get('freight', 0)); duty = money(q.get('duty_rate', 0)); tooling = money(q.get('tooling', 0))
        if min(unit, freight, duty, tooling) < 0: raise ValueError('negative values forbidden')
        if duty > 1: raise ValueError('duty out of range')
        total = ((unit * qty + freight) * (1 + duty) + tooling).quantize(Decimal('.01'), rounding=ROUND_HALF_UP)
        results.append({'supplier': supplier, 'total': total})
    return min(results, key=lambda x: (x['total'], x['supplier']))
