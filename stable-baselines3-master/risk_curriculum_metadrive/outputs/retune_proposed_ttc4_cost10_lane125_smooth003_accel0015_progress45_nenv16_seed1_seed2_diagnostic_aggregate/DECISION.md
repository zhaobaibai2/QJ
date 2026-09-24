# Decision: moderate lateral retune ttc4-cost10-lane1.25-smooth0.03-accel0.015-progress45 diagnostic aggregate

Time: 2026-06-30T23:00:54+0800

Aggregate root: `outputs/retune_proposed_ttc4_cost10_lane125_smooth003_accel0015_progress45_nenv16_seed1_seed2_diagnostic_aggregate`

Included seeds:
- seed1: `outputs/retune_proposed_ttc4_cost10_lane125_smooth003_accel0015_progress45_nenv16_seed1_1m/evaluations/summary.csv`
- seed2: `outputs/retune_proposed_ttc4_cost10_lane125_smooth003_accel0015_progress45_nenv16_seed2_1m/evaluations/summary.csv`

Mean formal evaluation across seed1/seed2:

| density | success | cost | collision | out_of_road | route | lane_dev | ttc_risk |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 0.00 | 0.980 | 0.000 | 0.000 | 0.000 | 0.990 | 0.081 | 0.0000 |
| 0.08 | 0.880 | 0.100 | 0.100 | 0.000 | 0.957 | 0.099 | 0.0045 |
| 0.15 | 0.630 | 0.280 | 0.270 | 0.010 | 0.850 | 0.150 | 0.0154 |

Seed-specific comparison to the previous ttc4-cost10-lane1 retune:
- seed1 d0.15: success 0.62 -> 0.64, cost 0.30 -> 0.28, route 0.869 -> 0.849, lane_dev 0.359 -> 0.102.
- seed1 d0.08: success 0.82 -> 0.88, cost 0.10 -> 0.12, route 0.923 -> 0.945, lane_dev 0.273 -> 0.072.
- seed2 d0.15: success 0.68 -> 0.62, cost 0.16 -> 0.28, route 0.871 -> 0.852, lane_dev 0.144 -> 0.198.

Interpretation:
- The candidate fixes the seed1 lateral-instability symptom: seed1 lane deviation drops sharply at d0.08 and d0.15, with slight d0.15 success/cost improvement.
- It fails the cross-seed robustness gate because seed2 high-density performance worsens materially versus lane1: d0.15 success drops and cost/lane deviation increase.
- The two-seed mean at d0.15 is success=0.630, cost=0.280, route=0.850; this is not better than guard_only or shield_only means and is not enough to promote.

Decision:
- Do not launch seed0 for this candidate.
- Do not promote this retune as the final main method.
- Keep it as a diagnostic showing that mild lateral/smooth strengthening can repair one unstable seed but introduces seed sensitivity. The paper main line should continue to emphasize action-guard dominance unless a guard-centered retune improves beyond guard_only/shield_only without sacrificing seed2.

Next action:
- Shift optimization from risk/lane reward retuning toward guard-centered or threshold-centered experiments, because repeated full-risk retunes have not beaten the action-guard baselines.
