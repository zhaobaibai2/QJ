# Decision: guard_only ttc12/v19 diagnostic aggregate

Time: 2026-06-30T23:56:10+0800

Aggregate root: outputs/retune_guard_only_ttc12_v19_nenv16_seed1_seed2_diagnostic_aggregate

Included seeds:
- seed1: outputs/retune_guard_only_ttc12_v19_nenv16_seed1_1m/evaluations/summary.csv
- seed2: outputs/retune_guard_only_ttc12_v19_nenv16_seed2_1m/evaluations/summary.csv

Mean formal evaluation across seed1/seed2:

| density | success | cost | collision | out_of_road | route | lane_dev | ttc_risk |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 0.0 | 0.990 | 0.000 | 0.000 | 0.000 | 0.991 | 0.054 | 0.0000 |
| 0.08 | 0.880 | 0.110 | 0.110 | 0.000 | 0.946 | 0.064 | 0.0025 |
| 0.15 | 0.650 | 0.270 | 0.270 | 0.000 | 0.866 | 0.120 | 0.0151 |

Same-seed comparison to existing guard_only ttc12/v18:
- seed1 d0.08: success 0.88 -> 0.92, cost 0.10 -> 0.06, route 0.934 -> 0.954.
- seed1 d0.15: success 0.66 -> 0.58, cost 0.16 -> 0.28, route 0.895 -> 0.861.
- seed2 d0.08: success 0.88 -> 0.84, cost 0.10 -> 0.16, route 0.933 -> 0.938.
- seed2 d0.15: success 0.62 -> 0.72, cost 0.24 -> 0.26, route 0.847 -> 0.871.

Interpretation:
- Raising the target speed from 18 to 19 gives a mixed trade-off rather than a clean improvement.
- The two-seed high-density mean improves success only slightly versus guard_only ttc12 same seeds, but cost worsens materially and route is essentially unchanged/slightly lower.
- seed1 is clearly worse at d0.15: success drops and cost increases. seed2 gains d0.15 success/route but still increases cost.
- d0.08 is not clean: seed1 improves, but seed2 worsens cost and success; the two-seed cost is above the original same-seed guard baseline.

Decision:
- Do not launch seed0 for ttc12/v19.
- Do not promote target_speed=19 as the final guard-centered setting.
- Keep default guard_only ttc12/v18 and shield_only as the cleaner action-guard baselines.
- Treat v19 as parameter-sensitivity evidence showing that relaxing the speed guard can raise high-density success on one seed, but the cost trade-off is too large for the paper main line.

Next action:
- Stop guard-threshold/speed micro-tuning for now. Move to evidence completion: either formal comparator symmetry (baseline/curriculum/risk seed1/2) or ablation symmetry (no_action_guard seed1/2, wo_lane/wo_smooth seed2) depending on the paper table priority.
