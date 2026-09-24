# P2 External Baselines Final Report

generated_at: 2026-07-01T18:23:26
run_group: ijmlc_p2_external_20260701_1733

## Completed Artifacts
- `results/ijmlc_control/p2_external_baselines/p2_rcpo_lagrangian_manifest.csv`
- `results/ijmlc_control/p2_external_baselines/p2_rss_ttc_filter_manifest.csv`
- `results/ijmlc_control/p2_external_baselines/rcpo_train_status.csv`
- `results/ijmlc_control/p2_external_baselines/rcpo_post_eval_status.csv`
- `results/ijmlc_control/p2_external_baselines/rss_ttc_eval_status.csv`
- `results/ijmlc_control/raw_csv/p2_external_all_episodes.csv`
- `results/ijmlc_control/summary_tables/p2_external_with_core_aggregate.csv`
- `results/ijmlc_control/manuscript/table4_external_baselines_d015.csv`
- `results/ijmlc_control/manuscript/table4_external_baselines_d015.tex`

## Protocol Verification
- RCPO/PPO-Lagrangian training: 3 seeds, `--timesteps 1000000`, `--n-envs 16`, models saved for seed0/1/2.
- RCPO normal evaluation: 3 seeds, `evaluate_from_config.py --n-envs 16`, 40 episodes per density.
- RCPO IJMLC diagnostics: 3 shards × 160 episodes = 480 episodes.
- RSS/TTC diagnostics: 3 shards × 160 episodes = 480 episodes, external action filter on frozen PPO baseline.
- Resource watchdog remained active; no low-memory trigger occurred.

## Table 4 d=0.15 Key Rows
| method | episodes | train_seeds | success_pct | cost_pct | route_completion_pct | collision_pct | out_of_road_pct | low_progress_pct | stop_ratio_pct | mean_speed_kmh | ttc_dangerous_pct | interventions_per_100_steps | control_loop_p95_ms |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PPO | 120 | 3 | 0.000 | 100.000 | 20.746 | 63.333 | 36.667 | 57.500 | 0.145 | 41.053 | 60.353 | 0.000 | 16.932 |
| RSS/TTC filter | 120 | 3 | 53.333 | 44.167 | 78.943 | 41.667 | 2.500 | 2.500 | 1.840 | 18.167 | 13.351 | 71.664 | 9.769 |
| RCPO-Lagrangian | 120 | 3 | 0.000 | 100.000 | 22.144 | 69.167 | 30.833 | 55.000 | 0.308 | 39.446 | 60.102 | 0.000 | 4.615 |
| Guard | 120 | 3 | 59.167 | 20.833 | 86.382 | 18.333 | 2.500 | 0.000 | 2.449 | 15.802 | 11.818 | 69.646 | 13.310 |
| Shield | 120 | 3 | 62.500 | 19.167 | 85.687 | 15.833 | 3.333 | 0.833 | 2.803 | 15.887 | 11.352 | 70.751 | 12.681 |
| Gated-risk | 120 | 3 | 61.667 | 18.333 | 86.874 | 18.333 | 0.000 | 0.833 | 3.527 | 15.303 | 11.421 | 67.872 | 12.398 |

## Interpretation
- RCPO-Lagrangian completed as a training-based safe-RL baseline, but it does not improve over PPO at d=0.15: success remains 0%, cost remains 100%, and route completion is only 22.1%. This should be reported as an external baseline failure, not hidden.
- RSS/TTC improves PPO substantially at d=0.15: success 53.3%, cost 44.2%, route completion 78.9%, showing that a classical runtime filter is a meaningful external comparator.
- Guard/Shield/Gated-risk remain stronger than RSS/TTC on safety at d=0.15, with cost around 18.3-20.8% and route completion around 85.7-86.9%.
- This supports the manuscript claim that runtime action/execution intervention is necessary; reward-level or training-only cost penalties are insufficient in this setup.

## Claim Boundaries
- Do not claim formal safety or certified guarantees.
- RCPO is a simple PPO-Lagrangian baseline implemented in this codebase because `sb3_contrib` is unavailable in the remote `sb3` environment.
- RSS/TTC is an external action filter, not the proposed Guard/Shield implementation.
- All P2 results are MetaDrive closed-loop simulation evidence, not real-world deployment evidence.

## Raw Status Snapshots

### RCPO Train Status
```csv
seed,status,start_time,end_time,exit_code,model_path,log_path
0,done,2026-07-01T17:34:52+08:00,2026-07-01T17:49:03+08:00,0,outputs/ijmlc_p2_external_baselines/rcpo_lagrangian_1m_nenv16/rcpo_lagrangian_ppo_s0/model/final_model.zip,results/ijmlc_control/logs/ijmlc_p2_external_20260701_1733_rcpo_s0.log
1,done,2026-07-01T17:49:03+08:00,2026-07-01T18:01:45+08:00,0,outputs/ijmlc_p2_external_baselines/rcpo_lagrangian_1m_nenv16/rcpo_lagrangian_ppo_s1/model/final_model.zip,results/ijmlc_control/logs/ijmlc_p2_external_20260701_1733_rcpo_s1.log
2,done,2026-07-01T18:01:45+08:00,2026-07-01T18:15:39+08:00,0,outputs/ijmlc_p2_external_baselines/rcpo_lagrangian_1m_nenv16/rcpo_lagrangian_ppo_s2/model/final_model.zip,results/ijmlc_control/logs/ijmlc_p2_external_20260701_1733_rcpo_s2.log
```

### RCPO Eval Status
```csv
stage,seed,status,start_time,end_time,exit_code,output_path,log_path
normal_eval,0,done,2026-07-01T18:16:32+08:00,2026-07-01T18:17:29+08:00,0,results/ijmlc_control/p2_external_baselines/rcpo_normal_eval_nenv16/rcpo_lagrangian_ppo_s0.csv,results/ijmlc_control/logs/ijmlc_p2_external_20260701_1733_rcpo_normal_eval_s0.log
normal_eval,1,done,2026-07-01T18:17:29+08:00,2026-07-01T18:18:27+08:00,0,results/ijmlc_control/p2_external_baselines/rcpo_normal_eval_nenv16/rcpo_lagrangian_ppo_s1.csv,results/ijmlc_control/logs/ijmlc_p2_external_20260701_1733_rcpo_normal_eval_s1.log
normal_eval,2,done,2026-07-01T18:18:27+08:00,2026-07-01T18:19:30+08:00,0,results/ijmlc_control/p2_external_baselines/rcpo_normal_eval_nenv16/rcpo_lagrangian_ppo_s2.csv,results/ijmlc_control/logs/ijmlc_p2_external_20260701_1733_rcpo_normal_eval_s2.log
diagnostic_eval,1,done,2026-07-01T18:19:30+08:00,2026-07-01T18:21:13+08:00,0,results/ijmlc_control/raw_csv/ijmlc_p2_external_20260701_1733_rcpo_diag_s1_episodes.csv,results/ijmlc_control/logs/ijmlc_p2_external_20260701_1733_rcpo_diag_s1.log
diagnostic_eval,0,done,2026-07-01T18:19:30+08:00,2026-07-01T18:21:19+08:00,0,results/ijmlc_control/raw_csv/ijmlc_p2_external_20260701_1733_rcpo_diag_s0_episodes.csv,results/ijmlc_control/logs/ijmlc_p2_external_20260701_1733_rcpo_diag_s0.log
diagnostic_eval,2,done,2026-07-01T18:19:30+08:00,2026-07-01T18:21:39+08:00,0,results/ijmlc_control/raw_csv/ijmlc_p2_external_20260701_1733_rcpo_diag_s2_episodes.csv,results/ijmlc_control/logs/ijmlc_p2_external_20260701_1733_rcpo_diag_s2.log
```

### RSS/TTC Eval Status
```csv
seed,status,start_time,end_time,exit_code,run_id,raw_csv,summary_csv,log_path
0,done,2026-07-01T17:34:52+08:00,2026-07-01T17:49:51+08:00,0,ijmlc_p2_external_20260701_1733_rss_ttc_s0,results/ijmlc_control/raw_csv/ijmlc_p2_external_20260701_1733_rss_ttc_s0_episodes.csv,results/ijmlc_control/summary_tables/ijmlc_p2_external_20260701_1733_rss_ttc_s0_summary.csv,results/ijmlc_control/logs/ijmlc_p2_external_20260701_1733_rss_ttc_s0.log
1,done,2026-07-01T17:34:52+08:00,2026-07-01T17:49:52+08:00,0,ijmlc_p2_external_20260701_1733_rss_ttc_s1,results/ijmlc_control/raw_csv/ijmlc_p2_external_20260701_1733_rss_ttc_s1_episodes.csv,results/ijmlc_control/summary_tables/ijmlc_p2_external_20260701_1733_rss_ttc_s1_summary.csv,results/ijmlc_control/logs/ijmlc_p2_external_20260701_1733_rss_ttc_s1.log
2,done,2026-07-01T17:34:52+08:00,2026-07-01T17:53:10+08:00,0,ijmlc_p2_external_20260701_1733_rss_ttc_s2,results/ijmlc_control/raw_csv/ijmlc_p2_external_20260701_1733_rss_ttc_s2_episodes.csv,results/ijmlc_control/summary_tables/ijmlc_p2_external_20260701_1733_rss_ttc_s2_summary.csv,results/ijmlc_control/logs/ijmlc_p2_external_20260701_1733_rss_ttc_s2.log
```
