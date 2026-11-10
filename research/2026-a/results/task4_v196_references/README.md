# V196: compiled bibliography identities for the V193 owned review

All 56 bibliography keys match the order recorded by the V193 compiler auxiliary file. There are 55 cited keys, no missing citation keys and no duplicate bibliography keys. The sole uncited entry is `parisedu`; an unused retained source is not itself a citation error and was not removed.

`inventory.json` records each bibliography key, exact owning TeX file and line, URL list, compiled citation use and source citation locations. `inventory.csv` is the compact table. The three `CaseReferences` entries are expanded from the generated macro; its citation sites are labelled as macro-definition locations rather than mistaken for direct body locations. The complete reachable source set has 17 TeX files and is SHA-bound in `verification.json`.

There are 63 URL occurrences across the 56 entries. `teamtable`, `istanbul` and `legacycase` have no URL; their supplied-input/archive identities remain explicit. URL presence does not certify availability, authenticity, measurement compatibility or claim support. This audit does not certify all original data, crawl the 63 URLs or establish complete AI disclosure. No contradiction was apparent in the four method entries' local bibliographic metadata; publisher metadata was not revalidated here.

`compiled.aux` was copied from the existing local V193 build. That build's PDF SHA256 exactly matched the current owned V193 PDF (`fb9b2d0f95f544c41f2de02e15a58673f15a8ac8efc4dcadb173f0a272474dae`) at collection. This is a local compiler artifact, not a server-compile receipt. The audit compares the stored compiler keys with the source bibliography and binds the current PDF and all source inputs.

Reproduce the bounded identity audit from the research repository root:

```sh
.venv-v120/bin/python research/2026-a/scripts/audit_task4_v196_references.py
```

No manuscript, model, input values or current navigation was modified.
