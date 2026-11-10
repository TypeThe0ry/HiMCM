# Oslo 2026: resident-district evidence on adolescent leisure

The official Ungdata catalogue supplies separate lower- and upper-secondary district reports from the January–April 2026 school survey. Four unaltered reports, from Alna and Søndre Nordstrand, are retained with HTTP receipts. Each report includes tables covering all fifteen districts. Repetition across publications verifies table transcription, not independent respondents or measurement replication. The catalogue was retrieved successfully; the separate OsloMet project URL returned HTTP404 and is retained as a failed route, despite an indexed web rendering being available.

## What these records measure

The reports group school respondents by **self-reported residential district**, rather than school location. Lower-secondary respondents are described as aged13–16; upper-secondary respondents as16–19. All percentages are publisher-rounded whole numbers. The lower-stage foreword states weighting to give an even distribution across the three school grades. The upper-stage foreword does not supply the same statement; no equal-weighting assumption is transferred between stages. Participation is voluntary and respondents may omit answers. Survey-wide or district participant counts are not item-specific denominators.

Physical PDF pages13,21,28 (printed10,18,25) supply six selected measures per district:

| Measure | Definition |
| --- | --- |
| `meeting_places_good` | Perceived local places to meet other young people in free time, very/fairly good |
| `sports_facilities_good` | Perceived local sports facilities, very/fairly good |
| `cultural_provision_good` | Perceived local cultural provision, very/fairly good |
| `public_transport_good` | Perceived local public transport provision, very/fairly good |
| `sports_club_previous_month` | Sports-club activity/meetings/practice at least once during the previous month |
| `parents_lack_activity_money` | Parents sometimes/often lack money for desired leisure activities, including sports, cinema, birthdays and trips |

The financial item covers multiple activity types. It does not isolate swimming fees or establish inability to use a particular facility. Perceived provision, financial constraints and participation are distinct outcomes; individual records linking them were not obtained. Neither school-grade groups nor resident districts identify exact-age14/18 preferences, causal effects, individual access, disability eligibility or a longitudinal trend. These2026 observations do not replace the2025 primary inputs.

## Source identity issue and inclusion decision

The Søndre **upper-stage** report has a Søndre cover/foreword, but selected local charts identify Alna. For example, physical page21 shows a local Alna belonging value58; its all-district chart shows Alna58 and Søndre55. On page20, local meeting-place/sports-facility provision54/57 agrees with the all-district Alna row54/57, rather than Søndre57/65. Corresponding Alna upper-stage charts agree with these Alna values. This is a documented local identity mismatch, not a claim about every page or the provider's original survey database.

The selected all-district table values agree between the two reports within each stage. The90 upper-stage extracted cells remain quarantined from interpretation and no cross-stage difference is calculated. The90 lower-stage cells are retained as descriptive published context, with all six measures on three relevant pages visually checked. No new primary-model value or score bound is admitted. See the [results](../../results/current_oslo_youth2026/README.md).

## Retrieval and reproduction

`*.receipt.json` records requested/final URL, retrieval UTC, HTTP status, content type, body length and SHA256. Original bodies are preserved, including the failed project page. All four successful PDF links occur in `catalogue.html`. The selection uses two district reports to check repeated tables and their local identity, not to estimate a two-district population.

Run from the research repository with a new external output directory:

```bash
PYTHONDONTWRITEBYTECODE=1 /data/scratch/himcm-current-check-env/bin/python research/2026-a/scripts/task4_current_oslo_youth2026.py --output-dir /data/scratch/oslo-youth2026-new
```

The extractor uses system Poppler layout text, asserts complete district rows and matches duplicate tables before writing results. Root visual checks and the separate provenance review supplement extraction. No agency was contacted and no respondent-level data was collected.
