# proposed_wo_lane n_envs=16 seed0-1 aggregate

Generated: 2026-06-30T21:43:33+08:00

Sources:
- `outputs/tuned_ablation_wo_lane_nenv16_seed0_1m/evaluations/summary.csv`
- `outputs/tuned_ablation_wo_lane_nenv16_seed1_1m/evaluations/summary.csv`

Protocol: `proposed_wo_lane`, seeds 0/1, n_envs=16, timesteps=1M, horizon=1500, lane reward ablated (`reward_weights.lane=0.0`), TTC/cost/smooth/accel/action guard/curriculum kept.

Mean over seeds:
| density | success mean | success std | cost mean | cost std | collision mean | out mean | route mean | lane dev mean |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0.00 | 0.940 | 0.085 | 0.000 | 0.000 | 0.000 | 0.000 | 0.989 | 0.347 |
| 0.08 | 0.900 | 0.000 | 0.080 | 0.028 | 0.080 | 0.000 | 0.964 | 0.341 |
| 0.15 | 0.610 | 0.014 | 0.280 | 0.000 | 0.280 | 0.000 | 0.859 | 0.344 |

Comparison to full proposed mean:
| density | wo_lane success | full success | delta success | wo_lane cost | full cost | delta cost | wo_lane route | full route | delta route | wo_lane lane dev | full lane dev | delta lane dev |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0.00 | 0.940 | 0.973 | -0.033 | 0.000 | 0.000 | +0.000 | 0.989 | 0.989 | -0.000 | 0.347 | 0.132 | +0.215 |
| 0.08 | 0.900 | 0.833 | +0.067 | 0.080 | 0.133 | -0.053 | 0.964 | 0.929 | +0.035 | 0.341 | 0.155 | +0.186 |
| 0.15 | 0.610 | 0.620 | -0.010 | 0.280 | 0.247 | +0.033 | 0.859 | 0.865 | -0.006 | 0.344 | 0.178 | +0.166 |

Decision:
- Two seeds agree closely: removing lane reward does not collapse success, but it consistently raises lane deviation to about 0.344 at d0.15.
- At d0.15 the seed0-1 mean is success=0.610, cost=0.280, route=0.859. This is near the full proposed success mean but with higher cost and much worse lateral tracking.
- Paper claim boundary: lane reward is best framed as a lateral-stability and dense-traffic safety/tracking term, not as the sole source of success-rate gains.
- Next: keep shield_only seed2 running. For reward components, prioritize `proposed_wo_smooth` seed1 next because wo_lane already has stable two-seed evidence while smooth has only seed0.
