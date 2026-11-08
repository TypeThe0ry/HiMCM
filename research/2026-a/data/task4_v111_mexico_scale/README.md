# V111 Mexico: direct travel-scale re-evaluation

The script imports a fresh instance of the V108 fixed-weight design derivation and replaces only its time-bin utility endpoints with exp(-t/tau), for tau 15,20,30,45,60 minutes. Original files are unchanged. The full fixed family of nine prefixes per endpoint, including unobserved categories, remains. It derives each candidate ratio and Taylor standard error from the same published24-dimensional moments, then recomputes the V108 outer envelope with t3384 critical value. Tau30 matches V108 within1e-14.

Current-stage interpretation remains conditional; completed-secondary transition membership stays optional. Nontravel and unspecified-time codes retain[0,1]. Final nonresponse-adjusted weights are fixed, FPC omitted; no new confidence guarantee or simultaneous band over tau is asserted. This is direct re-evaluation of observed bin information, not a power transform of the existing mean utility interval. New observations:0.

Reproduce: `python3 derive.py`. Public moments are verified against the original manifest before use. Summary records the input moment hash, source-script hash and all candidate calculations. No personal records are read or emitted.
