# Decision: retune proposed ttc4-cost10-lane1 three-seed aggregate

Time: 2026-06-30T22:32:54+0800

Aggregate root: `outputs/retune_proposed_ttc4_cost10_lane1_nenv16_seed0_seed1_seed2_aggregate`

Included seeds:
- seed0: `outputs/retune_proposed_ttc4_cost10_lane1_nenv16_seed0_1m/evaluations/summary.csv`
- seed1: `outputs/retune_proposed_ttc4_cost10_lane1_nenv16_seed1_1m/evaluations/summary.csv`
- seed2: `outputs/retune_proposed_ttc4_cost10_lane1_nenv16_seed2_1m/evaluations/summary.csv`

Mean formal evaluation:

| density | success | cost | collision | out_of_road | route | lane_dev | ttc_risk |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 0.00 | 0.967 | 0.000 | 0.000 | 0.000 | 0.991 | 0.150 | 0.0000 |
| 0.08 | 0.887 | 0.073 | 0.073 | 0.000 | 0.953 | 0.156 | 0.0062 |
| 0.15 | 0.620 | 0.240 | 0.220 | 0.020 | 0.853 | 0.207 | 0.0199 |

Key comparison:
- vs original full proposed at d0.08: success improves from 0.833 to 0.887 and cost improves from 0.133 to 0.073.
- vs original full proposed at d0.15: success is unchanged at 0.620, cost slightly improves from 0.247 to 0.240, but route drops from 0.865 to 0.853.
- vs shield_only three-seed at d0.15: success 0.620 vs 0.627, cost 0.240 vs 0.227, route 0.853 vs 0.871, lane_dev 0.207 vs 0.105. Retune does not beat action-guard-only.
- vs guard_only three-seed at d0.15: success 0.620 vs 0.633, cost 0.240 vs 0.207, route 0.853 vs 0.868. Retune does not beat guard+curriculum.

Decision:
- Do not promote this retune as the final main method.
- It is useful as a diagnostic: reducing risk reward strength improves medium-density safety/success relative to the old full proposed, but does not fix high-density robustness and increases lane deviation in seed1.
- Next tuning direction should preserve the lower risk reward but increase lateral/smooth regularization, or otherwise pivot paper claims toward action guard dominance.
