# Santiago EOD2012: acquired research mirror, pending admission

Four real Parquet tables downloaded from PLUMAS-research/palomatrix-dtpm, observed repository commit38cf073e28e0cc42aad271b8df7b228dff1c66cf. SHA256 and exact download URLs are in manifest.json. Parsed counts:18,264 households;60,054 persons;113,591 trips;1,200 code definitions. schema.json and codebook.csv are derived directly from the archived tables.

Provenance: the archived mirror conversion script downloads https://dcc.uchile.cl/~egraells/gds-data/eod2012.tgz (University of Chile mirror). These are converted research-hosted copies, not bytes fetched directly from SECTRA. The converter joins age and trip dissemination/distance fields; conversion provenance must be checked before assuming raw-field equivalence. Repository code was read, not executed.

Official survey source: https://www.sectra.gob.cl/info-territorial/region-metropolitana-de-santiago/ ; survey is Gran Santiago2012. A later official recalibration procurement exists; current mirror weight vintage is not yet verified. Do not call these current measurements or substitute metropolitan scope for Santiago municipality.

Candidate fields: household Comuna, person Estudios/Curso/Actividad/DondeEstudia, trip Proposito/HoraIni/HoraFin/TiempoViaje/CodigoTiempo, day-specific person and trip weights. Validate current upper-secondary enrolment vs attainment, home-to-school direction, unique person-day, time units/missing codes and weight vintage before extraction. No new city observation is admitted in this commit.

Parsing environment: /tmp/himcm-parquet-arm/bin/python, isolated Homebrew Python venv with pandas and pyarrow. Default x86 Python lacked a Parquet engine; no global installation was changed. All four files begin with PAR1 and pandas.read_parquet succeeded.

Current model unchanged: S=100 sqrt(B)/(sqrt(A)+sqrt(B)), B=sum(w*u²), A=sum(w*(1-u)²), u within evidence intervals. Main/aux weights (1-alpha)/8 and alpha/2. No rank rerun for unchanged model inputs; last validated possible-champion set remains25 cities.
