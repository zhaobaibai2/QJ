# P3 Seed Extension Decision

generated_at: 2026-07-01T19:13:34

## Decision

Do not launch seed3/seed4 retraining in the current formal evidence package. Keep it as a reviewer-demand reserve experiment.

## Reason

- Current core diagnostics already use 3 training seeds and 120 episodes per method-density cell.
- Wilson/bootstrap CI tables have been generated: `manuscript/table_supp_ci_d015.csv` and `manuscript/table_supp_seed_scatter_d015.csv`.
- P2 external baselines add independent comparison evidence: RCPO-Lagrangian and RSS/TTC.
- The main qualitative gaps are already separated: risk-only non-motion, PPO/RCPO unsafe lower bound, RSS/TTC intermediate, and Guard/Shield/Gated stronger progress-safety tradeoff.
- Training seed3/seed4 for all six core methods would require 12 additional 1M-timestep runs with `--n-envs 16`, and should only be launched if a reviewer/editor explicitly demands 5 training seeds.

## If Needed Later

Run variants: baseline, risk, guard_only, shield_only, proposed_gated_risk, no_action_guard.
Seeds: 3 and 4.
Training: `scripts/train.py --timesteps 1000000 --n-envs 16`.
Evaluation: `scripts/evaluate_from_config.py --n-envs 16` plus IJMLC diagnostics for d=0.15 first.

## Boundary

Do not mix older `outputs/stage1000_true_proposed_s3_nenv8` or `stage1000_true_proposed_s4s5_nenv16` into the current formal matrix, because they are not the same variant set/protocol as the IJMLC core table.
