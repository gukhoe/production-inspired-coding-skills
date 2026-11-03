from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

def _decimal(value, field):
    if isinstance(value, bool): raise ValueError(f'{field}: boolean invalid')
    try: d = Decimal(str(value))
    except (InvalidOperation, TypeError, ValueError): raise ValueError(f'{field}: invalid number')
    if not d.is_finite(): raise ValueError(f'{field}: nonfinite number')
    return d

def evaluate(quotes, quantity):
    # SOR: quantity is positive integer, duty is decimal fraction, quotes nonempty.
    # PFMEA: nonfinite amounts, invalid quantity, duplicate supplier, invalid duty,
    #         unexpected mutation, and equal-cost ordering are explicit failure modes.
    qty = _decimal(quantity, 'quantity')
    if qty <= 0 or qty != qty.to_integral_value(): raise ValueError('quantity: positive integer required')
    if not isinstance(quotes, (list, tuple)) or not quotes: raise ValueError('quotes: nonempty list required')
    seen = set(); results = []
    for q in quotes:
        if not isinstance(q, dict): raise ValueError('quote: mapping required')
        supplier = q.get('supplier')
        if not isinstance(supplier, str) or not supplier.strip(): raise ValueError('supplier: nonempty string required')
        supplier = supplier.strip()
        if supplier.casefold() in seen: raise ValueError('supplier: duplicate')
        seen.add(supplier.casefold())
        unit = _decimal(q.get('unit_price'), 'unit_price')
        freight = _decimal(q.get('freight', 0), 'freight')
        duty = _decimal(q.get('duty_rate', 0), 'duty_rate')
        tooling = _decimal(q.get('tooling', 0), 'tooling')
        if any(v < 0 for v in (unit, freight, duty, tooling)): raise ValueError('negative amount')
        if duty > 1: raise ValueError('duty_rate: expected fraction between 0 and 1')
        total = ((unit * qty + freight) * (1 + duty) + tooling).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        results.append({'supplier': supplier, 'total': total})
    return min(results, key=lambda x: (x['total'], x['supplier'].casefold()))
