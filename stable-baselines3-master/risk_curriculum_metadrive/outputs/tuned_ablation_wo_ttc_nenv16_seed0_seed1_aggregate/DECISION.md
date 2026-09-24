# Mechanism Screen Update

Generated: 2026-06-30T21:00:21+08:00

Completed in this update:
- proposed_wo_ttc seed1: outputs/tuned_ablation_wo_ttc_nenv16_seed1_1m
- shield_only seed0: outputs/tuned_compare_shield_only_nenv16_seed0_1m

proposed_wo_ttc seed0-1 mean:
- d0.00: success=1.000, cost=0.000, route=0.992
- d0.08: success=0.870, cost=0.080, collision=0.080, route=0.946
- d0.15: success=0.550, cost=0.370, collision=0.370, route=0.824

shield_only seed0:
- d0.00: success=1.00, cost=0.00, route=0.992
- d0.08: success=0.96, cost=0.04, collision=0.02, out=0.02, route=0.975
- d0.15: success=0.56, cost=0.32, collision=0.32, out=0.00, route=0.833

Interpretation:
- proposed_wo_ttc is high-variance: seed0 was clearly weak at d0.15, seed1 was strong. Do not claim TTC necessity until seed2 resolves the variance.
- shield_only is not a collapse. It is very strong at d0.00/d0.08 but weaker at d0.15 than guard_only/full seed0, so action guard alone is a major mechanism but does not fully solve dense traffic.

Next:
- Run proposed_wo_ttc seed2.
- Run shield_only seed1 to test whether the strong medium-density result is seed-stable.
