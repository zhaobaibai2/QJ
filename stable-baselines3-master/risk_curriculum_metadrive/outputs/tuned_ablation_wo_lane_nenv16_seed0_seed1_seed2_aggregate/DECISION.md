# Decision: proposed_wo_lane three-seed ablation aggregate

Time: 2026-07-01T00:36:00+0800

Aggregate root: outputs/tuned_ablation_wo_lane_nenv16_seed0_seed1_seed2_aggregate

Included seeds:
- seed0: outputs/tuned_ablation_wo_lane_nenv16_seed0_1m/evaluations/summary.csv
- seed1: outputs/tuned_ablation_wo_lane_nenv16_seed1_1m/evaluations/summary.csv
- seed2: outputs/tuned_ablation_wo_lane_nenv16_seed2_1m/evaluations/summary.csv

Mean formal evaluation across seed0/1/2:

| density | success | cost | collision | out_of_road | route | lane_dev | ttc_risk |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 0.0 | 0.960 | 0.000 | 0.000 | 0.000 | 0.990 | 0.349 | 0.0000 |
| 0.08 | 0.913 | 0.060 | 0.060 | 0.000 | 0.969 | 0.363 | 0.0023 |
| 0.15 | 0.607 | 0.280 | 0.280 | 0.000 | 0.844 | 0.362 | 0.0141 |

Interpretation:
- Removing the lane reward does not collapse raw success, but it consistently increases lane deviation across seeds.
- The three-seed high-density mean is slightly weaker than the full proposed aggregate in cost and route completion.
- The lane term should be framed as a lateral-stability and route-quality component rather than the dominant success mechanism.

Decision:
- Accept as the three-seed lane-reward ablation.
- Do not tune this ablation; use it to support the lane-stability component claim.
