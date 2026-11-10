# Swiss school-personnel route: reuse V170/V171 evidence

The current BFS asset page still links the2024/25 school-personnel workbook, asset36478952. A fresh response is byte-identical to [the V170 original](../task4_v170_zurich/bfs_staff_2024_25_original.xlsx). The2024/25 SSP handbook, asset32010182, is byte-identical to [the V171 original](../task4_v171_bfs_scope/bfs_SSP_2024_25_manual_original.pdf). Their new receipts point to those existing bodies; duplicate files are not retained. This follow-up adds no teacher measurement or new source product.

The current selected-route index had omitted these two prior reviews. Adding them changes the next acquisition action: check their source scope and unresolved conditions before searching for or downloading the same products again. The [V170 review](../task4_v170_zurich/README.md) and [V171 methodology review](../task4_v171_bfs_scope/README.md) remain intact; their historical scientific/manuscript version labels describe their own stage.

## What the retained sources establish

- The full workbook differs from the public-only PxWeb cube. T10 contains national public teacher FTE86866.4 (`J7`) and private teacher FTE10242.2 (`J11`), including private unallocated-stage FTE3453.2 (`I11`). The last quantity is inside the total, not a missing-teacher count. These values were already verified in V170.
- T8 is public-only by canton; Zürich all-stage FTE13797.7 is `H7`. T11 separately covers school leadership. A national all-stage total can be considered as a deliberately broad candidate enclosing population; it need not equal a city-specific ratio. The inclusion and publication precision must nevertheless support an upper bound before it is used in one.
- The national handbook defines reporting of public/private school teaching activities, school locations and postholders. Temporary replacements for occupied posts are not counted as additional teaching posts. FTE uses activity workload divided by the corresponding full-time basis (`C.7/C.8`), with matching units. This is the SSP workload statistic, distinct from a STATENT wage-model estimate.
- Handbook physical/printed pages6,9–10,19–20 describe reporting responsibilities, teaching scope, reference days and FTE units. The primary/secondary reference day is chosen by the canton between school-year start and31December; the handbook requests coordination with pupil statistics rather than certifying identical dates for every published table.
- The existing city pupil subtotal8581 is upper-secondary Mittelschule pupils, public plus private, in the school year starting2024. It is a positive subset excluding vocational schools, not a complete city pupil total. Its nominal school-year label agrees with2024/25, so a generic year-mismatch objection would be inaccurate. Exact reference-day and target teaching/post scope still need matching evidence.

## Current eligibility decision

No teacher cap or utility bound is admitted. The numerical public/private totals and the compulsory census design support further examination, but the selected evidence does not certify complete actual inclusion of every target2024/25 activity, a single-sided reporting/estimation envelope, or an outward numerical precision rule. This is an unresolved guarantee, not a finding that the published totals are wrong or incomplete. The older Eurostat private-coverage warning does not itself invalidate a different BFS publication. Missing qualification cells in T9 also do not prove that T10's totals omit those people.

Zurich's primary `upper_secondary_ptr` remains `[0,1]`. We do not compute a city ratio by pairing these totals or invent a rounding margin. No provider was contacted. The original user CSV, scientific bounds, model weights, manuscript and PDF remain unchanged. [Verification](../../results/current_swiss_staff_scope_review/verification.json) checks fresh receipt reuse, selected raw workbook cells and handbook definitions, alongside existing scientific/manuscript bindings; it does not convert those checks into source-completeness certification.

## Download-before-repeat check

Before a source request, search the research data and design notes for its exact URL, official asset identifier, basename and likely provider terms. For this route:

```bash
rg -l '36478952|32010182|bfs_staff_2024_25|SSP_2024_25_manual' research/2026-a/data research/2026-a/design --glob '*.json' --glob '*.md' --glob '*.py'
```

Read the matching scope and reopening condition. A new access timestamp, portal layout or repeated download is not a new observation. Current route lists are selected navigation, not an exhaustive catalogue of historical acquisition. Reopen this route with actual resolution of the remaining inclusion, reference and numerical-bound conditions.
