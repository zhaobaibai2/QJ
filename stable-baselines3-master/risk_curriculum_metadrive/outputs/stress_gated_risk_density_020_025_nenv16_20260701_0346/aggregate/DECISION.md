# Stress decision: proposed_gated_risk 0.20/0.25

Time: 2026-07-01T03:59:56+08:00

## Protocol

- Frozen proposed_gated_risk seed0/1/2 models
- Densities: 0.20 and 0.25
- Episodes: 50 per density per seed
- n_envs=16, device=cuda

## Three-seed stress mean

- d0.20: success=0.447, cost=0.367, route=0.766, collision=0.367.
- d0.25: success=0.220, cost=0.527, route=0.628, collision=0.527.

## Interpretation

At d0.20, proposed_gated_risk is close to the retuned full-proposed and shield/guard stress band, but does not dominate. At d0.25, it improves over the prior retuned full-proposed and shield_only means in success/route, but remains below guard_only in success and cost. This supports a conditional-risk mechanism addendum, not a replacement of the guard/shield-centered main claim.
