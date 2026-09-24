# Decision: curriculum three-seed formal comparator aggregate

Time: 2026-07-01T01:51:50+0800

Aggregate root: outputs/tuned_compare_curriculum_nenv16_seed0_seed1_seed2_aggregate

Included seeds:
- seed0: outputs/tuned_compare_curriculum_nenv16_seed0_1m/evaluations/summary.csv
- seed1: outputs/tuned_compare_curriculum_nenv16_seed1_1m/evaluations/summary.csv
- seed2: outputs/tuned_compare_curriculum_nenv16_seed2_1m/evaluations/summary.csv

Protocol: `curriculum`, seeds 0/1/2, n_envs=16, timesteps=1M, horizon=1500, EPISODES=50. Curriculum enabled, no risk reward, no action guard.

Mean formal evaluation across seed0/1/2:

| density | success | cost | collision | out_of_road | route | speed | lane_dev | ttc_risk |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0.00 | 0.007 | 0.993 | 0.000 | 0.993 | 0.349 | 46.900 | 0.303 | 0.0000 |
| 0.08 | 0.000 | 1.000 | 0.373 | 0.627 | 0.236 | 42.125 | 0.279 | 0.0968 |
| 0.15 | 0.000 | 1.000 | 0.627 | 0.373 | 0.177 | 38.592 | 0.261 | 0.1760 |

Comparison to baseline mean:

| density | curriculum success | baseline success | delta success | curriculum cost | baseline cost | delta cost | curriculum route | baseline route | delta route |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0.00 | 0.007 | 0.007 | +0.000 | 0.993 | 0.993 | +0.000 | 0.349 | 0.303 | +0.046 |
| 0.08 | 0.000 | 0.000 | +0.000 | 1.000 | 1.000 | +0.000 | 0.236 | 0.242 | -0.006 |
| 0.15 | 0.000 | 0.000 | +0.000 | 1.000 | 1.000 | +0.000 | 0.177 | 0.190 | -0.013 |

Comparison to full proposed mean:

| density | curriculum success | full success | delta success | curriculum cost | full cost | delta cost | curriculum route | full route | delta route |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0.00 | 0.007 | 0.973 | -0.967 | 0.993 | 0.000 | +0.993 | 0.349 | 0.989 | -0.640 |
| 0.08 | 0.000 | 0.833 | -0.833 | 1.000 | 0.133 | +0.867 | 0.236 | 0.929 | -0.693 |
| 0.15 | 0.000 | 0.620 | -0.620 | 1.000 | 0.247 | +0.753 | 0.177 | 0.865 | -0.689 |

Interpretation:
- Curriculum alone improves some training-window behavior, but final held-out evaluation still fails: mean success remains near zero and cost is near or at one across densities.
- It is not a substitute for the action guard. Without guard, final policies still fail mostly through out_of_road at low density and collision at traffic densities.
- Compared with the risk comparator, curriculum-only drives substantially farther, but this progress is unsafe.

Decision:
- Accept this as the three-seed curriculum formal comparator.
- Do not tune this comparator; it answers the no-risk/no-guard curriculum-only question.
- Main comparator symmetry is now closed for baseline, risk, curriculum, guard_only, shield_only, and full proposed aggregates.

File placement:
- PDFs remain in each single-run `figures/` directory, including `curriculum_stage.pdf`. This aggregate directory intentionally contains CSV and Markdown evidence only.
