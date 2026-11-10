# V195 Warsaw: two new source-file routes, no admission

Two newly targeted official files returned HTTP202 with zero-byte HTML responses. Neither a PPTX presentation nor a PDF report was obtained. The travel utility remains unknown; this package makes no numerical inference from search snippets and supplies no model update.

The routes were the city-hosted WBR2025 results presentation (`WBR Prezentacja -04.15 FINAL.pptx`) and the WBR2015 stageIV traffic-model report. The latter is a model-building report: even a successful download would require separating observed durations from calibrated network attributes before evaluating any empirical candidate. The WBR2025 presentation URL was discovered through a source link in an indexed AMRON article; its authenticity/content could not be checked because the official response contained no file.

`collect.py` records the actual status, content type, UTC request time, byte count and SHA256 in `retrievals.json`. The zero-byte responses are deliberately named `.bin`, rather than mislabelled as successful PPTX/PDF originals. `verify.py` verifies the archived responses and the explicit no-admission decision. Collection refuses to overwrite an existing capture and caps any download at20MB. Each route was attempted once, then skipped.

Earlier routes are not represented as new evidence. V132 already examined WBR2025 public summaries; V138 recovered the2022 report with an age15+ survey and a Warsaw school-trip sample base22. Those files are retained in their original packages. No new city/high-school one-way travel mean, distribution or matching denominator was obtained here. The current V192 model, user CSV, weights, intervals and V193 paper are unchanged; actual scoring-width reduction is zero.
