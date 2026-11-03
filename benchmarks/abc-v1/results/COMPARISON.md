# A/B/C comparison

| Group | Pass | Source lines | Runtime of 18 tests (ms, single run) |
|---|---:|---:|---:|
| A | 13/18 | 6 | 0.103 |
| B | 17/18 | 23 | 0.261 |
| C | 18/18 | 33 | 0.123 |

A fails quantity zero, fractional quantity, duplicate supplier, nonfinite unit input, and HALF_UP rounding. B fails duplicate supplier. C passes all 18 tests.

C's extra 10 lines vs B are not proof of superior efficiency. Millisecond results fluctuate and should not be compared for speed. No AI token count or actual agent development time was captured. Single-task, single-implementation-per-group experiment; cannot generalize or attribute to the skills themselves.
