# Third bounded root-log window

The latest authenticated window covers complete lines after the preceding 380,482,614-byte prefix through byte431,293,385, ending **10 November2026,20:32:42.716UTC** (11 November04:32 in Singapore). It adds51 root contexts labelled `gpt-6.1-sol`,239 selected visible records (three requests/replies,191 commentary,45 final messages) and1,367 plaintext top-level assistant tool inputs. Seventy recorded spawn requests specify49 `gpt-6.1-terra` and21 `gpt-6-luna` labels. Request labels and context identifiers do not attest serving builds or successful execution.

Three nonoverlapping source windows now account for167 root contexts,762 selected visible records and4,604 tool inputs. The two continuation windows record148 spawn requests:77 Terra,28 Luna and43 unspecified/null. Initial-window spawn labels are not counted in that subtotal. `coverage_summary.json` verifies the manifest/prefix chain and aggregate counts; it does not turn selected records into a complete transcript.

The fixed-cutoff capture and independent audit preserve exact selected exports outside both repositories. Their directory is mode0700 and files mode0600. New public artifacts contain whitelisted metadata, inventories and hashes, with selector length/hash fingerprints; they do not contain selected message bodies or tool-argument strings. Earlier frozen selectors retain request prefixes. Fingerprints are not an anonymity or content-redaction guarantee. Unredacted private tool inputs may contain copied material. Raw logs and exact selected-record exports are not published.

Excluded source-record types include reasoning, system/developer messages, tool results, attachments, injected continuations and unselected user records. Child sessions, other chats, team members and work after the cutoff remain outside the capture. `complete_team_ai_history=false` and `submission_ready=false` therefore remain in force. The private exports are not submission transcripts; actual team query/response coverage still requires reconciliation with the applicable policy.

Fixed replay (use actual private paths; do not write exports in either repository):

```bash
PYTHONDONTWRITEBYTECODE=1 python research/2026-a/scripts/task4_current_ai_continuation2.py --session /absolute/root-log.jsonl --private-output /absolute/private-export-directory
PYTHONDONTWRITEBYTECODE=1 python research/2026-a/scripts/audit_current_ai_continuation2.py --session /absolute/root-log.jsonl --private-output /absolute/private-export-directory
```

The capture defaults to the registered cutoff; advancing it requires explicit`--refresh` and prefix checks. The auditor is read-only by default; reports require explicit`--output` and overwrite approval via its argument. Optional`--paper-baseline COMMIT` compares pre-AI source and six resources against the selected Git commit. Before manuscript updates it verified the existing source,658 frozen scientific files, both seven-dependency paper copies and PDF. A later AI-only paper audit separately verifies the new source and rendered pages. The two scratch negative controls reject a synthetic public message body and an altered aggregate count without modifying real records.
