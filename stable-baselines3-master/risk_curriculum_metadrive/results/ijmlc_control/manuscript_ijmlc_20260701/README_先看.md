# IJMLC Manuscript Package - README

This directory is the P6 manuscript package built from the completed IJMLC evidence package.

## Main files
- `main.tex`: Springer Nature `sn-jnl` author-year manuscript draft.
- `main.pdf`: compiled proof PDF, generated after `latexmk` succeeds.
- `references.bib`: source-checked BibTeX file for the current draft.
- `citation_verification_report.md`: reference metadata verification report.
- `claim_evidence_map.md`: exact claim-to-file evidence map.
- `writing_rationale_matrix.md`: section-level writing logic.
- `submission_checklist.md`: IJMLC/Springer readiness checklist.
- `official_requirements_20260701.md`: current official requirements used for formatting decisions.

## Evidence source
All tables and figures are generated from `../manuscript`, `../raw_csv`, and `../summary_tables` under `results/ijmlc_control`.

## Training and evaluation protocol note
- Training and ordinary SB3 evaluation use `--n-envs 16` in the `sb3` conda environment.
- IJMLC diagnostics use parallel per-seed/per-method shards to preserve per-step TTC, speed, intervention, stop-ratio, and latency logs.
- This is intentional: vectorized standard evaluation is fast for episode outcomes; diagnostic shards are needed for reviewer-facing mechanism metrics.

## Supervision
The resource watchdog is `../watchdog_resource_guard.py` with log `../logs/resource_watchdog.log`.
Current stop rule: MemAvailable < 3.0 GiB or GPU free memory < 2048 MiB stops current IJMLC jobs.

## Remaining before actual submission
- Replace anonymous author and affiliation placeholders.
- Confirm funding, competing interests, and author contributions.
- Add public data/code repository URLs or DOI if required by the final author team.
