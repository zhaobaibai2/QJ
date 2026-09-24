# Final Paper Manifest 2026-07-01 04:15

This directory is the paper-facing manifest for the current n_envs=16 evidence package.

## What is here

- `table_manifest.csv`: table inventory and source boundaries.
- `figure_manifest.csv`: figure inventory and source boundaries.
- `pdf_figure_manifest.csv`: copied PDF figure inventory.
- `table1_formal_main_d015.*`: formal main table at density 0.15.
- `table2_ablation_d015.*`: mechanism ablation table at density 0.15.
- `table3_stress_ranked.*`: stress robustness table at density 0.20/0.25.
- `claim_boundary_matrix.csv`: conservative claim boundaries for manuscript writing.
- `pdf_figures/`: curated paper-use PDF figures.

## PDF placement policy

Paper-facing PDFs are copied under `pdf_figures/`:

- `pdf_figures/framework/`: method framework diagram copied from the existing n_envs=16 run; the plotting script is `scripts/plot_framework_diagram.py`, but current system matplotlib fails under NumPy 2.2.6 ABI mismatch.
- `pdf_figures/behavior_rollouts/`: qualitative behavior and representative trajectory PDFs.
- `pdf_figures/source_single_seed_metrics/`: selected source run PDFs kept for visual diagnostics only.

The many historical PDFs under `outputs/*/figures/` are intentionally left in their original run directories for provenance. They should not be cited as aggregate evidence unless the corresponding aggregate CSV in `paper_tables_20260701_0258` or this manifest is used.

Generated at 2026-07-01T04:20:43.206561+08:00.

## External Seed Robustness Addendum

The external scenario-seed sweep completed after this manifest was first generated. The manifest now includes `table4_external_seed_robustness.csv`, copied from `outputs/external_seed_robustness_nenv16_20260701_0425/aggregate/mean_by_label_density.csv`. Use it as reviewer-facing validation of frozen models under `test_start_seed=20000/30000`, not as additional training or tuning evidence.

Latest addendum source: `codex_longrun_iscsic/paper_tables_20260701_0258/external_seed_robustness_addendum.md`.

