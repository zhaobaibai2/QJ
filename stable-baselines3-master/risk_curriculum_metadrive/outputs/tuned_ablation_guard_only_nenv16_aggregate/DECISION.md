# Guard-only n_envs=16 aggregate decision

Sources:
- seed0: `outputs/tuned_ablation_guard_only_nenv16_seed0_1m/evaluations/summary.csv`
- seed1: `outputs/tuned_ablation_guard_only_nenv16_seed1_1m/evaluations/summary.csv`
- seed2: `outputs/tuned_ablation_guard_only_nenv16_seed2_1m/evaluations/summary.csv`

Mean by density:
| density | success | route_completion | collision | out_of_road | cost | reward | episode_length | speed | lane_deviation | steering_variation | accel_variation | ttc_risk |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0.000 | 0.973 | 0.990 | 0.000 | 0.000 | 0.000 | 571.668 | 1105.480 | 18.309 | 0.062 | 0.010 | 0.226 | 0.000 |
| 0.080 | 0.873 | 0.940 | 0.093 | 0.000 | 0.093 | 536.204 | 1076.860 | 17.989 | 0.079 | 0.013 | 0.236 | 0.004 |
| 0.150 | 0.633 | 0.868 | 0.200 | 0.007 | 0.207 | 454.250 | 1100.900 | 16.124 | 0.136 | 0.017 | 0.311 | 0.016 |

Std by density:
| density | success | route_completion | collision | out_of_road | cost | reward | episode_length | speed | lane_deviation | steering_variation | accel_variation | ttc_risk |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0.000 | 0.023 | 0.001 | 0.000 | 0.000 | 0.000 | 15.796 | 26.191 | 0.004 | 0.017 | 0.006 | 0.001 | 0.000 |
| 0.080 | 0.012 | 0.012 | 0.012 | 0.000 | 0.012 | 10.846 | 12.318 | 0.105 | 0.016 | 0.006 | 0.005 | 0.001 |
| 0.150 | 0.023 | 0.025 | 0.040 | 0.012 | 0.042 | 18.864 | 50.581 | 0.105 | 0.021 | 0.009 | 0.012 | 0.001 |

Comparison to full proposed mean (guard_only - full):
| density | success_guard_only | success_full_proposed | delta_success_guard_minus_full | cost_guard_only | cost_full_proposed | delta_cost_guard_minus_full | route_completion_guard_only | route_completion_full_proposed | delta_route_completion_guard_minus_full | collision_guard_only | collision_full_proposed | delta_collision_guard_minus_full | out_of_road_guard_only | out_of_road_full_proposed | delta_out_of_road_guard_minus_full |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0.000 | 0.973 | 0.973 | 0.000 | 0.000 | 0.000 | 0.000 | 0.990 | 0.989 | 0.001 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| 0.080 | 0.873 | 0.833 | 0.040 | 0.093 | 0.133 | -0.040 | 0.940 | 0.929 | 0.012 | 0.093 | 0.127 | -0.033 | 0.000 | 0.007 | -0.007 |
| 0.150 | 0.633 | 0.620 | 0.013 | 0.207 | 0.247 | -0.040 | 0.868 | 0.865 | 0.003 | 0.200 | 0.233 | -0.033 | 0.007 | 0.013 | -0.007 |

Decision:
- Guard-only is not a weak ablation. At d0.15 it matches or slightly exceeds the current full proposed mean: success 0.633 vs 0.620, cost 0.207 vs 0.247, route 0.868 vs 0.865.
- This means the current full risk-reward setting cannot support a strong claim that risk reward improves over guard+curriculum. The evidence currently supports guard+curriculum as the dominant mechanism.
- Next action: retune full proposed with reduced risk-reward aggressiveness or reframe the method/claim. Do not freeze the paper table with risk reward as the central improvement until this is resolved.
