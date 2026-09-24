# Decision: proposed retune ttc4-cost10-lane1 seed2

Time: 2026-06-30T22:11:54+0800

Root: `outputs/retune_proposed_ttc4_cost10_lane1_nenv16_seed2_1m`

Protocol:
- variant: proposed
- seed: 2
- n_envs: 16
- total steps: 1,000,000
- horizon: 1500
- eval episodes: 50 per density
- reward setting: ttc=4.0, cost=10.0, lane=1.0, smooth=0.02, accel=0.01, crash=100.0, out=150.0, target_speed=18 km/h, progress=40.0

Formal evaluation:

| density | success | cost | collision | out_of_road | route | lane_dev | ttc_risk |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 0.00 | 1.00 | 0.00 | 0.00 | 0.00 | 0.991 | 0.116 | 0.0000 |
| 0.08 | 0.86 | 0.10 | 0.10 | 0.00 | 0.951 | 0.114 | 0.0044 |
| 0.15 | 0.68 | 0.16 | 0.14 | 0.02 | 0.871 | 0.144 | 0.0125 |

Comparisons:
- Original full proposed seed2 at d0.15: success 0.48, cost 0.32, route 0.826. This retune improves seed2 to success 0.68, cost 0.16, route 0.871.
- Current full proposed three-seed mean at d0.15: success 0.620, cost 0.247, route 0.865. This single seed is above that mean, but this is not enough for a final claim.
- shield_only seed2 at d0.15: success 0.76, cost 0.14, route 0.913. The retune is improved but still does not beat the strongest action-guard-only seed2.
- shield_only three-seed mean at d0.15: success 0.627, cost 0.227, route 0.871. The retune seed2 is competitive with this mean, but needs seed0/seed1.

Decision:
- Promote this retune to a multi-seed candidate, not to the final method yet.
- Launch seed0 and seed1 with the exact same configuration.
- Claim boundary until seed0/seed1 finish: risk reward should be framed as a candidate high-density refinement around the action guard, not as a proven dominant mechanism.
