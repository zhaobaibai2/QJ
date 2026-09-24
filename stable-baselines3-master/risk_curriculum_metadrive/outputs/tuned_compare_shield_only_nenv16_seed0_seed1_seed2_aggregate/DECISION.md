# shield_only n_envs=16 seed0-2 aggregate

Generated: 2026-06-30T21:50:06+08:00

Sources:
- `outputs/tuned_compare_shield_only_nenv16_seed0_1m/evaluations/summary.csv`
- `outputs/tuned_compare_shield_only_nenv16_seed1_1m/evaluations/summary.csv`
- `outputs/tuned_compare_shield_only_nenv16_seed2_1m/evaluations/summary.csv`

Protocol: `shield_only`, seeds 0/1/2, n_envs=16, timesteps=1M, horizon=1500. This is action guard only: no risk reward and no curriculum.

Mean over seeds:
| density | success mean | success std | cost mean | cost std | collision mean | out mean | route mean | lane dev mean |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0.00 | 0.993 | 0.012 | 0.000 | 0.000 | 0.000 | 0.000 | 0.992 | 0.061 |
| 0.08 | 0.913 | 0.050 | 0.067 | 0.023 | 0.047 | 0.020 | 0.959 | 0.070 |
| 0.15 | 0.627 | 0.115 | 0.227 | 0.090 | 0.227 | 0.000 | 0.871 | 0.105 |

Comparison to full proposed mean:
| density | shield success | full success | delta success | shield cost | full cost | delta cost | shield route | full route | delta route |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0.00 | 0.993 | 0.973 | +0.020 | 0.000 | 0.000 | +0.000 | 0.992 | 0.989 | +0.002 |
| 0.08 | 0.913 | 0.833 | +0.080 | 0.067 | 0.133 | -0.067 | 0.959 | 0.929 | +0.030 |
| 0.15 | 0.627 | 0.620 | +0.007 | 0.227 | 0.247 | -0.020 | 0.871 | 0.865 | +0.006 |

Comparison to guard_only mean:
| density | shield success | guard success | delta success | shield cost | guard cost | delta cost | shield route | guard route | delta route |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0.00 | 0.993 | 0.973 | +0.020 | 0.000 | 0.000 | +0.000 | 0.992 | 0.990 | +0.001 |
| 0.08 | 0.913 | 0.873 | +0.040 | 0.067 | 0.093 | -0.027 | 0.959 | 0.940 | +0.019 |
| 0.15 | 0.627 | 0.633 | -0.007 | 0.227 | 0.207 | +0.020 | 0.871 | 0.868 | +0.003 |

Decision:
- shield_only is now a three-seed mechanism control and is very strong. At d0.15 it reaches success=0.627, cost=0.227, route=0.871.
- It matches or slightly exceeds the current full proposed aggregate at d0.15 and is close to guard_only. This means action guard alone explains a large fraction of the current gains.
- Paper claim boundary: current evidence does not support a risk-reward-dominant story. The defensible main line is action guard as the primary stabilizer, curriculum/risk rewards as refinements whose contribution must be shown through high-density and component-specific evidence.
- Next: keep `proposed_wo_smooth` seed1 running and aggregate it with seed0 when complete. After reward-component replication, consider a new full-proposed retune that preserves shield_only stability while adding only a minimal dense-traffic reward refinement.
