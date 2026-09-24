# External Seed Robustness n_envs=16

Frozen-model reviewer validation. This sweep reuses completed formal models and changes only `test_start_seed` to 20000 and 30000. It evaluates densities 0.08 and 0.15 with 50 episodes per density, n_envs=16.

Use `aggregate/mean_by_label_density.csv`, `aggregate/rank_density_0p15.csv`, and `aggregate/DECISION.md` for paper-facing interpretation. Raw per-episode rows are in `aggregate/all_episode_rows.csv`.
