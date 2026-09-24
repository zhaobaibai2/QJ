# Light-Risk Proposed Retuning Decision

Generated: 2026-06-30T20:15:44+08:00

Roots:
- outputs/tuning_proposed_light_risk_ttc3_cost25_lane03_nenv16_seed0_1m
- outputs/tuning_proposed_light_risk_ttc3_cost25_lane03_nenv16_seed2_1m

Protocol: proposed, seeds 0 and 2, n_envs=16, timesteps=1M, horizon=1500, 50 eval episodes per density. Weights: ttc=3, cost=25, lane=0.3, crash=80, out=150, overspeed=3, target_speed=18, progress=40, success_bonus=55, ttc_threshold=12.

Mean over seeds 0 and 2:
- d0.00: success=0.970, cost=0.000, route=0.990
- d0.08: success=0.880, cost=0.090, collision=0.090, out=0.000, route=0.943
- d0.15: success=0.580, cost=0.290, collision=0.280, out=0.010, route=0.840

Decision:
- Not promoted as the current main full-proposed setting.
- It slightly improves the medium-density point relative to the current three-seed full proposed/guard-only means, but it underperforms at d0.15 where the paper needs the strongest evidence.
- Relative to guard_only at d0.15, light-risk has lower success and route completion and higher cost/collision. Therefore the risk-reward contribution is still not proven as a robust dominant mechanism.
- Next evidence priority: complete reward-component ablations (`proposed_wo_lane`, `proposed_wo_smooth`) under the tuned full-proposed protocol, while keeping guard+curriculum as the current strongest mechanism claim.
