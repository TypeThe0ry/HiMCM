# Recovering school journeys through transport-related stops

Eight previously unknown journeys can be recovered from the existing RHTS 2010–2011 diary: seven known current high-school members and one optional member. Their intermediate activities are only transfer, passenger drop-off or passenger pick-up. The original 365 known and 37 optional direct journeys are unchanged. Known observed journeys therefore increase to 372; optional observed journeys to 38. No new respondent or new download is claimed.

## A purpose screen prevents false precision

Among 26 people whose first school-purpose trip began away from home, 23 have an earlier explicitly observed home departure. Fifteen of those chains include work, shopping, social or other activities. They remain diagnostic records and **do not update commute utilities**. For example, one optional member spends 480 minutes at work between travel segments; the full out-of-home episode lasts 600 minutes, versus 120 minutes of movement. Calling all 600 minutes school travel would change the measurement concept.

The conservative intermediate-purpose set is {4,5,6}, using the official manual's codes: 4 transfer/change travel mode;5 passenger drop-off;6 passenger pick-up. Code7 is fuel and code8 is drive-through service; neither is treated as transfer. This semantic rule is fixed before comparing rankings, not chosen to obtain a favorable rank. The remaining three known members have no visible home departure and keep [0,1].

## Reconstruction

For the same first school-purpose destination as V20, select the latest preceding trip explicitly marked ORIG_HOME=1. Activity code3 or equality of a transport-zone identifier is not proof of returning to one's own home. Two actual diagnostic chains illustrate this: an intermediate activity is coded3 but DEST_HOME and the following ORIG_HOME are both0.

Departure clocks are unfolded relative to the 03:00 diary boundary. Arrival time equals the unfolded departure plus the reported linked-trip duration. Require valid clocks and durations, no overlapping segments, increasing place sequence, one tour ID and no unresolved return-home flag within the chain. Place numbers need not be consecutive because linking may merge transfer legs. Do not impose an arbitrary dwell-time cap.

For transport-stop chains:

    T = arrival_at_first_school_purpose - last_observed_home_departure
      = sum(segment_durations) + sum(intermediate_dwell_times)
    u = exp(-T/30).

T includes transport-related waiting and passenger-service stops; it is not merely in-vehicle movement time. School-purpose codes retain V20's class/study or other-school-activity definition, not independent school-campus authentication. Historical age, roster membership, household sampling and reporting limitations remain unchanged.

| Household/person | Membership | Elapsed minutes | Movement | Dwell |
| --- | --- | ---: | ---: | ---: |
| 3204720/4 | known | 39 | 29 | 10 |
| 3325547/4 | known | 26 | 25 | 1 |
| 3331321/3 | known | 40 | 35 | 5 |
| 3373716/2 | known | 25 | 15 | 10 |
| 3439404/2 | known | 14 | 13 | 1 |
| 3513440/3 | known | 45 | 44 | 1 |
| 3952565/5 | known | 25 | 22 | 3 |
| 3735626/1 | optional | 85 | 83 | 2 |

These are anonymized public survey identifiers, used to reproduce the calculation. `chain_audit.csv` also retains rejected activity episodes and failure reasons; `student_journey_audit.csv` preserves all603 members and the unchanged weights.

## Bounds and verification

Optional-member ratio extrema are recomputed, followed by the same1,000 seeded county-stratified household bootstrap draws over all5,766 NYC households. The new identification interval and exploratory envelope are nested within V20 because only unknown journey utilities are resolved; population, weights and sampling draws are held fixed. This bootstrap remains exploratory, not official confidence coverage.

Independent raw-data reconstruction and fractional programming reproduce the all-age identification interval [.2292748683,.5438871635] and the under-19 interval [.2559764089,.4995663152]. Tests cover midnight, last departure after returning home, nonconsecutive place IDs, overlapping or invalid segment times, missing home records and long work stops. The extractor asserts every original direct journey is unchanged.

[Model results](../../results/task4_v21_nyc_chains/README.md). Source bytes remain in [V20](../task4_v20_nyc_travel/README.md); hashes are recorded in `summary.json`.
