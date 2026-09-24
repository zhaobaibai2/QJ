# shield_only n_envs=16 seed0-1 interim aggregate

Generated: 2026-06-30T21:25:29+08:00

Sources:
- `outputs/tuned_compare_shield_only_nenv16_seed0_1m/evaluations/summary.csv`
- `outputs/tuned_compare_shield_only_nenv16_seed1_1m/evaluations/summary.csv`

Protocol: `shield_only`, seeds 0/1, n_envs=16, timesteps=1M, horizon=1500. This is action guard only: no risk reward and no curriculum.

Mean over seeds:
| density | success mean | success std | cost mean | cost std | collision mean | out mean | route mean | lane dev mean |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0.00 | 0.990 | 0.014 | 0.000 | 0.000 | 0.000 | 0.000 | 0.991 | 0.067 |
| 0.08 | 0.940 | 0.028 | 0.060 | 0.028 | 0.040 | 0.020 | 0.960 | 0.078 |
| 0.15 | 0.560 | 0.000 | 0.270 | 0.071 | 0.270 | 0.000 | 0.850 | 0.117 |

Decision:
- shield_only is clearly not a weak control. With only two seeds it reaches d0.08 success=0.940, cost=0.060, route=0.960; at d0.15 it reaches success=0.560, cost=0.270, route=0.850.
- It remains below full proposed and guard_only on high-density success, but seed1 confirms seed0 was not a one-off. Action guard alone is a major mechanism.
- Next action: launch shield_only seed2 to make this a proper three-seed mechanism control before final paper claims.
