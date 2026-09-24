# Decision: baseline three-seed formal comparator aggregate

Time: 2026-07-01T01:27:33+0800

Aggregate root: outputs/tuned_compare_baseline_nenv16_seed0_seed1_seed2_aggregate

Included seeds:
- seed0: outputs/tuned_compare_baseline_nenv16_seed0_1m/evaluations/summary.csv
- seed1: outputs/tuned_compare_baseline_nenv16_seed1_1m/evaluations/summary.csv
- seed2: outputs/tuned_compare_baseline_nenv16_seed2_1m/evaluations/summary.csv

Protocol: `baseline`, seeds 0/1/2, n_envs=16, timesteps=1M, horizon=1500, EPISODES=50. No risk reward, no action guard, no curriculum.

Mean formal evaluation across seed0/1/2:

| density | success | cost | collision | out_of_road | route | speed | lane_dev | ttc_risk |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0.00 | 0.007 | 0.993 | 0.000 | 0.993 | 0.303 | 46.020 | 0.357 | 0.0000 |
| 0.08 | 0.000 | 1.000 | 0.453 | 0.547 | 0.242 | 43.417 | 0.338 | 0.0903 |
| 0.15 | 0.000 | 1.000 | 0.627 | 0.373 | 0.190 | 39.445 | 0.317 | 0.1328 |

Comparison to full proposed mean:

| density | baseline success | full success | delta success | baseline cost | full cost | delta cost | baseline route | full route | delta route |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0.00 | 0.007 | 0.973 | -0.967 | 0.993 | 0.000 | +0.993 | 0.303 | 0.989 | -0.687 |
| 0.08 | 0.000 | 0.833 | -0.833 | 1.000 | 0.133 | +0.867 | 0.242 | 0.929 | -0.687 |
| 0.15 | 0.000 | 0.620 | -0.620 | 1.000 | 0.247 | +0.753 | 0.190 | 0.865 | -0.676 |

Interpretation:
- The unguarded non-curriculum baseline fails the formal held-out protocol: mean success is 0.000 at all densities and mean cost is 1.000 at all densities.
- Unlike the risk comparator, this is not idle stagnation; route completion is nonzero but dominated by out_of_road and collision failures.
- This provides the lower-bound comparator for the action-guard/curriculum evidence chain.

Decision:
- Accept this as the three-seed baseline formal comparator.
- Do not tune this comparator; it is the intended unguarded lower bound.
- Next: launch curriculum seed1/2 to close the remaining main-comparator symmetry gap.

File placement:
- PDFs remain in each single-run `figures/` directory. This aggregate directory intentionally contains CSV and Markdown evidence only.
