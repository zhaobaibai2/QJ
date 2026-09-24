# P2 External Baselines Protocol

generated_at: 2026-07-01T17:34:45
run_group: ijmlc_p2_external_20260701_1733

## Formal Training Policy
- RCPO/PPO-Lagrangian uses `scripts/train.py --variant rcpo_lagrangian`.
- Each RCPO training run uses `--n-envs 16` and `--timesteps 1000000`.
- Seeds are run sequentially to avoid opening 48 MetaDrive subprocesses at once.
- Resource watchdog is active: MemAvailable < 3 GiB or GPU free < 2048 MiB stops current P2 tasks.

## Formal Evaluation Policy
- Normal SB3 evaluation remains `scripts/evaluate_from_config.py --n-envs 16` when used for aggregate success/cost tables.
- IJMLC diagnostic evaluation remains single-env per shard because TTC, stop ratio, per-step latency and external action filters need step-level state.
- RSS/TTC classical filter is evaluated as an external action filter on frozen PPO baseline policies, not as the proposed Guard/Shield.

## Claims Supported
- RCPO/PPO-Lagrangian: training-based safe-RL external baseline without runtime action guard.
- RSS/TTC: non-learning classical runtime filter baseline applied to identical frozen PPO policies.
- These two rows fill P2/Table4 external comparison; they do not replace the P1/P4 GuardShield diagnostic evidence.
