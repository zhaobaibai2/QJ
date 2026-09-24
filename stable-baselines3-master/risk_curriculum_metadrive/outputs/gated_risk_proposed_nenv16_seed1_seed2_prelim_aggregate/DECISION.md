# PRELIMINARY 2-seed decision: proposed_gated_risk

This aggregate uses only seeds 1 and 2. It is diagnostic and must not be used as a final three-seed table.

## Two-seed means

- d0.00: success=0.940, cost=0.000, route=0.987, gate_rate=0.895.
- d0.08: success=0.850, cost=0.080, route=0.959, gate_rate=0.876.
- d0.15: success=0.590, cost=0.280, route=0.843, gate_rate=0.764.

## Interpretation

The gated-risk mechanism fixes the prior risk-only route-stagnation failure and produces usable held-out driving at all formal densities. It does not currently displace the guard_only/shield_only/retuned-full three-seed evidence at d0.15, where success is slightly lower and cost is slightly higher.

Decision: launch seed0 to complete the three-seed diagnostic. Keep the paper claim boundary guard/shield-centered unless seed0 materially changes the aggregate.
