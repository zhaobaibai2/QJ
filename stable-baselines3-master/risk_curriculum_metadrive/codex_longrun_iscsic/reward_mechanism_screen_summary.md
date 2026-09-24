# Reward and Mechanism Screen Summary

All screens use seed=2, n_envs=10, eval_n_envs=10, 50 episodes per density unless noted. Formal proposed uses 1.5M timesteps; screens use 500k.

| screen | kind | density | success | cost | route | collision | out | shield | change |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| formal_proposed_s2_1p5M | formal | 0.00 | 0.760 | 0.000 | 0.967 | 0.000 | 0.000 | 0.865 | baseline RewardWeights, full 1.5M |
| formal_proposed_s2_1p5M | formal | 0.08 | 0.700 | 0.140 | 0.927 | 0.140 | 0.000 | 0.847 | baseline RewardWeights, full 1.5M |
| formal_proposed_s2_1p5M | formal | 0.15 | 0.540 | 0.400 | 0.755 | 0.400 | 0.000 | 0.756 | baseline RewardWeights, full 1.5M |
| R1_completion_boost | reward_screen | 0.00 | 0.900 | 0.000 | 0.983 | 0.000 | 0.000 | 0.860 | progress=45 success_bonus=80 |
| R1_completion_boost | reward_screen | 0.08 | 0.900 | 0.020 | 0.968 | 0.020 | 0.000 | 0.847 | progress=45 success_bonus=80 |
| R1_completion_boost | reward_screen | 0.15 | 0.320 | 0.520 | 0.761 | 0.520 | 0.000 | 0.725 | progress=45 success_bonus=80 |
| R5_moderate_completion | reward_screen | 0.00 | 0.900 | 0.000 | 0.983 | 0.000 | 0.000 | 0.856 | progress=40 success_bonus=60 |
| R5_moderate_completion | reward_screen | 0.08 | 0.740 | 0.060 | 0.948 | 0.060 | 0.000 | 0.845 | progress=40 success_bonus=60 |
| R5_moderate_completion | reward_screen | 0.15 | 0.440 | 0.500 | 0.751 | 0.500 | 0.000 | 0.734 | progress=40 success_bonus=60 |
| R3_completion_plus_safety | reward_screen | 0.00 | 0.800 | 0.000 | 0.974 | 0.000 | 0.000 | 0.862 | progress=45 success_bonus=80 crash/out=120 |
| R3_completion_plus_safety | reward_screen | 0.08 | 0.760 | 0.120 | 0.948 | 0.120 | 0.000 | 0.850 | progress=45 success_bonus=80 crash/out=120 |
| R3_completion_plus_safety | reward_screen | 0.15 | 0.500 | 0.500 | 0.779 | 0.500 | 0.000 | 0.738 | progress=45 success_bonus=80 crash/out=120 |
| R2_safety_soften | reward_screen | 0.00 | 0.780 | 0.000 | 0.972 | 0.000 | 0.000 | 0.859 | cost=15 overspeed=1.0 |
| R2_safety_soften | reward_screen | 0.08 | 0.740 | 0.060 | 0.936 | 0.060 | 0.000 | 0.844 | cost=15 overspeed=1.0 |
| R2_safety_soften | reward_screen | 0.15 | 0.440 | 0.480 | 0.747 | 0.460 | 0.020 | 0.736 | cost=15 overspeed=1.0 |
| R4_no_action_guard | mechanism_screen | 0.00 | 0.020 | 0.980 | 0.297 | 0.000 | 0.980 | 0.000 | use_action_guard=False |
| R4_no_action_guard | mechanism_screen | 0.08 | 0.000 | 1.000 | 0.247 | 0.380 | 0.620 | 0.000 | use_action_guard=False |
| R4_no_action_guard | mechanism_screen | 0.15 | 0.000 | 1.000 | 0.181 | 0.480 | 0.520 | 0.000 | use_action_guard=False |
| A_ttc_ablation | mechanism_screen | 0.00 | 0.880 | 0.000 | 0.982 | 0.000 | 0.000 | 0.855 | reward_ttc=0.0 |
| A_ttc_ablation | mechanism_screen | 0.08 | 0.680 | 0.180 | 0.903 | 0.160 | 0.020 | 0.835 | reward_ttc=0.0 |
| A_ttc_ablation | mechanism_screen | 0.15 | 0.340 | 0.600 | 0.727 | 0.520 | 0.080 | 0.747 | reward_ttc=0.0 |

## Current conclusions
- R1 improves d0.08 but fails d0.15, so strong completion boost alone is too aggressive.
- R5 moderate completion has promising mid-run windows but does not beat formal proposed at final eval.
- R3 does not beat formal proposed and loses R1 medium-density gain.
- R2 does not improve high-density success, so simply softening cost/overspeed is not enough.
- no_action_guard collapses safety/completion, so action guard is necessary.
- proposed_wo_ttc worsens medium/high-density safety, so TTC reward should remain enabled.
- Current formal proposed baseline remains the best high-density seed2 candidate among this screen batch.
