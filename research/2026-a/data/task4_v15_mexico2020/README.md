# Mexico City 2020: official microdata, year replacement and uncertain school-stage membership

The official INEGI2020 expanded-questionnaire ZIP is now archived (10,295,515 bytes), together with four variable dictionaries, the complete XLSX dictionary, official download catalog and survey metadata. SHA256 values and exact URLs are in manifest.json. The raw person table has276,007 unique records and expands to9,159,393 private-household residents across all16 CDMX boroughs. No adult work commute or generic city travel proxy is used.

## What is observed and what is reconstructed

The2020 questionnaire asks current school attendance, completed educational stage/grade and usual direct home-to-school time. ASISTEN=1 means attending in2020, whereas the2015 yes code was5. Current stage is **not directly observed**. The same conditional progression reconstruction used for the officially replicated2015 EMS table is retained: completed secondary grade3, or completed0–2 years at levels4/5/7, among current attenders. The2020 dictionary independently confirms these level meanings and the completed-grade question. Repetition, alternative course lengths and switching programs can violate this reconstruction; the model does not estimate that misclassification.

The2015 filter was audited: it already combined attendance with completed grade and reproduced all five official EMS travel bins. It was not a naive use of highest education alone. It remains a conditional reconstruction, and its official-tabulation match does not prove individually correct current enrollment.

Times are household-adult proxy reports of direct home-to-school duration, including access/wait/transfer time and excluding incidental stops. If the respondent normally starts elsewhere, the question asks the hypothetical direct trip from home. These are not GPS records or necessarily a trip made on the survey day. Collection was March2–27,2020, with reference date March15, during the onset of COVID disruption; no2026 current-condition claim is made.

## Real extracted counts

| Scope | Classified sample rows | Expanded classified students | Time codes1,2,3,4,5,6,9 |
| --- | ---: | ---: | --- |
| Age3–17 | 7,655 | 253,889 | 48,914;85,840;83,336;30,856;2,284;2,475;184 |
| All-age school-stage reconstruction | 11,293 | 374,756 | 67,823;122,786;118,938;46,802;3,581;14,543;283 |

The classified all-age sample spans14–85, so it includes adult education and must not be described as an adolescent sample. Neither cohort uses age alone to identify school stage. Unknown-age codes do not occur in the classified samples. Codes6 (no school trip, including distance learning) and9 (unspecified time) retain utility[0,1]. Valid duration bins are<=15,16–30,31–60,>60–120 and>120 minutes, with conservative continuous closures[0,15],[15,30],[30,60],[60,120],[120,infinity].

For n_k students in each time bin, m unknown-duration students and total N, utility u=exp(-t/30) gives L=sum(n_k exp(-b_k/30))/N and U=(sum(n_k exp(-a_k/30))+m)/N. No midpoints, uniform distributions or half-roundtrip assumption are used. These are weighted sample identification bounds, not design-based confidence intervals.

## New method: retain uncertain stage membership

Current attenders with unspecified stage or grade expand to8,665 persons in the younger scope and10,628 in the all-age scope. They are not automatically dropped or declared high-school students. Their existing travel-bin information is retained. The optional pool intentionally includes every unspecified stage/grade case and may therefore be overinclusive. Unknown-attendance cases are outside this known-attender analysis; these bounds do not cover every potentially enrolled person.

Let the classified group have total weight N and utility numerator interval[A,B]. Optional person/group i has expansion weight w_i and utility interval[a_i,b_i]; z_i in{0,1} indicates possible membership. Compute:

    L = min_z (A + sum_i z_i*w_i*a_i)/(N + sum_i z_i*w_i)
    U = max_z (B + sum_i z_i*w_i*b_i)/(N + sum_i z_i*w_i).

For the minimum, sort a_i ascending and evaluate all prefixes including empty; for the maximum, sort b_i descending. At an optimum, adding an omitted endpoint below the current lower ratio or removing an included endpoint above it would improve the objective; hence a sorted prefix suffices. Equal endpoints may be grouped despite unequal positive weights. This is exact for the specified independent inclusion choices, not for unknown population constraints or reconstruction errors. Bounds may use different member sets. Open duration bins produce closure bounds rather than necessarily attained endpoints.

| Scope | Classified-only bound | Unknown stage retained | Coarse bound discarding optional travel information |
| --- | --- | --- | --- |
| Age3–17 | [0.287882,0.545565] | [0.286762,0.554445] | [0.278381,0.560563] |
| All age | [0.275542,0.553098] | [0.274197,0.559361] | [0.267943,0.565423] |

Retaining membership uncertainty widens the classified-only bounds appropriately. Exploiting the optional students' actual travel bins reduces width by5.14% and4.14%, respectively, relative to treating their utilities as entirely unknown. This reduction comes from measured information, not a reduced missingness assumption.

## Recomputed model comparison

`../../results/task4_v15_mexico2020/` contains25-city ranks with all other V7 criteria and weights fixed. The2020 value **replaces** the2015 Mexico travel cell in each scenario. Different years are never intersected; none of the four2020 intervals is nested inside the2015 interval.

| Version/scope | Mexico decision rank | Mexico total score interval width | Possible champions |
| --- | ---: | ---: | ---: |
| 2015 classified minors baseline | 21 | 43.2788 | 25 |
| 2020 classified minors | 20 | 43.1413 | 25 |
| 2020 minors, uncertain stage retained | 20 | 43.2566 | 25 |
| 2020 classified all-age students | 21 | 43.3304 | 25 |
| 2020 all-age, uncertain stage retained | 21 | 43.4155 | 25 |

The minors comparison changes two decision ranks; the all-age extension changes none. All25 cities also remain possible over continuous auxiliary weights alpha=[.05,.2]. The newer evidence does not identify a champion or prove causal improvement in travel. The2015 baseline remains preserved for reproducibility; these explicitly labeled2020 comparisons do not silently change existing historical analyses.

Current TOPSIS S=100 sqrt(sum(w*u²))/(sqrt(sum(w*u²))+sqrt(sum(w*(1-u)²))). Main weights are(1-alpha)/8, auxiliary alpha/2, defaultalpha=.1. Score bounds L_i,U_i yield possible champions U_i>=max(k!=i)L_k and worst regret max(0,max(k!=i)U_k-L_i).

## Validation and reproduction

All source hashes,276,007 person IDs, entity codes, positive weights and16 boroughs are checked. A second agent independently reproduced both scopes' seven weighted bins and sample counts. Tests verify the changed attendance coding, preservation of optional rather than mandatory membership, and exhaustive subset extrema for both real optional pools. An independent mathematical review checked2,000 random cases and106,210 subset combinations. New cohort-uncertainty bounds contain classified-only bounds and are contained in the coarse optional-information envelope.

```sh
python3 research/2026-a/data/task4_v15_mexico2020/extract_commute.py
python3 research/2026-a/data/task4_v15_mexico2020/test_membership.py
python3 research/2026-a/scripts/task4_mexico2020_comparison.py
```
