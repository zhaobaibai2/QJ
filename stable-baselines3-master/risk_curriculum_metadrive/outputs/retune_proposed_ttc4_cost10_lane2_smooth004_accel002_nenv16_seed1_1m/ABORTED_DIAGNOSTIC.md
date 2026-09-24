
## 2026-06-30 abort lateral/smooth retune lane2-smooth004-accel002 seed1/seed2
- Time: 2026-06-30T22:38:56+0800.
- Roots: outputs/retune_proposed_ttc4_cost10_lane2_smooth004_accel002_nenv16_seed1_1m and seed2_1m.
- Abort reason: mid-run evidence showed severe progress suppression. At about 524k/540k timesteps both runs remained in stage0 with window_route_completion about 0.10/0.09 and success_rate 0. This is much worse than the preceding ttc4-cost10-lane1 retune, which had already reached stage1/2 by this point.
- Diagnosis: lane=2.0 plus smooth=0.04/accel=0.02 over-regularizes motion and should not be completed as a formal candidate.
- Decision: stop these diagnostic runs and launch a gentler lateral retune instead: lane around 1.25, smooth 0.03, accel 0.015, with slightly higher progress reward to preserve motion.
