# proposed_wo_ttc n_envs=16 seed0-2 aggregate

Generated: 2026-06-30T21:20:19+08:00

Sources:
- `outputs/tuned_ablation_wo_ttc_nenv16_seed0_1m/evaluations/summary.csv`
- `outputs/tuned_ablation_wo_ttc_nenv16_seed1_1m/evaluations/summary.csv`
- `outputs/tuned_ablation_wo_ttc_nenv16_seed2_1m/evaluations/summary.csv`

Protocol: `proposed_wo_ttc`, seeds 0/1/2, n_envs=16, timesteps=1M, horizon=1500, ent_coef=0.01, TTC reward ablated (`reward_ttc=0.0`), lane=1.0, cost=50, crash=120, out_of_road=150, target_speed=18, progress=40, success_bonus=55, stage2_success=0.50, stage2_cost=0.25, demote_cost=0.35.

Mean over seeds:
| density | success mean | success std | cost mean | cost std | collision mean | out mean | route mean | lane dev mean |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0.00 | 0.987 | 0.023 | 0.000 | 0.000 | 0.000 | 0.000 | 0.991 | 0.129 |
| 0.08 | 0.900 | 0.072 | 0.067 | 0.046 | 0.067 | 0.000 | 0.950 | 0.141 |
| 0.15 | 0.540 | 0.111 | 0.360 | 0.171 | 0.360 | 0.000 | 0.823 | 0.174 |

Comparison to full proposed mean (`outputs/candidate_lane1_out150_cost50_nenv16_aggregate`):
| density | wo_ttc success | full success | delta success | wo_ttc cost | full cost | delta cost | wo_ttc route | full route | delta route |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0.00 | 0.987 | 0.973 | +0.013 | 0.000 | 0.000 | +0.000 | 0.991 | 0.989 | +0.002 |
| 0.08 | 0.900 | 0.833 | +0.067 | 0.067 | 0.133 | -0.067 | 0.950 | 0.929 | +0.021 |
| 0.15 | 0.540 | 0.620 | -0.080 | 0.360 | 0.247 | +0.113 | 0.823 | 0.865 | -0.042 |

Comparison to guard_only mean (`outputs/tuned_ablation_guard_only_nenv16_aggregate`):
| density | wo_ttc success | guard success | delta success | wo_ttc cost | guard cost | delta cost | wo_ttc route | guard route | delta route |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0.00 | 0.987 | 0.973 | +0.013 | 0.000 | 0.000 | +0.000 | 0.991 | 0.990 | +0.001 |
| 0.08 | 0.900 | 0.873 | +0.027 | 0.067 | 0.093 | -0.027 | 0.950 | 0.940 | +0.010 |
| 0.15 | 0.540 | 0.633 | -0.093 | 0.360 | 0.207 | +0.153 | 0.823 | 0.868 | -0.045 |

Decision:
- TTC ablation is now a three-seed result, not a seed0-only screen.
- `proposed_wo_ttc` is acceptable at d0.00 and strong at d0.08 (mean success=0.900, cost=0.067, route=0.950), so TTC reward is not required for easy/medium-density driving under guard+curriculum.
- At d0.15 it is clearly weaker than the current full proposed aggregate: success=0.540 vs 0.620, cost=0.360 vs 0.247, route=0.823 vs 0.865. It is also weaker than guard_only at d0.15.
- The effect is high-variance but negative on average at high density (d0.15 success std=0.111; seed1 was strong, seeds0/2 were weaker). Paper claim should say TTC reward improves dense-traffic robustness on average, not that removing TTC always collapses.
- This result supports a reward-component story only at high density. It does not overturn the larger mechanism finding that guard+curriculum remains dominant under the current protocol.

Next:
- Keep running `shield_only` seed1 to determine whether action guard alone is seed-stable.
- If `shield_only` seed1 finishes strong, launch `shield_only` seed2 and aggregate; the paper main claim may need to foreground action-guard/curriculum and present risk reward as a dense-traffic refinement rather than the sole core mechanism.
- Replicate `proposed_wo_lane` and `proposed_wo_smooth` only after the shield-only branch is resolved, because guard/shield evidence has higher claim impact.
