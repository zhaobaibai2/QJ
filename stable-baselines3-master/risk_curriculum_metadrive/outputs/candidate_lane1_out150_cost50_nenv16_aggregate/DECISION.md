# Candidate lane1/out150 cost50 n_envs16 aggregate

Generated: 2026-06-30T18:16:43+08:00

Sources:
- outputs/tuning_proposed_defensive_h1500_lane1_out150_cost50_nenv16_1m/evaluations/summary.csv
- outputs/candidate_lane1_out150_cost50_nenv16_seed1_1m/evaluations/summary.csv
- outputs/candidate_lane1_out150_cost50_nenv16_seed2_1m/evaluations/summary.csv

Protocol: proposed, seeds 0/1/2, n_envs=16, timesteps=1M, horizon=1500, ent_coef=0.01, reward_ttc=6, reward_cost=50, reward_lane=1.0, target_speed=18, progress=40, success_bonus=55, crash=120, out=150, ttc_threshold=12.

| density | success mean | success std | cost mean | cost std | collision mean | out mean | route mean |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 0.00 | 0.973 | 0.012 | 0.000 | 0.000 | 0.000 | 0.000 | 0.989 |
| 0.08 | 0.833 | 0.042 | 0.133 | 0.042 | 0.127 | 0.007 | 0.929 |
| 0.15 | 0.620 | 0.122 | 0.247 | 0.070 | 0.233 | 0.013 | 0.865 |

Decision:
- Current main-method candidate: KEEP AS CURRENT BEST, not frozen final.
- d0.15 mean passes the promotion gate (success_mean >= 0.60 and cost_mean <= 0.28), but seed2 is weak (success=0.48, cost=0.32), so the method needs comparison/ablation evidence and possibly one stability-oriented follow-up if later baselines are close.
- Main remaining failure at d0.15 is collision, not out-of-road; lane/out tuning worked on out-of-road but did not fully solve dense-traffic interaction.
