# External Seed Robustness Decision

Protocol: frozen trained models, n_envs=16, test_start_seed in {20000, 30000}, densities 0.08 and 0.15, 50 episodes per density per trained seed.

## Density 0.15 ranking

1. shield_only: success=0.687, cost=0.207, route=0.878, units=6, episodes=300
2. proposed_gated_risk: success=0.663, cost=0.213, route=0.866, units=6, episodes=300
3. guard_only: success=0.613, cost=0.240, route=0.852, units=6, episodes=300
4. retuned_full: success=0.597, cost=0.280, route=0.838, units=6, episodes=300
5. no_action_guard: success=0.000, cost=1.000, route=0.191, units=6, episodes=300
6. risk_only: success=0.000, cost=0.000, route=0.009, units=6, episodes=300

## Claim boundary

- This is external scenario-seed validation of frozen models, not additional training or tuning.
- Use it to support robustness of the guard/shield-centered conclusion if positive methods remain ahead of risk-only/no-action-guard controls.
- If a positive method drops materially below the formal held-out table, report the drop as external-seed sensitivity rather than hiding it.
- Risk-only zero-cost rows must still be interpreted together with route completion.
