# EXPERIMENT_COVERAGE_AUDIT_20260701_0405

Time: 2026-07-01T04:04:23+08:00

## Current Paper Direction

The strongest verified paper line is action-guard/shield-centered robustness. Risk reward, TTC, lane, smoothness, curriculum, and gated-risk shaping are refinements or diagnostic mechanisms. The evidence still does not support a risk-reward-dominant main claim.

## Completed Main Evidence

- `outputs/tuned_ablation_guard_only_nenv16_aggregate`: 3 seeds, formal n_envs=16. d0.15 success=0.633, cost=0.207, route=0.868.
- `outputs/tuned_compare_shield_only_nenv16_seed0_seed1_seed2_aggregate`: 3 seeds. d0.15 success=0.627, cost=0.227, route=0.871.
- `outputs/retune_proposed_ttc4_cost10_lane1_nenv16_seed0_seed1_seed2_aggregate`: 3 seeds. d0.15 success=0.620, cost=0.240, route=0.853.
- `outputs/gated_risk_proposed_nenv16_seed0_seed1_seed2_aggregate`: 3 seeds. d0.15 success=0.600, cost=0.253, route=0.849. Use as mechanism addendum, not replacement.

## Completed Comparators

- `outputs/tuned_compare_baseline_nenv16_seed0_seed1_seed2_aggregate`: unguarded baseline fails through unsafe driving.
- `outputs/tuned_compare_curriculum_nenv16_seed0_seed1_seed2_aggregate`: curriculum-only final evaluation remains unsafe.
- `outputs/tuned_compare_risk_nenv16_seed0_seed1_seed2_aggregate`: risk-only fails by low-speed/route stagnation.

## Completed Ablations

- `outputs/tuned_ablation_no_action_guard_nenv16_seed0_seed1_seed2_aggregate`: removing action guard collapses held-out safety and route quality.
- `outputs/tuned_ablation_wo_ttc_nenv16_seed0_seed1_seed2_aggregate`: TTC is a refinement, not the dominant mechanism.
- `outputs/tuned_ablation_wo_lane_nenv16_seed0_seed1_seed2_aggregate`: lane reward supports lateral stability.
- `outputs/tuned_ablation_wo_smooth_nenv16_seed0_seed1_seed2_aggregate`: smooth/accel terms support stability but have seed variance.

## Completed Stress Evidence

- `outputs/stress_density_020_025_nenv16_20260701_0153/aggregate`: frozen guard/shield/full/baseline/curriculum/risk stress table.
- `outputs/stress_gated_risk_density_020_025_nenv16_20260701_0346/aggregate`: gated-risk stress addendum. d0.20 success=0.447, cost=0.367, route=0.766; d0.25 success=0.220, cost=0.527, route=0.628.

## Rejected or Diagnostic Tuning Branches

- `outputs/retune_guard_only_ttc13_v18_nenv16_seed1_seed2_diagnostic_aggregate`: do not expand; medium-density drop and mixed high-density trade-off.
- `outputs/retune_guard_only_ttc12_v19_nenv16_seed1_seed2_diagnostic_aggregate`: do not expand; small high-density success gain comes with material cost increase.
- `outputs/retune_proposed_ttc4_cost10_lane125_smooth003_accel0015_progress45_nenv16_seed1_seed2_diagnostic_aggregate`: do not expand; seed trade-off is mixed.

## Paper Package Status

Primary package: `codex_longrun_iscsic/paper_tables_20260701_0258`.

Added robustness/statistics files:
- `seed_level_robustness_formal.csv`
- `seed_paired_deltas_vs_guard_shield.csv`
- `seed_level_robustness_stress.csv`
- `reviewer_statistics_notes.md`

## Next Work Recommendation

Do not open another reward-only retune. If more experiment work is needed, prioritize reviewer-facing validation rather than new mechanism chasing:

1. Generate trajectory/behavior evidence for representative success/failure cases under guard_only, shield_only, retuned_full, and proposed_gated_risk.
2. Package final paper figures/tables with source paths and claim boundaries.
3. Optionally run one external-seed robustness sweep only after deciding the final manuscript method name.
