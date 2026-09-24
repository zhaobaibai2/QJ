# Seed0 Reward Component Ablation Summary

Generated: 2026-06-30T20:35:35+08:00

Included methods:
- full_proposed: tuned full proposed seed0
- wo_ttc: tuned proposed_wo_ttc seed0
- wo_lane: tuned proposed_wo_lane seed0
- wo_smooth: tuned proposed_wo_smooth seed0
- guard_only: guard+curriculum seed0

High-density d0.15 snapshot:
- full_proposed: d0.15 success=0.70, cost=0.24, collision=0.22, route=0.872, lane_dev=0.138
- wo_ttc: d0.15 success=0.44, cost=0.54, collision=0.54, route=0.743, lane_dev=0.181
- wo_lane: d0.15 success=0.60, cost=0.28, collision=0.28, route=0.862, lane_dev=0.348
- wo_smooth: d0.15 success=0.58, cost=0.24, collision=0.24, route=0.849, lane_dev=0.154
- guard_only: d0.15 success=0.62, cost=0.22, collision=0.20, route=0.861, lane_dev=0.151

Interpretation:
- Removing TTC is the largest degradation on seed0, especially cost/collision at d0.15.
- Removing lane reward keeps medium-density success high but increases lane deviation and weakens high-density success/cost.
- Removing smooth/accel terms does not collapse final evaluation, but it weakens high-density success and training conversion relative to full seed0.
- Guard-only remains close to full seed0, reinforcing that guard+curriculum is a major mechanism; full seed0 still has the best d0.15 success among the reward-component seed0 table.

Next decision:
- Replicate selected reward-component ablations beyond seed0 before paper-level claims. Priority order: wo_ttc seed1/2 for the strongest negative effect, then wo_lane/wo_smooth seed1 if resources allow.
- Also run shield_only seed0 to isolate whether the action guard alone works without curriculum.
