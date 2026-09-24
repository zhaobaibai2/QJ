# Decision: risk three-seed formal comparator aggregate

Time: 2026-07-01T00:58:42+0800

Aggregate root: outputs/tuned_compare_risk_nenv16_seed0_seed1_seed2_aggregate

Included seeds:
- seed0: outputs/tuned_compare_risk_nenv16_seed0_1m/evaluations/summary.csv
- seed1: outputs/tuned_compare_risk_nenv16_seed1_1m/evaluations/summary.csv
- seed2: outputs/tuned_compare_risk_nenv16_seed2_1m/evaluations/summary.csv

Protocol: `risk`, seeds 0/1/2, n_envs=16, timesteps=1M, horizon=1500, EPISODES=50. This keeps risk reward and action guard enabled, but disables curriculum.

Mean formal evaluation across seed0/1/2:

| density | success | cost | collision | out_of_road | route | speed | lane_dev | ttc_risk |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0.00 | 0.000 | 0.000 | 0.000 | 0.000 | 0.009 | 0.013 | 0.003 | 0.0000 |
| 0.08 | 0.000 | 0.000 | 0.000 | 0.000 | 0.009 | 0.013 | 0.005 | 0.0000 |
| 0.15 | 0.000 | 0.000 | 0.000 | 0.000 | 0.009 | 0.014 | 0.006 | 0.0000 |

Comparison to full proposed mean:

| density | risk success | full success | delta success | risk cost | full cost | delta cost | risk route | full route | delta route |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0.00 | 0.000 | 0.973 | -0.973 | 0.000 | 0.000 | +0.000 | 0.009 | 0.989 | -0.981 |
| 0.08 | 0.000 | 0.833 | -0.833 | 0.000 | 0.133 | -0.133 | 0.009 | 0.929 | -0.920 |
| 0.15 | 0.000 | 0.620 | -0.620 | 0.000 | 0.247 | -0.247 | 0.009 | 0.865 | -0.856 |

Interpretation:
- The three risk seeds reproduce the same low-speed route-stagnation failure: success=0.000 at all evaluated traffic densities and route completion remains around 0.009.
- The zero cost is not a valid safety win because the policy barely drives; it avoids collisions by not making meaningful progress.
- Risk reward plus action guard without curriculum is therefore not a viable formal comparator under this protocol.

Decision:
- Accept this as the three-seed risk comparator aggregate.
- Do not tune this comparator mid-stream; tuning would change the comparator question.
- Paper boundary: use this to argue that dense risk reward alone does not explain the usable-driving result; curriculum and/or guarded training dynamics are required for learning progress.

File placement:
- PDFs remain in each single-run `figures/` directory. This aggregate directory intentionally contains CSV and Markdown evidence only.
