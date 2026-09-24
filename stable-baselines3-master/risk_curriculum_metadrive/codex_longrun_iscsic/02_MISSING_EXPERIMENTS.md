# 02_MISSING_EXPERIMENTS

更新时间：2026-06-29 22:12:15 CST

## P0 缺口

1. 主对比三种子未完成：`baseline`, `risk`, `curriculum` 的 seed1/2 需要按 `timesteps=1000000`, `horizon=1200`, `n_envs=4`, densities `0.00/0.08/0.15`, episodes `50` 补齐。
2. 同协议 `proposed` seed0/1/2 可先从现有正式 proposed 结果复用，但必须在最终表里注明源路径和旧 run 的 `n_envs`/协议差异；若要求严格 n_envs=4，则需重跑。
3. 消融未完成：最低 `proposed_wo_ttc` seeds 0/1/2 与 `no_action_guard` seeds 0/1/2；再补 `proposed_wo_lane`, `proposed_wo_smooth`, `reward_only`, `guard_only`。
4. Defensive fixed ttc12/v18 仍需至少 3 个完整 seeds，并使用新评估 CSV 记录 `shield_*_rate`。
5. 英文 IEEE 初稿必须等 P0 结果固定后再写；当前 `paper/main_zh.tex` 不能直接翻译投稿。

## 推荐下一批顺序任务

1. `risk seed1` 训练加评估。
2. `risk seed2`。
3. `baseline seed1/2`。
4. `curriculum seed1/2`。
5. `proposed_wo_ttc` 与 `no_action_guard` 消融。
6. `defensive ttc12/v18` fixed 多种子。

## 当前主对比状态表

```csv
method,seed,config_count,usable_eval_count,best_eval
baseline,0,3,1,/home/aaa/data/qj/stable-baselines3-master/risk_curriculum_metadrive/outputs/paper_comparison_seed0/evaluations/baseline_ppo_s0.csv
baseline,1,0,0,
baseline,2,0,0,
risk,0,2,1,/home/aaa/data/qj/stable-baselines3-master/risk_curriculum_metadrive/outputs/paper_comparison_seed0/evaluations/risk_ppo_s0.csv
risk,1,0,0,
risk,2,0,0,
curriculum,0,2,1,/home/aaa/data/qj/stable-baselines3-master/risk_curriculum_metadrive/outputs/paper_comparison_seed0/evaluations/curriculum_ppo_s0.csv
curriculum,1,0,0,
curriculum,2,0,0,
proposed,0,11,5,/home/aaa/data/qj/stable-baselines3-master/risk_curriculum_metadrive/outputs/stage1000_final_candidate/evaluations/proposed_ppo_s0.csv;/home/aaa/data/qj/stable-baselines3-master/risk_curriculum_metadrive/outputs/final_paper_results/evaluations/proposed_ppo_s0.csv
proposed,1,2,3,/home/aaa/data/qj/stable-baselines3-master/risk_curriculum_metadrive/outputs/final_paper_results/evaluations/proposed_ppo_s1.csv;/home/aaa/data/qj/stable-baselines3-master/risk_curriculum_metadrive/outputs/stage1000_stable_proposed_multiseed/evaluations/proposed_ppo_s1.csv
proposed,2,2,1,/home/aaa/data/qj/stable-baselines3-master/risk_curriculum_metadrive/outputs/stage1000_true_proposed_multiseed/evaluations/proposed_ppo_s2.csv
```

## 当前 defensive 状态表

```csv
seed,config_count,eval_count,configs,evals
24,1,0,/home/aaa/data/qj/stable-baselines3-master/risk_curriculum_metadrive/outputs/defensive_proposed_ttc12v18_s24s25_nenv32/runs/defensive_proposed_ppo_s24/config.json,
25,1,1,/home/aaa/data/qj/stable-baselines3-master/risk_curriculum_metadrive/outputs/defensive_proposed_ttc12v18_s24s25_nenv32/runs/defensive_proposed_ppo_s25/config.json,/home/aaa/data/qj/stable-baselines3-master/risk_curriculum_metadrive/outputs/defensive_proposed_ttc12v18_s24s25_nenv32/evaluations/defensive_proposed_ppo_s25.csv
26,0,0,,
27,0,0,,
```

## 2026-06-29 协议变更：n_envs=10

用户要求全部改为 10 个环境训练/测试。此前 n_envs=4 的 risk seed1 已停止并移动到 interrupted 目录，不进入正式汇总。

后续 P0 主协议：

- train n_envs: 10
- eval n_envs: 10
- timesteps: 1000000
- horizon: 1200 for main/ablation; 1500 for fixed defensive
- eval episodes: 50
- densities: 0.00, 0.08, 0.15

正式输出目录：

- outputs/iscsic_main_nenv10
- outputs/iscsic_ablation_nenv10
- outputs/defensive_ttc12_v18_nenv10_final

## 2026-06-30 协议更新：n_envs=10 + 1.5M 候选

基于 risk seed2 的 1M/1.5M/2M 诊断：

- 1M: success = 0.76 / 0.64 / 0.40 at densities 0.00 / 0.08 / 0.15
- 1.5M: success = 0.90 / 0.80 / 0.44
- 2.0M: success = 0.90 / 0.72 / 0.34

结论：1M 对低/中密度偏短；2M 对高密度退化；正式 10 环境候选协议先采用 `timesteps=1500000`, `n_envs=10`, `eval_n_envs=10`, `ent_coef=0.01`, `horizon=1200`。

后续需要按该候选协议补齐：

1. proposed seeds 0/1/2；
2. risk seeds 0/1/2；
3. baseline seeds 0/1/2；
4. curriculum seeds 0/1/2；
5. P0 消融：proposed_wo_ttc、no_action_guard seeds 0/1/2；
6. 若 P0 表固定，再补更多消融和 defensive fixed 多 seed。

失败/诊断目录仍不得进入正式主表：`diagnostic_failed_*`, `tuning_extend_*`, `tuning_*`, `interrupted_*`, `smoke*`, `probe*`。
