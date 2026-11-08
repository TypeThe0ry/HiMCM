# V107 Mexico City: relax the lower-to-upper-secondary progression assumption

The age14–18 travel-utility identification interval widens from **[0.283284, 0.543641]** to **[0.235342, 0.591740]**. This revision changes membership assumptions using the same 2020 census sample; it does not estimate a measured error rate or introduce newly collected trips.

The source records completed education rather than directly observed current school stage. Its metadata explicitly says that during holidays after a school cycle, the reported grade/level is the one just approved. Attending respondents with three completed lower-secondary grades therefore do not directly establish current upper-secondary enrollment. V107 makes those records optional members. The earlier interpretation of levels4/5/7 with completed grades0–2 remains conditional, so this is a targeted relaxation, not complete elimination of stage assumptions.

| Group | Sample records | Expanded survey weight |
|---|---:|---:|
| Retained conditional upper-secondary members | 5,590 | 188,069 |
| Completed lower-secondary transition, now optional | 3,627 | 117,497 |
| Previously optional age/attendance/stage records | 86 | 2,202 |

All 3,627 transition records encode completed grade as `03`; numerical parsing is essential. Unknown-age records remain optional under the existing rule. No student identity fields are emitted.

## Independent verification

`independent_audit.py` reads the original ZIP independently, checks all276,007 person records for source geography and uniqueness, and reproduces the three groups without importing the production classifier or interval implementation. It verifies the reused source hashes and holiday/last-approved metadata clauses, then exactly reproduces V72's earlier groups, counts and interval.

For utility endpoints `u(t)=exp(-t/30)`, each optional time-bin mass may be included or excluded. The resulting mean is a linear-fractional function over a box with a strictly positive fixed denominator. Its extrema occur at vertices. The audit enumerates **64 old and256 revised inclusion vertices per endpoint**, independently of the production prefix algorithm. Both intervals agree with absolute discrepancy **0.0**. Unknown travel bins retain utility[0,1]; the same observed duration-bin closures are used before and after.

Run from the repository root:

```sh
python3 research/2026-a/data/task4_v107_mexico_membership/independent_audit.py
```

These are weighted-sample identification bounds, not sampling confidence intervals. Optional membership is assigned no probability. No city ranking, model registry or manuscript is changed by this source package.
