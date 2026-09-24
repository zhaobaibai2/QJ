# Decision: guard_only ttc13/v18 diagnostic aggregate

Time: 2026-06-30T23:28:54+0800

Aggregate root: `outputs/retune_guard_only_ttc13_v18_nenv16_seed1_seed2_diagnostic_aggregate`

Included seeds:
- seed1: `outputs/retune_guard_only_ttc13_v18_nenv16_seed1_1m/evaluations/summary.csv`
- seed2: `outputs/retune_guard_only_ttc13_v18_nenv16_seed2_1m/evaluations/summary.csv`

Mean formal evaluation across seed1/seed2:

| density | success | cost | collision | out_of_road | route | lane_dev | ttc_risk |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 0.00 | 0.980 | 0.000 | 0.000 | 0.000 | 0.990 | 0.084 | 0.0000 |
| 0.08 | 0.840 | 0.120 | 0.120 | 0.000 | 0.941 | 0.107 | 0.0040 |
| 0.15 | 0.600 | 0.180 | 0.180 | 0.000 | 0.872 | 0.150 | 0.0157 |

Same-seed comparison to existing guard_only ttc12/v18:
- seed1 d0.08: success 0.88 -> 0.84, cost 0.10 -> 0.08, route 0.934 -> 0.954.
- seed1 d0.15: success 0.66 -> 0.58, cost 0.16 -> 0.20, route 0.895 -> 0.857.
- seed2 d0.08: success 0.88 -> 0.84, cost 0.10 -> 0.16, route 0.933 -> 0.929.
- seed2 d0.15: success 0.62 -> 0.62, cost 0.24 -> 0.16, route 0.847 -> 0.886.

Interpretation:
- ttc13 gives a mixed trade-off, not a promotion. It improves seed2 d0.15 cost/route, but hurts seed1 d0.15 success/cost/route.
- The two-seed d0.15 mean is success=0.600, cost=0.180, route=0.872. Compared with guard_only ttc12 same seeds, success drops while cost only modestly improves and route is essentially unchanged.
- d0.08 success drops for both seeds, and seed2 d0.08 cost worsens. This violates the gate that medium-density performance should stay near guard_only.

Decision:
- Do not launch seed0 for ttc13/v18.
- Do not promote ttc13 as the final guard-centered setting.
- Keep default guard_only ttc12/v18 as the cleaner action-guard baseline and treat ttc13 as parameter-sensitivity evidence.

Next action:
- Avoid more one-dimensional TTC-threshold increases. If more tuning is needed, test orthogonal action-guard behavior such as target-speed/overspeed guard or freeze the paper claim around the verified action-guard mechanism.
