# Decision: proposed_gated_risk three-seed diagnostic

Time: 2026-07-01T03:44:30+08:00

## Protocol

- Variant: proposed_gated_risk
- Seeds: 0, 1, 2
- Training: PPO, n_envs=16, timesteps=1M, horizon=1500
- Evaluation: 50 episodes per density, densities 0.00/0.08/0.15, n_envs=16
- Mechanism: action guard + curriculum remain enabled; continuous risk penalties are gated by motion/progress and local risk. Event penalties remain ungated.

## Three-seed mean

- d0.00: success=0.940, cost=0.000, route=0.988, gate_rate=0.887.
- d0.08: success=0.867, cost=0.080, route=0.961, gate_rate=0.865.
- d0.15: success=0.600, cost=0.253, route=0.849, gate_rate=0.764.

## Interpretation

Gated risk fixes the risk-only stagnation failure: route completion is usable across all formal densities and zero-cost behavior is no longer caused by not driving. The three-seed d0.15 mean remains slightly below guard_only, shield_only, and the prior retuned full-proposed aggregate, so it should not replace the existing main paper result.

Paper use: keep the main claim guard/shield-centered. Use proposed_gated_risk as a mechanism addendum showing that conditional risk shaping is viable and avoids the risk-only failure, but does not yet provide a statistically stronger main result.
