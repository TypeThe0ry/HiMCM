# Santiago EOD2012: acquired research mirror, pending admission

Four real Parquet tables downloaded from PLUMAS-research/palomatrix-dtpm, observed repository commit38cf073e28e0cc42aad271b8df7b228dff1c66cf. SHA256 and exact download URLs are in manifest.json. Parsed counts:18,264 households;60,054 persons;113,591 trips;1,200 code definitions. schema.json and codebook.csv are derived directly from the archived tables.

Provenance: the archived mirror conversion script downloads https://dcc.uchile.cl/~egraells/gds-data/eod2012.tgz (University of Chile mirror). These are converted research-hosted copies, not bytes fetched directly from SECTRA. The converter joins age and trip dissemination/distance fields; conversion provenance must be checked before assuming raw-field equivalence. Repository code was read, not executed.

Official survey source: https://www.sectra.gob.cl/info-territorial/region-metropolitana-de-santiago/ ; survey is Gran Santiago2012. A later official recalibration procurement exists; current mirror weight vintage is not yet verified. Do not call these current measurements or substitute metropolitan scope for Santiago municipality.

Candidate fields: household Comuna, person Estudios/Curso/Actividad/DondeEstudia, trip Proposito/HoraIni/HoraFin/TiempoViaje/CodigoTiempo, day-specific person and trip weights. Validate current upper-secondary enrolment vs attainment, home-to-school direction, unique person-day, time units/missing codes and weight vintage before extraction. No new city observation is admitted in this commit.

Parsing environment: /tmp/himcm-parquet-arm/bin/python, isolated Homebrew Python venv with pandas and pyarrow. Default x86 Python lacked a Parquet engine; no global installation was changed. All four files begin with PAR1 and pandas.read_parquet succeeded.

Current model unchanged: S=100 sqrt(B)/(sqrt(A)+sqrt(B)), B=sum(w*u²), A=sum(w*(1-u)²), u within evidence intervals. Main/aux weights (1-alpha)/8 and alpha/2. No rank rerun for unchanged model inputs; last validated possible-champion set remains25 cities.

## Raw CSV verification

Acquired real University Chile eod2012.tgz (9,445,461bytes) from the converter's documented source. audit_raw.py verifies unique keys and equality of17 core fields covering geography, activity, education, timestamps, trip duration and weights against archived Parquet. UTF-8-sig is required; interpreting source CSV as Latin1 corrupts accented municipality names and correctly fails equality checks. SHA256 is in raw_verification.json.

Provisional filter Actividad containing B, DondeEstudia=4, Estudios in{5,7} yields3,096 persons in the metro survey but only67 with household Comuna=SANTIAGO. Comuna in household data is TEXT, not numeric code70 from the parameter lookup; using70 would incorrectly produce zero. This is a classification diagnostic, not verified current high-school enrollment. Original questionnaire wording for Estudios/Curso remains unlocated; historical categories in the education codebook reinforce the need to distinguish attainment and current enrollment.

No model admission or rank update. The raw archive includes CSVs and parameter tables but no questionnaire. Next extraction must preserve person-day denominators and missing journeys, identify home-to-school direction, and explicitly report the geography and conditional cohort. Do not extrapolate the67-person municipal candidate sample to metro-wide students.

## Conditional person-day commute extraction

extract_commute.py restricts the provisional cohort to normal-season working days and uses person Factor_LaboralNormal once per person (not trip expansion weights). It selects the first time-ordered study-purpose trip whose archived origin equals the household coordinate to1e-6 in source coordinate units. Valid positive duration and CodigoTiempo=0 are required. Unidentified home origin, no qualifying trip, questionable duration or unknown departure ordering retain utility[0,1]. This equality rule is intentionally strict; geocoding/jitter semantics remain unverified. It is not evidence that other students do not commute. No arbitrary spatial radius is introduced.

Results: metro1954 candidate persons,65 with accepted direct-trip duration; weighted utility[0.010543,0.981813]. Santiago comuna45 persons,1 accepted duration; weighted utility[0.012695,0.982495]. All candidate weights positive and observed. Formula T_L=sum(w_p*l_p)/sum(w_p), T_U=sum(w_p*h_p)/sum(w_p), observed l=h=exp(-minutes/30), unresolved l=0,h=1. These are sample-weighted missingness bounds, not design-based confidence intervals or contemporary population estimates.

Conditional classification,2012 vintage, geography and geocoding uncertainties prevent main-model admission. The separate task4_santiago_conditional.py scenario rerun changes no city decision rank; Santiago remains13 and25 cities remain possible champions. Its score width39.298 shrinks only to39.196 (metro scenario) or39.190 (comuna scenario). This does not establish a real model improvement. Main arrays are copied before scenario replacement and source observations stay unchanged.

Verification: household/person/trip keys unique; household join many-to-one; one audit row per candidate person-day; positive observed weights; ordered utility endpoints. No absence of recorded journey is assigned zero travel time. conditional_person_audit.csv contains pseudonymous source record identifiers and weights, no names or coordinates; original archive remains source evidence.

## Reported trip-chain audit

The preferred conditional extractor is now audit_trip_chain.py. It chooses the day's first study-purpose departure BEFORE testing the home origin, correcting the earlier order that could skip an unconfirmed earlier study trip. Tied first departures or missing trip order stay[0,1]. Home is confirmed either by archived coordinate equality or by the immediately preceding departure being a reported return-home trip, with arrival before departure and identical destination-to-origin coordinates. No radius threshold is used. Full-day and current-cohort semantics still require the questionnaire.

The chain confirms13 additional metro records and1 additional comuna record: identified durations78/1954 and2/45. Utility bounds become[0.014100,0.977592] metro and[0.017678,0.977771] comuna. These are conditional weighted missingness bounds, not population confidence intervals. Tests cover return-home chain acceptance, unconfirmed origin, tied departure, and earlier unidentified study trip; all passed.

Rerun python3 research/2026-a/scripts/task4_santiago_conditional.py --chain: no decision ranks change, Santiago13, possible champions25. Comuna score width39.2984→39.1534; metro39.2984→39.1671. Main observations remain unchanged.

New questionnaire lead (not yet fetched or verified): Ministry transport library catalog https://biblioteca.mtt.gob.cl/documento/28168c0a-d9d3-45b2-a1d7-25f702334b9d ; third-party directory links a report archive Drive ID13_j6G1vaG1acOuL-W5okvAEJ0aaGKO7e. Verify ownership/source and contents before relying on it; no questionnaire definition was established in this round.
