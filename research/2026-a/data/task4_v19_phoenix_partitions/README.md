# Phoenix: disjoint subgroup information under overlapping school records

The 96 previously matched schools' official Arizona FY2025 graduation responses contain subgroup counts that the earlier All-group calculation did not use. This extraction reuses those exact archived responses; it adds no new survey respondents or downloaded observations. Each source file and the school-selection tables are hashed in `source_hashes.json`.

The most informative partition is race/ethnicity. Within each category take the largest school lower count, then sum categories. Conditional on mutually exclusive and stable person-level categories across records, the unique graduate lower bound increases from 655 to 1,056, and the non-graduate lower bound from 263 to 279. School memberships themselves may overlap arbitrarily.

| Category | Graduate lower bound | Witness school ID | Non-graduate lower bound | Witness school ID |
| --- | ---: | ---: | ---: | ---: |
| African American | 92 | 5448 | 27 | 80990 |
| Hispanic | 480 | 5437 | 160 | 969999 |
| Native American | 25 | 89571 | 13 | 89571 |
| White | 459 | 79268 | 79 | 80025 |
| Asian, Multiple Races, Pacific Islander | 0 each | No positive bound | 0 each | No positive bound |

Female/Male category maxima sum to the previous 655/263 and add no information. The two partition totals are combined by maximum, never added together. Missing and suppressed counts remain unknown; no negative suppression marker becomes a count. Categories need not exhaust All: unclassified students remain outside the partition and cannot be silently assigned a label.

## Assumptions and official definitions

The ADE [CNA Graph User Manual 2025](https://www.azed.gov/sites/default/files/2025/12/CNA%20Graph%20User%20Manual%202025.pdf), section 10, explicitly describes exclusive ethnicity groups in graduation reporting. Its example covers the 2024 five-year cohort. That supports the reporting categories but does not establish that one person has the same label across every duplicated record in the four-year API used here. See the [source audit](../task4_v19_phoenix_county/source_audit.json) for evidence type and scope; original PDF bytes were not obtained.

Global admission remains false. The conditional bounds also inherit consistent graduate status within the same statewide cohort, the selected public-school target, and unresolved current-versus-2024 school locations. A county aggregate could tighten the statewide upper bounds only if it shared this scope and actually contained the target. The official county workbook download failed, so no county number replaces the state counts.

## Formula

For outcome type T (graduate or non-graduate), let a_s be a school's All-group lower count and b_sr its lower count for category r. Under stable categories:

    T_lower = max(max_s a_s, sum_r max_s b_sr).

If delta bounds extra category memberships caused by cross-record label changes, the valid bound is:

    T_lower(delta) = max(max_s a_s, sum_r max_s b_sr - delta).

Delta counts excess distinct category memberships, not schools or ordinary duplicate rows. One person reported in three distinct categories contributes two; repeated records in one category contribute zero. Separate budgets apply to graduates and non-graduates. No such budget has been empirically estimated; delta=0 is a condition, not a new observation. With no label-consistency restriction retain the old All-only bound.

Using state graduates G_state=74,261 and non-graduates F_state=20,240:

    q_lower = G_lower/(G_lower + F_state)
    q_upper = G_state/(G_state + F_lower).

Stable-label scenario: [0.0495867769,0.9962570432]; unrestricted-label baseline: [0.0313472123,0.9964709355]. This is a partial-identification interval for the inherited school target, not an estimated city graduation rate or a confidence interval.

Run `python3 research/2026-a/data/task4_v19_phoenix_partitions/extract.py`. Full model comparison and validation are in [V19 results](../../results/task4_v19_partition_outcomes/README.md).
