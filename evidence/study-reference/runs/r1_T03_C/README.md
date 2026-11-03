# Production balance

Inputs: daily production capacity, number of working days, and demand for the same period. The executable uses the supplied values: 450, 20, and 9200.

Outputs: total production and the applicable shortage, surplus, or exact-match message. Total production is daily capacity multiplied by working days. Shortage and surplus are nonnegative; at most one is positive. Total production + shortage - surplus equals demand.

Acceptance example: 450 × 20 = 9000, giving a shortage of 200 against demand of 9200. Targeted tests also cover surplus and an exact match.

Scope: arithmetic calculation with the given numeric inputs. Inventory, scheduling, variable daily production, and input interfaces are outside this request.

Run the example:

```sh
python3 runlog.py --kind example -- python3 production.py
```

Run verification:

```sh
python3 runlog.py --kind test -- python3 -m unittest -v test_production.py
```
