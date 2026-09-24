# EXPERIMENT_COMPLETION_AUDIT_20260701_0845

Time: 2026-07-01T08:45:49+08:00

## Executive Decision

Current evidence is broad enough for a conservative manuscript package, but the claim must be guard/shield-centered. The evidence does not support a risk-reward-dominant or full-method-always-best story. No active training/evaluation process is running, and no new tuning branch should be started without a specific manuscript or reviewer gap.

## Runtime State

- Remote root: /home/aaa/data/qj/stable-baselines3-master/risk_curriculum_metadrive.
- Process check at 2026-07-01 08:41 CST found no active MetaDrive training/evaluation process.
- GPU check showed desktop/remote-display usage only; no CUDA training job was active.
- Wider /home/aaa/data/qj scan did not show a separate active CAR-Gate/iscsic2026_metadrive_riskgate tree; this project remains the authoritative experiment line.

## Protocol Integrity

- Accepted model configs checked: 33; bad n_envs/model checks: 0.
- Episode evaluation CSVs checked: 72; bad eval_n_envs checks: 0.
- Paper table source paths checked: missing sources=0.
- Summary CSVs inside run directories may omit eval_n_envs; they are secondary summaries, not the authoritative episode-level protocol proof.

## Requirement Matrix

| Requirement | Status | Evidence | Decision | Next action |
|---|---|---|---|---|
| 16-env formal protocol | verified | 33 accepted model configs checked; 72 episode eval CSVs checked | config_bad=0, eval_bad=0, source_missing=0 | keep n_envs=16; do not mix n_envs=8/10/32 diagnostics into paper tables |
| main comparison baselines | complete | main_comparators_nenv16.csv; baseline/risk/curriculum/guard/shield/retuned/full entries | d0.15 shield_only success=0.627 cost=0.227; risk success=0.000 route=0.009 | write as guard/shield-centered result; risk-only is negative control due route stagnation |
| component ablations | complete | ablation_mechanism_nenv16.csv; no_action_guard/wo_ttc/wo_lane/wo_smooth/guard_only | no_action_guard d0.15 success=0.000 cost=1.000 | use no_action_guard as strongest necessity evidence; TTC/lane/smooth as refinements |
| gated-risk innovation | complete_addendum | gated_risk_mechanism_addendum.csv; gated-risk stress; external seed robustness | formal d0.15 success=0.600 cost=0.253; external d0.15 success=0.663 cost=0.213 | keep as viable refinement, not superiority over shield_only |
| stress and external robustness | complete | stress_density_020_025.csv; gated_risk_stress_mean.csv; external_seed_robustness_* | external d0.15 shield_only success=0.687 cost=0.207; proposed_gated_risk Wilson high=0.714 | use as reviewer-facing validation of frozen models, not tuning target |
| parameter tuning closure | complete_diagnostic | retune DECISION files; defensive_ttc14_v18 aggregate/DECISION | ttc14/v18 d0.15 success=0.573 cost=0.260; below gate 0.60/0.25 | do not open more TTC-only or reward-only retunes without a new manuscript-driven gap |
| qualitative behavior evidence | complete | behavior_rollouts_20260701_0406 and final_manifest pdf_figures | representative d0.15 seed10003 behavior plots present; 20 final-manifest PDFs verified earlier | use as mechanism illustration only, not aggregate replacement |
| current runtime supervision | idle_ready | 2026-07-01 08:41 process/GPU check | no active MetaDrive training/evaluation process; GPU desktop-only usage | stand by for manuscript packaging or narrowly scoped reviewer validation; no blind new training |

## Paper Claim Boundary

- Strong claim: action guard/shield is the dominant stabilizing mechanism under dense traffic.
- Strong negative-control claim: risk-only and no-action-guard fail for different reasons; risk-only stagnates and no-action-guard drives unsafely.
- Moderate claim: gated risk fixes risk-only stagnation and is competitive, but it is not statistically or practically dominant over shield_only.
- Moderate claim: TTC/lane/smooth rewards refine behavior and explain mechanisms; they should not be presented as the primary source of robustness.
- Stress/external-seed evidence should be framed as frozen-model validation, not as additional tuning evidence.

## Closed Tuning Decisions

- defensive ttc14/v18 nenv16: diagnostic only; d0.15 success=0.573 and cost=0.260 fail the 0.60/0.25 gate.
- guard ttc13/v18 and ttc12/v19 diagnostics: not promoted because medium/high-density trade-offs were mixed.
- moderate lateral/smooth retune: not promoted because it fixed one seed but worsened another.
- recommendation: stop reward-only/TTC-only micro-tuning unless a new reviewer question forces it.

## Files To Use For Manuscript

- Table manifest: codex_longrun_iscsic/final_paper_manifest_20260701_0415/table_manifest.csv.
- Claim boundary: codex_longrun_iscsic/final_paper_manifest_20260701_0415/claim_boundary_matrix.csv.
- Main tables: table1_formal_main_d015.*, table2_ablation_d015.*, table3_stress_ranked.*, table4_external_seed_robustness*.
- Source package: codex_longrun_iscsic/paper_tables_20260701_0258/.
- This requirement matrix: codex_longrun_iscsic/EXPERIMENT_REQUIREMENT_MATRIX_20260701_0845.csv.

## Next Supervision Rule

The next action should be manuscript/table/figure packaging or a tightly scoped reviewer-style validation. Do not start broad new training just because the GPU is idle; the current empirical bottleneck is claim framing, not lack of another run.
