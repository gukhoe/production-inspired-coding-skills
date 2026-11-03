from decimal import Decimal
import copy

def run(evaluate):
    base = [{'supplier':'Alpha','unit_price':'10.00','freight':'100','duty_rate':'0.1','tooling':'1000'}, {'supplier':'Beta','unit_price':'11.00','freight':'0','duty_rate':'0','tooling':'0'}]
    def throws(quotes, qty):
        try: evaluate(quotes, qty)
        except (ValueError, TypeError, KeyError, ArithmeticError): return True
        return False
    cases = {
        'correct_winner': lambda: evaluate(base, 100)['supplier']=='Beta',
        'correct_total': lambda: Decimal(str(evaluate(base, 100)['total']))==Decimal('1100.00'),
        'quantity_zero': lambda: throws(base,0),
        'quantity_negative': lambda: throws(base,-1),
        'quantity_fractional': lambda: throws(base,1.5),
        'empty_quotes': lambda: throws([],100),
        'negative_unit': lambda: throws([dict(base[0],unit_price=-1)],100),
        'negative_freight': lambda: throws([dict(base[0],freight=-1)],100),
        'duty_over_one': lambda: throws([dict(base[0],duty_rate=1.2)],100),
        'nan_unit': lambda: throws([dict(base[0],unit_price='NaN')],100),
        'boolean_quantity': lambda: throws(base,True),
        'duplicate_supplier': lambda: throws([base[0],dict(base[0],supplier='alpha')],100),
        'empty_supplier': lambda: throws([dict(base[0],supplier=' ')],100),
        'tie_deterministic': lambda: evaluate([{'supplier':'Z','unit_price':10},{'supplier':'A','unit_price':10}],1)['supplier']=='A',
        'no_input_mutation': lambda: (lambda original: (evaluate(base,100), base==original)[1])(copy.deepcopy(base)),
        'rounding_half_up': lambda: Decimal(str(evaluate([{'supplier':'A','unit_price':'0.005'}],1)['total']))==Decimal('0.01'),
        'nonfinite_infinity': lambda: throws([dict(base[0],unit_price='Infinity')],100),
        'negative_tooling': lambda: throws([dict(base[0],tooling=-1)],100),
    }
    out={}
    for name, fn in cases.items():
        try: out[name]={'pass':bool(fn())}
        except Exception as e: out[name]={'pass':False,'error':type(e).__name__+': '+str(e)[:160]}
    return out
