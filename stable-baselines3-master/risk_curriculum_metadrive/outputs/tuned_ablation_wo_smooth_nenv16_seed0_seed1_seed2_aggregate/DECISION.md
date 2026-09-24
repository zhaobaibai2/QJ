# Decision: proposed_wo_smooth three-seed ablation aggregate

Time: 2026-07-01T00:36:00+0800

Aggregate root: outputs/tuned_ablation_wo_smooth_nenv16_seed0_seed1_seed2_aggregate

Included seeds:
- seed0: outputs/tuned_ablation_wo_smooth_nenv16_seed0_1m/evaluations/summary.csv
- seed1: outputs/tuned_ablation_wo_smooth_nenv16_seed1_1m/evaluations/summary.csv
- seed2: outputs/tuned_ablation_wo_smooth_nenv16_seed2_1m/evaluations/summary.csv

Mean formal evaluation across seed0/1/2:

| density | success | cost | collision | out_of_road | route | lane_dev | ttc_risk |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 0.0 | 0.973 | 0.000 | 0.000 | 0.000 | 0.989 | 0.178 | 0.0000 |
| 0.08 | 0.820 | 0.147 | 0.140 | 0.007 | 0.918 | 0.195 | 0.0046 |
| 0.15 | 0.567 | 0.287 | 0.280 | 0.007 | 0.821 | 0.245 | 0.0174 |

Interpretation:
- Removing smooth/accel regularization is high-variance: seed2 recovers better than seed1, but the three-seed mean remains weaker than full proposed at medium/high density.
- The smooth/accel terms are stabilizers, not the dominant mechanism; their absence hurts average route/safety and training consistency.

Decision:
- Accept as the three-seed smooth/accel ablation.
- Keep the claim bounded to stability and average dense-traffic degradation, not universal per-seed failure.
