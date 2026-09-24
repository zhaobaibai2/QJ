# proposed_wo_smooth n_envs=16 seed0-1 aggregate

Generated: 2026-06-30T22:03:11+08:00

Sources:
- `outputs/tuned_ablation_wo_smooth_nenv16_seed0_1m/evaluations/summary.csv`
- `outputs/tuned_ablation_wo_smooth_nenv16_seed1_1m/evaluations/summary.csv`

Protocol: `proposed_wo_smooth`, seeds 0/1, n_envs=16, timesteps=1M, horizon=1500, smooth and accel rewards ablated (`reward_weights.smooth=0.0`, `reward_weights.accel=0.0`), TTC/lane/cost/action guard/curriculum kept.

Mean over seeds:
| density | success mean | success std | cost mean | cost std | collision mean | out mean | route mean | lane dev | steer var | accel var |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0.00 | 0.990 | 0.014 | 0.000 | 0.000 | 0.000 | 0.000 | 0.990 | 0.206 | 0.015 | 0.229 |
| 0.08 | 0.820 | 0.028 | 0.160 | 0.028 | 0.150 | 0.010 | 0.909 | 0.222 | 0.021 | 0.238 |
| 0.15 | 0.530 | 0.071 | 0.330 | 0.127 | 0.320 | 0.010 | 0.793 | 0.274 | 0.034 | 0.316 |

Comparison to full proposed mean:
| density | wo_smooth success | full success | delta success | wo_smooth cost | full cost | delta cost | wo_smooth route | full route | delta route |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0.00 | 0.990 | 0.973 | +0.017 | 0.000 | 0.000 | +0.000 | 0.990 | 0.989 | +0.001 |
| 0.08 | 0.820 | 0.833 | -0.013 | 0.160 | 0.133 | +0.027 | 0.909 | 0.929 | -0.019 |
| 0.15 | 0.530 | 0.620 | -0.090 | 0.330 | 0.247 | +0.083 | 0.793 | 0.865 | -0.072 |

Decision:
- Removing smooth/accel is harmful across the two seeds, especially at d0.08/d0.15.
- At d0.15 the two-seed mean is success=0.530, cost=0.330, route=0.793; this is well below full proposed and below shield/guard controls.
- Paper claim boundary: smooth/accel terms are not the main mechanism, but they materially stabilize learning/evaluation and should remain in the final full setting unless a later retune proves otherwise.
- Next: continue retune proposed ttc4-cost10-lane1 seed2 to final evaluation; do not launch more reward ablations until this retune is judged.
