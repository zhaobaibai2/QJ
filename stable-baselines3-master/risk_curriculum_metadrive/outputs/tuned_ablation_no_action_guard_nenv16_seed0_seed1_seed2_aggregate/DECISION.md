# Decision: no_action_guard three-seed ablation aggregate

Time: 2026-07-01T00:13:20+0800

Aggregate root: outputs/tuned_ablation_no_action_guard_nenv16_seed0_seed1_seed2_aggregate

Included seeds:
- seed0: outputs/tuned_ablation_no_action_guard_nenv16_seed0_1m/evaluations/summary.csv
- seed1: outputs/tuned_ablation_no_action_guard_nenv16_seed1_1m/evaluations/summary.csv
- seed2: outputs/tuned_ablation_no_action_guard_nenv16_seed2_1m/evaluations/summary.csv

Mean formal evaluation across seed0/1/2:

| density | success | cost | collision | out_of_road | route | lane_dev | ttc_risk |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 0.0 | 0.027 | 0.973 | 0.000 | 0.973 | 0.254 | 0.327 | 0.0000 |
| 0.08 | 0.000 | 1.000 | 0.293 | 0.707 | 0.202 | 0.316 | 0.1199 |
| 0.15 | 0.000 | 1.000 | 0.513 | 0.487 | 0.172 | 0.281 | 0.1953 |

Key seed-level observation:
- seed1/seed2 showed temporary training-window recovery near the middle/end of training, but held-out evaluation still collapsed to success=0 and cost=1.0 at all densities.
- Failure mode changes with density: low density is dominated by out_of_road, while medium/high density add substantial collision.

Interpretation:
- Removing the action guard is a decisive failure under the formal n_envs=16 held-out protocol.
- Training-window success is not reliable for this ablation; the final evaluation exposes unsafe high-speed/off-road behavior.
- This supports a strong but precise claim: action-level guarding is necessary for stable held-out safety and completion in the current method. It should not be softened based on mid-run logs.

Decision:
- Accept this aggregate as the three-seed no_action_guard ablation.
- No further no_action_guard rescue/tuning should be run; rescue would change the ablation question.
- Use this in the paper as a key mechanism ablation, with seed-level rows visible to avoid over-summarizing.

Next action:
- Move to remaining evidence gaps: either complete `wo_lane` and `wo_smooth` seed2 for ablation symmetry, or run formal comparator seed1/2 for baseline/curriculum/risk.
