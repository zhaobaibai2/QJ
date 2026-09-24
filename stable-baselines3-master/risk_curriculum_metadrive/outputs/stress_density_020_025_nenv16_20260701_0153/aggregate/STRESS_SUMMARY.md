# Stress density 0.20/0.25 n_envs=16

Generated: 2026-07-01T02:55:36.125071+08:00

Protocol: evaluation-only, 50 episodes per density, densities 0.20 and 0.25, n_envs=16, device=cuda. Each label has three seeds and 100 episodes per seed unless noted in status.tsv.

| label | density | success | cost | collision | out_of_road | route | speed_kmh | lane_dev | ttc_risk |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| baseline | 0.20 | 0.000 | 1.000 | 0.647 | 0.353 | 0.165 | 37.092 | 0.323 | 0.1605 |
| baseline | 0.25 | 0.000 | 1.000 | 0.760 | 0.240 | 0.158 | 36.308 | 0.296 | 0.1837 |
| curriculum | 0.20 | 0.000 | 1.000 | 0.627 | 0.373 | 0.164 | 36.977 | 0.271 | 0.1875 |
| curriculum | 0.25 | 0.000 | 1.000 | 0.733 | 0.267 | 0.157 | 35.546 | 0.250 | 0.2246 |
| full_proposed_candidate | 0.20 | 0.380 | 0.400 | 0.380 | 0.020 | 0.744 | 13.905 | 0.206 | 0.0247 |
| full_proposed_candidate | 0.25 | 0.207 | 0.587 | 0.560 | 0.027 | 0.587 | 12.151 | 0.217 | 0.0324 |
| guard_only | 0.20 | 0.413 | 0.407 | 0.380 | 0.027 | 0.733 | 13.805 | 0.173 | 0.0243 |
| guard_only | 0.25 | 0.267 | 0.487 | 0.460 | 0.027 | 0.658 | 12.145 | 0.206 | 0.0303 |
| retune_proposed_ttc4_cost10_lane1 | 0.20 | 0.453 | 0.380 | 0.340 | 0.040 | 0.753 | 14.356 | 0.239 | 0.0278 |
| retune_proposed_ttc4_cost10_lane1 | 0.25 | 0.173 | 0.687 | 0.647 | 0.040 | 0.571 | 12.848 | 0.273 | 0.0324 |
| risk | 0.20 | 0.000 | 0.000 | 0.000 | 0.000 | 0.009 | 0.014 | 0.006 | 0.0000 |
| risk | 0.25 | 0.000 | 0.000 | 0.000 | 0.000 | 0.009 | 0.014 | 0.006 | 0.0000 |
| shield_only | 0.20 | 0.480 | 0.360 | 0.340 | 0.020 | 0.778 | 14.303 | 0.140 | 0.0238 |
| shield_only | 0.25 | 0.193 | 0.587 | 0.533 | 0.053 | 0.609 | 11.870 | 0.201 | 0.0330 |

Ranking by success then lower cost is written to `rank_by_density.csv`.

Short interpretation:
- d0.20: shield_only has the highest mean success, followed by retune_proposed_ttc4_cost10_lane1 and guard_only.
- d0.25: guard_only is the best high-density stress survivor by success and cost.
- Baseline and curriculum fail through collision/out-of-road; risk has zero cost only because it barely moves.
- Full proposed variants do not dominate guard/shield under stress; use this as robustness evidence for action-guard mechanisms, not risk-reward dominance.
