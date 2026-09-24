# P6 IJMLC Manuscript Build Report

generated_at: 2026-07-01T19:27:06.194715

## Output directory
`/home/aaa/data/qj/stable-baselines3-master/risk_curriculum_metadrive/results/ijmlc_control/manuscript_ijmlc_20260701`

## Main manuscript artifacts
- `main.tex`: Springer Nature `sn-jnl` author-year source.
- `main.pdf`: compiled proof PDF, 13 pages, 402370 bytes.
- `references.bib`: working bibliography.
- `claim_evidence_map.md`: claim-to-data evidence map.
- `writing_rationale_matrix.md`: manuscript logic matrix.
- `submission_checklist.md`: IJMLC/Springer checklist.
- `official_requirements_20260701.md`: source URLs and applied formatting decisions.

## Compile verification
- `latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex`: return code 0.
- Abstract word count: 217 words.
- PDF pages: 13.
- Final log grep found no undefined references/citations, no Overfull boxes, no duplicate destination warnings, and no fatal errors.

## Evidence embedded
- P1/P4 core and density diagnostics from `manuscript/table3_*`, `table6_*`, raw/aggregate CSVs.
- P2 external baselines from `P2_EXTERNAL_BASELINES_FINAL_REPORT.md` and `table4_external_baselines_d015.csv`.
- P5 sensitivity from `table_supp_sensitivity.csv` and sensitivity figures.
- CI/seed scatter from `table_supp_ci_d015.csv` and `table_supp_seed_scatter_d015.csv`.
- Runtime overhead from `table7_runtime_overhead.csv` and Fig. 7.

## Boundaries still retained
- Simulation-only MetaDrive evidence.
- No formal/certified/real-world safety claim.
- Seed3/seed4 extension remains reviewer-demand reserve, not part of formal current tables.
- Author names, funding, author contribution, and public data/code DOI still need author-team input.
- Bibliography has a citation verification report; final author team may still export through a reference manager if desired.


## Citation verification
- `citation_verification_report.md` generated under the manuscript directory.
- Current `references.bib` has source-backed URL/DOI/arXiv/PMLR/JMLR/AAAI metadata.
- Latest `latexmk` after bibliography update returned code 0 and log grep found no undefined citations/references, no Overfull boxes, no duplicate destination warnings, and no fatal errors.


## Publication table/figure revision

- Revised report: `results/ijmlc_control/FIGURE_TABLE_REVISION_REPORT.md`
- New figure directory: `results/ijmlc_control/figures_publication`
- New table directory: `results/ijmlc_control/tables_publication`
- Main manuscript now uses complete diagnostic tables and six redesigned publication figures.


## Publication table/figure revision

- Revised report: `results/ijmlc_control/FIGURE_TABLE_REVISION_REPORT.md`
- New figure directory: `results/ijmlc_control/figures_publication`
- New table directory: `results/ijmlc_control/tables_publication`
- Main manuscript now uses complete diagnostic tables and six redesigned publication figures.


## Publication table/figure revision

- Revised report: `results/ijmlc_control/FIGURE_TABLE_REVISION_REPORT.md`
- New figure directory: `results/ijmlc_control/figures_publication`
- New table directory: `results/ijmlc_control/tables_publication`
- Main manuscript now uses complete diagnostic tables and six redesigned publication figures.


## Publication table/figure revision

- Revised report: `results/ijmlc_control/FIGURE_TABLE_REVISION_REPORT.md`
- New figure directory: `results/ijmlc_control/figures_publication`
- New table directory: `results/ijmlc_control/tables_publication`
- Main manuscript now uses complete diagnostic tables and six redesigned publication figures.


## Publication table/figure revision

- Revised report: `results/ijmlc_control/FIGURE_TABLE_REVISION_REPORT.md`
- New figure directory: `results/ijmlc_control/figures_publication`
- New table directory: `results/ijmlc_control/tables_publication`
- Main manuscript now uses complete diagnostic tables and six redesigned publication figures.


## Publication table/figure revision

- Revised report: `results/ijmlc_control/FIGURE_TABLE_REVISION_REPORT.md`
- New figure directory: `results/ijmlc_control/figures_publication`
- New table directory: `results/ijmlc_control/tables_publication`
- Main manuscript now uses complete diagnostic tables and six redesigned publication figures.


## Publication table/figure revision

- Revised report: `results/ijmlc_control/FIGURE_TABLE_REVISION_REPORT.md`
- New figure directory: `results/ijmlc_control/figures_publication`
- New table directory: `results/ijmlc_control/tables_publication`
- Main manuscript now uses complete diagnostic tables and six redesigned publication figures.


## Publication table/figure revision

- Revised report: `results/ijmlc_control/FIGURE_TABLE_REVISION_REPORT.md`
- New figure directory: `results/ijmlc_control/figures_publication`
- New table directory: `results/ijmlc_control/tables_publication`
- Main manuscript now uses complete diagnostic tables and six redesigned publication figures.


## IJMLC journalization revision

- Generated: 2026-07-01T20:01:33
- Manuscript: `results/ijmlc_control/manuscript_ijmlc_20260701/main.tex` and `main.pdf`
- Report: `results/ijmlc_control/IJMLC_JOURNALIZATION_REPORT.md`
- Generator: `results/ijmlc_control/scripts/build_ijmlc_journal_revision.py`
- Key changes: IJMLC cybernetic-feedback framing, expanded related work, formal method equations, Algorithm 1, claim-to-evidence table, mechanism-decomposition table, revised Fig. 1/Fig. 2/Fig. 5/Fig. 6, no rotated tables.
- Known evidence boundary: current raw CSVs are episode-level; representative step-level trace figure requires a future diagnostic run with per-step logging.

<!-- IJMLC_JOURNAL_REVISION_FINAL_START -->

## IJMLC journal revision final status (2026-07-01 20:10:22)

- Manuscript package: `results/ijmlc_control/manuscript_ijmlc_20260701`.
- Final compiled PDF: `manuscript_ijmlc_20260701/main.pdf`, 26 pages, 34 references.
- Table orientation fix: all generated main-text and appendix tables are portrait `table` floats; generated manuscript/table files contain no `sidewaystable`, `landscape`, `resizebox`, or `rotatebox` commands.
- Table interpretation fix: main and appendix metric headers now mark desired directions, e.g. success/route `up`, cost/collision/out/TTC/stop/low-progress `down`; density summary reports `Cost red.` and `Route gain` explicitly.
- Visual polish: paragraph-style tables use ragged-right columns to avoid stretched text and ugly forced hyphenation; Fig. 1 and Fig. 2 label overlaps were removed.
- Evidence scope: training/ordinary evaluation use 16 SB3 parallel environments; IJMLC diagnostics are per-seed shards for episode-level TTC/speed/stop/intervention/route/latency traceability.
- Supervision: resource watchdog remains the required guard; it stops IJMLC jobs when Linux MemAvailable is below 3.0 GiB or free GPU memory is below 2048 MiB.
- Limitation retained: current raw CSVs are episode-level, not step-level; no representative route/speed/TTC time-series trace was fabricated.

<!-- IJMLC_JOURNAL_REVISION_FINAL_END -->
