# EXPERIMENT_AND_MANUSCRIPT_STATUS_20260701_0858

Time: 2026-07-01T08:57:39+08:00
Remote root: `/home/aaa/data/qj/stable-baselines3-master/risk_curriculum_metadrive`

## Current Runtime State

- Latest supervision script result: `OK_IDLE` at 2026-07-01T08:57:13.
- Active MetaDrive experiment processes: 0.
- GPU state at 08:57: RTX 4070 SUPER, about 846 / 12282 MiB used, no training CUDA job.
- Decision: do not launch broad new training merely because the GPU is idle.

## Experiment Completion Evidence

The current paper-facing experiment matrix is complete under the formal `n_envs=16` protocol:

- Main comparisons: `codex_longrun_iscsic/paper_tables_20260701_0258/main_comparators_nenv16.csv`, 21 / 21 rows.
- Component ablations: `codex_longrun_iscsic/paper_tables_20260701_0258/ablation_mechanism_nenv16.csv`, 15 / 15 rows.
- Stress density 0.20/0.25: `codex_longrun_iscsic/paper_tables_20260701_0258/stress_density_020_025.csv`, 14 / 14 rows.
- Gated-risk addendum: `codex_longrun_iscsic/paper_tables_20260701_0258/gated_risk_mechanism_addendum.csv`, 15 / 15 rows.
- External-seed robustness mean: `codex_longrun_iscsic/paper_tables_20260701_0258/external_seed_robustness_mean.csv`, 12 / 12 rows.
- External-seed Wilson intervals: `codex_longrun_iscsic/paper_tables_20260701_0258/external_seed_robustness_d015_wilson95.csv`, 6 / 6 rows.
- Protocol audit: 33 accepted model configs checked, bad configs 0; 72 episode eval CSVs checked, bad eval CSVs 0.

## Parameter and Tuning Closure

- `defensive_ttc14_v18_nenv16_tuning` remains diagnostic only: density 0.15 success 0.573, cost 0.260, below the 0.60 / 0.25 promotion gate.
- Guard `ttc13/v18`, `ttc12/v19`, moderate lateral/smooth retunes, and reward-only micro-tuning are not promoted because their seed or density trade-offs do not improve the guard/shield-centered manuscript line.
- Current empirical bottleneck is writing and claim framing, not lack of another broad run.

## Manuscript Artifacts Updated This Pass

- Rebuilt `paper/results_section_guard_shield_20260701.tex` as a compact-label, evidence-grounded Results/Experiments draft. It now has 127 lines and uses concise table labels such as Guard, Shield, Full, Retuned full, and Gated risk.
- Rebuilt and verified `paper/results_section_guard_shield_20260701_standalone.pdf`; `pdflatex` completed successfully after two passes, 3 pages, no fatal errors.
- Rebuilt `paper/generated_results.tex` from the formal density-0.15 main table. It is no longer an empty table and now contains 9 methods with Success, Route, Collision, OutRoad, Cost, and TTC columns.
- Recompiled `paper/main_zh.pdf` with `xelatex`; output succeeded, 4 pages. Remaining warnings are font substitution and old equation overfull boxes, not errors from the new generated table.

## Claim Boundary To Preserve

- Strong claim: action guard/shield is the dominant stabilizing mechanism in dense MetaDrive traffic.
- Strong negative-control claim: risk-only and no-action-guard fail for different reasons; risk-only is stagnation, no-action-guard is unsafe driving.
- Moderate claim: TTC, lane, smoothness, and gated risk are refinements around the guard/shield mechanism.
- Do not claim risk-only, full proposed, or gated risk is universally dominant over `shield_only` / `guard_only`.
- Stress and external seed evaluations are frozen-model validation, not tuning targets.

## Next Useful Work

- Rewrite the old Chinese `paper/main_zh.tex` around the guard/shield-centered story. It still contains the earlier risk-aware curriculum framing.
- Use the new `paper/results_section_guard_shield_20260701.tex` and final manifest tables as the source of truth for the Results section.
- Only run a new experiment if a specific reviewer-style gap is identified, such as one more external test-start seed; do not restart blind tuning.
