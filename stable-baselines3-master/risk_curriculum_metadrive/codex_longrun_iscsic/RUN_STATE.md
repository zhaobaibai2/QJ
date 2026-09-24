# RUN_STATE

更新时间：2026-06-29 22:12:15 CST

## 当前状态

- 远程项目目录：`/home/aaa/data/qj/stable-baselines3-master/risk_curriculum_metadrive`。
- 检查时无训练/评估进程，RTX 4070 SUPER 可用。
- 第一阶段审计文件已创建/更新。
- 代码复现修复已同步到远程并通过静态验证。
- `outputs/final_iscsic_results` 已重建。

## 本轮使用的 skill

- `academic-research-skills-codex`: 用于证据分级、反 cherry-picking、ledger 分类。
- `Supervisor-Skills-main`: 用于审稿风险和实验缺口整理。
- `CCF-Figure-main`: 已读取图表 skill，当前仅生成程序化结果图，后续论文图再调用。

## 下一步

启动单个训练 job：

```bash
python scripts/train.py --variant risk --algo ppo --seed 1 --timesteps 1000000 --horizon 1200 --device cuda --output-dir outputs/iscsic_main_nenv4/runs --n-envs 4
```

训练结束后用 `scripts/evaluate_from_config.py` 做 50 episodes 三密度评估。

## 已完成

- 修复 `n_envs`、reward/guard split、shield rate logging、defensive Python 路径。
- 新增 `evaluate_from_config.py`。
- 重写 `build_final_outputs.py` 并成功生成最终汇总骨架。

## 失败/待复核

- 旧结果中 defensive CSV 缺 intervention rate，不能补写，只能通过新评估/新训练产生。

## 后台任务更新 

- 启动 P0 主对比：risk seed1, timesteps=1000000, horizon=1200, n_envs=4, device=cuda。

## 监督记录 2026-06-29T22:15:45+08:00

-  正在训练：最近检查约 102400 / 1000000 timesteps，fps 约 820，显存约 1GB，无 OOM/崩溃。
- 早期 success=0、route_completion 约 0.08-0.09，暂不调参；继续观察中后段学习曲线。

## 监督记录 2026-06-29T22:16:27+08:00

- risk seed1 正在训练：上次检查约 102400 / 1000000 timesteps，fps 约 820，显存约 1GB，无 OOM/崩溃。
- 早期 success=0、route_completion 约 0.08-0.09，暂不调参；继续观察中后段学习曲线。
- 注：上一条 RUN_STATE 记录因 shell 反引号转义问题丢失了 risk seed1 字样，训练本身未受影响。

## 监督记录 2026-06-29T22:17:49+08:00

- risk seed1 继续正常训练：最近日志约 176128 timesteps，fps 约 780-820，显存约 1GB。
- route_completion 已从早期 0.08 左右提升，最近最高约 0.20；success 仍为 0，暂不调参，继续观察到 250k checkpoint 和 500k 中段。
- 注：一次辅助日志解析命令因 shell 变量转义失败，后台训练未受影响。

## 协议变更 2026-06-29T22:20:52+08:00

- 用户要求全部改为 10 个环境训练/测试；已停止此前 n_envs=4 的 risk seed1 训练进程组 PGID=77772。
- 4 环境中断产物已移至 outputs/interrupted_nenv4_protocol_change_20260629_222052，标记为 interrupted，不进入正式汇总。
- 后续正式 P0 实验改用 outputs/iscsic_main_nenv10。

## 协议更新 2026-06-29T22:24:15+08:00

- 用户要求全部改为 10 个环境训练/测试；代码默认已更新：ExperimentConfig.n_envs=10，train.py 默认 --n-envs=10，run_one_defensive_proposed.py 默认 --n-envs=10。
- evaluate_from_config.py 已新增默认 --n-envs=10，并调用并行 VecEnv 评估；评估 CSV 会写 eval_n_envs。
- scripts/build_final_outputs.py 已加入 interrupted 排除，并已重建 final_iscsic_results。
- 后续正式目录改用 outputs/iscsic_main_nenv10、outputs/iscsic_ablation_nenv10、outputs/defensive_ttc12_v18_nenv10_final。

## 后台任务更新 2026-06-29T22:25:04+08:00

- 启动 P0 主对比：risk seed1, timesteps=1000000, horizon=1200, train_n_envs=10, eval_n_envs=10, device=cuda。

## 监督记录 2026-06-29T22:26:33+08:00

- risk seed1 n_envs=10 已启动并通过初始健康检查；10 个 worker 正常，config.json 记录 n_envs=10。
- 初始 fps 约 1300，显存约 1GB；等待 250k checkpoint 和中段曲线再判断是否需要调参。

## 监督记录 2026-06-29T22:27:16+08:00

- risk seed1 n_envs=10 正常训练：最近约 122880 / 1000000 timesteps，fps 约 1130-1180，显存约 1GB。
- 早期 success=0、route_completion 较低，暂不调参；继续观察到 250k checkpoint 后再判断。

## 监督记录 2026-06-29T22:29:58+08:00

- risk seed1 n_envs=10 已生成 checkpoint_250000_steps.zip；最近约 276480 timesteps，fps 约 1045，显存约 1GB。
- 学习开始上升但明显慢于此前中断的 n_envs=4 试跑：mean_speed_kmh 约 2.8-3.0，route_completion 约 0.21-0.26，success 仍为 0。
- 决策：不中断正式 n_envs=10 seed1，继续观察到 500k；若 500k 仍低速/低路线完成，按 scientific-brainstorming/实验调参路线分析 rollout/update 节奏并开 tuning 分支。

## 监督记录 2026-06-29T22:34:22+08:00

- risk seed1 n_envs=10 已生成 checkpoint_500000_steps.zip；约 512000 timesteps 时 fps 约 970。
- 中段学习曲线转好：mean_speed_kmh 约 15-17，route_completion 多次约 0.99，success_rate 约 0.27。
- 决策：不调参不中断，继续跑完 1M 并进入 10 环境正式评估。

## 监督记录 2026-06-29T22:39:46+08:00

- risk seed1 n_envs=10 已生成 checkpoint_750000_steps.zip；约 788480 timesteps 时 fps 约 922。
- 后段训练表现可用：success_rate 约 0.57-0.62，mean_speed_kmh 约 19.5，route_completion 多数接近 0.98-0.99。
- 决策：继续跑完 1M，不中断；训练结束后自动执行 10 环境三密度评估。

## 后台任务完成 2026-06-29T22:46:21+08:00

- risk seed1 n_envs=10 训练、10 环境三密度 50 episode 评估和 final_iscsic_results 重建完成。
- 下一步：risk seed2 n_envs=10。

## 完成记录 2026-06-29T22:48:04+08:00

- risk seed1 n_envs=10 已完成：final_model.zip、10 环境三密度 50 episode 评估、final_iscsic_results 重建。
- 评估结果：density 0.00 success=0.86 collision=0.00 cost=0.00；0.08 success=0.80 collision=0.04 cost=0.04；0.15 success=0.50 collision=0.34 cost=0.38。
- CSV: outputs/iscsic_main_nenv10/evaluations/risk_ppo_s1.csv；eval_n_envs=10。
- 下一步启动 risk seed2 n_envs=10。

## 后台任务更新 2026-06-29T22:48:35+08:00

- 启动 P0 主对比：risk seed2, timesteps=1000000, horizon=1200, train_n_envs=10, eval_n_envs=10, device=cuda。

## 监督记录 2026-06-29T22:49:27+08:00

- risk seed2 n_envs=10 初始健康检查正常：约 40960 / 1000000 timesteps，fps 约 1300，显存约 1GB，10 个 worker 正常。
- 早期 success=0，route_completion 低，符合 PPO 初期状态；继续观察到 250k checkpoint。

## 失败诊断 2026-06-29T22:56:07+08:00

- risk seed2 n_envs=10 v1 在 500k 判据失败：mean_speed_kmh 约 0.075-0.18，route_completion 约 0.01，success=0，std 下降到约 0.565。
- 判定为 idle policy collapse；非显存/进程故障，action guard 也基本未触发。
- 已停止并归档到 outputs/diagnostic_failed_idle_collapse_risk_s2_nenv10_20260629_225607，不进入正式主表。
- 下一步按 scientific-brainstorming 失败归因策略做最小调参：增加 PPO ent_coef，启动 n_envs=10 entropy-v2 诊断重跑。

## 调参任务启动 2026-06-29T22:57:18+08:00

- 启动 risk seed2 nenv10 entropy-v2 诊断重跑：ent_coef=0.01，其他 reward/guard/horizon/timesteps 不变。
- 目的：修复 v1 的 idle policy collapse；该目录先标为 diagnostic/tuning，不与 risk seed1 v1 混合做正式均值。

## 调参监督 2026-06-29T23:01:30+08:00

- risk seed2 nenv10 entropy-v2 到 250k checkpoint：mean_speed_kmh 约 1.7-2.1，route_completion 约 0.13，success=0，std 约 0.99。
- 与失败 v1 相比，v2 已避免 std/idle collapse；但尚未快速起飞。决策：继续观察到 500k，再决定是否采用或继续调参。

## 调参监督 2026-06-29T23:06:17+08:00

- risk seed2 nenv10 entropy-v2 到 500k checkpoint：mean_speed_kmh 约 15-16，route_completion 多次接近 0.99，success_rate 约 0.10-0.15，std 约 0.69。
- 判定：v2 已修复 v1 的 idle collapse，继续跑完并评估。若最终结果合格，需把 ent_coef=0.01 作为 risk 协议并重跑 seed1 保持主表一致。

## 调参监督 2026-06-29T23:11:21+08:00

- risk seed2 nenv10 entropy-v2 到 750k 后仍健康：success_rate 约 0.45-0.50，mean_speed_kmh 约 16-18，route_completion 多数接近 0.99。
- 决策：继续跑完 1M 并执行正式 10 环境评估。

## 调参任务完成 2026-06-29T23:18:28+08:00

- risk seed2 nenv10 entropy-v2 训练和评估完成。需要根据结果决定是否采用 v2 并重跑 seed1/后续主对比。

## 收敛性分析 2026-06-29T23:22:24+08:00

- risk seed2 entropy-v2 1M 评估：0.00 success=0.76，0.08 success=0.64，0.15 success=0.40；低于 risk seed1 1M 的 0.86/0.80/0.50。
- 训练曲线显示 500k 后才起飞，900k-1M success_rate 仍在 0.60-0.67 波动，不是充分收敛。
- 已把 entropy_v2/diagnostic_failed/tuning_extend 目录从 final_iscsic_results 自动汇总中排除，避免调参结果与正式协议混表。
- 下一步执行 seed2 从 1M checkpoint 继续训练到 1.5M 的延长诊断；若评估明显提升，再考虑把主协议加长并重跑对应 seeds。

## 延长训练诊断启动 2026-06-29T23:22:55+08:00

- 从 risk seed2 entropy-v2 的 1M final_model 继续训练额外 500k，等效总训练步数约 1.5M。
- 参数保持 n_envs=10, ent_coef=0.01, horizon=1200, reward/guard 不变；该目录先排除 final 汇总。

## 延长训练诊断完成 2026-06-29T23:35:35+08:00

- risk seed2 1M->1.5M 延长训练和评估完成。需要比较 1M vs 1.5M 决定是否加大正式训练步数。

## 收敛性诊断 2026-06-29T23:38:30+08:00

- risk seed2 entropy-v2 从 1M 延长到约 1.5M 后，10 环境评估结果为：density 0.00 success=0.90 collision=0.00 cost=0.00；0.08 success=0.80 collision=0.10 cost=0.10；0.15 success=0.44 collision=0.50 cost=0.50。
- 相比 1M：0.00 success +0.14，0.08 +0.16，0.15 仅 +0.04；高密度 route/reward 未改善。
- 判断：1M 对低/中密度确实偏短，但高密度低成功率不能只归因为未收敛，主要瓶颈仍是碰撞/防御策略。
- 下一步：同参数继续 1.5M->2.0M 做最后一次加步数诊断；若高密度仍无明显提升，停止单纯加步数，转为防御/奖励参数调优。

## 延长训练诊断启动 2026-06-29T23:39:00+08:00

- 已启动 risk seed2 1.5M->2.0M 延长诊断，参数保持 n_envs=10, ent_coef=0.01, horizon=1200, reward/guard 不变。
- 输出目录：outputs/tuning_extend_risk_s2_nenv10_ent001_1p5m_to_2m；该目录继续排除正式汇总。

## 收敛性诊断完成 2026-06-29T23:52:30+08:00

- risk seed2 entropy-v2 2.0M 评估：density 0.00 success=0.90 collision=0.00 cost=0.00；0.08 success=0.72 collision=0.04 cost=0.04；0.15 success=0.34 collision=0.56 out_of_road=0.04 cost=0.60。
- 三点比较：1M success=0.76/0.64/0.40；1.5M=0.90/0.80/0.44；2.0M=0.90/0.72/0.34。
- 判断：1M 对低/中密度不充分，但 1.5M 后继续到 2.0M 没有改善高密度，反而退化；停止单纯加步数路线。
- 下一步：启动 balanced-safety 调参诊断，从 1.5M 最优 checkpoint 继续 500k，测试是否能压高密度 collision。

## 防御调参诊断启动 2026-06-29T23:53:00+08:00

- 已启动 balanced-safety risk seed2，从 1.5M checkpoint 继续 500k。
- 参数：n_envs=10, ent_coef=0.01, target_speed_kmh=16, ttc_threshold=8, ttc=6, cost=45, crash/out_of_road penalty=120, curriculum hard density=0.15。
- 输出目录：outputs/tuning_balanced_safety_risk_s2_nenv10_from1p5m；该目录继续排除正式汇总。

## 防御调参诊断中止 2026-06-30T00:00:20+08:00

- balanced-safety 诊断在约 1.78M 等效步数中止：mean_speed_kmh 约 15，success_rate 从约 0.55 继续跌到约 0.30。
- 失败原因：target_speed=16/ttc_threshold=8/cost=45 的组合过保守，降低碰撞风险的同时严重损害完成率；不再跑完，不进入正式表。
- 已归档为 diagnostic_failed_overconservative_balanced_safety_risk_s2_nenv10_*。
- 下一步：改用 mild-safety 调参，保留较高完成速度，只温和提高 TTC/碰撞代价。

## 防御调参诊断启动 2026-06-30T00:02:30+08:00

- 已启动 mild-safety risk seed2，从 1.5M checkpoint 继续 500k。
- 参数：n_envs=10, ent_coef=0.01, target_speed_kmh=18, ttc_threshold=6, ttc=4, cost=30, crash/out_of_road penalty=100, curriculum hard density=0.15。
- 判据：若 density 0.15 collision 明显下降且 success 不低于 1.5M 的 0.44，才考虑采用；否则继续保留 1.5M 作为步数诊断结果。

## 防御调参诊断中止 2026-06-30T00:09:00+08:00

- mild-safety 诊断在约 1.78M 等效步数中止：mean_speed_kmh 约 15-17，success_rate 从约 0.53 下降到约 0.42-0.45，reward 明显下降且仍有 collision 样本。
- 失败原因：温和提高 TTC/代价/碰撞惩罚仍会破坏完成率，未证明可降低高密度 collision 并保持 success。
- 已归档为 diagnostic_failed_mild_safety_risk_s2_nenv10_*。
- 当前结论：1M 低/中密度确实未完全收敛，1.5M 是更合理的训练长度；但高密度 0.15 的低成功率不是单纯步数问题，主要是碰撞/策略鲁棒性瓶颈。

## 正式候选协议更新 2026-06-30T00:14:00+08:00

- 根据 risk seed2 1M/1.5M/2M 诊断，正式 n_envs=10 候选协议从 1M 调整为 timesteps=1500000, ent_coef=0.01, horizon=1200。
- 理由：1.5M 改善低/中密度；2M 高密度退化；balanced-safety 和 mild-safety 均破坏完成率。
- 下一步：优先启动论文核心方法 proposed seed0 的 n_envs=10 候选协议训练与 10 环境三密度评估。

## 后台任务启动 2026-06-30T00:15:30+08:00

- 启动正式候选主方法：proposed seed0, timesteps=1500000, horizon=1200, train_n_envs=10, eval_n_envs=10, ent_coef=0.01, device=cuda。
- 输出目录：outputs/iscsic_main_nenv10_1p5m_ent001。
- 训练结束后自动执行 evaluate_from_config.py 三密度 50 episode 评估，并重建 final_iscsic_results。

## 监督记录 2026-06-30T00:17:00+08:00

- proposed seed0 n_envs=10 早期健康检查通过：10 个 worker 正常，显存约 1GB，fps 约 2800，已到约 205k timesteps。
- 当前仍在 curriculum stage 0，mean_speed_kmh 约 2-3，success_rate=0；符合早期探索，但需要观察到 375k/750k checkpoint 是否起飞。

## 监督记录 2026-06-30T00:19:10+08:00

- proposed seed0 n_envs=10 已生成 checkpoint_375000_steps.zip。
- 健康信号：curriculum 已从 stage 0 升到 stage 2；mean_speed_kmh 约 15-16；route_completion 多次约 0.98；success_rate 约 0.23。
- 决策：未出现 idle collapse，继续跑到 750k checkpoint，不调参不中断。

## 监督记录 2026-06-30T00:22:40+08:00

- proposed seed0 n_envs=10 检查到约 553k timesteps；尚未到 750k checkpoint。
- 进入 curriculum stage 2 后 success_rate 暂时回落到约 0.07，但 mean_speed_kmh 约 15-17，route_completion 已出现 0.96-0.99，episode_cost 近期较低。
- 判定：不是 idle collapse，属于课程难度提升后的中段回落；继续观察到 750k checkpoint。若 750k 仍低于 0.15，再考虑中止/重调。

## 监督记录 2026-06-30T00:27:45+08:00

- proposed seed0 n_envs=10 已生成 checkpoint_750000_steps.zip；约 798720 timesteps。
- 中段恢复：success_rate 约 0.32，window_success 约 0.37-0.43，mean_speed_kmh 约 19，route_completion 多次约 0.99，近期 episode_cost 多为 0。
- 决策：训练健康但未充分收敛，继续跑到 1.125M checkpoint。

## 监督记录 2026-06-30T00:31:40+08:00

- proposed seed0 n_envs=10 检查到约 983k timesteps；尚未到 1.125M checkpoint。
- 当前 success_rate 约 0.23-0.30，低于预期；但 mean_speed_kmh 约 18-20，route_completion 多数 0.90+，近期 cost 较低。
- 判断：不是不会行驶，而是完成判定/高难路线稳定性不足；继续到 1.125M，并最终以三密度评估决定是否采用或重跑。

## 监督记录 2026-06-30T00:33:55+08:00

- proposed seed0 n_envs=10 到约 1.096M timesteps；尚未写出 1.125M checkpoint。
- 后段有恢复：window_success 最高约 0.467，success_rate 约 0.37；mean_speed_kmh 约 18-19，route_completion 多次约 0.99。
- 风险：window_cost 约 0.20，说明高密度/难路线仍可能有碰撞或出界；最终需要以 density=0.15 评估确认。
- 决策：继续跑完 1.5M，不中止。

## 失败诊断 2026-06-30T00:40:40+08:00

- proposed seed0 1.5M n_envs=10 在约 1.23M-1.27M 进入 curriculum stage 3 后崩溃：window_success=0，window_cost 约 0.73-0.77，window_route_completion 约 0.39-0.42。
- 原因判断：默认 hard stage traffic_density=0.22，明显高于正式 stress eval density=0.15；课程难度跳变导致后段策略退化。
- 已中止并归档到 outputs/diagnostic_failed_stage3_overhard_proposed_s0_nenv10_20260630_003222，不进入正式主表。
- 下一步：按 scientific-brainstorming 失败归因策略做最小代码调参：把课程 medium/hard density 对齐为 0.08/0.15，保持 reward/guard 不变，重跑 proposed seed0。

## 代码调参 2026-06-30T00:43:30+08:00

- 已备份 racrl/config.py 到 racrl/config.py.bak_20260630_curriculum_density_align。
- 已把 DEFAULT_STAGES 对齐正式评估密度：medium 0.10->0.08，hard 0.22->0.15；reward/guard/PPO 其他参数不变。
- py_compile 通过。下一步重跑 proposed seed0 n_envs=10, 1.5M, ent_coef=0.01。

## 后台任务启动 2026-06-30T00:44:30+08:00

- 重跑 proposed seed0：density-aligned curriculum, timesteps=1500000, horizon=1200, train_n_envs=10, eval_n_envs=10, ent_coef=0.01。
- 输出目录：outputs/iscsic_main_nenv10_1p5m_ent001。
- 监督重点：进入 stage 3 后 window_success/cost 是否稳定，不再复现 hard density=0.22 崩溃。

## 监督记录 2026-06-30T00:35:00+08:00

- density-aligned proposed seed0 早期健康检查通过：config.json 记录 n_envs=10, ent_coef=0.01, stages=0.00/0.03/0.08/0.15。
- 约 225k timesteps 已升到 stage 1，出现 success=1 样本；fps 约 2760-2780，10 个 worker 正常。
- 决策：继续到 375k checkpoint，重点观察后续 stage 3 是否不再崩溃。

## 监督记录 2026-06-30T00:38:30+08:00

- density-aligned proposed seed0 到约 358k timesteps，已进入 stage 2；success_rate 约 0.18，mean_speed_kmh 约 13-17。
- 当前比上一轮同阶段略弱，但没有 idle collapse；window_cost 仍低，尚未进入关键 stage 3。
- 决策：继续跑到 750k，观察 success_rate 是否恢复到 0.30+。

## 监督记录 2026-06-30T00:42:30+08:00

- density-aligned proposed seed0 检查到约 584k timesteps，尚未到 750k checkpoint。
- 训练在恢复：window_success 从约 0.23 升到 0.367，window_route_completion 到约 0.856，mean_speed_kmh 约 18，success_rate 约 0.24。
- 决策：继续到 750k；当前没有复现上轮 stage 3 崩溃。

## 监督记录 2026-06-30T00:47:00+08:00

- density-aligned proposed seed0 到约 727k timesteps，已进入 stage 3。
- 关键验证：stage 3 未复现上一轮崩溃；window_success=0.5，window_cost=0.033，window_route_completion=0.902，mean_speed_kmh 约 19。
- 判断：默认 hard density=0.22 是上一轮后段崩溃的主要原因；density-aligned 课程有效。
- 决策：继续跑到 1.125M 和 1.5M 最终评估。

## 监督记录 2026-06-30T00:52:10+08:00

- density-aligned proposed seed0 到约 870k timesteps，stage 3 后未复现 cost 爆炸：window_cost 从 0.267 降到约 0.133。
- 但 window_success 暂时为 0，route_completion 多在 0.56-0.66，mean_speed_kmh 约 14-16；问题从“碰撞崩溃”转为“hard stage 完成率不足”。
- 决策：继续观察到 1.1M；若仍无成功恢复，下一轮应考虑进度/目标速度或课程门槛，而不是增加安全惩罚。

## 失败诊断 2026-06-30T01:00:30+08:00

- density-aligned proposed seed0 在约 0.83M-0.97M 的 stage 3 连续 window_success=0；window_cost 较低但 route_completion 多为 0.5-0.65，mean_speed_kmh 波动约 10-18。
- 判断：课程密度对齐修复了 cost/collision 爆炸，但 hard stage 完成率仍不足；继续跑满 1.5M 预期收益低。
- 已中止并归档到 outputs/diagnostic_failed_stage3_completion_proposed_s0_nenv10_20260630_005130，不进入正式主表。
- 下一步检查训练 hard stage 是否还含 accident_prob=0.02 等与正式评估不一致因素，再做最小课程修正。

## 失败诊断 2026-06-30T01:04:30+08:00

- 代码检查确认训练 hard stage 仍为 accident_prob=0.02 且 horizon=1000，而正式评估 build_env 使用 accident_prob=0.0 且 horizon=1200。
- 这导致 hard stage 训练比目标评估协议更短、更难，符合当前现象：低 collision/cost 但 route/success 长期不足。
- 已停止并归档当前 density-aligned run 到 already_archived，不进入正式主表。
- 下一步最小修正：hard stage 对齐为 density=0.15, accident_prob=0.0, horizon=1200；保持 reward/guard/PPO 不变。

## 代码调参 2026-06-30T01:05:30+08:00

- 已备份 racrl/config.py 到 racrl/config.py.bak_20260630_hard_stage_eval_align。
- 已把 hard stage 对齐正式评估协议：density=0.15, accident_prob=0.0, horizon=1200。
- py_compile 通过。下一步重跑 proposed seed0 n_envs=10, 1.5M, ent_coef=0.01。

## 后台任务启动 2026-06-30T01:06:30+08:00

- 重跑 proposed seed0：eval-aligned hard stage, timesteps=1500000, horizon=1200, train_n_envs=10, eval_n_envs=10, ent_coef=0.01。
- 输出目录：outputs/iscsic_main_nenv10_1p5m_ent001。
- hard stage 当前为 density=0.15, accident_prob=0.0, horizon=1200；监督重点是 stage 3 route/success 是否恢复。

## 监督记录 2026-06-30T01:08:10+08:00

- eval-aligned proposed seed0 早期健康检查通过：config.json 记录 hard stage=(density 0.15, accident_prob 0.0, horizon 1200)。
- 约 225k timesteps 到 stage 1，success_rate 约 0.07；10 worker/fps 正常。
- 决策：继续到 375k 和 750k，重点检查 stage 3 完成率是否恢复。

## 监督记录 2026-06-30T01:11:30+08:00

- eval-aligned proposed seed0 已生成 checkpoint_375000_steps.zip；约 389k timesteps 已进入 stage 2。
- window_success 约 0.30，mean_speed_kmh 最高约 17.4，route_completion 有 0.72+；早期没有 idle/cost 崩溃。
- 决策：继续跑到 750k，观察 stage 3 是否维持成功率。

## 监督记录 2026-06-30T01:15:00+08:00

- eval-aligned proposed seed0 检查到约 584k timesteps，尚未进入 stage 3。
- 中段健康：window_success 约 0.30-0.37，window_route_completion 约 0.85-0.89，mean_speed_kmh 约 19。
- 决策：继续到 750k，等待进入 hard stage 后再判断。

## 监督记录 2026-06-30T01:18:40+08:00

- eval-aligned proposed seed0 到约 717k timesteps，仍在 stage 2，尚未进入 hard stage。
- window_success 在 0.13-0.40 波动，route_completion 约 0.85-0.90，mean_speed_kmh 约 18-19，window_cost 低。
- 决策：继续等待进入 stage 3；暂不中止。

## 监督记录 2026-06-30T01:22:20+08:00

- eval-aligned proposed seed0 到约 819k timesteps，仍在 stage 2；checkpoint_750000 已生成。
- window_success 从 0.33 降到 0.067，route_completion 仍约 0.83-0.86，mean_speed_kmh 约 17-19，cost 较低。
- 风险：stage2_success=0.50 可能导致 hard stage 暴露不足；如果到 1.0M 仍未进入 stage 3，将中止并调低 stage2 晋级门槛。

## 失败诊断 2026-06-30T01:27:30+08:00

- eval-aligned proposed seed0 跑到约 993k 仍停留在 stage 2；window_success 多为 0.17-0.27，未稳定达到 stage2_success=0.50。
- 问题判断：当前主瓶颈不是环境不一致，而是课程晋级门槛过严，导致 hard density=0.15 暴露不足。
- 已停止并归档到 outputs/diagnostic_failed_stage2_gate_too_strict_proposed_s0_nenv10_20260630_010730，不进入正式主表。
- 下一步最小课程调参：stage2_success 从 0.50 降到 0.25，并启用 allow_demote，避免 hard stage 失败后永久卡死。

## 代码调参 2026-06-30T01:28:30+08:00

- 已备份 racrl/config.py 到 racrl/config.py.bak_20260630_curriculum_gate_relax。
- 已把 stage2_success 0.50->0.25，demote_grace_episodes 60->40，allow_demote False->True。
- py_compile 通过。下一步重跑 proposed seed0 n_envs=10, 1.5M, ent_coef=0.01。

## 后台任务启动 2026-06-30T01:29:30+08:00

- 重跑 proposed seed0：gate-relaxed curriculum, timesteps=1500000, horizon=1200, train_n_envs=10, eval_n_envs=10, ent_coef=0.01。
- 当前协议：stages=0.00/0.03/0.08/0.15，hard accident=0.0，hard horizon=1200，stage2_success=0.25，allow_demote=True。
- 输出目录：outputs/iscsic_main_nenv10_1p5m_ent001。

## 监督记录 2026-06-30T01:31:00+08:00

- gate-relaxed proposed seed0 早期配置确认：n_envs=10, ent_coef=0.01, stage2_success=0.25, allow_demote=True, hard=(0.15, accident 0, horizon 1200)。
- 约 205k timesteps 仍在 stage 0，mean_speed_kmh 约 3-5，暂未成功；fps/worker 正常。
- 决策：继续到 375k。

## 监督记录 2026-06-30T01:35:00+08:00

- gate-relaxed proposed seed0 最新检查到约 440k timesteps，已进入 stage 2。
- 当前 window_success 约 0.13-0.30，mean_speed_kmh 约 13-15，window_route_completion 约 0.71-0.79，未见 idle collapse 或 cost 爆炸。
- 决策：继续到 750k；只有进入 hard stage 后才能判断 gate relaxation 是否有效。

## 监督记录 2026-06-30T01:39:20+08:00

- gate-relaxed proposed seed0 到约 645k timesteps，已进入 stage 3。
- 关键健康信号：stage 3 出现 success=1；window_success 约 0.267，window_cost 约 0.133，route_completion 出现 0.989，未出现 hard-stage 崩溃。
- 判断：stage2_success=0.25 + allow_demote 的课程门槛修正有效，解决了 hard stage 暴露不足问题。
- 决策：继续跑到 750k/1.1M，不中止。

## 监督记录 2026-06-30T01:43:00+08:00

- gate-relaxed proposed seed0 到约 727k timesteps 后处于 stage 3；连续窗口 window_success=0，window_cost 约 0.17-0.30，route_completion 多为 0.55-0.65。
- 与之前相比，已经解决 hard stage 暴露不足，但 hard stage 初期仍不稳定。
- 下一步先检查 callbacks.py 的 demotion 逻辑是否会真正把失败 hard stage 退回恢复；如果不会，需要修复 demotion 或调整 hard stage 进入/退出策略。

## 监督记录 2026-06-30T01:47:00+08:00

- gate-relaxed proposed seed0 到约 829k timesteps，仍在 hard stage。
- hard stage 目前 window_success=0，但 window_cost 约 0.10-0.13，route_completion 约 0.63-0.71，mean_speed_kmh 约 13-16。
- 判断：安全/cost 不再是主要瓶颈，问题更像完成距离/目标速度不足。
- 决策：继续到约 1.0M；若仍无 hard-stage 成功恢复，将停止并转向目标速度/进度奖励调参。

## 失败诊断 2026-06-30T01:52:00+08:00

- gate-relaxed proposed seed0 在 hard stage 约 0.88M-0.92M 后恶化：window_success 仍为 0，window_cost 升到约 0.56，route_completion 降到约 0.50，出现 out_of_road/collision。
- 判断：放松 stage2_success 解决了 hard-stage 暴露不足，但从 density 0.08 直接跳到 0.15 仍过陡，且 demotion 条件太苛刻，失败后无法恢复。
- 已停止并归档到 outputs/diagnostic_failed_hard_stage_collapse_gate_relax_proposed_s0_nenv10_20260630_012516，不进入正式主表。
- 下一步使用 scientific-brainstorming 失败归因：增加 pre-hard 0.12 阶段，并放宽 demotion 条件。

## 代码调参 2026-06-30T01:55:00+08:00

- 使用 remote scientific-brainstorming skill 做失败归因：hard stage 暴露已解决，但 0.08->0.15 跳变仍过陡，且 demotion 逻辑太苛刻。
- 已增加 prehard stage：density=0.12, map_blocks=6, accident_prob=0.0, horizon=1100。
- 已放宽 demotion：success 低且 route 低或 cost 高即可退级；demote_route_completion=0.65, demote_cost=0.45。
- py_compile 通过。下一步重跑 proposed seed0 n_envs=10, 1.5M, ent_coef=0.01。

## 后台任务启动 2026-06-30T01:56:30+08:00

- 重跑 proposed seed0：prehard curriculum + relaxed demotion, timesteps=1500000, horizon=1200, train_n_envs=10, eval_n_envs=10, ent_coef=0.01。
- 当前协议：stages=0.00/0.03/0.08/0.12/0.15，stage2_success=0.25，allow_demote=True，demotion route<0.65 或 cost>0.45。
- 输出目录：outputs/iscsic_main_nenv10_1p5m_ent001。

## 监督记录 2026-06-30T01:58:20+08:00

- prehard proposed seed0 早期配置确认：n_envs=10, ent_coef=0.01, stages=0.00/0.03/0.08/0.12/0.15，demotion route<0.65 或 cost>0.45。
- 约 205k timesteps 仍在 stage 0；window_cost 约 0.4，route_completion 约 0.33，mean_speed_kmh 约 2，早期表现偏弱。
- 决策：继续观察到 375k；若仍未恢复或晋级，将考虑回滚/缩小 demotion 调整。

## 监督记录 2026-06-30T02:01:30+08:00

- prehard proposed seed0 到约 410k timesteps，checkpoint_375000 已生成。
- 已观察到 demotion 生效：stage 2 因窗口不稳退回 stage 1；overall success_rate 仍约 0.29-0.38，mean_speed_kmh 约 14-15。
- 判断：demotion 修复了“失败后卡死”问题，但可能偏激进；当前不是失败，继续观察是否能重新晋级并稳定。
- 决策：继续到 750k，再决定是否调整 demote_route_completion。

## 2026-06-30 convergence analysis checkpoint
- User question: whether low 1M success is simply non-convergence and whether to increase training steps.
- Evidence from completed 10-env evals:
  - seed1 1M ent=0: d0.00 success 0.86, d0.08 0.80, d0.15 0.50.
  - seed2 1M ent=0.01: d0.00 success 0.76, d0.08 0.64, d0.15 0.40.
  - seed2 1.5M ent=0.01: d0.00 success 0.90, d0.08 0.80, d0.15 0.44.
  - seed2 2.0M ent=0.01: d0.00 success 0.90, d0.08 0.72, d0.15 0.34.
- Interpretation: 1M is undertrained for low/medium density, but high-density d0.15 is not solved by more steps alone; 2M degraded, indicating curriculum/late-stage instability.
- Current proposed prehard run at ~727k: stage3, window_success 0.133, window_cost 0.30, window_route_completion 0.654, latest success example exists with route_completion 0.99. Continue monitoring before parameter change.

## 2026-06-30 prehard run recovery checkpoint
- At ~808k the run demoted from prehard(stage3) to medium(stage2), but recovered instead of collapsing.
- By ~880k it returned to stage3 with window_success 0.267, window_cost 0.0333, route 0.88.
- By ~911k it promoted to hard(stage4) with window_success 0.333, window_cost 0.0333, route 0.899, and hard-stage successful episodes appeared around 911k-922k.
- Decision: do not stop/restart; continue to 1.5M and evaluate. Current evidence supports 1.5M as more appropriate than 1M, but not blind extension beyond 1.5M until eval confirms.

## 2026-06-30 proposed seed0 1.5M prehard final eval
- Root: outputs/iscsic_main_nenv10_1p5m_ent001
- Model: outputs/iscsic_main_nenv10_1p5m_ent001/runs/proposed_ppo_s0/model/final_model.zip
- Eval CSV: outputs/iscsic_main_nenv10_1p5m_ent001/evaluations/proposed_ppo_s0.csv
- 10-env eval summary:
  - d0.00 success 0.82, collision 0.00, out_of_road 0.00, cost 0.00, route 0.9776.
  - d0.08 success 0.76, collision 0.06, out_of_road 0.06, cost 0.12, route 0.9294.
  - d0.15 success 0.60, collision 0.32, out_of_road 0.02, cost 0.34, route 0.8557.
- Interpretation for user question: 1M was undertrained for easy/medium, but high-density weakness is not fixed by blindly increasing steps. The prehard 1.5M curriculum improved d0.15 to 0.60, while previous seed2 2M degraded to 0.34, so next action is multi-seed 1.5M prehard rather than 2M blind extension.

## 2026-06-30 nenv10 seed1 launch ledger update
- Protocol override from user: all current formal retraining/evaluation should use 10 environments, not the pasted-text default 4 environments.
- Seed0 proposed 1.5M prehard completed and evaluated at 10 envs; d0.15 success 0.60, cost 0.34.
- Seed1 proposed 1.5M prehard launched under the same 10-env protocol; PID 95509, train PID 95516.
- Ledger and command history updated for seed0 and seed1.

## 2026-06-30 seed1 early health checkpoint
- Run: outputs/iscsic_main_nenv10_1p5m_ent001/runs/proposed_ppo_s1
- At ~420k timesteps seed1 reached stage2 with window_success 0.40, route 0.75, cost 0.167.
- At ~450k timesteps seed1 reached prehard stage3 with window_success 0.333, route 0.792, cost 0.10.
- Decision: healthy early progression; no parameter change. Continue toward hard-stage stability and final 1.5M evaluation.

## 2026-06-30 seed1 hard-stage checkpoint
- Seed1 reached hard stage4 by ~635k timesteps: window_success 0.30, window_cost 0.20, window_route_completion 0.791.
- Recent hard episodes have cost=0 but not always success; no immediate collision/out-of-road explosion after promotion.
- Decision: keep running to 1.0M/1.5M; do not adjust parameters mid-run.

## 2026-06-30 seed1 1M stability checkpoint
- Seed1 reached hard stage4 and produced successful episodes around ~860k-870k.
- Hard stage later degraded: around ~890k-901k window_success fell to 0.033-0.067 and cost rose to 0.367-0.467, causing demotion to stage3 by ~911k.
- Around ~932k stage3 recovered a successful episode with route 0.989.
- Interpretation: not simply lack of learning; policy can succeed but hard-stage stability drifts. Final eval should be complemented by checkpoint diagnostics if final checkpoint is poor.

## 2026-06-30 seed1 final and checkpoint diagnostics
- Seed1 final eval CSV: outputs/iscsic_main_nenv10_1p5m_ent001/evaluations/proposed_ppo_s1.csv
  - d0.00 success 0.88, cost 0.00, route 0.9842.
  - d0.08 success 0.76, collision 0.10, cost 0.10, route 0.9169.
  - d0.15 success 0.32, collision 0.60, cost 0.62, route 0.7029.
- Seed1 checkpoint_750k diagnostic eval:
  - d0.00 success 0.84; d0.08 success 0.78; d0.15 success 0.38, cost 0.48.
- Seed1 checkpoint_1125k diagnostic eval:
  - d0.00 success 0.88; d0.08 success 0.58; d0.15 success 0.42, cost 0.46.
- Current two-seed final proposed prehard mean:
  - d0.00 success 0.85, cost 0.00.
  - d0.08 success 0.76, cost 0.11.
  - d0.15 success 0.46, cost 0.48.
- Interpretation: 1.5M prehard helps seed0 but is not robust across seeds. More steps alone do not solve this; checkpoint behavior shows density-specific policy drift and hard-stage instability.
- Next action candidate: before expanding many seeds, test a small stabilizing curriculum variant, e.g. require more sustained prehard performance before stage4 or evaluate/save best checkpoint by validation density. Keep all results labeled diagnostic unless protocol is fixed before multi-seed.

## 2026-06-30 route-gate diagnostic launch
- Code change: added `stage2_route_completion=0.85` and required stage>=2 promotion to satisfy success, route completion, and cost.
- Rationale: seed1 final showed hard-stage instability and final d0.15 success 0.32; checkpoint diagnostics showed policy drift rather than simple undertraining.
- Diagnostic run launched: proposed seed1, 1.5M, n_envs=10, ent_coef=0.01, root `outputs/tuning_routegate_prehard_nenv10_1p5m`.
- This is diagnostic, not final benchmark, until compared against the previous same-seed protocol.

## 2026-06-30 route-gate early health checkpoint
- Diagnostic route-gate seed1 run is active: PID 97338 / train PID 97346.
- Config verified: n_envs=10, timesteps=1.5M, ent_coef=0.01, stage2_route_completion=0.85.
- Around ~369k timesteps it reached stage2 with window_success 0.433, window_cost 0.10, window_route_completion 0.77.
- Interpretation: new route gate did not stall early training; it is delaying prehard promotion until route completion is more stable, as intended.
- Continue monitoring to 600k-750k for stage3 entry and later hard-stage stability.

## 2026-06-30 route-gate 0.85 stopped
- Stopped diagnostic route-gate 0.85 at ~768k because it remained in stage2 and narrowly missed the route threshold repeatedly (route window up to ~0.843).
- Decision: 0.85 is too strict. Next diagnostic will use stage2_route_completion=0.80, preserving all other settings.

## 2026-06-30 route-gate 0.80 diagnostic launch
- Lowered stage2_route_completion from 0.85 to 0.80 after 0.85 stayed in stage2 through ~768k.
- New diagnostic launched: proposed seed1, 1.5M, n_envs=10, ent_coef=0.01, root `outputs/tuning_routegate080_prehard_nenv10_1p5m`.
- Only changed this one gate threshold; reward, guard, stages, demotion and entropy are unchanged.

## 2026-06-30 route-gate 0.80 mid checkpoint
- Diagnostic route-gate 0.80 seed1 reached stage3 by ~461k timesteps.
- Promotion window: success 0.267, route 0.807, cost 0.0667.
- This is more suitable than 0.85, which stayed in stage2 through ~768k. Continue to hard-stage stability check.

## 2026-06-30 route-gate 0.80 failed and reverted
- Route-gate 0.80 reached stage3 at ~461k but later collapsed to stage0 by ~727k-809k: success 0, route window ~0.06, low-speed/out-of-road behavior.
- Stopped run and restored pre-route-gate curriculum code from backups.
- Conclusion: hard-stage instability is not solved by adding a route completion gate alone. Next diagnostics should target policy drift/checkpoint selection or smoother optimization, not stricter promotion gates.

## 2026-06-30 low-learning-rate diagnostic launch
- Added `ExperimentConfig.learning_rate` and `scripts/train.py --learning-rate`; py_compile passed.
- Restored original prehard curriculum after route-gate failures.
- Launched diagnostic: proposed seed1, n_envs=10, 1.5M, ent_coef=0.01, learning_rate=1e-4, root `outputs/tuning_lr1e4_prehard_nenv10_1p5m`.
- Rationale: seed1 showed policy drift/final checkpoint degradation; lower LR tests whether smaller PPO updates stabilize hard/prehard without changing reward/guard/curriculum.

## 2026-06-30 lr1e-4 early checkpoint
- Diagnostic low-LR seed1 is active: PID 98726 / train PID 98734.
- Config verified: n_envs=10, learning_rate=1e-4, ent_coef=0.01.
- Around ~420k it reached stage2; window briefly showed success 0.40, route 0.815, cost 0.0.
- Around ~450k-480k it remained stage2 with route ~0.71-0.73, success ~0.03-0.10, low cost. Learning is slower than 3e-4 but not collapsed.
- Continue to 750k to check prehard/hard entry and stability.

## 2026-06-30 low-lr 1e-4 live check at ~1.01M
- Active job: outputs/tuning_lr1e4_prehard_nenv10_1p5m, PID 98734, n_envs=10, lr=1e-4, ent=0.01, seed=1.
- Latest log around 1,013,760 steps: still curriculum stage 3; window_route_completion about 0.76, window_success down to 0.033, window_cost about 0.20.
- Interpretation: this supports partial non-convergence / slow adaptation, but not a simple "more steps will fix it" story; success is drifting downward before hard-stage promotion. Continue monitoring before deciding whether to stop or let finish.

## 2026-06-30 stopped low-lr 1e-4 diagnostic
- Stopped PID 98734 / wrapper 98726 at ~1.064M steps after demotion to stage2 and degraded window metrics.
- Next: evaluate checkpoint_750000_steps.zip with n_envs=10, episodes=50, densities 0.00/0.08/0.15.

## 2026-06-30 low-lr checkpoint result
- Evaluated low-LR seed1 750k checkpoint with n_envs=10 and 50 episodes/density.
- Result: d0.00 success=0.86 cost=0.00 route=0.980; d0.08 success=0.74 cost=0.12 route=0.927; d0.15 success=0.34 cost=0.62 route=0.713.
- Decision: do not extend 1e-4; launch 2e-4 seed1 diagnostic next.

## 2026-06-30 launched lr2e-4 diagnostic
- Launched proposed PPO seed1, n_envs=10, timesteps=1.5M, ent_coef=0.01, learning_rate=2e-4.
- Output root: outputs/tuning_lr2e4_prehard_nenv10_1p5m.
- Purpose: intermediate LR diagnostic after 1e-4 degraded/demoted and 3e-4 showed seed instability.

## 2026-06-30 lr2e-4 early check at ~409k
- Active PID 99868, n_envs=10, lr=2e-4, ent=0.01.
- At ~409,600 steps: curriculum stage=1, window_route_completion=0.804, window_success=0.233, window_cost=0.10.
- Interpretation: learning speed is better than lr=1e-4 and no early collapse yet; continue to ~700k+ before deciding.

## 2026-06-30 lr2e-4 mid check at ~594k
- Active PID 99868. Reached stage2 around 543k.
- Latest around 593,920 steps: stage=2, window_route_completion=0.717, window_success=0.0333, window_cost=0.133.
- Interpretation: faster than lr=1e-4, not collapsed, but medium-stage success remains weak. Continue to ~750k/900k before decision.

## 2026-06-30 lr2e-4 check at ~747k
- Active PID 99868. Reached stage3 around 706k; checkpoint_750000_steps.zip exists.
- Latest around 747,520 steps: stage=3, window_route_completion=0.755, window_success=0.0667, window_cost=0.267.
- Interpretation: lr=2e-4 reaches prehard faster than 1e-4 but success remains weak. Continue toward ~1.0M to check for recovery vs demotion.

## 2026-06-30 lr2e-4 hard-stage instability at ~880k
- Reached hard stage4 around 829k with window_success=0.267, window_route_completion=0.806, window_cost=0.20.
- Degraded by ~870k and demoted to stage3: window_success=0.0, window_route_completion=0.608, window_cost=0.30.
- Interpretation: lr=2e-4 learns faster than 1e-4 but still shows hard-stage instability. Allow until ~1.0M for possible recovery; stop if no recovery.

## 2026-06-30 lr2e-4 check at ~963k
- Active PID 99868. After hard-stage demotion, run recovered to stage3 rather than collapsing.
- Latest around 962,560 steps: stage=3, window_route_completion=0.732, window_success=0.133, window_cost=0.167.
- Decision: continue to ~1.125M checkpoint; do not stop yet, but current evidence still does not support blind step increase as the main solution.

## 2026-06-30 stopped lr2e-4 diagnostic
- Stopped lr2e-4 seed1 after checkpoint_1125000_steps.zip; training did not stabilize hard stage.
- Next: evaluate checkpoint_1125000_steps.zip with n_envs=10, 50 episodes/density.

## 2026-06-30 lr2e-4 checkpoint evaluation result
- Evaluated checkpoint_1125000_steps.zip with n_envs=10 and 50 episodes/density.
- Result: d0.00 success=0.74 cost=0.00 route=0.973; d0.08 success=0.74 cost=0.10 route=0.939; d0.15 success=0.38 cost=0.52 route=0.767.
- Current conclusion for 1M question: low success is partly due to hard-stage learning difficulty, but evidence does not support simply increasing timesteps; 1.5M/2M and LR diagnostics show policy drift and hard-stage instability.
- Next recommended tuning direction: checkpoint selection / curriculum hard-stage stabilization, not raw step increase.

## 2026-06-30 launched stage2 strict-gate diagnostic
- Used remote scientific-brainstorming-main for failure-driven tuning after LR and route-gate diagnostics.
- Launched proposed PPO seed1, n_envs=10, timesteps=1.5M, ent_coef=0.01, default learning_rate=3e-4.
- Only mechanism changed: stage2_success 0.25 -> 0.35 and stage2_cost 0.45 -> 0.35.
- Output root: outputs/tuning_stage2strict035_prehard_nenv10_1p5m.
- Purpose: delay hard-stage promotion until prehard is more stable, testing whether hard-stage instability is caused by premature promotion rather than insufficient total timesteps.

## 2026-06-30 relaunched stage2 strict-gate diagnostic after CLI fix
- Fixed scripts/train.py to expose curriculum-gate CLI arguments and verified --help/py_compile.
- Relaunched proposed seed1 strict-gate run after removing the failed empty output root.
- Expected config: n_envs=10, ent_coef=0.01, learning_rate=3e-4, stage2_success=0.35, stage2_cost=0.35.

## 2026-06-30 strict-gate config verification
- Active strict-gate run train PID 101841, wrapper PID 101834, n_envs=10.
- Config verified: learning_rate=3e-4, ent_coef=0.01, stage2_success=0.35, stage2_cost=0.35, allow_demote=True.
- Early at ~92k steps: stage0, route window ~0.185, success 0; normal warmup.

## 2026-06-30 strict-gate early check at ~430k
- Active train PID 101841. Checkpoint_375000_steps.zip exists.
- Reached stage2 by ~379k, briefly demoted to stage1, then returned to stage2.
- Around 419,840 steps: stage=2, window_route_completion=0.840, window_success=0.300, window_cost=0.000.
- Interpretation: strict stage2 gate is delaying prehard promotion as intended because success has not reached 0.35. Continue to ~700k to check whether this produces a more stable stage3 transition.

## 2026-06-30 strict-gate mid check at ~563k
- Active train PID 101841. Entered stage3 around ~512k despite stricter stage2_success=0.35 gate, indicating it had a sufficiently strong stage2 window before promotion.
- Latest around 563,200 steps: stage=3, window_route_completion=0.746, window_success=0.100, window_cost=0.167.
- Interpretation: not collapsed; strict gate now delays hard-stage promotion because stage3->hard also requires success >=0.35 and cost <=0.35. Continue to ~750k to inspect prehard stability.

## 2026-06-30 strict-gate check at ~706k
- Active train PID 101841. Stage2 promotion to stage3 occurred around 655k with a stronger window: success=0.367, route=0.869, cost=0.167.
- After stage3 transition, window weakened by ~706k: stage=3, success=0.100, route=0.688, cost=0.300.
- Interpretation: strict gate produced a cleaner promotion than default, but prehard remains unstable. Continue to ~900k to see whether stage3 recovers before hard promotion.

## 2026-06-30 strict-gate check at ~829k
- Active train PID 101841. checkpoint_750000_steps.zip exists.
- Latest around 829,440 steps: stage=3, window_route_completion=0.745, window_success=0.133, window_cost=0.100.
- Compared with lr2e-4, this run avoids early hard-stage promotion near ~829k, but prehard success is still below the stricter 0.35 gate. Continue to ~1.0M to distinguish delayed stabilization from stage3 stagnation.

## 2026-06-30 strict-gate check at ~932k
- Active train PID 101841. Still stage3, no hard-stage promotion.
- Latest around 931,840 steps: stage=3, window_route_completion=0.771, window_success=0.100, window_cost=0.167.
- Interpretation: stricter gate prevents premature hard exposure but has not raised prehard success enough. Continue until checkpoint_1125000_steps.zip, then stop/evaluate if still stage3-stagnant.

## 2026-06-30 strict-gate check at ~1.136M
- checkpoint_1125000_steps.zip exists; active train PID 101841.
- Around 1,136,640 steps: still stage3, but window improved to success=0.267, route=0.794, cost=0.100.
- Decision: do not stop yet because recovery is visible and gate threshold is close. Continue to ~1.25M to see if it enters hard with better prehard stability.

## 2026-06-30 stopped strict-gate diagnostic
- Stopped strict-gate seed1 after checkpoint_1125000_steps.zip and additional monitoring to ~1.239M.
- Latest before stop: stage3, window_success about 0.167, route about 0.766, cost about 0.20; no hard-stage promotion.
- Next: evaluate checkpoint_1125000_steps.zip with n_envs=10, 50 episodes/density.

## 2026-06-30 strict-gate checkpoint evaluation result
- Evaluated checkpoint_1125000_steps.zip with n_envs=10 and 50 episodes/density.
- Result: d0.00 success=0.76 cost=0.00 route=0.976; d0.08 success=0.78 cost=0.04 route=0.974; d0.15 success=0.38 cost=0.52 route=0.732.
- Current decision: gate tightening helps medium density but does not fix high-density collision/success. Next tuning target: defensive TTC / target-speed fixed parameter protocol with n_envs=10.

## 2026-06-30 launched defensive ttc12/v18 nenv10 seed26
- Fixed defensive script evaluation to pass n_envs=args.n_envs before launch.
- Launched .
- Purpose: high-density failures are collision-dominated; pasted plan recommends defensive ttc12/v18 for density 0.15 stress. This run tests the fixed defensive protocol under the user-updated 10-env requirement.

## 2026-06-30 defensive ttc12/v18 seed26 verified
- Active wrapper PID 103267, train PID 103275, n_envs=10.
- Output root: outputs/defensive_ttc12_v18_nenv10_final.
- Config verified: seed=26, timesteps=1M, horizon=1500, ttc_threshold=12.0, target_speed_kmh=18.0, n_envs=10.
- Note: earlier RUN_STATE append attempted to include a backticked command and shell printed a harmless local error; the actual training process is running correctly.

## 2026-06-30 defensive seed26 early/mid check at ~440k
- Active defensive train PID 103275, n_envs=10, ttc12/v18, horizon=1500.
- Reached stage2 by ~410k. Stage1 window was strong (success up to 0.667, route 0.785, cost 0.0).
- Latest around 440,320 steps: stage2, route=0.695, success=0.0333, cost=0.167.
- Interpretation: ttc12/v18 is not causing early low-speed stagnation; continue toward 650k/750k to inspect medium/prehard behavior.

## 2026-06-30 defensive seed26 check at ~625k
- Active train PID 103275. checkpoint_500000_steps.zip exists.
- Still stage2 at ~624,640 steps: route=0.741, success=0.0333, cost=0.133.
- Interpretation: ttc12/v18 does not collapse, but the defensive config uses a strict stage2_success=0.50 and may remain in medium. Continue toward 750k/end before deciding whether to stop or let auto-evaluate.

## 2026-06-30 defensive seed26 check at ~809k
- Active train PID 103275. checkpoint_750000_steps.zip exists.
- Still stage2 around 808,960 steps: route=0.760, success=0.133, cost=0.167.
- Interpretation: defensive ttc12/v18 is not collapsed but appears constrained by strict stage2_success=0.50. Let run finish and auto-evaluate; likely next tuning is to relax defensive stage2 gate or use checkpoint evaluation.

## 2026-06-30 defensive seed26 completed
- Completed ttc12/v18 seed26 under n_envs=10 for train and evaluation.
- Result: d0.00 success=0.98 cost=0.00 route=0.990; d0.08 success=0.88 cost=0.10 route=0.954; d0.15 success=0.60 cost=0.28 route=0.848.
- This meets the high-density reference target for a single seed and is stronger than the previous gate/LR diagnostics. Next: expand same fixed protocol to seed27.

## 2026-06-30 launched defensive ttc12/v18 nenv10 seed27
- Launched second fixed-protocol defensive run after seed26 succeeded.
- Command: python scripts/run_one_defensive_proposed.py --seed 27 --n-envs 10 --timesteps 1000000 --root outputs/defensive_ttc12_v18_nenv10_final --ttc-threshold 12.0 --target-speed 18.0 --device cuda.
- Purpose: test whether seed26 high-density success 0.60 / cost 0.28 is reproducible under the same n_envs=10 protocol.

## 2026-06-30 defensive seed27 check at ~440k
- Active train PID 104182, n_envs=10, ttc12/v18.
- Seed27 started worse than seed26 with early stage0 out-of-road/low route, but recovered by ~410k and promoted to stage1.
- Around 419,840 steps: stage1 promotion window was strong (success=0.767, route=0.879, cost=0.233).
- Latest around 440,320 steps: stage1, route=0.685, success=0.200, cost=0.267.
- Interpretation: not stuck; continue to 650k/750k to check stage2 and whether it follows seed26.

## 2026-06-30 defensive seed27 check at ~614k
- Active train PID 104182. checkpoint_500000_steps.zip exists.
- Stage2 by mid training. Latest around 614,400 steps: stage2, route=0.767, success=0.0667, cost=0.0667.
- Interpretation: weaker than seed26 but not collapsed; low cost and reasonable route suggest final eval may still be useful. Continue to finish because seed26 also ended in stage2 but evaluated well.

## 2026-06-30 defensive seed27 check at ~778k
- Active train PID 104182. checkpoint_750000_steps.zip exists.
- Still stage2 around 778,240 steps: route=0.746, success=0.167, cost=0.167.
- Interpretation: weaker and more variable than seed26, but similar stage2-only training pattern. Let it finish and auto-evaluate under n_envs=10 to test reproducibility.

## 2026-06-30 defensive seed27 completed
- Completed ttc12/v18 seed27 under n_envs=10 for train and evaluation.
- Combined seed26/27 summary from auto report: d0.00 success=0.96, d0.08 success=0.87, d0.15 success=0.60, d0.15 cost/collision=0.29.
- Both seed CSVs use eval_n_envs=10. Next: launch seed28 to complete the 3-seed fixed defensive protocol.

## 2026-06-30 launched defensive ttc12/v18 nenv10 seed28
- Launched third fixed-protocol defensive run to satisfy the minimum 3-seed requirement.
- Command: python scripts/run_one_defensive_proposed.py --seed 28 --n-envs 10 --timesteps 1000000 --root outputs/defensive_ttc12_v18_nenv10_final --ttc-threshold 12.0 --target-speed 18.0 --device cuda.
- Purpose: complete 3-seed evidence for Defensive RAC-PPO ttc12/v18 under n_envs=10.

## 2026-06-30 convergence check: defensive_ttc12_v18_nenv10_final
- User asked whether the 1M success rate is low because the policy has not converged and whether training steps should be increased.
- Evidence checked: seed26/seed27 final eval CSVs, train logs, monitor CSVs; seed28 live process/logs.
- Fixed protocol still uses n_envs=10 for training and eval.
- seed26/seed27 final evaluation: density0.00 success 0.98/0.94, density0.08 0.88/0.86, density0.15 0.60/0.60. Low and medium density are already strong; high density remains cost/collision limited.
- seed26/seed27 training logs at 0.93M-1.00M remain in curriculum stage2 with window_success around 0.03-0.33 and route_completion around 0.73-0.85. This suggests stage2/high-density transition instability rather than simple global undertraining.
- seed28 live at roughly 0.46M has reached stage2 once and demoted back to stage1; current latest monitor windows show success around 0.32-0.36 over the last 50-100 episodes and stage_mean around 1.4-1.5.
- Decision: do not blindly extend all runs yet. Finish seed28 first. If the 3-seed pattern confirms high-density plateau, run a controlled longer-step diagnostic with checkpoint/eval comparison rather than assuming 2M will fix it.

## 2026-06-30 seed28 completed and convergence decision
- seed28 completed at 1,003,520 steps and wrote final_model plus evaluation CSV.
- Final eval uses eval_n_envs=10.
- seed28: d0.00 success 0.98, d0.08 0.88, d0.15 0.72. It improves high-density over seed26/27 (both 0.60), but final training logs remain curriculum stage2 with window_success=0.133 and rollout success_rate=0.11.
- Three-seed high-density d0.15: success=0.640+-0.069, cost/collision=0.260+-0.053, route_completion=0.852+-0.031.
- Decision: do not declare 1M fully converged. Do not blindly rerun all final seeds at higher steps yet. Launch one controlled longer-step diagnostic with the same fixed defensive protocol and n_envs=10 to test whether 1.5M/2M improves high-density evaluation or only extends the stage2 plateau.

## 2026-06-30 launched longer-step convergence diagnostic
- Launched controlled diagnostic instead of blindly replacing all final runs.
- PID: 106755 wrapper; train PID: 106759.
- Command: python scripts/run_one_defensive_proposed.py --seed 28 --n-envs 10 --timesteps 1500000 --root outputs/defensive_ttc12_v18_nenv10_steps_diag_1p5m --ttc-threshold 12.0 --target-speed 18.0 --device cuda.
- Log: outputs/defensive_ttc12_v18_nenv10_steps_diag_1p5m/logs/defensive_s28_ttc12_v18_1p5m_20260630_052110.log.
- Verified config: seed=28, n_envs=10, horizon=1500, lr=3e-4, stage2_success=0.5, stage2_cost=0.25, ttc_threshold=12.0, target_speed_kmh=18.0.
- Early status: stage0, ~51k steps, fps ~3100, normal startup. This run will answer whether 1M is undertrained for high-density robustness.

## 2026-06-30 continuation check: 1.5M convergence diagnostic live
- Re-read the pasted task file locally before continuing. Current user override remains n_envs=10 for all new train/eval jobs.
- Checked live remote status for outputs/defensive_ttc12_v18_nenv10_steps_diag_1p5m.
- Active process: wrapper PID 106755, training PID 106759, with 10 environment subprocesses.
- Current progress from log: ~225,280 timesteps, stage oscillating between stage0/stage1, latest window_success=0.10, window_cost=0.00, window_route_completion=0.616; this is normal early-phase behavior and no intervention is needed yet.
- GPU status: ~1022 MiB / 12282 MiB, utilization around 17%; no memory pressure.

## 2026-06-30 1.5M diagnostic monitor at ~491k
- Active training PID 106759; still n_envs=10 and single training job.
- Checkpoint generated: checkpoint_375000_steps.zip.
- Latest log progress: ~491,520 timesteps, stage2.
- Latest windows from monitor: last100 success=0.06, cost=0.18, route=0.707, stage_mean=2.0; last50 success=0.08, cost=0.14, route=0.733.
- Interpretation: the run reached stage2 but is currently weaker than the prior 1M seed28 at comparable/mid phases. Continue to 750k/1M before deciding; do not stop early yet because high-density eval can differ from rollout windows.

## 2026-06-30 1.5M diagnostic monitor at ~747k
- Active training PID 106759; n_envs=10; still the only training job.
- Checkpoints generated: checkpoint_375000_steps.zip and checkpoint_750000_steps.zip.
- Latest log progress: ~747,520 timesteps, stage2.
- Latest monitor windows: last100 success=0.14, cost=0.18, route=0.780, stage_mean=2.0; last200 success=0.105, cost=0.18, route=0.768.
- Interpretation: no clear breakthrough by 750k. Continue to 1.125M and final 1.5M because this diagnostic is specifically testing whether additional steps help high-density performance.

## 2026-06-30 1.5M diagnostic monitor at ~1.06M
- Active training PID 106759; n_envs=10; still the only training job.
- Latest progress: ~1,064,960 timesteps, stage2.
- Latest monitor windows: last50 success=0.26, cost=0.06, route=0.819; last100 success=0.21, cost=0.11, route=0.792; last400 success=0.177, cost=0.13, route=0.790.
- Interpretation: recovery after 750k is visible. This provides tentative support that >1M may help, but final evaluation is still required because rollout windows and held-out density evaluation differ.

## 2026-06-30 1.5M diagnostic monitor at ~1.26M
- Active training PID 106759; n_envs=10; only training job.
- Checkpoints generated: checkpoint_375000_steps.zip, checkpoint_750000_steps.zip, checkpoint_1125000_steps.zip.
- Latest progress: ~1,259,520 timesteps, stage2.
- Latest monitor windows: last50 success=0.18, cost=0.08, route=0.809; last100 success=0.17, cost=0.12, route=0.810; last200 success=0.21, cost=0.11, route=0.818; last400 success=0.215, cost=0.117, route=0.803.
- Interpretation: performance is more stable than at 750k, but still no decisive breakthrough. Final held-out evaluation is needed before increasing official timesteps.

## 2026-06-30 1.5M diagnostic training complete; eval pending
- Training reached 1,505,280 timesteps and wrote checkpoint_1500000_steps.zip plus final_model.zip.
- Active script is now expected to evaluate and build figures/report; evaluation CSV not yet present at this check.
- Final monitor windows before eval: last50 success=0.28, cost=0.08, route=0.814; last100 success=0.20, cost=0.09, route=0.820; last200 success=0.255, cost=0.08, route=0.840; last400 success=0.228, cost=0.092, route=0.831.
- Interpretation: final training windows are better than the 1M run tail, but final held-out density evaluation remains the decision gate for whether longer training is useful.

## 2026-06-30 1.5M diagnostic result and decision
- Diagnostic completed and wrote eval CSV, summary, figures, and report under outputs/defensive_ttc12_v18_nenv10_steps_diag_1p5m.
- Same seed comparison, n_envs=10, ttc12/v18:
  - 1M seed28: d0.00 success=0.98 cost=0.00 route=0.989; d0.08 success=0.88 cost=0.10 route=0.954; d0.15 success=0.72 cost=0.20 route=0.885.
  - 1.5M seed28: d0.00 success=0.96 cost=0.00 route=0.991; d0.08 success=0.78 cost=0.16 route=0.911; d0.15 success=0.58 cost=0.36 route=0.825.
- Decision: increasing steps to 1.5M worsens held-out evaluation. Do not scale final protocol to longer training. Next action: evaluate intermediate checkpoints or tune curriculum/early stopping.

## 2026-06-30 checkpoint diagnostic conclusion for 1.5M seed28
- Screening eval: 20 episodes per density, densities 0.08 and 0.15, n_envs=10, from same 1.5M run config.
- Results:
  - 375k: d0.08 success=0.70 cost=0.20 route=0.916; d0.15 success=0.55 cost=0.35 route=0.881.
  - 750k: d0.08 success=0.90 cost=0.05 route=0.954; d0.15 success=0.45 cost=0.40 route=0.765.
  - 1125k: d0.08 success=0.85 cost=0.00 route=0.987; d0.15 success=0.60 cost=0.40 route=0.797.
  - 1500k: d0.08 success=0.85 cost=0.10 route=0.947; d0.15 success=0.60 cost=0.30 route=0.861.
- Same-seed 1M final full eval remains better at high density: d0.15 success=0.72 cost=0.20 route=0.885.
- Decision: extra training steps are not the main fix. Do not adopt 1.5M. Next small-step tuning: increase only ttc_threshold from 12 to 14, keep target_speed=18 and n_envs=10, run 500k screening seed28.

## 2026-06-30 launched ttc14/v18 500k screening
- Purpose: after 1.5M longer training failed, test one safety-side parameter change for high-density collision/cost.
- Single changed mechanism: ttc_threshold 12.0 -> 14.0. Kept target_speed=18.0, horizon=1500, lr=3e-4, stage2 gates, seed=28, n_envs=10.
- PID: wrapper 108982, training 108987.
- Command: python scripts/run_one_defensive_proposed.py --seed 28 --n-envs 10 --timesteps 500000 --root outputs/tuning_ttc14_v18_nenv10_500k --ttc-threshold 14.0 --target-speed 18.0 --device cuda.
- Verified config: n_envs=10, ttc_threshold=14.0, target_speed_kmh=18.0.
- Early status: ~61k steps, stage0, normal startup.
- This is screening only and must not be mixed with final ttc12/v18 fixed-protocol results.

## 2026-06-30 ttc14/v18 500k screening monitor at ~410k
- Active training PID 108987; n_envs=10; only job.
- Checkpoints generated: 125k, 250k, 375k.
- Latest progress: ~409,600 timesteps; stage2 reached.
- Latest monitor windows: last50 success=0.26, cost=0.12, route=0.781; last100 success=0.23, cost=0.16, route=0.753; last200 success=0.27, cost=0.175, route=0.742.
- Interpretation: training is viable. Await final 500k evaluation before judging whether ttc14 improves safety over ttc12.

## 2026-06-30 ttc14/v18 500k screening result
- ttc14/v18 seed28 500k completed and evaluated with n_envs=10.
- Result: d0.08 success=0.78 cost=0.20 route=0.888 collision=0.20; d0.15 success=0.48 cost=0.32 route=0.829 collision=0.32.
- Decision: do not expand ttc14/v18. Next single-parameter screen: lower target_speed from 18 to 16 while returning ttc_threshold to 12.

## 2026-06-30 launched ttc12/v16 500k screening
- Purpose: after ttc14/v18 failed, test lowering target speed to reduce high-density collision/cost.
- Single changed mechanism: target_speed 18.0 -> 16.0. Restored ttc_threshold=12.0; kept horizon=1500, lr=3e-4, stage2 gates, seed=28, n_envs=10.
- PID: wrapper 109756, training 109761.
- Command: python scripts/run_one_defensive_proposed.py --seed 28 --n-envs 10 --timesteps 500000 --root outputs/tuning_ttc12_v16_nenv10_500k --ttc-threshold 12.0 --target-speed 16.0 --device cuda.
- Verified config: n_envs=10, ttc_threshold=12.0, target_speed_kmh=16.0.
- Early status: ~51k steps, stage0, normal startup.
- Screening only; do not mix with final ttc12/v18 fixed protocol.

## 2026-06-30 ttc12/v16 500k screening result
- ttc12/v16 seed28 500k completed and evaluated with n_envs=10.
- Result: d0.00 success=0.84 cost=0.00 route=0.975; d0.08 success=0.76 cost=0.08 route=0.944; d0.15 success=0.52 cost=0.22 route=0.857.
- Decision: do not expand v16. Current best fixed defensive protocol remains ttc12/v18 at 1M; longer steps and tested single-parameter safety changes did not improve held-out metrics.

## 2026-06-30 launched P0 main baseline seed1
- After defensive diagnostics, returned to P0 main comparison queue.
- Launched baseline seed1 under current n_envs=10 candidate main protocol: timesteps=1,500,000, horizon=1200, ent_coef=0.01, device=cuda.
- PID: wrapper 111991, training 111996.
- Command: python scripts/train.py --variant baseline --algo ppo --seed 1 --timesteps 1500000 --horizon 1200 --n-envs 10 --ent-coef 0.01 --device cuda --output-dir outputs/iscsic_main_nenv10_1p5m_ent001/runs; then evaluate_from_config with episodes=50, densities=0.00/0.08/0.15, n_envs=10.
- Verified config: variant=baseline, seed=1, horizon=1200, n_envs=10, ent_coef=0.01, learning_rate=3e-4.
- Early status: ~30k steps, normal startup. This run fills one missing P0 main-comparison seed.

## 2026-06-30 baseline seed1 monitor at ~112k
- Active P0 main-comparison training: baseline PPO seed1, n_envs=10, timesteps=1.5M, horizon=1200, ent_coef=0.01.
- PID: wrapper 111991, training 111996, 10 worker env subprocesses.
- Current progress from log: ~112,640 timesteps.
- GPU status: ~1022 MiB / 12282 MiB, low utilization, no memory pressure.
- Early rollout success_rate=0.0 with low route completion, which is expected for baseline early training. No intervention.

## 2026-06-30 baseline seed1 monitor at ~317k
- Active P0 main-comparison training baseline seed1; n_envs=10, 1.5M, ent_coef=0.01.
- Current progress: ~317,440 timesteps.
- Monitor windows: last100 success=0.10, cost=0.90, route=0.531, speed=25.57; last200 success=0.11, cost=0.89, route=0.555.
- Interpretation: baseline is learning fast driving but with high safety cost/collision, which is expected for the baseline comparator. Continue without intervention.

## 2026-06-30 baseline seed1 monitor at ~563k
- Active P0 main-comparison training baseline seed1; n_envs=10, 1.5M, ent_coef=0.01.
- Checkpoint generated: checkpoint_375000_steps.zip.
- Current progress: ~563,200 timesteps.
- Monitor windows from CSV at check time: last100 success=0.10, cost=0.91, route=0.436; last800 success=0.072, cost=0.929, route=0.494.
- Log shows repeated collision/out-of-road at high speed. This is acceptable for baseline comparator and should be preserved rather than tuned away.

## 2026-06-30 baseline seed1 monitor at ~881k
- Active P0 main-comparison training baseline seed1; n_envs=10, 1.5M, ent_coef=0.01.
- Checkpoints generated: 375k and 750k.
- Current progress: ~880,640 timesteps.
- Monitor windows: last400 success=0.333, cost=0.647, route=0.657; last800 success=0.250, cost=0.741, route=0.593.
- Interpretation: baseline starts succeeding but remains unsafe/high-cost, suitable as main comparator. Continue to completion and evaluate.

## 2026-06-30 baseline seed1 monitor at ~1.27M
- Active P0 main-comparison training baseline seed1; n_envs=10, 1.5M, ent_coef=0.01.
- Checkpoints generated: 375k, 750k, 1125k.
- Current progress: ~1,269,760 timesteps.
- Monitor windows: last200 success=0.535, cost=0.450, route=0.743; last800 success=0.380, cost=0.611, route=0.669.
- Interpretation: route/success improved substantially while safety cost remains high; continue to final evaluation.

## 2026-06-30 baseline seed1 completed
- Completed P0 main-comparison baseline PPO seed1 under n_envs=10, timesteps=1.5M, horizon=1200, ent_coef=0.01.
- Evaluation CSV: outputs/iscsic_main_nenv10_1p5m_ent001/evaluations/baseline_ppo_s1.csv; eval_n_envs=10, 50 episodes per density.
- Results: d0.00 success=0.00 cost=1.00 route=0.327; d0.08 success=0.00 cost=1.00 route=0.223 collision=0.50 out=0.50; d0.15 success=0.00 cost=1.00 route=0.213 collision=0.68 out=0.32.
- Next: launch baseline seed2 to complete baseline seeds 1/2 for the main comparison queue.

## 2026-06-30 launched P0 main baseline seed2
- Launched baseline PPO seed2 under current n_envs=10 candidate main protocol: timesteps=1,500,000, horizon=1200, ent_coef=0.01, device=cuda.
- PID: wrapper 115057, training 115062.
- Command: python scripts/train.py --variant baseline --algo ppo --seed 2 --timesteps 1500000 --horizon 1200 --n-envs 10 --ent-coef 0.01 --device cuda --output-dir outputs/iscsic_main_nenv10_1p5m_ent001/runs; then evaluate_from_config with episodes=50, densities=0.00/0.08/0.15, n_envs=10.
- Verified config: variant=baseline, seed=2, horizon=1200, n_envs=10, ent_coef=0.01, learning_rate=3e-4.
- Early status: ~20k steps, normal startup.

## 2026-06-30 baseline seed2 monitor at ~82k
- Active P0 main-comparison training baseline seed2; n_envs=10, 1.5M, ent_coef=0.01.
- PID: wrapper 115057, training 115062, 10 env workers.
- Current progress: ~81,920 timesteps.
- Early rollout success_rate=0.0, low speed/route completion; normal startup behavior for baseline.
- GPU status: ~1023 MiB / 12282 MiB, no memory pressure.

## 2026-06-30 baseline seed2 monitor at ~389k
- Active P0 main-comparison training baseline seed2; n_envs=10, 1.5M, ent_coef=0.01.
- Checkpoint generated: checkpoint_375000_steps.zip.
- Current progress: ~389,120 timesteps.
- Monitor windows: last100 success=0.11, cost=0.89, route=0.527; last400 success=0.175, cost=0.807, route=0.568.
- Interpretation: seed2 has entered high-speed/high-cost baseline behavior similar to seed1. Continue to completion.

## 2026-06-30 baseline seed2 monitor at ~737k
- Active P0 main-comparison training baseline seed2; n_envs=10, 1.5M, ent_coef=0.01.
- Current progress: ~737,280 timesteps; 375k checkpoint exists, 750k checkpoint expected soon.
- Monitor windows: last100 success=0.51, cost=0.45, route=0.745; last400 success=0.39, cost=0.59, route=0.675.
- Interpretation: seed2 is learning route completion faster than seed1 at this stage, while still retaining high collision/cost. Continue to completion.

## 2026-06-30 baseline seed2 monitor at ~1.18M
- Active P0 main-comparison training baseline seed2; n_envs=10, 1.5M, ent_coef=0.01.
- Checkpoints generated: 375k, 750k, 1125k.
- Current progress: ~1,177,600 timesteps.
- Monitor windows: last100 success=0.40, cost=0.58, route=0.704; last800 success=0.36, cost=0.625, route=0.662.
- Interpretation: stable high-speed baseline with moderate success but high cost/collision. Continue to final model and evaluation.

## 2026-06-30 baseline seed2 completed
- Completed P0 main-comparison baseline PPO seed2 under n_envs=10, timesteps=1.5M, horizon=1200, ent_coef=0.01.
- Evaluation CSV: outputs/iscsic_main_nenv10_1p5m_ent001/evaluations/baseline_ppo_s2.csv; eval_n_envs=10, 50 episodes per density.
- Results: d0.00 success=0.00 cost=1.00 route=0.345; d0.08 success=0.14 cost=0.86 route=0.410 collision=0.30 out=0.56; d0.15 success=0.04 cost=0.96 route=0.360 collision=0.58 out=0.38.
- Baseline seeds 1/2 are now complete under the 1.5M n_envs=10 candidate protocol. Next: launch curriculum seed1.

## 2026-06-30 launched P0 main curriculum seed1
- Completed baseline seed2 and launched curriculum PPO seed1 under current n_envs=10 candidate main protocol: timesteps=1,500,000, horizon=1200, ent_coef=0.01, device=cuda.
- PID: wrapper 116547, training 116552.
- Command: python scripts/train.py --variant curriculum --algo ppo --seed 1 --timesteps 1500000 --horizon 1200 --n-envs 10 --ent-coef 0.01 --device cuda --output-dir outputs/iscsic_main_nenv10_1p5m_ent001/runs; then evaluate_from_config with episodes=50, densities=0.00/0.08/0.15, n_envs=10.
- Verified config: variant=curriculum, seed=1, horizon=1200, n_envs=10, ent_coef=0.01, learning_rate=3e-4, use_risk_reward=False, use_action_guard=False.
- Early status: ~61k steps, curriculum stage0, normal startup.

## 2026-06-30 convergence supervision note after defensive 1M vs 1.5M diagnostic
- User question: whether the moderate 1M success rate is mainly due to non-convergence and should be solved by increasing timesteps.
- Evidence: fixed defensive protocol ttc12/v18 seed28 at 1M reached d0.15 success=0.72, cost=0.20; the controlled 1.5M diagnostic under the same seed/protocol reached d0.15 success=0.58, cost=0.36, and also worsened d0.08 success from 0.88 to 0.78.
- Interpretation: current evidence does not support blind longer training as the primary fix. The issue is more likely curriculum/high-density distribution instability or checkpoint overtraining/forgetting, not simple under-training.
- Action policy: keep 1M ttc12/v18 as the fixed defensive benchmark for now; use longer-step runs only as diagnostics with checkpoint selection/early stopping, not as automatic replacement. Continue current P0 main comparison queue under n_envs=10.

## 2026-06-30 curriculum seed1 monitor at ~307k
- Active P0 main-comparison training curriculum seed1; n_envs=10, 1.5M, horizon=1200, ent_coef=0.01.
- Current progress: ~307,200 timesteps, stage=2.
- Recent log: rollout success_rate around 0.20; curriculum window_success=0.233, window_cost=0.767, window_route_completion=0.648.
- Interpretation: early/mid-early training remains high-cost and not yet stable. Continue monitoring; do not terminate or tune based only on 300k-stage noise.

## 2026-06-30 curriculum seed1 monitor at ~358k
- Active P0 main-comparison training curriculum seed1; n_envs=10, 1.5M, horizon=1200, ent_coef=0.01.
- Current progress from log: ~358,400 timesteps; stage=2.
- Monitor windows: last50 success=0.360 cost=0.640 route=0.682; last100 success=0.400 cost=0.580 route=0.729; last200 success=0.280 cost=0.710 route=0.660.
- Interpretation: early high-cost behavior persists, but recent success/route improved versus ~307k. Continue rather than interrupt; no extra training process launched.

## 2026-06-30 current main-result audit while curriculum seed1 runs
- Audited outputs/iscsic_main_nenv10_1p5m_ent001/evaluations/*_ppo_s*.csv.
- Confirmed 4 existing eval CSVs under current n_envs=10 protocol: baseline seeds 1/2 and proposed seeds 0/1.
- Proposed seed0/seed1 both use eval_n_envs=10, but d0.15 differs substantially (0.60 vs 0.32 success). This reinforces anti-cherry-picking requirement: preserve seed-level evidence and continue filling missing protocol cells.
- Active training remains curriculum seed1 only; no second training launched.

## 2026-06-30 curriculum seed1 monitor at ~502k
- Active P0 main-comparison training curriculum seed1; n_envs=10, 1.5M, horizon=1200, ent_coef=0.01.
- Current progress from log: ~501,760 timesteps; checkpoint_375000_steps.zip exists.
- Recent log shows stage=1, rollout success_rate 0.28, window_success 0.20, window_cost 0.80.
- Interpretation: curriculum seed1 has not stabilized and has regressed from stage2 to stage1 in this window. Continue until at least 750k/checkpoint before deciding whether it is a weak comparator result; do not launch any parallel training.

## 2026-06-30 build_final_outputs protocol-class fix
- Fixed scripts/build_final_outputs.py protocol classification to recognize the current main candidate protocol: timesteps=1.5M, horizon=1200, train n_envs=10, eval_n_envs=10, densities 0.00/0.08/0.15, >=50 episodes/density.
- Also recognizes the fixed defensive protocol: timesteps=1M, horizon=1500, train/eval n_envs=10, same densities/episode count, run path containing defensive.
- Verification: python -m py_compile scripts/build_final_outputs.py passed; python scripts/build_final_outputs.py completed and regenerated outputs/final_iscsic_results.
- Active training remained curriculum seed1 only while this script maintenance was done.

## 2026-06-30 build_final_outputs defensive label fix
- Fixed defensive CSV/run inference in scripts/build_final_outputs.py: CSVs whose variant column is proposed but whose path/run_dir contains defensive now resolve to defensive_proposed_ppo_s* run dirs.
- Added output-only relabeling so defensive fixed-protocol rows are variant=defensive_proposed in generated summaries, preventing them from being merged with main proposed.
- Verification: py_compile passed; build_final_outputs.py completed; final_benchmark now contains baseline seeds 1/2, proposed seeds 0/1, and defensive_proposed seeds 26/27/28 as separate methods.

## 2026-06-30 curriculum seed1 monitor at ~768k
- Active P0 main-comparison training curriculum seed1; n_envs=10, 1.5M, horizon=1200, ent_coef=0.01.
- Checkpoints: checkpoint_375000_steps.zip and checkpoint_750000_steps.zip exist.
- Current log progress: ~768,000 timesteps, stage=1.
- Monitor windows: last100 success=0.350 cost=0.650 route=0.715; last500 success=0.318 cost=0.684 route=0.712; last1000 success=0.335 cost=0.669 route=0.724.
- Interpretation: curriculum-only is behaving as a weak comparator and has not progressed beyond stage1 by mid-run. Continue to full 1.5M and evaluate to preserve an unmodified main-protocol result; do not tune mid-run.

## 2026-06-30 curriculum seed1 monitor at ~870k
- Active P0 main-comparison training curriculum seed1; n_envs=10, 1.5M, horizon=1200, ent_coef=0.01.
- Current log progress: ~870,400 timesteps, stage=1.
- Recent rollout success_rate increased to 0.45, but curriculum window_cost remains ~0.60 and window_success ~0.40; last episodes show high-speed out-of-road despite high route completion.
- Interpretation: no evidence that curriculum-only is converging to the safer higher-stage behavior under current protocol. Continue to final evaluation for a clean comparator result.

## 2026-06-30 curriculum seed1 monitor at ~1.03M
- Active P0 main-comparison training curriculum seed1; n_envs=10, 1.5M, horizon=1200, ent_coef=0.01.
- Current log progress: ~1,034,240 timesteps; stage=2.
- Recent rollout success_rate fell to 0.22-0.26; curriculum window_success=0.167-0.233 and window_cost=0.767-0.833.
- Interpretation: curriculum-only can re-enter stage2 but remains high-cost/collision-prone. Continue to final 1.5M and evaluate; do not tune mid-run.

## 2026-06-30 curriculum seed1 monitor at ~1.28M
- Active P0 main-comparison training curriculum seed1; n_envs=10, 1.5M, horizon=1200, ent_coef=0.01.
- Current log progress: ~1,280,000 timesteps; stage=2.
- Recent rollout success_rate around 0.37-0.41; window_success around 0.267-0.367; window_cost around 0.60-0.733.
- Interpretation: late training still shows high collision/cost and no stable low-risk convergence. Continue to final model/evaluation for formal comparator evidence.

## 2026-06-30 curriculum seed1 completed
- Completed P0 main-comparison curriculum PPO seed1 under n_envs=10, timesteps=1.5M, horizon=1200, ent_coef=0.01.
- Evaluation CSV: outputs/iscsic_main_nenv10_1p5m_ent001/evaluations/curriculum_ppo_s1.csv; eval_n_envs=10, 50 episodes per density.
- Results: d0.00 success=0.02 cost=0.98 route=0.323; d0.08 success=0.00 cost=1.00 route=0.247 collision=0.40 out=0.60; d0.15 success=0.00 cost=1.00 route=0.225 collision=0.52 out=0.48.
- Decision: record as formal weak comparator. Next launch risk seed1 to fill the missing risk-reward comparator under the same n_envs=10 candidate protocol.

## 2026-06-30 launched P0 main risk seed1
- Launched risk PPO seed1 under current n_envs=10 candidate main protocol: timesteps=1,500,000, horizon=1200, ent_coef=0.01, device=cuda.
- Command: python scripts/train.py --variant risk --algo ppo --seed 1 --timesteps 1500000 --horizon 1200 --n-envs 10 --ent-coef 0.01 --device cuda --output-dir outputs/iscsic_main_nenv10_1p5m_ent001/runs; then evaluate_from_config with episodes=50, densities=0.00/0.08/0.15, n_envs=10.
- PID at launch: wrapper 119448, training 119460.

## 2026-06-30 risk seed1 early monitor at ~92k
- Active P0 main-comparison training risk seed1; n_envs=10, 1.5M, horizon=1200, ent_coef=0.01.
- Verified config: variant=risk, seed=1, timesteps=1500000, horizon=1200, n_envs=10, ent_coef=0.01, learning_rate=3e-4, use_risk_reward=True, use_action_guard=True.
- Current progress from log: ~92,160 timesteps.
- Monitor windows: last50 success=0.000 cost=0.260 route=0.054 speed=1.11; shield_intervention_rate around 0.005.
- Interpretation: early risk policy is extremely conservative/stationary with low route completion. Continue to at least ~300k before judging, because startup behavior is expected to be slow under risk reward+guard.

## 2026-06-30 risk seed1 monitor at ~297k
- Active P0 main-comparison training risk seed1; n_envs=10, 1.5M, horizon=1200, ent_coef=0.01.
- Current progress from log: ~296,960 timesteps.
- Recent episodes show transition from stationary conservative behavior to slow route progress: mean_speed_kmh reached 7.29 in the latest logged episode, route_completion=0.54, cost=0.
- Monitor interpretation: success remains 0, but route/speed are improving and safety cost is low. Continue through 750k checkpoint before judging final usefulness.

## 2026-06-30 risk seed1 monitor at ~604k
- Active P0 main-comparison training risk seed1; n_envs=10, 1.5M, horizon=1200, ent_coef=0.01.
- Current progress from log: ~604,160 timesteps.
- Recent logs: mean_speed_kmh 16-18.5, route_completion about 0.99 in several episodes, cost=0, success=1 in the latest successful rollouts; rollout success_rate rose to 0.42.
- Interpretation: risk seed1 recovered from early stationary conservatism and is now a useful low-cost comparator candidate. Continue to full 1.5M and final eval.

## 2026-06-30 risk seed1 monitor at ~973k
- Active P0 main-comparison training risk seed1; n_envs=10, 1.5M, horizon=1200, ent_coef=0.01.
- Current progress from log: ~972,800 timesteps.
- Recent logs show stable route completion around 0.99, mean_speed_kmh ~18-19, episode_cost=0, and rollout success_rate around 0.53-0.55.
- Interpretation: risk reward+guard seed1 has become a useful safe/slow comparator rather than a failed conservative run. Continue to full 1.5M and final eval.

## 2026-06-30 risk seed1 monitor at ~1.32M
- Active P0 main-comparison training risk seed1; n_envs=10, 1.5M, horizon=1200, ent_coef=0.01.
- Current progress from log: ~1,320,960 timesteps.
- Recent logs: rollout success_rate around 0.51-0.53, route_completion near 0.99 on successful episodes, mean_speed_kmh around 18-19, most recent episodes have cost=0 with occasional collision.
- Interpretation: performance has plateaued around moderate success/low-cost behavior. Continue to final model and 10-env evaluation.

## 2026-06-30 risk seed1 completed
- Completed P0 main-comparison risk PPO seed1 under n_envs=10, timesteps=1.5M, horizon=1200, ent_coef=0.01.
- Evaluation CSV: outputs/iscsic_main_nenv10_1p5m_ent001/evaluations/risk_ppo_s1.csv; eval_n_envs=10, 50 episodes per density.
- Results: d0.00 success=0.90 cost=0.00 route=0.983; d0.08 success=0.70 cost=0.14 route=0.911 collision=0.12 out=0.02; d0.15 success=0.40 cost=0.52 route=0.741 collision=0.50 out=0.02.
- Decision: launch risk seed2 under the same current candidate protocol to complete the risk comparator pair and estimate seed stability.

## 2026-06-30 launched P0 main risk seed2
- Launched risk PPO seed2 under current n_envs=10 candidate main protocol: timesteps=1,500,000, horizon=1200, ent_coef=0.01, device=cuda.
- Command: python scripts/train.py --variant risk --algo ppo --seed 2 --timesteps 1500000 --horizon 1200 --n-envs 10 --ent-coef 0.01 --device cuda --output-dir outputs/iscsic_main_nenv10_1p5m_ent001/runs; then evaluate_from_config with episodes=50, densities=0.00/0.08/0.15, n_envs=10.

## 2026-06-30 risk seed2 early monitor at ~123k
- Active P0 main-comparison training risk seed2; n_envs=10, 1.5M, horizon=1200, ent_coef=0.01.
- Verified config: variant=risk, seed=2, timesteps=1500000, horizon=1200, n_envs=10, ent_coef=0.01, learning_rate=3e-4, use_risk_reward=True, use_action_guard=True.
- Current progress from log: ~122,880 timesteps.
- Monitor windows: last50 success=0.000 cost=0.400 route=0.062 speed=1.33; last100 success=0.000 cost=0.290 route=0.055 speed=1.17.
- Interpretation: seed2 shows the same early low-speed conservative startup as seed1. Continue toward 300k/600k before making any tuning decision.

## 2026-06-30 risk seed2 monitor at ~492k
- Active P0 main-comparison training risk seed2; n_envs=10, 1.5M, horizon=1200, ent_coef=0.01.
- Current progress from log: ~491,520 timesteps.
- Recent logs show recovery from stationary startup: mean_speed_kmh around 12.7-15.5, route_completion up to 0.896, but rollout success_rate remains only 0.03-0.05.
- Monitor interpretation: seed2 is learning slower than risk seed1 at comparable mid-run stages. Continue to at least 750k/1.125M before judging; this may become useful seed-variance evidence.

## 2026-06-30 risk seed2 monitor at ~819k
- Active P0 main-comparison training risk seed2; n_envs=10, 1.5M, horizon=1200, ent_coef=0.01.
- Checkpoints include checkpoint_375000_steps.zip and checkpoint_750000_steps.zip.
- Current progress from log: ~819,200 timesteps.
- Recent logs: route_completion often 0.94-0.99, mean_speed_kmh 16-18, cost=0 in shown episodes; rollout success_rate peaked around 0.48 and recently sits around 0.39.
- Monitor interpretation: seed2 recovered from slow startup and is now a useful comparator, though somewhat less stable than seed1. Continue to full 1.5M and final evaluation.

## 2026-06-30 risk seed2 monitor at ~1.24M
- Active P0 main-comparison training risk seed2; n_envs=10, 1.5M, horizon=1200, ent_coef=0.01.
- Current progress from log: ~1,239,040 timesteps.
- Recent logs show rollout success_rate around 0.55-0.57, mean_speed_kmh around 18.5-19.3, route_completion close to 0.99 in successful episodes, with occasional out-of-road cost.
- Interpretation: seed2 recovered and is now broadly comparable to risk seed1 in late training. Continue to final model/evaluation.

## 2026-06-30 risk seed2 completed
- Completed P0 main-comparison risk PPO seed2 under n_envs=10, timesteps=1.5M, horizon=1200, ent_coef=0.01.
- Evaluation CSV: outputs/iscsic_main_nenv10_1p5m_ent001/evaluations/risk_ppo_s2.csv; eval_n_envs=10, 50 episodes per density.
- Results: d0.00 success=0.90 cost=0.00 route=0.985; d0.08 success=0.74 cost=0.14 route=0.936 collision=0.14 out=0.00; d0.15 success=0.46 cost=0.52 route=0.808 collision=0.52 out=0.00.
- Two-seed risk comparator is stable: seed1 d0.15 success=0.40/cost=0.52, seed2 d0.15 success=0.46/cost=0.52. Next: launch proposed seed2 under the same current protocol to complete proposed seeds 0/1/2.

## 2026-06-30 launched P0 main proposed seed2
- Launched proposed PPO seed2 under current n_envs=10 candidate main protocol: timesteps=1,500,000, horizon=1200, ent_coef=0.01, device=cuda.
- Command: python scripts/train.py --variant proposed --algo ppo --seed 2 --timesteps 1500000 --horizon 1200 --n-envs 10 --ent-coef 0.01 --device cuda --output-dir outputs/iscsic_main_nenv10_1p5m_ent001/runs; then evaluate_from_config with episodes=50, densities=0.00/0.08/0.15, n_envs=10.

## 2026-06-30 proposed seed2 early monitor at ~246k
- Active P0 main-comparison training proposed seed2; n_envs=10, 1.5M, horizon=1200, ent_coef=0.01.
- Verified config: variant=proposed, seed=2, timesteps=1500000, horizon=1200, n_envs=10, ent_coef=0.01, learning_rate=3e-4, use_risk_reward=True, use_action_guard=True, stage2_success=0.25, stage2_cost=0.45.
- Current progress from log: ~245,760 timesteps; curriculum stage oscillates between 0 and 1.
- Monitor windows: last50 success=0.500 cost=0.100 route=0.780 speed=10.19 stage_mean=0.64; last100 success=0.300 cost=0.110 route=0.632.
- Interpretation: seed2 has a healthy early curriculum startup, better than risk-only early behavior. Continue to checkpoint_375k and mid-run monitoring.

## 2026-06-30 proposed seed2 monitor at ~604k
- Active P0 main-comparison training proposed seed2; n_envs=10, 1.5M, horizon=1200, ent_coef=0.01.
- Checkpoint_375000_steps.zip exists.
- Current progress from log: ~604,160 timesteps; stage=3 in recent logs.
- Recent logs: rollout success_rate around 0.27-0.30, window_success around 0.10-0.133, window_cost around 0.233-0.267, route around 0.64-0.69 at stage3.
- Monitor interpretation: seed2 reached hard/prehard stages early and remains relatively safe, but success/route are weak at this stage. Continue to 1.125M and final eval before judging.

## 2026-06-30 reward-function diagnosis note
- User asked whether current low/high-density success may be due to reward-function design and whether reward was optimized.
- Current answer from code/history: reward structure was made reproducible and split from action guard; curriculum stages/gates, entropy, TTC threshold and target speed were tuned. The main RewardWeights were not yet systematically optimized for the current 10-env 1.5M protocol.
- Current RewardWeights: base_scale=0.5, ttc=2.0, lane=0.5, smooth=0.02, accel=0.01, cost=20.0, overspeed=2.0, target_speed_kmh=20.0, progress=30.0, idle_penalty=0.15, success_bonus=40.0, crash/out_of_road_penalty=80.0, ttc_threshold=5.0.
- Hypothesis: hard-stage low success may be caused by reward imbalance: progress/success incentives may be too weak relative to risk/guard/overspeed shaping, producing safe but incomplete trajectories; alternatively TTC/guard may still not suppress high-density collisions enough.
- Action policy: do not alter the active proposed seed2 main-protocol run midstream. After it completes, prioritize reward/guard ablations and one or two short reward-weight screens before expanding more seeds.

## 2026-06-30 proposed seed2 monitor at ~1.00M and reward hypothesis update
- Active P0 main-comparison training proposed seed2; n_envs=10, 1.5M, horizon=1200, ent_coef=0.01.
- Current progress from log: ~1,003,520 timesteps; recent stage=4/hard.
- Monitor windows: last50 success=0.240 cost=0.380 route=0.728 speed=18.02 stage_mean=3.76; last200 success=0.180 cost=0.330 route=0.730.
- Interpretation: hard-stage low completion persists despite nonzero route progress and moderate speed. This strengthens the user-raised reward-function hypothesis: current reward/guard balance may overemphasize safety/intervention or underreward full completion in hard density.
- Action: finish this formal run unchanged, then prioritize no_action_guard/proposed_wo_ttc and a short reward-weight screen rather than immediately adding more seeds under the same reward.

## 2026-06-30 train.py reward-weight CLI support
- Added explicit reward-weight CLI options to scripts/train.py for traceable reward screens: base_scale, ttc, lane, smooth, accel, cost, overspeed, target_speed, progress, idle_penalty, min_speed, success_bonus, crash_penalty, out_of_road_penalty, and ttc_threshold.
- Reason: user asked whether reward function is the problem; reward screens must store changed weights in config.json rather than relying on temporary source edits.
- Verification: python -m py_compile scripts/train.py passed; train.py --help shows reward-progress, reward-success-bonus, reward-cost, reward-ttc-threshold and reward-target-speed.
- Active proposed seed2 run was already launched before this change and remains unaffected.

## 2026-06-30 reward tuning documentation initialized
- Created codex_longrun_iscsic/REWARD_TUNING_PLAN.md with current RewardWeights, observations, tuning principles and first screen candidates R1/R2/R3/R4.
- Created codex_longrun_iscsic/REWARD_TUNING_LEDGER.md for structured reward-screen records.
- Active formal proposed seed2 continues unchanged; reward screens will start only after it completes/evaluates.

## 2026-06-30 proposed seed2 monitor at ~1.22M
- Active P0 main-comparison training proposed seed2; n_envs=10, timesteps=1.5M, horizon=1200, ent_coef=0.01.
- Current progress from log: ~1,218,560 timesteps.
- Recent logs show instability after hard-stage exposure: rollout success_rate around 0.08-0.14, window_success as low as 0.033, window_cost up to 0.667, route_completion dropping in some episodes, and curriculum demotion from stage3 to stage2.
- Resource status is healthy: RTX 4070 SUPER memory around 1.1GB used, system memory available around 22GiB.
- Interpretation: this continues to support the reward/curriculum-balance hypothesis. Finish the formal run unchanged, then start traceable reward screens with n_envs=10 and ledger records.

## 2026-06-30 proposed seed2 completed and evaluated
- Completed P0 main-comparison proposed PPO seed2 under n_envs=10, timesteps=1.5M, horizon=1200, ent_coef=0.01.
- Evaluation CSV: outputs/iscsic_main_nenv10_1p5m_ent001/evaluations/proposed_ppo_s2.csv; eval_n_envs=10, 50 episodes per density.
- Results: d0.00 success=0.76 cost=0.00 route=0.967; d0.08 success=0.70 cost=0.14 route=0.927 collision=0.14 out=0.00; d0.15 success=0.54 cost=0.40 route=0.755 collision=0.40 out=0.00.
- Proposed seed comparison: seed0 d0.15 success=0.60/cost=0.34, seed1 d0.15 success=0.32/cost=0.62, seed2 d0.15 success=0.54/cost=0.40. There is meaningful high-density seed variance.
- Risk comparator remains more stable but lower: risk seed1/2 d0.15 success=0.40/0.46, cost=0.52/0.52.
- Decision: start R1 reward screen (completion_boost) before adding more full 1.5M seeds, because current failure mode is high-density completion/collision balance rather than missing evidence only.

## 2026-06-30 launched R1 reward screen completion_boost
- Launched R1 reward screen after proposed seed2 formal evaluation completed.
- Command: proposed PPO seed2, timesteps=500,000, horizon=1200, n_envs=10, ent_coef=0.01, reward_progress=45, reward_success_bonus=80, device=cuda.
- Output root: outputs/reward_screen_completion_boost_nenv10_500k
- Wrapper: /tmp/run_reward_completion_boost_s2_nenv10_500k.sh
- Evaluation target after training: 50 episodes per density at 0.00/0.08/0.15 with eval_n_envs=10.
- Decision rule: compare against current proposed seed2 and seed0/1; expand only if d0.15 success improves without unacceptable cost/collision inflation.

## 2026-06-30 R1 completion_boost monitor at ~348k
- Active reward screen R1: proposed seed2, 500k, n_envs=10, reward_progress=45, reward_success_bonus=80.
- Current progress from log: ~348,160 timesteps.
- Early/mid signal: stage2 reached; window_success up to 0.333, window_cost around 0.033 in recent stage2 log, rollout success_rate recently around 0.33-0.43.
- Interpretation: completion_boost does not immediately destabilize early safety and may improve completion pressure, but final density evaluation is required before any expansion decision.

## 2026-06-30 R1 completion_boost completed and evaluated
- R1 reward screen completed: proposed seed2, 500k, n_envs=10, reward_progress=45, reward_success_bonus=80.
- Evaluation CSV: outputs/reward_screen_completion_boost_nenv10_500k/evaluations/proposed_ppo_s2.csv; eval_n_envs=10, 50 episodes per density.
- Results: d0.00 success=0.90 cost=0.00 route=0.983; d0.08 success=0.90 cost=0.02 route=0.968 collision=0.02 out=0.00; d0.15 success=0.32 cost=0.52 route=0.761 collision=0.52 out=0.00.
- Interpretation: completion_boost improves low/medium density, especially d0.08, but degrades high-density safety/success relative to proposed seed2 d0.15 success=0.54/cost=0.40. Do not expand R1 directly.
- Decision: launch R3 completion_plus_safety: keep reward_progress=45 and reward_success_bonus=80, increase crash_penalty/out_of_road_penalty 80 -> 120 to test whether high-density collision can be reduced without losing the completion improvement.

## 2026-06-30 launched R3 reward screen completion_plus_safety
- Launched R3 reward screen: proposed seed2, timesteps=500,000, horizon=1200, n_envs=10, ent_coef=0.01.
- Reward changes: progress=45, success_bonus=80, crash_penalty=120, out_of_road_penalty=120; other RewardWeights unchanged.
- Output root: outputs/reward_screen_completion_plus_safety_nenv10_500k
- Wrapper: /tmp/run_reward_completion_plus_safety_s2_nenv10_500k.sh
- Evaluation target after training: 50 episodes per density at 0.00/0.08/0.15 with eval_n_envs=10.

## 2026-06-30 R3 completion_plus_safety monitor at ~379k
- Active R3 reward screen: proposed seed2, 500k, n_envs=10, reward_progress=45, reward_success_bonus=80, crash/out penalties=120.
- Current progress from log: ~378,880 timesteps.
- Mid-run signal is weaker than R1: stage oscillates around 0/1, recent rollout success_rate around 0.10-0.16, mean_speed around 5.6-7.2 km/h in shown episodes, and route_completion often below 0.5.
- Interpretation: stronger crash/out penalty may be over-conservative or may delay learning. Since the run is close to completion, continue to final evaluation rather than terminating on partial logs.

## 2026-06-30 R3 completion_plus_safety completed and evaluated
- R3 reward screen completed: proposed seed2, 500k, n_envs=10, reward_progress=45, reward_success_bonus=80, crash/out penalties=120.
- Evaluation CSV: outputs/reward_screen_completion_plus_safety_nenv10_500k/evaluations/proposed_ppo_s2.csv; eval_n_envs=10, 50 episodes per density.
- Results: d0.00 success=0.80 cost=0.00 route=0.974; d0.08 success=0.76 cost=0.12 route=0.948 collision=0.12 out=0.00; d0.15 success=0.50 cost=0.50 route=0.779 collision=0.50 out=0.00.
- Interpretation: R3 partially recovers high-density success versus R1, but remains worse than the formal proposed seed2 d0.15 success=0.54/cost=0.40 and loses R1 medium-density gain. Do not expand R3.
- Decision: launch R2 safety_soften to test the opposite reward hypothesis: cost/overspeed penalties may be too strong and may interfere with completion; reduce reward_cost 20 -> 15 and overspeed 2 -> 1 while leaving completion terms at baseline.

## 2026-06-30 launched R2 reward screen safety_soften
- Launched R2 reward screen: proposed seed2, timesteps=500,000, horizon=1200, n_envs=10, ent_coef=0.01.
- Reward changes: cost=15, overspeed=1.0; other RewardWeights unchanged from baseline.
- Output root: outputs/reward_screen_safety_soften_nenv10_500k
- Wrapper: /tmp/run_reward_safety_soften_s2_nenv10_500k.sh
- Evaluation target after training: 50 episodes per density at 0.00/0.08/0.15 with eval_n_envs=10.

## 2026-06-30 R2 safety_soften monitor at ~317k
- Active R2 reward screen: proposed seed2, 500k, n_envs=10, reward_cost=15, reward_overspeed=1.0.
- Current progress from log: ~317,440 timesteps.
- Mid-run signal: stage2 reached, recent window_success around 0.133-0.333, window_cost around 0.10, speed around 12-13 km/h in shown episodes, and no obvious early collision explosion in sampled log tail.
- Interpretation: R2 is a plausible screen to finish; it tests whether reducing safety/overspeed shaping improves completion without unacceptable cost.

## 2026-06-30 R2 safety_soften completed and evaluated
- R2 reward screen completed: proposed seed2, 500k, n_envs=10, reward_cost=15, reward_overspeed=1.0.
- Evaluation CSV: outputs/reward_screen_safety_soften_nenv10_500k/evaluations/proposed_ppo_s2.csv; eval_n_envs=10, 50 episodes per density.
- Results: d0.00 success=0.78 cost=0.00 route=0.972; d0.08 success=0.74 cost=0.06 route=0.936 collision=0.06 out=0.00; d0.15 success=0.44 cost=0.48 route=0.747 collision=0.46 out=0.02.
- Interpretation: reducing cost/overspeed does not solve high-density completion/safety and is worse than formal proposed seed2. Do not expand R2.
- Reward-screen summary so far: R1 improves medium density but fails high density; R3 partially fixes R1 high-density but remains worse than formal proposed; R2 is not better. Next: mechanism ablation, especially action guard/TTC interaction, because reward-only changes did not dominate.

## 2026-06-30 launched R4 mechanism screen no_action_guard
- Launched R4/no_action_guard mechanism screen: variant=no_action_guard, seed2, timesteps=500,000, horizon=1200, n_envs=10, ent_coef=0.01.
- Purpose: isolate whether action guard is helping/hurting the current proposed behavior, after R1/R2/R3 reward-only screens failed to improve high-density performance.
- Output root: outputs/ablation_no_action_guard_nenv10_500k
- Wrapper: /tmp/run_ablation_no_action_guard_s2_nenv10_500k.sh
- Evaluation target after training: 50 episodes per density at 0.00/0.08/0.15 with eval_n_envs=10.

## 2026-06-30 R4 no_action_guard monitor at ~338k
- Active R4 mechanism screen: no_action_guard seed2, 500k, n_envs=10, use_risk_reward=True, use_action_guard=False, curriculum=True.
- Current progress from log: ~337,920 timesteps.
- Mid-run signal: stage2 reached; rollout success_rate around 0.30-0.39; window_success up to 0.333; window_cost around 0.233-0.333 in recent logs; out-of-road appeared in sampled tail.
- Interpretation: removing action guard may increase completion freedom, but safety/cost risk rises. Final density evaluation needed to quantify the tradeoff.

## 2026-06-30 R4 no_action_guard completed and evaluated
- R4 mechanism screen completed: variant=no_action_guard, seed2, 500k, n_envs=10, use_risk_reward=True, use_action_guard=False, curriculum=True.
- Evaluation CSV: outputs/ablation_no_action_guard_nenv10_500k/evaluations/no_action_guard_ppo_s2.csv; eval_n_envs=10, 50 episodes per density.
- Results: d0.00 success=0.02 cost=0.98 route=0.297 out=0.98; d0.08 success=0.00 cost=1.00 route=0.247 collision=0.38 out=0.62; d0.15 success=0.00 cost=1.00 route=0.181 collision=0.48 out=0.52.
- Interpretation: removing action guard collapses safety and completion, even at d0.00. This strongly supports action guard as a necessary stabilizing/safety mechanism rather than the main cause of high-density completion limitation.
- Decision: do not remove action guard. Next mechanism screen: proposed_wo_ttc to isolate TTC reward contribution while keeping action guard/curriculum structure.

## 2026-06-30 launched mechanism screen proposed_wo_ttc
- Launched proposed_wo_ttc mechanism screen: seed2, timesteps=500,000, horizon=1200, n_envs=10, ent_coef=0.01.
- Purpose: isolate TTC reward contribution after reward-only screens failed and no_action_guard collapsed.
- Output root: outputs/ablation_proposed_wo_ttc_nenv10_500k
- Wrapper: /tmp/run_ablation_proposed_wo_ttc_s2_nenv10_500k.sh
- Evaluation target after training: 50 episodes per density at 0.00/0.08/0.15 with eval_n_envs=10.

## 2026-06-30 proposed_wo_ttc monitor at ~348k
- Active mechanism screen: proposed_wo_ttc seed2, 500k, n_envs=10, reward_ttc=0.0, use_action_guard=True, curriculum=True.
- Current progress from log: ~348,160 timesteps.
- Mid-run signal: recent rollout success_rate around 0.35-0.38; window_success peaked at 0.633 but later sits around 0.133-0.167; stage around 1; out-of-road appears in sampled tail.
- Interpretation: removing TTC reward does not immediately collapse learning, but may weaken safety boundary and curriculum progression. Continue to final evaluation.

## 2026-06-30 proposed_wo_ttc completed and evaluated
- Mechanism screen completed: variant=proposed_wo_ttc, seed2, 500k, n_envs=10, reward_ttc=0.0, use_action_guard=True, curriculum=True.
- Evaluation CSV: outputs/ablation_proposed_wo_ttc_nenv10_500k/evaluations/proposed_wo_ttc_ppo_s2.csv; eval_n_envs=10, 50 episodes per density.
- Results: d0.00 success=0.88 cost=0.00 route=0.982; d0.08 success=0.68 cost=0.18 route=0.903 collision=0.16 out=0.02; d0.15 success=0.34 cost=0.60 route=0.727 collision=0.52 out=0.08.
- Interpretation: removing TTC reward worsens medium/high-density safety and high-density success relative to formal proposed seed2. TTC reward is useful and should remain enabled.
- Current tuning conclusion: action guard and TTC reward are both necessary; reward-only screens with large completion/safety changes did not beat formal proposed. Next reward direction should be gentler, not extreme: moderate completion boost while keeping TTC/action guard and baseline cost penalties.

## 2026-06-30 reward/mechanism screen summary generated
- Generated codex_longrun_iscsic/reward_mechanism_screen_summary.csv and .md.
- Used remote scientific-brainstorming skill logic for failure analysis after R1/R2/R3/R4/TTC screens.
- Current conclusion: keep action guard and TTC reward; avoid extreme reward changes; next screen is R5 moderate_completion with progress=40, success_bonus=60.

## 2026-06-30 reward/mechanism screen summary generated
- Generated codex_longrun_iscsic/reward_mechanism_screen_summary.csv and .md.
- Used remote scientific-brainstorming skill logic for failure analysis after R1/R2/R3/R4/TTC screens.
- Current conclusion: keep action guard and TTC reward; avoid extreme reward changes; next screen is R5 moderate_completion with progress=40, success_bonus=60.

## 2026-06-30 launched R5 reward screen moderate_completion
- Launched R5 reward screen: proposed seed2, timesteps=500,000, horizon=1200, n_envs=10, ent_coef=0.01.
- Reward changes: progress=40, success_bonus=60; TTC reward/action guard/cost/crash/out penalties remain baseline.
- Rationale: R1 progress=45/success=80 improved medium density but over-hurt high-density; R5 tests a gentler completion boost.
- Output root: outputs/reward_screen_moderate_completion_nenv10_500k
- Wrapper: /tmp/run_reward_moderate_completion_s2_nenv10_500k.sh
- Evaluation target after training: 50 episodes per density at 0.00/0.08/0.15 with eval_n_envs=10.

## 2026-06-30 R5 moderate_completion monitor at ~348k
- Active R5 reward screen: proposed seed2, 500k, n_envs=10, reward_progress=40, reward_success_bonus=60.
- Current progress from log: ~348,160 timesteps.
- Mid-run signal is promising: stage2 reached; recent window_cost=0.0; window_success around 0.467-0.667; rollout success_rate peaked around 0.54; sampled episodes show no obvious collision/out-of-road spike.
- Interpretation: gentler completion boost may be better balanced than R1/R3. Continue to final evaluation before expansion decision.

## 2026-06-30 R5 moderate_completion completed and evaluated
- R5 reward screen completed: proposed seed2, 500k, n_envs=10, reward_progress=40, reward_success_bonus=60.
- Evaluation CSV: outputs/reward_screen_moderate_completion_nenv10_500k/evaluations/proposed_ppo_s2.csv; eval_n_envs=10, 50 episodes per density.
- Results: d0.00 success=0.90 cost=0.00 route=0.983; d0.08 success=0.74 cost=0.06 route=0.948 collision=0.06 out=0.00; d0.15 success=0.44 cost=0.50 route=0.751 collision=0.50 out=0.00.
- Interpretation: R5 had promising mid-run windows but final evaluation does not beat formal proposed seed2. Moderate completion boost alone is not sufficient.
- Reward tuning conclusion: keep baseline reward/guard/TTC for formal results for now; use R1 as diagnostic evidence that completion incentives can improve medium density, but do not promote any reward screen to final candidate yet.

## 2026-06-30 launched P0 main curriculum seed2
- Launched curriculum PPO seed2 under current n_envs=10 candidate main protocol: timesteps=1,500,000, horizon=1200, ent_coef=0.01, device=cuda.
- Purpose: complete curriculum comparator seed pair under the formal 10-env protocol. Reward screens did not improve high-density over formal proposed, so return to missing P0 evidence.
- Command: python scripts/train.py --variant curriculum --algo ppo --seed 2 --timesteps 1500000 --horizon 1200 --n-envs 10 --ent-coef 0.01 --device cuda --output-dir outputs/iscsic_main_nenv10_1p5m_ent001/runs; then evaluate_from_config with episodes=50, densities=0.00/0.08/0.15, n_envs=10.
- Wrapper: /tmp/run_main_curriculum_s2_nenv10_1p5m_ent001.sh

## 2026-06-30 curriculum seed2 early monitor at ~164k
- Active P0 main-comparison training curriculum seed2; n_envs=10, 1.5M, horizon=1200, ent_coef=0.01.
- Verified config: variant=curriculum, seed=2, timesteps=1500000, horizon=1200, n_envs=10, ent_coef=0.01, use_risk_reward=False, use_action_guard=False, curriculum=True.
- Current progress from log: ~163,840 timesteps.
- Early signal: reached stage2; window_success peaked around 0.567 at stage1 and 0.433 at stage2; route_completion in sampled successful/near-success windows is moderate/high, but some out-of-road costs already appear.
- Interpretation: early learning is healthy for a curriculum-only comparator. Continue; this run is required evidence for comparator seed stability, not a replacement for proposed.

## 2026-06-30 curriculum seed2 monitor at ~369k
- Active P0 main-comparison training curriculum seed2; n_envs=10, 1.5M, horizon=1200, ent_coef=0.01.
- Current progress from log: ~368,640 timesteps.
- Mid-run signal: still at stage2; window_success around 0.19-0.27, but window_cost is very high around 0.733-0.800. Sampled episodes show frequent vehicle collisions, mean_speed_kmh around 28-30, and no risk reward/action guard.
- Interpretation: curriculum-only learns speed/progress but has poor safety, which is useful comparator evidence. Continue to final evaluation; do not stop early because the run is needed for formal comparison and seed stability.

## 2026-06-30 curriculum seed2 monitor at ~614k
- Active P0 main-comparison training curriculum seed2; n_envs=10, 1.5M, horizon=1200, ent_coef=0.01.
- Current progress from log: ~614,400 timesteps.
- Signal: still stage2; window_cost remains very high around 0.70-0.83, window_success around 0.167-0.30, mean_speed_kmh often 25-34, with frequent collision/out-of-road examples.
- Interpretation: curriculum-only comparator is learning fast/high-speed trajectories but has poor safety. Continue to full training/evaluation for formal evidence, but do not use it as a candidate safe policy.

## 2026-06-30 curriculum seed2 monitor at ~840k
- Active P0 main-comparison training curriculum seed2; n_envs=10, 1.5M, horizon=1200, ent_coef=0.01.
- Current progress from log: ~839,680 timesteps.
- Signal: reached stage4/hard; rollout success_rate around 0.20-0.21; window_cost around 0.433-0.600 in recent logs; route_completion often 0.80-0.90 but success remains low under hard horizon/density.
- Interpretation: curriculum-only can progress through stages and maintain route progress, but lacks safety/risk control. Continue to final evaluation for formal comparator evidence.

## 2026-06-30 curriculum seed2 monitor at ~1.14M
- Active P0 main-comparison training curriculum seed2; n_envs=10, 1.5M, horizon=1200, ent_coef=0.01.
- Current progress from log: ~1,136,640 timesteps.
- Signal: curriculum remains around stage2; rollout success_rate around 0.17-0.26, window_cost remains high at 0.60-0.77, and mean_speed_kmh often near 28-31 in successful samples.
- Interpretation: no evidence that curriculum-only safety is converging; it continues to serve as an unsafe/high-speed comparator. Continue to final evaluation.

## 2026-06-30 curriculum seed2 monitor at ~1.36M
- Active P0 main-comparison training curriculum seed2; n_envs=10, 1.5M, horizon=1200, ent_coef=0.01.
- Current progress from log: ~1,361,920 timesteps.
- Signal: hard stage instability is clear: window_cost around 0.70-0.80, window_success around 0.067-0.10 in recent hard-stage logs, with repeated vehicle collisions and high speeds.
- Interpretation: curriculum-only fails the safety objective under hard density. Finish unchanged for final benchmark evidence.

## 2026-06-30 curriculum seed2 completed and evaluated
- Completed P0 main-comparison curriculum PPO seed2 under n_envs=10, timesteps=1.5M, horizon=1200, ent_coef=0.01.
- Evaluation CSV: outputs/iscsic_main_nenv10_1p5m_ent001/evaluations/curriculum_ppo_s2.csv; eval_n_envs=10, 50 episodes per density.
- Results: d0.00 success=0.02 cost=0.98 route=0.399 out=0.98; d0.08 success=0.00 cost=1.00 route=0.252 collision=0.48 out=0.52; d0.15 success=0.02 cost=0.98 route=0.250 collision=0.62 out=0.36.
- Interpretation: curriculum-only seed2 confirms seed1 failure pattern. Curriculum alone is not safe and has very poor evaluation success despite high-speed/high-progress training samples.
- Current P0 evidence: baseline seeds 1/2 and curriculum seeds 1/2 are weak; risk seeds 1/2 are stable safe comparators; proposed seeds 0/1/2 improve over risk on mean high-density success but show seed variance.
- Next: run formal 1.5M proposed_wo_ttc ablation under n_envs=10 to strengthen the claim that TTC reward contributes beyond action guard/curriculum.

## 2026-06-30 launched formal ablation proposed_wo_ttc seed2
- Launched formal proposed_wo_ttc PPO seed2 under current n_envs=10 candidate main protocol: timesteps=1,500,000, horizon=1200, ent_coef=0.01, device=cuda.
- Purpose: strengthen ablation evidence for TTC reward contribution at the same full horizon/step budget as the main comparison.
- Command: python scripts/train.py --variant proposed_wo_ttc --algo ppo --seed 2 --timesteps 1500000 --horizon 1200 --n-envs 10 --ent-coef 0.01 --device cuda --output-dir outputs/iscsic_main_nenv10_1p5m_ent001/runs; then evaluate_from_config with episodes=50, densities=0.00/0.08/0.15, n_envs=10.
- Wrapper: /tmp/run_main_proposed_wo_ttc_s2_nenv10_1p5m_ent001.sh

## 2026-06-30 proposed_wo_ttc seed2 early monitor at ~287k
- Active formal ablation training proposed_wo_ttc seed2; n_envs=10, 1.5M, horizon=1200, ent_coef=0.01.
- Verified config earlier: reward_ttc=0.0, use_action_guard=True, use_risk_reward=True, curriculum=True.
- Current progress from log: ~286,720 timesteps.
- Early signal: still around stage0/1; rollout success_rate only around 0.07 in the sampled tail; route_completion is improving but no strong early success burst.
- Interpretation: early learning is weaker than formal proposed seed2 and consistent with the 500k TTC ablation trend. Continue to full evaluation for formal ablation evidence.

## 2026-06-30 proposed_wo_ttc seed2 monitor at ~614k
- Active formal ablation training proposed_wo_ttc seed2; n_envs=10, 1.5M, horizon=1200, ent_coef=0.01.
- Current progress from log: ~614,400 timesteps.
- Signal: reached stage3; rollout success_rate remains low around 0.07-0.18 in recent logs; window_cost around 0.20-0.33, route_completion window around 0.69-0.78.
- Interpretation: the policy is learning route progress but remains weaker than formal proposed seed2 at comparable stage. Continue to full evaluation for TTC reward ablation evidence.

## 2026-06-30 proposed_wo_ttc seed2 monitor at ~932k
- Active formal ablation training proposed_wo_ttc seed2; n_envs=10, 1.5M, horizon=1200, ent_coef=0.01.
- Current progress from log: ~931,840 timesteps.
- Signal: stage3; window_cost around 0.20-0.30, route_completion window around 0.70-0.75, but rollout success_rate remains low around 0.05-0.10.
- Interpretation: without TTC reward the policy can make route progress, but completion stability is weak. Continue to full evaluation.

## 2026-06-30 proposed_wo_ttc seed2 monitor at ~1.23M
- Active formal ablation training proposed_wo_ttc seed2; n_envs=10, 1.5M, horizon=1200, ent_coef=0.01.
- Current progress from log: ~1,228,800 timesteps.
- Signal: still stage3; rollout success_rate around 0.14-0.16; window_cost around 0.23-0.27; route window around 0.71-0.74, with occasional high route_completion episodes but low success stability.
- Interpretation: this ablation supports the hypothesis that TTC reward helps completion/safety stability beyond action guard. Continue to final CSV.


## 2026-06-30 launched nenv8 defensive ttc12/v18 seed26
- Time: 2026-06-30T14:00:53+08:00
- Protocol: scripts/run_one_defensive_proposed.py --seed 26 --n-envs 8 --timesteps 1000000 --root outputs/defensive_ttc12_v18_nenv8_final --ttc-threshold 12.0 --target-speed 18.0 --device cuda.
- Purpose: first 8-env migration check for the strongest current self-method branch; compare with existing nenv10 seed26 result before scaling to seed27/28 or changing parameters.
- Log: outputs/defensive_ttc12_v18_nenv8_final/logs/defensive_s26_nenv8_20260630_140018.log
- PID: 7802; PGID: 7795.
- Initial health: process and 8 VecEnv workers are running; early log shows n_envs=8 and fps around 2500-2700.

## 2026-06-30 nenv8 defensive seed26 monitor at ~319k
- Time: 2026-06-30T14:03:04+08:00
- Checkpoint: checkpoint_250000_steps.zip exists.
- Health: process still running with 8 workers; GPU memory about 922 MiB, fps about 2220-2245.
- Training signal: reached stage1 by ~311k; latest success_rate about 0.07, route_completion sample up to 0.865, std about 0.68, no collision/out-of-road in sampled tail.
- Decision: continue; not an idle-collapse run. Recheck around 500k.

## 2026-06-30 nenv8 defensive seed26 monitor at ~459k
- Time: 2026-06-30T14:05:05+08:00
- Health: process still running with 8 workers; GPU memory about 922 MiB, fps recently 1729-1915.
- Training signal: reached stage2; success_rate peaked around 0.44 near 401k and later fluctuated around 0.16-0.26; route_completion has high samples around 0.96-0.98.
- Risk signal: one sampled out_of_road at ~442k and window_cost rose to about 0.30, so the run is learning but unstable.
- Decision: continue to 500k/750k; no intervention yet because this is not idle collapse and still has route/success learning.

## 2026-06-30 nenv8 defensive seed26 monitor at ~614k
- Time: 2026-06-30T14:07:45+08:00
- Checkpoint: checkpoint_500000_steps.zip exists.
- Health: process still running with 8 workers; GPU memory about 922 MiB; fps recently about 1466-1555.
- Training signal: stage2, success_rate about 0.27, window_success around 0.20-0.37, window_route_completion around 0.80-0.85.
- Risk signal: one sampled collision near ~598k, but window_cost stayed low around 0.07-0.10 afterward.
- Decision: continue to final; do not interrupt because there is meaningful learning and no collapse.

## 2026-06-30 nenv8 defensive seed26 monitor at ~786k
- Time: 2026-06-30T14:12:58+08:00
- Checkpoint: checkpoint_750000_steps.zip exists.
- Health: process still running with 8 workers; GPU memory about 896 MiB; fps recently about 1285-1367.
- Training signal: still stage2; success_rate roughly 0.14-0.19 in latest tail, window_success about 0.10-0.27, route_completion has high samples near 0.99 but instability remains.
- Risk signal: recent sampled collision/out_of_road events exist; std down to about 0.44 but not a full idle collapse.
- Decision: let seed26 finish and judge by final 3-density evaluation, because the earlier nenv10 defensive protocol also had imperfect training-stage logs but strong held-out eval.


## 2026-06-30 launched nenv8 defensive ttc12/v18 seed27
- Time: 2026-06-30T14:21:39+08:00
- Protocol: scripts/run_one_defensive_proposed.py --seed 27 --n-envs 8 --timesteps 1000000 --root outputs/defensive_ttc12_v18_nenv8_final --ttc-threshold 12.0 --target-speed 18.0 --device cuda.
- Rationale: seed26 nenv8 is usable (d0.15 success=0.60/cost=0.24) but d0.08 dropped versus nenv10; seed27 tests whether that is seed/noise or protocol degradation before tuning.
- Log: outputs/defensive_ttc12_v18_nenv8_final/logs/defensive_s27_nenv8_20260630_142139.log
- Launcher PID: 10678; main PID: 10685; PGID: 10678.


## 2026-06-30 protocol change to nenv16
- Time: 2026-06-30T14:24:15+08:00
- User requirement: switch experiments to n_envs=16; keep at least 4GB CPU memory and 2GB GPU memory free.
- Action: stopped the in-progress seed27 nenv8 run and archived partial artifacts under outputs/interrupted_nenv8_protocol_change_to_nenv16_20260630_142415.
- Stopped PGID: 10678.
- Note: completed nenv8 seed26 remains diagnostic only; new formal runs use nenv16 directories and TARGET_N_ENVS=16 summaries.


## 2026-06-30 launched nenv16 defensive ttc12/v18 seed26
- Time: 2026-06-30T14:25:31+08:00
- Protocol: scripts/run_one_defensive_proposed.py --seed 26 --n-envs 16 --timesteps 1000000 --root outputs/defensive_ttc12_v18_nenv16_final --ttc-threshold 12.0 --target-speed 18.0 --device cuda.
- Safety requirement: keep at least 4GB available CPU memory and 2GB free GPU memory.
- Rationale: first nenv16 migration check on strongest current self-method branch; compare with nenv8/nenv10 seed26 before expanding seeds.
- Log: outputs/defensive_ttc12_v18_nenv16_final/logs/defensive_s26_nenv16_20260630_142531.log
- Launcher PID: 11385; main PID: 11392; PGID: 11385.

## 2026-06-30 nenv16 defensive seed26 monitor at ~393k
- Time: 2026-06-30T14:29:12+08:00
- Safety: CPU available about 24GiB; GPU free about 10.9GiB, above the required 4GB CPU / 2GB GPU headroom.
- Checkpoint: checkpoint_250000_steps.zip exists.
- Training signal: reached stage2 by ~311k; success_rate peaked around 0.41 near 295k and is about 0.19 at 393k; window_success about 0.30, window_cost about 0.067, route_completion samples near 0.98.
- Decision: continue. nenv16 is currently safe and learning faster than the interrupted nenv8 seed27 and comparable/better than nenv8 seed26 early curve.

## 2026-06-30 nenv16 defensive seed26 monitor at ~524k
- Time: 2026-06-30T14:31:18+08:00
- Safety: CPU available about 23GiB; GPU free about 10.9GiB, above the required 4GB CPU / 2GB GPU headroom.
- Checkpoint: checkpoint_500000_steps.zip exists.
- Training signal: still stage2; route window about 0.75, latest cost window 0, std about 0.63. Success rate dropped from the earlier 0.35-0.41 peak to about 0.06-0.10.
- Decision: continue to 750k/final. Not an idle collapse because route progress remains high, cost is controlled, and exploration std has not collapsed.

## 2026-06-30 nenv16 defensive seed26 monitor at ~721k
- Time: 2026-06-30T14:34:03+08:00
- Safety: CPU available about 23GiB; GPU free about 10.9GiB, above the required 4GB CPU / 2GB GPU headroom.
- Training signal: still stage2; after a mid-run dip, latest success_rate recovered to about 0.19-0.20, window_success about 0.20-0.23, window_cost about 0.10-0.17, route window about 0.75-0.82.
- Decision: continue to final evaluation; no resource or collapse reason to stop.

## 2026-06-30 nenv16 defensive seed26 completed
- Time: 2026-06-30T14:42:35+08:00
- Evaluation CSV: outputs/defensive_ttc12_v18_nenv16_final/evaluations/defensive_proposed_ppo_s26.csv; eval_n_envs=16; 50 episodes per density.
- d0.00: success=0.92, cost=0.00, collision=0.00, route=0.990.
- d0.08: success=0.86, cost=0.08, collision=0.08, route=0.946.
- d0.15: success=0.66, cost=0.10, collision=0.10, route=0.930.
- Comparison: nenv16 improves high-density over nenv8 seed26 (0.60/0.24 cost) and nenv10 seed26 (0.60/0.28 cost), while staying near nenv10 at d0.08.
- Decision: adopt nenv16 as the current formal protocol and expand to seed27 before any new reward/defensive parameter tuning.


## 2026-06-30 launched nenv16 defensive ttc12/v18 seed27
- Time: 2026-06-30T14:42:40+08:00
- Protocol: scripts/run_one_defensive_proposed.py --seed 27 --n-envs 16 --timesteps 1000000 --root outputs/defensive_ttc12_v18_nenv16_final --ttc-threshold 12.0 --target-speed 18.0 --device cuda.
- Purpose: confirm the strong seed26 nenv16 result is reproducible before expanding to seed28 or tuning.
- Log: outputs/defensive_ttc12_v18_nenv16_final/logs/defensive_s27_nenv16_20260630_144235.log
- Launcher PID: 13808; main PID: 13815; PGID: 13808.


## 2026-06-30 protocol change to nenv32
- Time: 2026-06-30T14:44:48+08:00
- User requirement: try n_envs=32 because CPU/GPU memory are still largely free; keep at least 4GB available CPU memory and 2GB free GPU memory.
- Action: stopped the in-progress nenv16 seed27 run and archived partial artifacts under outputs/interrupted_nenv16_protocol_change_to_nenv32_20260630_144448.
- Stopped PGID: 13808.
- Note: completed nenv16 seed26 remains valid comparison evidence; new formal runs use nenv32 directories and TARGET_N_ENVS=32 summaries.


## 2026-06-30 launched nenv32 defensive ttc12/v18 seed26
- Time: 2026-06-30T14:45:56+08:00
- Protocol: scripts/run_one_defensive_proposed.py --seed 26 --n-envs 32 --timesteps 1000000 --root outputs/defensive_ttc12_v18_nenv32_final --ttc-threshold 12.0 --target-speed 18.0 --device cuda.
- Safety requirement: keep at least 4GB available CPU memory and 2GB free GPU memory.
- Purpose: test whether nenv32 improves throughput/results beyond the strong completed nenv16 seed26 result.
- Log: outputs/defensive_ttc12_v18_nenv32_final/logs/defensive_s26_nenv32_20260630_144548.log
- Launcher PID: 14217; main PID: 14224; PGID: 14217.

## 2026-06-30 nenv32 defensive seed26 monitor at ~393k
- Time: 2026-06-30T14:48:05+08:00
- Safety: CPU available about 24GiB; GPU free about 10.9GiB, above the required 4GB CPU / 2GB GPU headroom.
- Throughput: fps about 3600-4000, clearly faster than nenv16/nenv8.
- Checkpoint: checkpoint_249984_steps.zip exists.
- Training signal: still stage0 at ~393k; route window about 0.50, cost window 0, std about 0.88, success_rate 0.
- Decision: continue to 500k/750k. nenv32 is resource-safe and fast, but learning speed is not yet clearly better than nenv16, so final eval will decide protocol adoption.

## 2026-06-30 nenv32 defensive seed26 monitor at ~655k
- Time: 2026-06-30T14:50:07+08:00
- Safety: CPU available about 23GiB; GPU free about 10.95GiB, above the required 4GB CPU / 2GB GPU headroom.
- Throughput: fps about 2800-3100 in mid-run, still faster than nenv16.
- Checkpoints: checkpoint_249984_steps.zip and checkpoint_499968_steps.zip exist; non-round names are expected from callback frequency with 32 envs.
- Training signal: after slow stage0 start, reached stage2; success_rate peaked around 0.54 and latest stage2 has window_success about 0.30, window_cost about 0.033, route window about 0.836.
- Decision: continue to final evaluation; nenv32 is both safe and promising enough to finish.

## 2026-06-30 nenv32 defensive seed26 monitor at ~918k
- Time: 2026-06-30T14:53:37+08:00
- Safety: CPU available about 22GiB; GPU free about 10.95GiB, above the required 4GB CPU / 2GB GPU headroom.
- Throughput: nenv32 is faster than nenv16 early/mid-run; fps peaked around 3600-4000 and later dropped to about 2000-2200 as episodes became longer/harder.
- Training signal: reached stage3 multiple times; success_rate peaked around 0.68 at ~852k and later fluctuated to about 0.31 at ~918k; latest std about 0.59.
- Decision: continue to final evaluation. nenv32 is fast and resource-safe; final held-out metrics will decide whether it replaces nenv16.

## 2026-06-30 nenv32 defensive seed26 completed and rejected as final protocol
- Time: 2026-06-30T14:59:07+08:00
- Evaluation CSV: outputs/defensive_ttc12_v18_nenv32_final/evaluations/defensive_proposed_ppo_s26.csv; eval_n_envs=32; 50 episodes per density.
- nenv32 results: d0.00 success=1.00 cost=0.00 route=0.991; d0.08 success=0.78 cost=0.18 route=0.914; d0.15 success=0.54 cost=0.24 route=0.854.
- Same-seed comparison: nenv16 seed26 had d0.08 success=0.86 cost=0.08 and d0.15 success=0.66 cost=0.10.
- Interpretation: nenv32 is faster (about 3600-4000 fps early) and resource-safe, but degrades held-out medium/high-density success and safety.
- Decision: keep nenv32 as a throughput diagnostic only; restore formal default protocol to nenv16 and continue seed expansion there.


## 2026-06-30 relaunched nenv16 defensive ttc12/v18 seed27 after nenv32 diagnostic
- Time: 2026-06-30T14:59:49+08:00
- Protocol: scripts/run_one_defensive_proposed.py --seed 27 --n-envs 16 --timesteps 1000000 --root outputs/defensive_ttc12_v18_nenv16_final --ttc-threshold 12.0 --target-speed 18.0 --device cuda.
- Purpose: expand the best current formal protocol after nenv32 proved faster but worse on held-out metrics.
- Log: outputs/defensive_ttc12_v18_nenv16_final/logs/defensive_s27_nenv16_20260630_145943.log
- Launcher PID: 15496; main PID: 15503; PGID: 15496.

## 2026-06-30 ttc14/v18 nenv16 weak-seed validation status
- Time: 2026-06-30T16:09:19
- Protocol: scripts/run_one_defensive_proposed.py, n_envs=16, timesteps=1M, horizon=1500, ttc_threshold=14.0, target_speed=18.0, eval_n_envs=16.
- Seed27: d0.08 success=0.86 cost=0.06; d0.15 success=0.44 cost=0.38 collision=0.32 route=0.777.
- Seed28: d0.08 success=0.86 cost=0.12; d0.15 success=0.66 cost=0.20 collision=0.20 route=0.897.
- Current 2-seed mean d0.08: success=0.860, cost=0.090.
- Current 2-seed mean d0.15: success=0.550, cost=0.290.
- Decision: seed27 reduces high-density cost but does not improve success; seed28 improves both. Need seed26 before freezing or rejecting ttc14/v18, because two-seed mean is too narrow for paper-facing claim.
- Launched seed26 ttc14/v18 nenv16 at 2026-06-30 16:08 CST; log under outputs/defensive_ttc14_v18_nenv16_tuning/logs/launcher_s26_ttc14_v18_20260630_160822.out.

## 2026-06-30 correction on ttc14/v18 seed27 interpretation
- Time: 2026-06-30T16:09:40
- Correction: the earlier summary row with seed=27.5 was the aggregate over seed27 and seed28, not seed27 alone.
- Actual seed27 ttc14/v18: d0.08 success=0.86 cost=0.06; d0.15 success=0.44 cost=0.38 collision=0.32 route=0.777.
- Compared with ttc12/v18 seed27 (d0.15 success=0.56 cost=0.34), ttc14/v18 worsens this weak seed. Seed28 improved, so the tuning is unstable rather than ready to freeze.
- Decision: keep the already launched seed26 run only to complete evidence. Do not freeze ttc14/v18 unless the three-seed mean clearly passes and the weak-seed failure can be explained. If not, next tuning should target robustness instead of only raising TTC threshold.

## 2026-06-30 ttc14/v18 seed26 monitor at ~393k
- Time: 2026-06-30T16:12:01
- Health: process alive with 16 workers; GPU free about 10.9GB and CPU available about 23GB, above safety headroom.
- Checkpoint: checkpoint_250000_steps.zip exists.
- Training signal: stage1, total_timesteps about 393k, success_rate recently about 0.22-0.32, window_route_completion about 0.626, window_cost back to 0, std about 0.709.
- Decision: continue to 500k/750k. This is not idle collapse; still need final held-out d0.08/d0.15 before deciding whether ttc14/v18 is viable.

## 2026-06-30 ttc14/v18 seed26 monitor at ~622k
- Time: 2026-06-30T16:14:57
- Health: still alive with 16 workers; GPU free about 10.9GB.
- Checkpoint: checkpoint_500000_steps.zip exists.
- Training signal: reached stage2 by ~622k. Recent success_rate about 0.27; window_success about 0.433; window_route_completion about 0.754.
- Risk signal: window_cost about 0.30 and one sampled out_of_road episode appeared. This is not a crash/idle-collapse run, but ttc14/v18 is showing instability.
- Decision: continue to 750k/final evaluation; do not freeze ttc14/v18 from training curves alone. Final held-out d0.15 will decide.

## 2026-06-30 ttc14/v18 seed26 monitor at ~885k
- Time: 2026-06-30T16:18:55
- Checkpoint: checkpoint_750000_steps.zip exists.
- Training signal: around 835k-885k, stage2 briefly appeared but then demoted to stage1; recent success_rate about 0.05-0.11, route samples vary from 0.56 to 0.95.
- Risk signal: window_cost reached about 0.433 and sampled out_of_road occurred earlier. This suggests ttc14/v18 is unstable for seed26 as well.
- Decision: do not stop because the run is close to completion and final held-out CSV is needed for evidence. Expect likely diagnostic-only unless evaluation contradicts the training curve.


## 2026-06-30 ttc14/v18 nenv16 tuning completed and rejected
- Time: 2026-06-30T16:29:52+08:00
- Protocol: scripts/run_one_defensive_proposed.py, n_envs=16, timesteps=1M, horizon=1500, ttc_threshold=14.0, target_speed=18.0, eval_n_envs=16, 50 episodes per density.
- Evidence: outputs/defensive_ttc14_v18_nenv16_tuning/evaluations/summary.csv and per-seed CSVs for seeds 26/27/28.
- seed26 d0.15: success=0.62 cost=0.20 collision=0.20 out=0.00 route=0.842.
- seed27 d0.15: success=0.44 cost=0.38 collision=0.32 out=0.06 route=0.777.
- seed28 d0.15: success=0.66 cost=0.20 collision=0.20 out=0.00 route=0.897.
- mean d0.00: success=0.973 cost=0.000 collision=0.000 out=0.000 route=0.990.
- mean d0.08: success=0.867 cost=0.093 collision=0.087 out=0.007 route=0.953.
- mean d0.15: success=0.573 cost=0.260 collision=0.240 out=0.020 route=0.839.
- Gate result: FAIL. The d0.15 three-seed mean success=0.573 is below the 0.60 minimum and mean cost=0.260 is above the 0.25 ceiling.
- Interpretation: raising TTC threshold to 14 helps seed26/28 relative to the weakest ttc12/v18 cases but worsens seed27 success and remains unstable; improvement over ttc12/v18 mean is too small for a paper-facing final claim.
- Decision: keep ttc14/v18 as diagnostic parameter-sensitivity evidence only. Do not freeze it as Branch A. Move to Branch B standard comparison with n_envs=16 and start from the full proposed method, while retaining defensive results for appendix/tuning discussion.

## 2026-06-30 launch Branch B proposed seed0 nenv16
- Time: 2026-06-30T16:30:49+08:00
- Decision basis: previous n_envs=10 candidate protocol used ent_coef=0.01 after idle-collapse diagnostics; current user requirement is to rerun formal evidence with n_envs=16. Keep ent_coef=0.01 and move only the environment parallelism/protocol to n_envs=16.
- Command: N_ENVS=16 EPISODES=50 DEVICE=cuda codex_longrun_iscsic/run_formal_variant_nenv16.sh proposed 0 outputs/iscsic_main_nenv16_v2 1500000 1200 --ent-coef 0.01
- Protocol: Branch B standard main comparison, proposed full method, seed=0, horizon=1200, train/eval n_envs=16, densities=0.00/0.08/0.15, 50 eval episodes per density.
- Review target: if final d0.15 is underfit or safety-success tradeoff cannot serve the paper main line, inspect training stages/config and run targeted reward/gate/timestep diagnostics before expanding all seeds.

## 2026-06-30 actual Branch B proposed seed0 nenv16 launch
- Time: 2026-06-30T16:31:15+08:00
- Note: previous local wrapper attempt only wrote the decision note; the training launch is performed by this remote script.
- Command: N_ENVS=16 EPISODES=50 DEVICE=cuda codex_longrun_iscsic/run_formal_variant_nenv16.sh proposed 0 outputs/iscsic_main_nenv16_v2 1500000 1200 --ent-coef 0.01
- Expected artifacts: outputs/iscsic_main_nenv16_v2/runs/proposed_ppo_s0/config.json, final_model.zip, evaluations/proposed_ppo_s0.csv, figures, and run report.

## 2026-06-30 proposed seed0 nenv16 early health check
- Time: 2026-06-30T16:31:59+08:00
- Run: outputs/iscsic_main_nenv16_v2/runs/proposed_ppo_s0.
- Config verified: variant=proposed, seed=0, timesteps=1.5M, horizon=1200, n_envs=16, ent_coef=0.01, learning_rate=3e-4, curriculum/risk_reward/action_guard all enabled.
- Early log: reached about 49k timesteps, fps about 2500, stage=0, no crash/cost signal yet, low route completion as expected during warmup.
- Resource check: GPU free about 10.9GB, CPU available about 24GB, disk free about 35GB. Continue to 250k checkpoint before making quality decision.

## 2026-06-30 proposed seed0 nenv16 monitor at ~344k
- Time: 2026-06-30T16:34:18+08:00
- Health: process alive with 16 workers; GPU free about 10.9GB, above safety headroom.
- Training signal: reached stage1 around 327k with window_success about 0.50, window_route_completion about 0.732, window_cost about 0.033; then demoted to stage0 by 344k with window_success about 0.033, route window about 0.526, window_cost about 0.10.
- Interpretation: this is not idle collapse because success and route progress have appeared, but the policy is unstable after first promotion.
- Decision: continue to 500k/750k before tuning. If repeated demotion persists or final held-out d0.15 fails, inspect stage gates/reward safety balance before expanding all proposed seeds.

## 2026-06-30 proposed seed0 nenv16 monitor at ~475k
- Time: 2026-06-30T16:35:45+08:00
- Health: process alive with 16 workers; GPU free about 10.9GB; checkpoint_374992_steps.zip exists.
- Training signal: progressed beyond early instability and reached stage3 by about 475k. Recent window_success about 0.367 and window_route_completion about 0.736.
- Risk signal: stage3 window_cost about 0.233 and one out-of-road/cost sample appeared near 442k. This is acceptable to continue but not yet safe enough to expand all seeds blindly.
- Decision: continue to 750k/final. Main criterion is held-out d0.08/d0.15 cost and success after full eval; no parameter edit yet.

## 2026-06-30 proposed seed0 nenv16 monitor at ~557k
- Time: 2026-06-30T16:37:23+08:00
- Health: process alive; GPU free about 10.9GB; checkpoint_374992_steps.zip exists.
- Training signal: after reaching stage3 around 475k, current log around 557k is stage2 with window_route_completion about 0.718 and window_success about 0.133.
- Risk signal: window_cost fluctuated up to 0.400 around 540k and then fell to about 0.233 by 557k; ttc_risk begins to appear at hard enough traffic.
- Interpretation: standard proposed is learning but safety is not yet stable. Continue because mid-run stage demotion/cost spikes are informative but final held-out evaluation is the decisive evidence.
- Decision: keep running to 750k/final. If final d0.15 cost remains high, likely next diagnostic is safety-weight/gate tuning rather than more seeds only.

## 2026-06-30 proposed seed0 nenv16 monitor at ~672k
- Time: 2026-06-30T16:39:17+08:00
- Health: process alive; GPU free about 10.9GB.
- Training signal: recovered from earlier stage2/cost spike and reached stage4 hard around 655k. Recent window_cost about 0.067, window_route_completion about 0.837, success_rate about 0.34.
- Mechanism note: the full proposed method is now exposing hard-density TTC risk while keeping current sampled cost at zero, which is the intended safety-curriculum behavior.
- Decision: continue to 1M/1.5M and final evaluation. If held-out d0.15 is acceptable, expand Branch B seeds/variants under the same n_envs=16 + ent_coef=0.01 protocol.

## 2026-06-30 proposed seed0 nenv16 monitor at ~770k
- Time: 2026-06-30T16:41:41+08:00
- Health: process alive; checkpoint_749984_steps.zip now exists.
- Training signal: after a good stage4 window at ~655k, the policy is back at stage3 by ~770k with window_route_completion about 0.687 and window_success about 0.10.
- Risk signal: two recent collision/cost samples appeared near ~754k and ~770k; window_cost is about 0.167. This is below the earlier 0.40 spike but not yet paper-grade stable.
- Decision: continue to final evaluation for authoritative d0.08/d0.15 metrics. If final cost is high, next action should be targeted reward/gate tuning before broad seed expansion.

## 2026-06-30 proposed seed0 nenv16 monitor at ~885k
- Time: 2026-06-30T16:44:06+08:00
- Health: process alive; GPU free about 10.9GB; checkpoints at ~375k and ~750k exist.
- Training signal: still stage3 near 885k; route window about 0.749 but success window only about 0.033-0.10 in recent logs.
- Risk signal: window_cost fluctuates from about 0.133 to 0.333; recent sampled episodes can achieve high route completion, but held-out safety stability is uncertain.
- Decision: continue to final eval. Do not expand Branch B seeds until proposed seed0 final CSV is inspected. Likely next diagnostic, if final d0.15 is poor, is reward/gate safety tuning rather than just more timesteps.

## 2026-06-30 proposed seed0 nenv16 monitor at ~1.0M
- Time: 2026-06-30T16:47:02+08:00
- Health: process alive; checkpoints at ~375k and ~750k exist.
- Training signal: around 966k-999k the run is stage4 hard, with recent success samples but unstable success window.
- Risk signal: window_cost reached about 0.400 at ~999k, including recent crash_vehicle/cost samples. This is a warning sign for the final d0.15 safety claim.
- Decision: continue to 1.5M and final held-out eval. Do not expand additional proposed seeds until final CSV is checked; if cost remains high, next step is safety reward/gate tuning.

## 2026-06-30 proposed seed0 nenv16 monitor at ~1.15M
- Time: 2026-06-30T16:50:48+08:00
- Health: process alive; checkpoint_1124976_steps.zip now exists.
- Training signal: around 1.15M still mostly stage3, with route window about 0.707 and success window about 0.067 in the latest logged block.
- Risk signal: window_cost spiked to about 0.533 near 1.11M and then recovered to about 0.133 by 1.15M. Safety remains unstable, even though sampled episodes often have no immediate cost.
- Decision: finish the scheduled 1.5M and evaluate. Treat this as a pending quality gate, not accepted main evidence yet.

## 2026-06-30 proposed seed0 nenv16 monitor at ~1.36M
- Time: 2026-06-30T16:55:13+08:00
- Health: process alive; GPU free about 10.9GB; final checkpoint not yet written, but 1.125M checkpoint exists.
- Training signal: latest blocks around 1.31M-1.36M remain stage3, with route window around 0.77-0.81 and success window around 0.13-0.20.
- Risk signal: window_cost improved from earlier spikes to about 0.067-0.133. Safety has improved late, but success/stage progression remain weaker than ideal.
- Decision: finish and inspect final evaluation CSV before deciding whether to expand seeds or launch a safety/target-speed/TTC tuning diagnostic.

## 2026-06-30 proposed seed0 nenv16 training completed, evaluation running
- Time: 2026-06-30T16:58:37+08:00
- Training status: completed 1.5M scheduled timesteps and saved outputs/iscsic_main_nenv16_v2/runs/proposed_ppo_s0/model/final_model.zip plus checkpoint_1499968_steps.zip.
- Final training signal: still stage3 near 1.507M, window_route_completion about 0.794, window_success about 0.20, window_cost about 0.20. Not a clean training-curve pass, so held-out eval is decisive.
- Evaluation status: scripts/evaluate_from_config.py is running with eval_n_envs=16, densities 0.00/0.08/0.15, 50 episodes per density.

## 2026-06-30 Branch B proposed seed0 nenv16 completed and failed main gate
- Time: 2026-06-30T17:03:41+08:00
- Run: outputs/iscsic_main_nenv16_v2/runs/proposed_ppo_s0.
- Protocol: proposed full method, seed0, train/eval n_envs=16, timesteps=1.5M, horizon=1200, ent_coef=0.01, eval 50 episodes per density.
- Evaluation CSV: outputs/iscsic_main_nenv16_v2/evaluations/proposed_ppo_s0.csv; summary: outputs/iscsic_main_nenv16_v2/evaluations/summary.csv.
- d0.00: success=0.90 cost=0.00 collision=0.00 out=0.00 route=0.984 shield=0.862.
- d0.08: success=0.76 cost=0.12 collision=0.12 out=0.00 route=0.929 shield=0.842.
- d0.15: success=0.48 cost=0.42 collision=0.40 out=0.02 route=0.791 shield=0.749.
- Gate result: FAIL for paper main line. High-density cost/collision is too high and success is below target; do not expand this exact protocol to seed1/seed2 as the main proposed method.
- Decision: launch targeted safety tuning using stronger TTC/collision penalties and lower target speed, based on defensive branch evidence and prior reward screens showing completion-only tuning worsens high-density collision.

## 2026-06-30 launch proposed safety-tuned seed0 nenv16 screen
- Time: 2026-06-30T17:03:41+08:00
- Output root: outputs/tuning_proposed_safety_ttc12_v18_nenv16_1m.
- Command: N_ENVS=16 EPISODES=50 DEVICE=cuda codex_longrun_iscsic/run_formal_variant_nenv16.sh proposed 0 outputs/tuning_proposed_safety_ttc12_v18_nenv16_1m 1000000 1200 --ent-coef 0.01 --reward-ttc 6 --reward-cost 40 --reward-overspeed 3 --reward-target-speed 18 --reward-progress 40 --reward-success-bonus 55 --reward-crash-penalty 120 --reward-out-of-road-penalty 120 --reward-ttc-threshold 12 --stage2-success 0.40 --stage2-cost 0.25 --demote-cost 0.35
- Hypothesis: stronger TTC/cost/crash penalties and lower target speed should reduce d0.15 collision/cost relative to standard proposed seed0, while preserving enough route completion for a safety-success tradeoff.
- Promotion rule: only expand if d0.15 cost is materially below 0.42 and preferably <=0.25 without collapsing d0.08 success.

## 2026-06-30 safety-tuned proposed seed0 nenv16 early health check
- Time: 2026-06-30T17:04:21+08:00
- Run: outputs/tuning_proposed_safety_ttc12_v18_nenv16_1m/runs/proposed_ppo_s0.
- Config verified: n_envs=16, timesteps=1M, horizon=1200, ent_coef=0.01, reward_ttc=6, reward_cost=40, target_speed=18, progress=40, success_bonus=55, crash/out=120, ttc_threshold=12, stage2_success=0.40, stage2_cost=0.25, demote_cost=0.35.
- Early log: about 32k timesteps, stage0, no cost/collision yet; low route completion is expected during warmup.
- Resource check: GPU free about 10.8GB, CPU available about 24GB, disk free about 41GB. Continue to 250k/500k quality checks.

## 2026-06-30 safety-tuned proposed seed0 monitor at ~311k
- Time: 2026-06-30T17:06:20+08:00
- Health: process alive; checkpoint_250000_steps.zip exists; GPU free about 10.9GB.
- Training signal: reached stage1 by about 278k-311k. Success window remains low at about 0.067; route window dropped from about 0.600 to 0.436, while sampled route can reach about 0.604.
- Risk signal: window_cost ranges about 0.067-0.200. Safety pressure is working, but the run may be too conservative/slow early.
- Decision: continue to 500k before changing parameters. Watch whether route/success recover under the lower target speed and stronger TTC/cost penalties.

## 2026-06-30 safety-tuned proposed seed0 monitor at ~508k
- Time: 2026-06-30T17:08:24+08:00
- Health: process alive; checkpoints at 250k and 500k exist; GPU free about 10.9GB.
- Training signal: still stage1 around 508k. Route window improved to about 0.685, success window about 0.133; sampled route can reach about 0.829 but an out-of-road cost sample appeared.
- Risk/benefit: stronger safety tuning is slowing curriculum progress but may reduce high-density collision relative to standard proposed. It is not idle collapse.
- Decision: continue to 750k/final evaluation. If final d0.15 cost improves but success collapses, next diagnostic should relax completion/speed slightly rather than revert to standard reward.

## 2026-06-30 safety-tuned proposed seed0 monitor at ~704k
- Time: 2026-06-30T17:11:14+08:00
- Health: process alive; checkpoints at 250k and 500k exist; GPU free about 10.9GB.
- Training signal: recovered from slow early stage1 and reached stage3 by about 688k. Window_route_completion peaked around 0.862 and window_success about 0.467; current sampled route remains moderate to high.
- Risk signal: window_cost is 0.0 in the recent stage2/stage3 blocks, a clear improvement over the standard proposed run's high-cost training windows.
- Decision: continue to final evaluation. This screen remains promising for reducing d0.15 cost; final success tradeoff will decide promotion.

## 2026-06-30 safety-tuned proposed seed0 monitor at ~918k
- Time: 2026-06-30T17:14:47+08:00
- Health: process alive; checkpoints at 250k/500k/750k exist.
- Training signal: after reaching stage3 earlier, latest log near 918k is stage2 with route window about 0.749 and success window about 0.067.
- Risk signal: recent window_cost is low, about 0.033-0.067, much lower than standard proposed, but success appears under pressure.
- Decision: finish and evaluate. If final d0.15 cost drops strongly but success is too low, next tuning should relax success/completion pressure or reduce safety strength slightly.

## 2026-06-30 safety-tuned proposed seed0 training completed, evaluation running
- Time: 2026-06-30T17:17:50+08:00
- Training status: completed 1M scheduled timesteps and saved outputs/tuning_proposed_safety_ttc12_v18_nenv16_1m/runs/proposed_ppo_s0/model/final_model.zip plus checkpoint_1000000_steps.zip.
- Final training signal: stage2 near 1.016M, window_route_completion about 0.743, window_success about 0.167, window_cost about 0.133.
- Interpretation before eval: much lower apparent cost than standard proposed, but success/stage progression is weaker. Held-out eval will decide whether this is a useful safety-success tradeoff.
- Evaluation status: evaluate_from_config.py is running with eval_n_envs=16, densities 0.00/0.08/0.15, 50 episodes per density.

## 2026-06-30 safety-tuned proposed seed0 nenv16 screen completed and rejected
- Time: 2026-06-30T17:21:05+08:00
- Run: outputs/tuning_proposed_safety_ttc12_v18_nenv16_1m/runs/proposed_ppo_s0.
- Protocol: proposed seed0, train/eval n_envs=16, timesteps=1M, horizon=1200, ent_coef=0.01, reward_ttc=6, cost=40, target_speed=18, progress=40, success_bonus=55, crash/out=120, ttc_threshold=12, stage2_success=0.40, stage2_cost=0.25, demote_cost=0.35.
- Evaluation CSV: outputs/tuning_proposed_safety_ttc12_v18_nenv16_1m/evaluations/proposed_ppo_s0.csv.
- d0.00: success=0.70 cost=0.00 collision=0.00 out=0.00 route=0.969 shield=0.860.
- d0.08: success=0.64 cost=0.12 collision=0.10 out=0.02 route=0.935 shield=0.839.
- d0.15: success=0.28 cost=0.40 collision=0.34 out=0.06 route=0.704 shield=0.699.
- Gate result: FAIL. Compared with standard proposed seed0 d0.15 success=0.48/cost=0.42, cost only improves slightly while success collapses. Do not expand this configuration.
- Decision: launch defensive-like horizon1500 cost50 diagnostic, because prior defensive branch suggests horizon1500 + stricter progression gives better high-density tradeoff than horizon1200 safety penalty alone.

## 2026-06-30 launch defensive-like proposed h1500 cost50 seed0 nenv16 screen
- Time: 2026-06-30T17:21:05+08:00
- Output root: outputs/tuning_proposed_defensive_h1500_cost50_nenv16_1m.
- Command: N_ENVS=16 EPISODES=50 DEVICE=cuda codex_longrun_iscsic/run_formal_variant_nenv16.sh proposed 0 outputs/tuning_proposed_defensive_h1500_cost50_nenv16_1m 1000000 1500 --ent-coef 0.01 --reward-ttc 6 --reward-cost 50 --reward-overspeed 3 --reward-target-speed 18 --reward-progress 40 --reward-success-bonus 55 --reward-crash-penalty 120 --reward-out-of-road-penalty 120 --reward-ttc-threshold 12 --stage2-success 0.50 --stage2-cost 0.25 --demote-cost 0.35
- Hypothesis: horizon=1500 and stricter stage2 gate should preserve route/success better than the failed horizon1200 safety screen, while cost=50 attempts to push d0.15 cost below the defensive ttc12/v18 mean.
- Promotion rule: must beat standard proposed seed0 on d0.15 cost by a clear margin and avoid the safety-tuned screen's success collapse.

## 2026-06-30 defensive-like h1500 cost50 seed0 early health check
- Time: 2026-06-30T17:21:39+08:00
- Run: outputs/tuning_proposed_defensive_h1500_cost50_nenv16_1m/runs/proposed_ppo_s0.
- Config verified: n_envs=16, timesteps=1M, horizon=1500, ent_coef=0.01, reward_ttc=6, reward_cost=50, target_speed=18, progress=40, success_bonus=55, crash/out=120, ttc_threshold=12, stage2_success=0.50, stage2_cost=0.25, demote_cost=0.35.
- Early log: about 32k timesteps, stage0, no cost/collision, low route completion as expected.
- Resource check: GPU free about 10.8GB, CPU available about 24GB, disk free about 41GB. Continue to 250k/500k checks.

## 2026-06-30 defensive-like h1500 cost50 seed0 monitor at ~295k
- Time: 2026-06-30T17:23:35+08:00
- Health: process alive; checkpoint_250000_steps.zip exists; GPU free about 10.8GB.
- Training signal: reached stage1 by ~278k. Recent window_success rose to about 0.233, with route window around 0.528-0.607.
- Risk signal: window_cost is 0.0-0.10 in early stage1, better than the failed horizon1200 safety screen at comparable progress.
- Decision: continue to 500k/750k. This diagnostic is still viable because horizon1500 appears to preserve early success better while keeping cost low.

## 2026-06-30 defensive-like h1500 cost50 seed0 monitor at ~508k
- Time: 2026-06-30T17:26:11+08:00
- Health: process alive; checkpoints at 250k and 500k exist.
- Training signal: around 508k still stage1, but route window is strong at about 0.813 and success window about 0.267. This is better route/success behavior than the failed horizon1200 safety screen.
- Risk signal: window_cost rose to about 0.233, near the intended stage2 cost ceiling. It is not yet clean enough to freeze.
- Decision: continue to 750k/final. Need final d0.15 cost to decide whether cost50 helps or just trades instability for route.

## 2026-06-30 defensive-like h1500 cost50 seed0 monitor at ~688k
- Time: 2026-06-30T17:28:58+08:00
- Health: process alive; checkpoints at 250k and 500k exist.
- Training signal: reached stage2 by about 672k. Window_route_completion about 0.854, window_success about 0.30, and success samples appear.
- Risk signal: cost spiked around 622k-639k up to window_cost about 0.30, then improved to about 0.10 by 672k-688k.
- Decision: continue to 750k/final. This is now the most promising tuning screen so far because it preserves route/success better than the horizon1200 safety screen while recovering cost.

## 2026-06-30 defensive-like h1500 cost50 seed0 monitor at ~918k
- Time: 2026-06-30T17:32:16+08:00
- Health: process alive; checkpoints at 250k/500k/750k exist.
- Training signal: around 900k-918k the run is stage2 and success_rate increases, but route samples are mixed.
- Risk signal: window_cost worsened to about 0.333-0.467, mainly out-of-road samples, despite cost50. This is a serious warning sign.
- Decision: continue to final held-out eval for evidence, but do not treat this diagnostic as promotable unless the CSV unexpectedly shows much lower d0.15 cost.

## 2026-06-30 defensive-like h1500 cost50 seed0 training completed, evaluation running
- Time: 2026-06-30T17:35:19+08:00
- Training status: completed 1M scheduled timesteps and saved outputs/tuning_proposed_defensive_h1500_cost50_nenv16_1m/runs/proposed_ppo_s0/model/final_model.zip plus checkpoint_1000000_steps.zip.
- Final training signal: stage2 near 1.016M, window_route_completion about 0.776, window_success about 0.467, window_cost about 0.20.
- Interpretation before eval: better success/route than the horizon1200 safety screen, but out-of-road/cost instability remains. Held-out eval decides promotion or rejection.
- Evaluation status: evaluate_from_config.py is running with eval_n_envs=16, densities 0.00/0.08/0.15, 50 episodes per density.

## 2026-06-30 defensive-like h1500 cost50 seed0 screen completed: improved but failed
- Time: 2026-06-30T17:38:31+08:00
- Run: outputs/tuning_proposed_defensive_h1500_cost50_nenv16_1m/runs/proposed_ppo_s0.
- Protocol: proposed seed0, n_envs=16, timesteps=1M, horizon=1500, ent_coef=0.01, reward_ttc=6, cost=50, target_speed=18, progress=40, success_bonus=55, crash/out=120, ttc_threshold=12, stage2_success=0.50, stage2_cost=0.25.
- Evaluation CSV: outputs/tuning_proposed_defensive_h1500_cost50_nenv16_1m/evaluations/proposed_ppo_s0.csv.
- d0.00: success=0.96 cost=0.00 collision=0.00 out=0.00 route=0.986 shield=0.867.
- d0.08: success=0.84 cost=0.12 collision=0.10 out=0.02 route=0.936 shield=0.846.
- d0.15: success=0.54 cost=0.34 collision=0.24 out=0.10 route=0.815 shield=0.716.
- Gate result: FAIL but improved. Compared with standard proposed seed0, d0.15 improved from success=0.48/cost=0.42 to success=0.54/cost=0.34, but cost remains too high and out_of_road=0.10 is a new bottleneck.
- Decision: next tuning should target lane/out-of-road control, not just global cost. Launch h1500 lane/out diagnostic with lower target speed and stronger lane/out penalties.

## 2026-06-30 launch defensive-like h1500 lane/out seed0 nenv16 screen
- Time: 2026-06-30T17:38:31+08:00
- Output root: outputs/tuning_proposed_defensive_h1500_lane2_v16_cost50_nenv16_1m.
- Command: N_ENVS=16 EPISODES=50 DEVICE=cuda codex_longrun_iscsic/run_formal_variant_nenv16.sh proposed 0 outputs/tuning_proposed_defensive_h1500_lane2_v16_cost50_nenv16_1m 1000000 1500 --ent-coef 0.01 --reward-ttc 6 --reward-cost 50 --reward-overspeed 3 --reward-target-speed 16 --reward-progress 40 --reward-lane 2.0 --reward-success-bonus 55 --reward-crash-penalty 120 --reward-out-of-road-penalty 150 --reward-ttc-threshold 12 --stage2-success 0.50 --stage2-cost 0.25 --demote-cost 0.35
- Hypothesis: h1500/cost50 improved success but left high out_of_road and lane deviation; stronger lane/out penalty plus target_speed=16 should reduce d0.15 cost without repeating the horizon1200 success collapse.
- Promotion rule: must reduce d0.15 cost below 0.34 and preferably <=0.25 while keeping success near or above 0.50.

## 2026-06-30 defensive-like h1500 lane/out seed0 early health check
- Time: 2026-06-30T17:39:05+08:00
- Run: outputs/tuning_proposed_defensive_h1500_lane2_v16_cost50_nenv16_1m/runs/proposed_ppo_s0.
- Config verified: n_envs=16, timesteps=1M, horizon=1500, ent_coef=0.01, reward_ttc=6, reward_cost=50, reward_lane=2.0, target_speed=16, progress=40, success_bonus=55, crash=120, out=150, ttc_threshold=12, stage2_success=0.50, stage2_cost=0.25.
- Early log: about 32k timesteps, stage0, no cost/collision; shaped reward is much lower because lane penalty is stronger.
- Resource check: GPU free about 10.8GB, CPU available about 24GB, disk free about 41GB. Continue to 250k; watch for over-conservative/low-motion collapse.

## 2026-06-30 defensive-like h1500 lane2/v16 seed0 early rejected
- Time: 2026-06-30T17:41:32+08:00
- Run: outputs/tuning_proposed_defensive_h1500_lane2_v16_cost50_nenv16_1m/runs/proposed_ppo_s0.
- Status at about 311k: still stage0, window_route_completion about 0.077-0.082, window_success=0, window_cost=0, mean_speed about 0.5-0.6 km/h.
- Interpretation: reward_lane=2.0 plus target_speed=16 and strong out penalty makes the policy too conservative/low-motion. This is early idle/slow-motion collapse, not a useful paper candidate.
- Decision: terminate this run early and do not evaluate it. Launch a milder lane/out diagnostic: lane=1.0, target_speed=18, out penalty=150, keeping horizon1500 and cost50.

## 2026-06-30 launch defensive-like h1500 lane1/out150 seed0 nenv16 screen
- Time: 2026-06-30T17:41:32+08:00
- Output root: outputs/tuning_proposed_defensive_h1500_lane1_out150_cost50_nenv16_1m.
- Command: N_ENVS=16 EPISODES=50 DEVICE=cuda codex_longrun_iscsic/run_formal_variant_nenv16.sh proposed 0 outputs/tuning_proposed_defensive_h1500_lane1_out150_cost50_nenv16_1m 1000000 1500 --ent-coef 0.01 --reward-ttc 6 --reward-cost 50 --reward-overspeed 3 --reward-target-speed 18 --reward-progress 40 --reward-lane 1.0 --reward-success-bonus 55 --reward-crash-penalty 120 --reward-out-of-road-penalty 150 --reward-ttc-threshold 12 --stage2-success 0.50 --stage2-cost 0.25 --demote-cost 0.35
- Hypothesis: a moderate lane penalty and stronger out penalty may reduce out_of_road without the lane2/v16 low-motion collapse.

## 2026-06-30 defensive-like h1500 lane1/out150 seed0 screen completed: promoted to candidate
- Time: 2026-06-30T17:57:38+08:00
- Run: outputs/tuning_proposed_defensive_h1500_lane1_out150_cost50_nenv16_1m/runs/proposed_ppo_s0.
- Protocol: proposed seed0, n_envs=16, timesteps=1M, horizon=1500, ent_coef=0.01, reward_ttc=6, reward_cost=50, reward_lane=1.0, target_speed=18, progress=40, success_bonus=55, crash=120, out=150, ttc_threshold=12, stage2_success=0.50, stage2_cost=0.25, demote_cost=0.35.
- Evaluation CSV: outputs/tuning_proposed_defensive_h1500_lane1_out150_cost50_nenv16_1m/evaluations/proposed_ppo_s0.csv; summary.csv exists.
- d0.00: success=0.96 cost=0.00 collision=0.00 out=0.00 route=0.988 shield=0.868.
- d0.08: success=0.88 cost=0.10 collision=0.10 out=0.00 route=0.965 shield=0.850.
- d0.15: success=0.70 cost=0.24 collision=0.22 out=0.02 route=0.872 shield=0.712.
- Comparison: vs standard proposed seed0 d0.15 improved from success=0.48/cost=0.42/route=0.791 to success=0.70/cost=0.24/route=0.872. Vs h1500 cost50 seed0 improved from success=0.54/cost=0.34/out=0.10 to success=0.70/cost=0.24/out=0.02.
- Interpretation: moderate lane penalty plus stronger out-of-road penalty fixes the lane2/v16 low-motion failure and materially reduces high-density cost while preserving route completion. The remaining d0.15 failures are mostly collision (0.22), not out-of-road.
- Gate result: PROMOTE TO CANDIDATE, not final. Expand seeds 1 and 2 with the same n_envs=16 protocol before freezing paper-facing results. If seed1/2 mean d0.15 remains success>=0.60 and cost<=0.28, use this as the main proposed setting and start ablations/comparisons against it.

## 2026-06-30 launch candidate lane1/out150 seed1-2 nenv16 replication
- Time: 2026-06-30T17:58:25+08:00
- Roots: outputs/candidate_lane1_out150_cost50_nenv16_seed1_1m and outputs/candidate_lane1_out150_cost50_nenv16_seed2_1m.
- Protocol: proposed seeds 1 and 2, n_envs=16, timesteps=1M, horizon=1500, ent_coef=0.01, reward_ttc=6, reward_cost=50, reward_lane=1.0, target_speed=18, progress=40, success_bonus=55, crash=120, out=150, ttc_threshold=12, stage2_success=0.50, stage2_cost=0.25, demote_cost=0.35.
- Reason: seed0 promoted to candidate with d0.15 success=0.70/cost=0.24/out=0.02, but paper-facing main proposed setting requires multi-seed replication.
- Run policy: use independent roots for seed1/seed2 to avoid parallel root-level figure/report write conflicts; aggregate after both finish.

## 2026-06-30 candidate lane1/out150 seed1-2 monitor at ~600k
- Time: 2026-06-30T18:04:12+08:00
- Roots: outputs/candidate_lane1_out150_cost50_nenv16_seed1_1m and outputs/candidate_lane1_out150_cost50_nenv16_seed2_1m.
- Resource status: parallel n_envs=16 + n_envs=16 remains safe; GPU free about 10.5GB, CPU memory available about 21GB.
- Seed1 status: checkpoint_500000_steps.zip exists; by ~590k reached stage2, window_success about 0.667 at one check, rollout success_rate about 0.40, cost near 0.00-0.03.
- Seed2 status: checkpoint_500000_steps.zip exists; by ~590k reached stage2 once, then stage1/2 fluctuation; rollout success_rate about 0.28-0.32, cost about 0.10.
- Interpretation: both seeds had a slow stage0 start but recovered, so this is not the lane2/v16 idle collapse. Continue to 750k/final held-out evaluation.

## 2026-06-30 candidate lane1/out150 seed0-2 aggregate completed
- Time: 2026-06-30T18:17:01+08:00
- Aggregate root: outputs/candidate_lane1_out150_cost50_nenv16_aggregate.
- Files: summary_by_seed.csv, mean_by_density.csv, DECISION.md.
- Sources: seed0 from outputs/tuning_proposed_defensive_h1500_lane1_out150_cost50_nenv16_1m/evaluations/summary.csv; seed1/2 from outputs/candidate_lane1_out150_cost50_nenv16_seed1_1m and seed2_1m.
- d0.00 mean: success=0.973, cost=0.000, route=0.989.
- d0.08 mean: success=0.833, cost=0.133, collision=0.127, out=0.007, route=0.929.
- d0.15 mean: success=0.620, cost=0.247, collision=0.233, out=0.013, route=0.865.
- Variance warning: d0.15 success std=0.122 and seed2 is weak (success=0.48, cost=0.32). This is acceptable as current best only because the three-seed mean passes the promotion gate, not because every seed is clean.
- Decision: keep lane1/out150/cost50 as current main-method candidate and start ablations/comparisons around it. Remaining bottleneck is high-density collision, not out-of-road.

## 2026-06-30 launch tuned-protocol comparison/ablation seed0 batch A
- Time: 2026-06-30T18:18:25+08:00
- Runs launched: baseline seed0 and proposed_wo_ttc seed0.
- Roots: outputs/tuned_compare_baseline_nenv16_seed0_1m and outputs/tuned_ablation_wo_ttc_nenv16_seed0_1m.
- Protocol: n_envs=16, timesteps=1M, horizon=1500, ent_coef=0.01, target_speed=18, progress=40, cost=50, lane=1.0 where applicable, success_bonus=55, crash=120, out=150, stage2_success=0.50, stage2_cost=0.25, demote_cost=0.35.
- Important ablation detail: proposed_wo_ttc intentionally omits --reward-ttc so get_variant_config keeps TTC weight at 0.0; all other tuned reward/curriculum settings match the candidate.
- Purpose: baseline tests vanilla PPO under same horizon; proposed_wo_ttc tests whether TTC risk term is needed for the high-density safety-success tradeoff.

## 2026-06-30 tuned-protocol proposed_wo_ttc seed0 nenv16 completed
- Time: 2026-06-30T18:38:32.
- Root: outputs/tuned_ablation_wo_ttc_nenv16_seed0_1m.
- Protocol: proposed_wo_ttc seed0, n_envs=16, timesteps=1M, horizon=1500, ent_coef=0.01, target_speed=18, progress=40, cost=50, lane=1.0, success_bonus=55, crash=120, out=150, stage2_success=0.50, stage2_cost=0.25, demote_cost=0.35.
- Config check: reward_ttc=0.0 by variant; action guard and curriculum stay enabled. This is the intended TTC reward ablation, not a mistaken low-TTC full method.
- CSV: outputs/tuned_ablation_wo_ttc_nenv16_seed0_1m/evaluations/summary.csv.
- d0.00: success=1.00 cost=0.00 collision=0.00 out=0.00 route=0.992.
- d0.08: success=0.92 cost=0.04 collision=0.04 out=0.00 route=0.975.
- d0.15: success=0.44 cost=0.54 collision=0.54 out=0.00 route=0.743.
- Comparison to full tuned proposed seed0: full d0.15 success=0.70 cost=0.24 collision=0.22 out=0.02 route=0.872; removing TTC drops success by 0.26 and increases collision/cost by about 0.30.
- Interpretation: TTC reward is important specifically for dense-traffic collision suppression. The ablation can look strong at easy/medium density, but it fails the paper-relevant high-density safety-success tradeoff.
- Decision: keep TTC in the main method. Do not expand proposed_wo_ttc to more seeds until baseline/risk/curriculum/no_action_guard seed0 comparisons are available, unless the paper explicitly needs a three-seed TTC ablation table.

## 2026-06-30 tuned-protocol baseline seed0 nenv16 completed
- Time: 2026-06-30T18:44:31.
- Root: outputs/tuned_compare_baseline_nenv16_seed0_1m.
- Protocol: baseline seed0, n_envs=16, timesteps=1M, horizon=1500, ent_coef=0.01, same evaluation densities and episode budget as tuned proposed.
- Config check: use_risk_reward=False, use_action_guard=False, curriculum=False. Reward CLI values are recorded for protocol parity but are not active in baseline shaping.
- CSV: outputs/tuned_compare_baseline_nenv16_seed0_1m/evaluations/summary.csv.
- d0.00: success=0.02 cost=0.98 collision=0.00 out=0.98 route=0.302.
- d0.08: success=0.00 cost=1.00 collision=0.40 out=0.60 route=0.234.
- d0.15: success=0.00 cost=1.00 collision=0.62 out=0.38 route=0.177.
- Comparison to full tuned proposed seed0: full d0.15 success=0.70 cost=0.24 route=0.872; baseline d0.15 success=0.00 cost=1.00 route=0.177.
- Interpretation: vanilla PPO under this 1M/h1500/n_envs16 protocol fails even at easy density, mostly by leaving the road at d0.00 and by mixed collision/out failures under traffic. This is a strong main-comparison baseline, not a competitive candidate.
- Decision: do not expand baseline seeds immediately. Next batch should isolate mechanisms: risk without curriculum and no_action_guard under the same tuned reward/curriculum settings.

## 2026-06-30 launch tuned-protocol comparison/ablation seed0 batch B
- Time: 2026-06-30T18:45:43.
- Runs launched: risk seed0 and no_action_guard seed0.
- Roots: outputs/tuned_compare_risk_nenv16_seed0_1m and outputs/tuned_ablation_no_action_guard_nenv16_seed0_1m.
- Protocol: n_envs=16, timesteps=1M, horizon=1500, ent_coef=0.01, reward_ttc=6, reward_cost=50, overspeed=3, target_speed=18, progress=40, lane=1.0, success_bonus=55, crash=120, out=150, ttc_threshold=12, stage2_success=0.50, stage2_cost=0.25, demote_cost=0.35.
- Purpose: risk tests risk reward + action guard without curriculum; no_action_guard tests tuned reward + curriculum without action guard. Together with baseline and proposed_wo_ttc, these isolate the main paper mechanisms.
- Resource check after launch: two n_envs=16 jobs active; GPU and system memory remain within safe range.
- Next monitor: verify config JSON/logs, then check early learning around 100k/250k. Kill early only if a true collapse appears (idle/zero-route or config mismatch), otherwise evaluate to final CSV.

## 2026-06-30 batch B early config and health check
- Time: 2026-06-30T18:47:22.
- risk config verified: variant=risk, n_envs=16, horizon=1500, timesteps=1M, ent_coef=0.01, use_risk_reward=True, use_action_guard=True, curriculum=False, reward_ttc=6, cost=50, lane=1.0, target_speed=18, progress=40, success_bonus=55, crash=120, out=150, ttc_threshold=12.
- no_action_guard config verified: variant=no_action_guard, n_envs=16, horizon=1500, timesteps=1M, ent_coef=0.01, use_risk_reward=True, use_action_guard=False, curriculum=True, same tuned reward weights.
- risk early signal around 115k: mean_speed below 1 km/h, route about 0.058, success=0, cost=0. This may be low-motion collapse caused by risk/guard without curriculum; wait until 250k-300k before deciding.
- no_action_guard early signal around 180k: stage0, route about 0.19-0.25, speed about 1.4 km/h, success=0, window_cost about 0.10. Slow but not yet a confirmed collapse.
- Decision: continue both to the next monitor. Do not tune parameters mid-run because these are mechanism comparisons; only stop early if the trajectory remains idle/zero-route and cannot produce meaningful paper evidence.

## 2026-06-30 batch B monitor at risk~328k no_action_guard~475k
- Time: 2026-06-30T18:50:26.
- risk: checkpoint_250000 exists; around 295k-328k still no curriculum, success_rate=0, episode length near 1500, mean_speed about 0.5-0.6 km/h, route about 0.02-0.03, cost=0. This is low-motion collapse, likely because risk reward + guard without curriculum over-penalizes motion.
- Decision for risk: continue to final CSV rather than kill, because the failure itself is a useful comparison showing why curriculum/staging is needed.
- no_action_guard: checkpoint_250000 exists; around 442k-475k reached stage2, rollout success_rate about 0.30-0.38, speed about 8-10 km/h, recent cost=0, route samples around 0.45-0.78.
- Decision for no_action_guard: continue to final CSV. It is viable enough that the key question is high-density collision/cost without the guard, not learning collapse.

## 2026-06-30 batch B completed: risk and no_action_guard seed0 nenv16
- Time: 2026-06-30T19:03:02.
- risk root: outputs/tuned_compare_risk_nenv16_seed0_1m; summary CSV exists.
- risk config: use_risk_reward=True, use_action_guard=True, curriculum=False. It isolates risk reward + guard without curriculum.
- risk d0.00/d0.08/d0.15: success=0.00 at all densities, cost=0.00 at all densities, route about 0.009, speed about 0.013 km/h, episode_length=1500. Interpretation: low-motion/idle collapse, not a usable policy. Curriculum/staging is necessary to make the risk+guard mechanism move.
- no_action_guard root: outputs/tuned_ablation_no_action_guard_nenv16_seed0_1m; summary CSV exists.
- no_action_guard config: use_risk_reward=True, use_action_guard=False, curriculum=True. It isolates action guard removal under the tuned reward/curriculum protocol.
- no_action_guard d0.00: success=0.08 cost=0.92 collision=0.00 out=0.92 route=0.295.
- no_action_guard d0.08: success=0.00 cost=1.00 collision=0.32 out=0.68 route=0.177.
- no_action_guard d0.15: success=0.00 cost=1.00 collision=0.46 out=0.54 route=0.171.
- Comparison to full tuned proposed seed0 d0.15: full success=0.70 cost=0.24 route=0.872; no_action_guard success=0.00 cost=1.00 route=0.171; risk success=0.00 cost=0.00 route=0.008.
- Paper interpretation: action guard is necessary to prevent high-speed out-of-road/collision evaluation failure, while curriculum is necessary to prevent risk+guard from becoming an idle safe-but-useless policy.
- Decision: do not expand risk or no_action_guard seeds now. Next run curriculum-only and guard_only to complete mechanism decomposition before deciding which ablations need multi-seed replication.

## 2026-06-30 launch tuned-protocol comparison/ablation seed0 batch C
- Time: 2026-06-30T19:03:49.
- Runs launched: curriculum seed0 and guard_only seed0.
- Roots: outputs/tuned_compare_curriculum_nenv16_seed0_1m and outputs/tuned_ablation_guard_only_nenv16_seed0_1m.
- Protocol: n_envs=16, timesteps=1M, horizon=1500, ent_coef=0.01, same tuned reward CLI values and evaluation protocol as the current main candidate.
- Purpose: curriculum isolates staged learning without risk reward/action guard; guard_only isolates action guard + curriculum without risk reward. These complete the seed0 mechanism decomposition with baseline, risk, no_action_guard, and proposed_wo_ttc.
- Next monitor: verify configs and early learning; continue unless there is a config mismatch or persistent zero-motion collapse.

## 2026-06-30 batch C early config and health check
- Time: 2026-06-30T19:05:45.
- curriculum config verified: use_risk_reward=False, use_action_guard=False, curriculum=True; n_envs=16, horizon=1500, timesteps=1M.
- guard_only config verified: use_risk_reward=False, use_action_guard=True, curriculum=True; n_envs=16, horizon=1500, timesteps=1M.
- curriculum around 213k: stage2 reached, window_success about 0.53, route window about 0.84, but recent out_of_road cost appears. It learns movement faster than baseline/risk but may lack safety control.
- guard_only around 197k: stage2 reached, window_success about 0.57, route window about 0.76, but recent out_of_road also appears. Guard helps movement relative to risk-only, but risk reward contribution still needs final eval.
- Decision: continue both to final CSV. These are mechanism comparisons and should not be tuned mid-run.

## 2026-06-30 batch C monitor at ~475k
- Time: 2026-06-30T19:11:41.
- curriculum: around 425k-475k, success_rate rises to about 0.50, stage2 reached, but window_cost is high (about 0.33-0.57) with both out_of_road and collision samples. Interpretation: curriculum alone can induce movement/success but lacks safety shaping/guarding.
- guard_only: around 425k-475k, stage3 reached with long route samples and low immediate cost, but rollout success_rate remains low around 0.04-0.06. Interpretation: guard+curriculum without risk reward may be safer than curriculum-only but has weak completion/success behavior.
- Decision: continue both to final CSV. The mid-run difference is mechanistically useful and should be verified under held-out density evaluation.

## 2026-06-30 batch C completed: curriculum and guard_only seed0 nenv16
- Time: 2026-06-30T19:26:49.
- curriculum root: outputs/tuned_compare_curriculum_nenv16_seed0_1m; summary CSV exists.
- curriculum config: use_risk_reward=False, use_action_guard=False, curriculum=True.
- curriculum d0.00: success=0.02 cost=0.98 collision=0.00 out=0.98 route=0.350.
- curriculum d0.08: success=0.00 cost=1.00 collision=0.32 out=0.68 route=0.256.
- curriculum d0.15: success=0.00 cost=1.00 collision=0.56 out=0.44 route=0.176.
- Interpretation: curriculum alone induces movement during training, but final evaluation fails by high-speed out-of-road/collision. Curriculum is not sufficient without the guard/safety mechanism.
- guard_only root: outputs/tuned_ablation_guard_only_nenv16_seed0_1m; summary CSV exists.
- guard_only config: use_risk_reward=False, use_action_guard=True, curriculum=True.
- guard_only d0.00: success=1.00 cost=0.00 route=0.992 shield_intervention_rate=0.872.
- guard_only d0.08: success=0.86 cost=0.08 collision=0.08 out=0.00 route=0.954 shield_intervention_rate=0.852.
- guard_only d0.15: success=0.62 cost=0.22 collision=0.20 out=0.02 route=0.861 shield_intervention_rate=0.728.
- Comparison to full tuned proposed seed0: full d0.15 success=0.70 cost=0.24 route=0.872. Guard_only is close: slightly lower success (-0.08), slightly lower cost (-0.02), similar route.
- Paper-risk interpretation: the guard+curriculum component explains a large part of the current seed0 gain. The risk reward contribution is positive on seed0 for high-density success, but not yet proven robust enough as a standalone claim.
- Decision: promote guard_only to critical comparison. Run guard_only seeds 1 and 2 before claiming the full method beats simpler guard+curriculum. If guard_only mean matches/exceeds full proposed, either retune the full risk reward or shift the paper claim toward guard/curriculum as the main mechanism.

## 2026-06-30 launch critical guard_only seed1-2 replication
- Time: 2026-06-30T19:27:33.
- Reason: guard_only seed0 is close to full tuned proposed seed0, so this is no longer a routine ablation. It must be replicated before writing the paper mechanism claim.
- Roots: outputs/tuned_ablation_guard_only_nenv16_seed1_1m and outputs/tuned_ablation_guard_only_nenv16_seed2_1m.
- Protocol: guard_only seeds 1 and 2, n_envs=16, timesteps=1M, horizon=1500, ent_coef=0.01, same tuned CLI reward values/evaluation protocol as full proposed candidate.
- Decision rule: compare three-seed guard_only aggregate against full proposed aggregate at d0.15. If guard_only mean is comparable or better, retune the full method or rewrite the claim so the core mechanism is guard+curriculum rather than risk reward alone.

## 2026-06-30 guard_only seed1-2 early config and health check
- Time: 2026-06-30T19:29:29.
- seed1 config verified: variant=guard_only, use_risk_reward=False, use_action_guard=True, curriculum=True, n_envs=16, horizon=1500, timesteps=1M.
- seed2 config verified: same protocol and switches as seed1.
- seed1 around 197k: reached stage2, window_success about 0.53, window_cost about 0.07, route window about 0.78. Healthy early learning.
- seed2 around 213k: still stage1, window_success about 0.17-0.30, window_cost about 0.37, route window about 0.59. Higher early cost than seed1 but not a confirmed collapse.
- Decision: continue both to final evaluation; guard_only is a critical comparison, so do not stop on ordinary seed variability.

## 2026-06-30 guard_only seed1-2 monitor at ~557k
- Time: 2026-06-30T19:35:56.
- seed1: around 524k-557k, stage2, window_cost about 0.03, route window about 0.82-0.83, rollout success_rate about 0.14-0.18, long route samples but many non-success timeouts.
- seed2: around 524k-557k, stage2, window_cost about 0.03-0.07, route window about 0.82-0.84, rollout success_rate about 0.12-0.18.
- Interpretation: both seeds show a guard_only pattern of low cost and long route completion, but weak success conversion at mid-training. This makes final held-out evaluation decisive.
- Decision: continue both to final CSV and aggregate guard_only seed0-2 before changing the main claim.

## 2026-06-30 guard_only seed0-2 aggregate completed
- Time: 2026-06-30T19:53:00.
- Aggregate root: outputs/tuned_ablation_guard_only_nenv16_aggregate.
- Files: summary_by_seed.csv, mean_by_density.csv, std_by_density.csv, compare_to_full_proposed_mean.csv, DECISION.md.
- Guard_only d0.00 mean: success=0.973 cost=0.000 route=0.990.
- Guard_only d0.08 mean: success=0.873 cost=0.093 collision=0.093 out=0.000 route=0.940.
- Guard_only d0.15 mean: success=0.633 cost=0.207 collision=0.200 out=0.007 route=0.868.
- Comparison to full proposed aggregate: at d0.15 guard_only is +0.013 success, -0.040 cost, +0.003 route, -0.033 collision, -0.007 out_of_road relative to current full proposed.
- Interpretation: the current full risk-reward setting does not beat guard+curriculum. The paper claim must not state that the risk reward is the dominant improvement under the current evidence.
- Decision: launch a light-risk full proposed retuning screen. Goal: retain the stability of guard_only while recovering any high-density success gain from a milder TTC/cost reward. If light-risk does not beat guard_only, reframe the main method around guard+curriculum and treat risk reward as optional/diagnostic.

## 2026-06-30 launch light-risk full proposed seed0 and seed2
- Time: 2026-06-30T19:53:49.
- Reason: guard_only seed0-2 aggregate matches/exceeds the current full proposed aggregate, so the full risk reward setting must be retuned before paper claims are frozen.
- Roots: outputs/tuning_proposed_light_risk_ttc3_cost25_lane03_nenv16_seed0_1m and outputs/tuning_proposed_light_risk_ttc3_cost25_lane03_nenv16_seed2_1m.
- Protocol: proposed seeds 0 and 2, n_envs=16, timesteps=1M, horizon=1500, ent_coef=0.01.
- Light-risk weights: ttc=3, cost=25, lane=0.3, crash=80, out=150, overspeed=3, target_speed=18, progress=40, success_bonus=55, ttc_threshold=12, stage2_success=0.50, stage2_cost=0.25, demote_cost=0.35.
- Purpose: keep guard+curriculum stability while adding milder risk shaping. Seed0 checks that the strong seed is not harmed; seed2 targets the weak seed in the current full proposed aggregate.
- Promotion rule: light-risk must beat guard_only aggregate at d0.15 or at least improve full proposed seed2 materially without hurting seed0. Otherwise the paper main line should pivot toward guard+curriculum.

## 2026-06-30 light-risk seed0/2 early config and health check
- Time: 2026-06-30T19:55:48.
- Config verified for both seeds: variant=proposed, use_risk_reward=True, use_action_guard=True, curriculum=True, n_envs=16, horizon=1500, timesteps=1M.
- Light-risk weights verified: ttc=3, cost=25, lane=0.3, crash=80, out=150, target_speed=18, progress=40, success_bonus=55.
- seed0 around 246k: stage1, window_cost about 0.03, route window about 0.60, rollout success_rate about 0.10. It is slower than guard_only but not collapsed.
- seed2 around 246k: still stage0, window_success=0, route window about 0.44, cost fluctuating but not catastrophic. This is weaker than desired and must be watched closely.
- Decision: continue to 500k before judging. If seed2 remains stage0/zero-success at 500k, light-risk is likely not solving the weak-seed issue.

## 2026-06-30 light-risk full proposed seed0/2 completed and rejected as main setting
- Time: 2026-06-30T20:15:44+08:00.
- Aggregate root: outputs/tuning_proposed_light_risk_ttc3_cost25_lane03_nenv16_aggregate.
- Files: summary_by_seed.csv, mean_by_density.csv, std_by_density.csv, compare_to_full_proposed_mean.csv, compare_to_guard_only_mean.csv, DECISION.md.
- Final seed0: d0.00 success=0.98 cost=0.00 route=0.991; d0.08 success=0.90 cost=0.06 collision=0.06 route=0.956; d0.15 success=0.64 cost=0.28 collision=0.26 out=0.02 route=0.859.
- Final seed2: d0.00 success=0.96 cost=0.00 route=0.990; d0.08 success=0.86 cost=0.12 collision=0.12 route=0.930; d0.15 success=0.52 cost=0.30 collision=0.30 out=0.00 route=0.821.
- Light-risk mean over seeds 0 and 2: d0.00 success=0.970 cost=0.000 route=0.990; d0.08 success=0.880 cost=0.090 route=0.943; d0.15 success=0.580 cost=0.290 collision=0.280 out=0.010 route=0.840.
- Comparison to guard_only 3-seed aggregate: at d0.08 light-risk is roughly comparable/slightly higher success, but at d0.15 it is worse (success 0.580 vs 0.633, cost 0.290 vs 0.207, collision 0.280 vs 0.200, route 0.840 vs 0.868).
- Comparison to current full proposed 3-seed aggregate: light-risk improves d0.08 but worsens d0.15 (success 0.580 vs 0.620, cost 0.290 vs 0.247, route 0.840 vs 0.865).
- Interpretation: milder TTC/cost/lane risk shaping did not solve the high-density weak-seed issue. The current evidence still says guard+curriculum is the robust mechanism; risk reward is not ready to be claimed as the dominant gain.
- Decision: do not promote this light-risk full setting. Run missing reward-component ablations next (`proposed_wo_lane`, `proposed_wo_smooth`) under the tuned full-proposed protocol, with CLI overrides chosen so the intended zeroed reward terms are not accidentally restored.

## 2026-06-30 launch reward-component ablations wo_lane and wo_smooth seed0
- Time: 2026-06-30T20:17:25+08:00.
- Roots: outputs/tuned_ablation_wo_lane_nenv16_seed0_1m and outputs/tuned_ablation_wo_smooth_nenv16_seed0_1m.
- Protocol: n_envs=16, timesteps=1M, horizon=1500, EPISODES=50, DEVICE=cuda, ent_coef=0.01, stage2_success=0.50, stage2_cost=0.25, demote_cost=0.35.
- Shared tuned full-proposed weights: ttc=6, cost=50, overspeed=3, target_speed=18, progress=40, success_bonus=55, crash=120, out_of_road=150, ttc_threshold=12.
- proposed_wo_lane config verified: variant=proposed_wo_lane, use_risk_reward=True, use_action_guard=True, curriculum=True, lane=0.0, smooth=0.02, accel=0.01.
- proposed_wo_smooth config verified: variant=proposed_wo_smooth, use_risk_reward=True, use_action_guard=True, curriculum=True, lane=1.0, smooth=0.0, accel=0.0.
- Early health at about 82k: both runs alive on GPU, still stage0 with success=0 and low route completion. This is treated as normal cold start; next checkpoint is around 250k before intervention.
- Purpose: complete reward-component ablations without accidentally restoring the ablated CLI weights. These results will support whether lane keeping and smoothness terms are material or mostly cosmetic relative to TTC/cost/guard/curriculum.

## 2026-06-30 reward-component ablations monitor at ~350k
- Time: 2026-06-30T20:19:59+08:00.
- proposed_wo_lane: around 344k, stage1, window_success about 0.30, rollout success_rate about 0.35, route window about 0.62, window_cost about 0.17. It is learning despite lane=0, but lane_deviation is visibly high in samples (about 0.4-1.0), so final eval should reveal whether lane reward mainly improves tracking/stability rather than raw success.
- proposed_wo_smooth: around 393k, still stage0, window_success=0, route window about 0.23, speed about 1.5 km/h, no cost yet. This looks like a real ablation degradation from removing smooth/accel regularization, not a launch/config failure.
- Decision: do not tune or rescue these ablations mid-run, because the purpose is to measure component removal under the same tuned full-proposed protocol. Continue to final held-out summary.csv and then decide whether to replicate with more seeds.

## 2026-06-30 reward-component ablation seed0 completed
- Time: 2026-06-30T20:35:35+08:00.
- Aggregate root: outputs/tuned_reward_component_ablation_seed0_aggregate.
- Files: seed0_component_ablation_summary.csv, deltas_vs_full_seed0.csv, DECISION.md.
- full_proposed seed0 d0.15: success=0.70, cost=0.24, collision=0.22, route=0.872.
- wo_ttc seed0 d0.15: success=0.44, cost=0.54, collision=0.54, route=0.743.
- wo_lane seed0 d0.15: success=0.60, cost=0.28, collision=0.28, route=0.862, lane_deviation=0.348.
- wo_smooth seed0 d0.15: success=0.58, cost=0.24, collision=0.24, route=0.849.
- Interpretation: TTC removal is the strongest reward-term degradation; lane removal mainly harms lateral tracking and high-density safety/success; smooth/accel removal weakens high-density success and training conversion but is less catastrophic than expected from mid-run.
- Decision: replicate at least wo_ttc beyond seed0 and add shield_only seed0 next. Do not overclaim reward terms from a single-seed table.

## 2026-06-30 launch wo_ttc seed1 and shield_only seed0
- Time: 2026-06-30T20:37:50+08:00.
- Roots: outputs/tuned_ablation_wo_ttc_nenv16_seed1_1m and outputs/tuned_compare_shield_only_nenv16_seed0_1m.
- proposed_wo_ttc seed1 config verified: use_risk_reward=True, use_action_guard=True, curriculum=True, n_envs=16, horizon=1500, timesteps=1M, ttc=0.0, lane=1.0, cost=50, crash=120, out=150.
- shield_only seed0 config verified: use_risk_reward=False, use_action_guard=True, curriculum=False, n_envs=16, horizon=1500, timesteps=1M.
- Early health: both alive on GPU. proposed_wo_ttc is still stage0/cold-start around 115k. shield_only has no curriculum and already shows the expected low-speed/low-route pattern: route about 0.06-0.07, success=0, one out-of-road sample.
- Purpose: replicate the strongest reward-term negative effect beyond seed0 and isolate whether the action guard alone can work without curriculum.
- Decision: continue both to final evaluation; do not tune shield_only because its role is a mechanism control, not a candidate method.

## 2026-06-30 wo_ttc seed1 and shield_only seed0 completed
- Time: 2026-06-30T21:00:21+08:00.
- wo_ttc aggregate root: outputs/tuned_ablation_wo_ttc_nenv16_seed0_seed1_aggregate.
- proposed_wo_ttc seed1 d0.15: success=0.66, cost=0.20, collision=0.20, route=0.905. This contradicts the seed0-only interpretation that TTC removal always collapses high-density performance.
- proposed_wo_ttc seed0-1 mean d0.15: success=0.550, cost=0.370, collision=0.370, route=0.824.
- shield_only seed0: d0.00 success=1.00 cost=0.00 route=0.992; d0.08 success=0.96 cost=0.04 collision=0.02 out=0.02 route=0.975; d0.15 success=0.56 cost=0.32 collision=0.32 out=0.00 route=0.833.
- Interpretation: action guard alone is a major mechanism and is very strong up to medium density, but high-density safety/success still lags guard_only/full. TTC reward contribution is high-variance across seeds and must not be overclaimed from seed0.
- Decision: launch proposed_wo_ttc seed2 and shield_only seed1 next. This resolves TTC variance and checks shield_only stability.

## 2026-06-30 launch wo_ttc seed2 and shield_only seed1
- Time: 2026-06-30T21:02:21+08:00.
- Roots: outputs/tuned_ablation_wo_ttc_nenv16_seed2_1m and outputs/tuned_compare_shield_only_nenv16_seed1_1m.
- proposed_wo_ttc seed2 config verified: use_risk_reward=True, use_action_guard=True, curriculum=True, n_envs=16, horizon=1500, timesteps=1M, ttc=0.0, lane=1.0, cost=50, crash=120, out=150.
- shield_only seed1 config verified: use_risk_reward=False, use_action_guard=True, curriculum=False, n_envs=16, horizon=1500, timesteps=1M.
- Early health: both runs alive on GPU. proposed_wo_ttc seed2 is cold-start stage0 around 131k. shield_only seed1 is still early and shows lower stability than seed0 with out-of-road samples; this is not yet a final judgement.
- Purpose: resolve the high variance between wo_ttc seed0 and seed1, and test whether shield_only seed0's strong medium-density result is seed-stable.


## 2026-06-30 wo_ttc seed2 completed and three-seed aggregate written
- Time: 2026-06-30T21:20:19+08:00.
- New aggregate root: outputs/tuned_ablation_wo_ttc_nenv16_seed0_seed1_seed2_aggregate.
- Files: summary_by_seed.csv, mean_by_density.csv, std_by_density.csv, compare_to_full_proposed_mean.csv, compare_to_guard_only_mean.csv, DECISION.md.
- proposed_wo_ttc seed2 final: d0.00 success=0.96 cost=0.00 route=0.990; d0.08 success=0.96 cost=0.04 collision=0.04 route=0.959; d0.15 success=0.52 cost=0.34 collision=0.34 route=0.821.
- Three-seed wo_ttc mean: d0.00 success=0.987 cost=0.000 route=0.991; d0.08 success=0.900 cost=0.067 collision=0.067 route=0.950; d0.15 success=0.540 cost=0.360 collision=0.360 route=0.823.
- Comparison to full proposed aggregate at d0.15: success 0.540 vs 0.620, cost 0.360 vs 0.247, route 0.823 vs 0.865. Removing TTC is worse on average in dense traffic.
- Comparison to guard_only aggregate at d0.15: success 0.540 vs 0.633, cost 0.360 vs 0.207, route 0.823 vs 0.868. The TTC-ablated full method is also weaker than guard+curriculum in dense traffic.
- Interpretation: TTC reward contribution is high-variance but negative when removed at d0.15. Claim boundary: TTC reward helps dense-traffic robustness on average; do not claim it is universally necessary or that risk reward dominates guard+curriculum.
- Active run still in progress: outputs/tuned_compare_shield_only_nenv16_seed1_1m. Current decision is to wait for shield_only seed1 before starting shield_only seed2 or additional reward ablation seeds.

## 2026-06-30 shield_only seed1 completed and seed0-1 interim aggregate written
- Time: 2026-06-30T21:25:29+08:00.
- New aggregate root: outputs/tuned_compare_shield_only_nenv16_seed0_seed1_aggregate.
- Files: summary_by_seed.csv, mean_by_density.csv, std_by_density.csv, compare_to_full_proposed_mean.csv, compare_to_guard_only_mean.csv, DECISION.md.
- shield_only seed1 final: d0.00 success=0.98 cost=0.00 route=0.991; d0.08 success=0.92 cost=0.08 collision=0.06 out=0.02 route=0.944; d0.15 success=0.56 cost=0.22 collision=0.22 route=0.867.
- shield_only seed0-1 mean: d0.00 success=0.990 cost=0.000 route=0.991; d0.08 success=0.940 cost=0.060 collision=0.040 out=0.020 route=0.960; d0.15 success=0.560 cost=0.270 collision=0.270 route=0.850.
- Interpretation: action guard alone is seed-stable enough to require a seed2 follow-up. It is very strong at easy/medium densities and still meaningful at high density, though high-density success remains below full proposed/guard_only means.
- Decision: launch shield_only seed2 next. Also begin proposed_wo_lane seed1 while the GPU is free, because lane reward ablation currently has only seed0 evidence.

## 2026-06-30 launch/config check shield_only seed2 and wo_lane seed1
- Time: 2026-06-30T21:27:13+08:00.
- Active roots: outputs/tuned_compare_shield_only_nenv16_seed2_1m and outputs/tuned_ablation_wo_lane_nenv16_seed1_1m.
- Launch protocol: n_envs=16, timesteps=1M, horizon=1500, EPISODES=50, DEVICE=cuda, ent_coef=0.01.
- shield_only seed2 config verified: variant=shield_only, seed=2, use_risk_reward=False, use_action_guard=True, curriculum=False. This completes the planned third seed for the action-guard-only mechanism control.
- proposed_wo_lane seed1 config verified: variant=proposed_wo_lane, seed=1, use_risk_reward=True, use_action_guard=True, curriculum=True, reward_weights.lane=0.0, ttc=6.0, smooth=0.02, accel=0.01, cost=50.0, crash=120.0, out=150.0.
- Early health: both processes alive. shield_only seed2 is in normal cold-start low-speed/low-route behavior. wo_lane seed1 shows high lane deviation/out-of-road risk early, which is expected for lane reward removal and should not be rescued mid-run unless it becomes a launch/config failure.
- Next checkpoint: inspect around 250k-350k timesteps for stage transition, cost window, and route/success trend; do not retune these controls before final evaluation unless the run crashes or config is wrong.

## 2026-06-30 mid-run health shield_only seed2 and wo_lane seed1
- Time: 2026-06-30T21:31:54+08:00.
- shield_only seed2 around 344k: no config/process issue; success_rate about 0.30, route samples up to about 0.99, some out-of-road/cost remains. This matches the seed0/1 recovery pattern and should continue to final evaluation.
- proposed_wo_lane seed1 around 623k: reached curriculum stage2, window_success about 0.30, window_cost about 0.067, window_route about 0.82. Lane deviation remains high in samples (roughly 0.38-0.50 recently, max up to 2.0), which is expected evidence for lane reward removal rather than a launch failure.
- Decision: continue both runs unchanged. No reward rescue or retune before final summaries because both are mechanism/ablation controls.

## 2026-06-30 wo_lane seed1 completed and seed0-1 aggregate written
- Time: 2026-06-30T21:43:33+08:00.
- New aggregate root: outputs/tuned_ablation_wo_lane_nenv16_seed0_seed1_aggregate.
- Files: summary_by_seed.csv, mean_by_density.csv, std_by_density.csv, compare_to_full_proposed_mean.csv, DECISION.md.
- proposed_wo_lane seed1 final: d0.00 success=0.88 cost=0.00 route=0.987 lane_dev=0.347; d0.08 success=0.90 cost=0.10 collision=0.10 route=0.971 lane_dev=0.322; d0.15 success=0.62 cost=0.28 collision=0.28 route=0.856 lane_dev=0.340.
- wo_lane seed0-1 mean: d0.00 success=0.940 cost=0.000 route=0.990 lane_dev=0.347; d0.08 success=0.900 cost=0.080 collision=0.080 route=0.964 lane_dev=0.341; d0.15 success=0.610 cost=0.280 collision=0.280 route=0.859 lane_dev=0.344.
- Interpretation: lane reward removal is seed-stable. It does not collapse success, but it consistently produces much higher lane deviation and slightly worse high-density cost/route than full proposed.
- Decision: do not tune wo_lane. Next reward-component replication priority is proposed_wo_smooth seed1, while shield_only seed2 continues to final evaluation.

## 2026-06-30 launch/config check wo_smooth seed1
- Time: 2026-06-30T21:44:26+08:00.
- Root: outputs/tuned_ablation_wo_smooth_nenv16_seed1_1m.
- Launch protocol: proposed_wo_smooth seed1, n_envs=16, timesteps=1M, horizon=1500, EPISODES=50, DEVICE=cuda, ent_coef=0.01.
- Config verified: use_risk_reward=True, use_action_guard=True, curriculum=True, reward_weights.ttc=6.0, lane=1.0, smooth=0.0, accel=0.0, cost=50.0, crash=120.0, out=150.0.
- Early health: alive, stage0/cold-start, success_rate=0. This is expected for a new reward-component ablation and should not be rescued before mid-run evidence.
- Active concurrent run: shield_only seed2 is still training and should be evaluated/aggregated when complete.

## 2026-06-30 shield_only seed2 completed and three-seed aggregate written
- Time: 2026-06-30T21:50:06+08:00.
- New aggregate root: outputs/tuned_compare_shield_only_nenv16_seed0_seed1_seed2_aggregate.
- Files: summary_by_seed.csv, mean_by_density.csv, std_by_density.csv, compare_to_full_proposed_mean.csv, compare_to_guard_only_mean.csv, DECISION.md.
- shield_only seed2 final: d0.00 success=1.00 cost=0.00 route=0.992; d0.08 success=0.86 cost=0.08 collision=0.06 out=0.02 route=0.958; d0.15 success=0.76 cost=0.14 collision=0.14 route=0.913.
- shield_only seed0-2 mean: d0.00 success=0.993 cost=0.000 route=0.992; d0.08 success=0.913 cost=0.067 collision=0.047 out=0.020 route=0.959; d0.15 success=0.627 cost=0.227 collision=0.227 route=0.871.
- Comparison to full proposed aggregate at d0.15: shield_only success 0.627 vs full 0.620, cost 0.227 vs 0.247, route 0.871 vs 0.865. Action guard alone matches/slightly exceeds the current full proposed mean.
- Comparison to guard_only at d0.15: shield_only success 0.627 vs guard_only 0.633, cost 0.227 vs 0.207, route 0.871 vs 0.868. Shield-only is close to guard+curriculum.
- Interpretation: action guard is the dominant verified mechanism. Current results do not support a risk-reward-dominant paper claim. Risk/reward components should be framed as high-density refinements unless a new retuned full variant clearly improves beyond shield/guard.
- Active run: proposed_wo_smooth seed1 continues; wait for final summary and aggregate with seed0.

## 2026-06-30 launch/config check proposed retune ttc4-cost10-lane1 seed2
- Time: 2026-06-30T21:51:22+08:00.
- Root: outputs/retune_proposed_ttc4_cost10_lane1_nenv16_seed2_1m.
- Rationale: shield_only three-seed aggregate matches/slightly exceeds current full proposed, so a conservative retune is needed. This candidate preserves action guard/curriculum/lane stability while reducing risk-reward aggressiveness.
- Protocol: proposed seed2, n_envs=16, timesteps=1M, horizon=1500, EPISODES=50, DEVICE=cuda, ent_coef=0.01.
- Config verified: use_risk_reward=True, use_action_guard=True, curriculum=True, reward_weights.ttc=4.0, lane=1.0, smooth=0.02, accel=0.01, cost=10.0, crash=100.0, out=150.0, ttc_threshold=12.0.
- Evaluation rule: this candidate is only useful if seed2 improves over the current full proposed seed2 and approaches shield_only seed2 at d0.15 without hurting d0.00/d0.08. Otherwise keep the paper claim pivot toward action guard dominance.
- Active concurrent run: proposed_wo_smooth seed1 continues.

## 2026-06-30 mid-run health wo_smooth seed1 and retune seed2
- Time: 2026-06-30T21:57:05+08:00.
- proposed_wo_smooth seed1 around 967k: still training near the end, stage2, success_rate about 0.10, window_success about 0.167, window_cost about 0.10, route window about 0.785. This looks weaker than desired and may confirm that removing smooth/accel harms training stability, but final held-out evaluation is required.
- retune proposed ttc4-cost10-lane1 seed2 around 623k: reached stage2, window_success about 0.333, window_cost about 0.10, window_route about 0.791. It is not collapsed and appears healthier than the original weak full-proposed seed2 at comparable mid-run points, but final d0.15 evaluation against shield_only seed2 is the gate.
- Decision: continue both unchanged. Do not promote retune until formal summary.csv exists.

## 2026-06-30 wo_smooth seed1 completed and seed0-1 aggregate written
- Time: 2026-06-30T22:03:11+08:00.
- New aggregate root: outputs/tuned_ablation_wo_smooth_nenv16_seed0_seed1_aggregate.
- Files: summary_by_seed.csv, mean_by_density.csv, std_by_density.csv, compare_to_full_proposed_mean.csv, DECISION.md.
- proposed_wo_smooth seed1 final: d0.00 success=1.00 cost=0.00 route=0.991; d0.08 success=0.80 cost=0.18 collision=0.16 out=0.02 route=0.879; d0.15 success=0.48 cost=0.42 collision=0.40 out=0.02 route=0.736.
- wo_smooth seed0-1 mean: d0.00 success=0.990 cost=0.000 route=0.990; d0.08 success=0.820 cost=0.160 collision=0.150 out=0.010 route=0.909; d0.15 success=0.530 cost=0.330 collision=0.320 out=0.010 route=0.792.
- Interpretation: removing smooth/accel materially hurts stability and high-density evaluation. Smooth/accel terms are not the dominant mechanism, but they should remain in the full setting.
- Decision: continue retune proposed ttc4-cost10-lane1 seed2 to final evaluation before launching more experiments.

## 2026-06-30 retune seed2 decision
- Time: 2026-06-30T22:11:54+0800.
- No active processes before relaunch; GPU was idle enough for new runs.
- retune proposed ttc4-cost10-lane1 seed2 passed the promotion gate for multi-seed validation: d0.15 success=0.68, cost=0.16, route=0.871.
- Next action: launch same retune for seed0 and seed1 with n_envs=16.

## 2026-06-30 launch retune proposed ttc4-cost10-lane1 seed0/seed1
- Time: 2026-06-30T22:13:15+0800.
- Roots: outputs/retune_proposed_ttc4_cost10_lane1_nenv16_seed0_1m and outputs/retune_proposed_ttc4_cost10_lane1_nenv16_seed1_1m.
- Protocol: variant=proposed, seeds=0/1, n_envs=16, timesteps=1M, horizon=1500, EPISODES=50, DEVICE=cuda.
- Reward args: ent_coef=0.01, ttc=4, cost=10, overspeed=3, target_speed=18, progress=40, lane=1.0, success_bonus=55, crash_penalty=100, out_of_road_penalty=150, ttc_threshold=12, stage2_success=0.50, stage2_cost=0.25, demote_cost=0.35.
- Purpose: complete the three-seed stability test for the promising retuned full-proposed candidate after seed2 improved the weak original full-proposed seed2.
- Early launch check: processes alive; formal config verification to follow after config files are fully written.

## 2026-06-30 retune proposed ttc4-cost10-lane1 seed0/1 completed and three-seed aggregate written
- Time: 2026-06-30T22:32:54+0800.
- New aggregate root: outputs/retune_proposed_ttc4_cost10_lane1_nenv16_seed0_seed1_seed2_aggregate.
- Files: summary_by_seed.csv, mean_by_density.csv, std_by_density.csv, compare_to_full_proposed_mean.csv, compare_to_guard_only_mean.csv, compare_to_shield_only_mean.csv, DECISION.md.
- seed0 final: d0.00 success=0.94 cost=0.00 route=0.991 lane_dev=0.071; d0.08 success=0.98 cost=0.02 route=0.986 lane_dev=0.081; d0.15 success=0.56 cost=0.26 route=0.819 lane_dev=0.118.
- seed1 final: d0.00 success=0.96 cost=0.00 route=0.991 lane_dev=0.263; d0.08 success=0.82 cost=0.10 route=0.923 lane_dev=0.273; d0.15 success=0.62 cost=0.30 route=0.869 lane_dev=0.359.
- three-seed mean: d0.00 success=0.967 cost=0.000 route=0.991; d0.08 success=0.887 cost=0.073 route=0.953; d0.15 success=0.620 cost=0.240 route=0.853 lane_dev=0.207.
- Interpretation: medium-density result improves over old full proposed, but high-density mean does not beat shield_only or guard_only and lane deviation worsens, especially seed1. Do not promote as final main method.
- Next tuning direction: keep lower risk penalty but strengthen lateral/smooth regularization, or formally pivot claims toward action-guard dominance if the next candidate fails.

## 2026-06-30 launch lateral/smooth retune ttc4-cost10-lane2-smooth004-accel002 seed1/seed2
- Time: 2026-06-30T22:34:02+0800.
- Roots: outputs/retune_proposed_ttc4_cost10_lane2_smooth004_accel002_nenv16_seed1_1m and outputs/retune_proposed_ttc4_cost10_lane2_smooth004_accel002_nenv16_seed2_1m.
- Protocol: proposed, seeds=1/2, n_envs=16, timesteps=1M, horizon=1500, EPISODES=50, DEVICE=cuda.
- Reward args: ent_coef=0.01, ttc=4, cost=10, lane=2.0, smooth=0.04, accel=0.02, overspeed=3, target_speed=18, progress=40, success_bonus=55, crash_penalty=100, out_of_road_penalty=150, ttc_threshold=12.
- Rationale: previous ttc4-cost10-lane1 aggregate improved d0.08 but failed to beat guard/shield at d0.15 and had high lane deviation, especially seed1. This run tests whether stronger lateral/smooth regularization fixes that failure without losing seed2 high-density behavior.
- Gate: promote only if seed1 lane deviation drops materially and d0.15 success/route/cost improve without seed2 collapsing.

## 2026-06-30 abort lateral/smooth retune lane2-smooth004-accel002 seed1/seed2
- Time: 2026-06-30T22:38:56+0800.
- Roots: outputs/retune_proposed_ttc4_cost10_lane2_smooth004_accel002_nenv16_seed1_1m and seed2_1m.
- Abort reason: mid-run evidence showed severe progress suppression. At about 524k/540k timesteps both runs remained in stage0 with window_route_completion about 0.10/0.09 and success_rate 0. This is much worse than the preceding ttc4-cost10-lane1 retune, which had already reached stage1/2 by this point.
- Diagnosis: lane=2.0 plus smooth=0.04/accel=0.02 over-regularizes motion and should not be completed as a formal candidate.
- Decision: stop these diagnostic runs and launch a gentler lateral retune instead: lane around 1.25, smooth 0.03, accel 0.015, with slightly higher progress reward to preserve motion.

## 2026-06-30 launch moderate lateral retune ttc4-cost10-lane125-smooth003-accel0015-progress45 seed1/seed2
- Time: 2026-06-30T22:39:26+0800.
- Roots: outputs/retune_proposed_ttc4_cost10_lane125_smooth003_accel0015_progress45_nenv16_seed1_1m and seed2_1m.
- Protocol: proposed, seeds=1/2, n_envs=16, timesteps=1M, horizon=1500, EPISODES=50, DEVICE=cuda.
- Reward args: ent_coef=0.01, ttc=4, cost=10, lane=1.25, smooth=0.03, accel=0.015, progress=45, overspeed=3, target_speed=18, success_bonus=55, crash_penalty=100, out_of_road_penalty=150, ttc_threshold=12.
- Rationale: lane2/smooth004 over-regularized and suppressed progress; this is a gentler lateral-stability retune with extra progress reward to preserve motion.
- Gate: seed1 must reduce lane deviation versus lane1 retune without losing d0.15 success/route; seed2 must remain competitive with its previous d0.15 result.

## 2026-06-30 moderate lateral retune seed1/seed2 diagnostic aggregate completed
- Time: 2026-06-30T23:00:54+0800.
- Aggregate root: outputs/retune_proposed_ttc4_cost10_lane125_smooth003_accel0015_progress45_nenv16_seed1_seed2_diagnostic_aggregate.
- Files: summary_by_seed.csv, mean_by_density.csv, std_by_density.csv, compare_to_lane1_same_seeds.csv, compare_to_lane1_seed1_seed2_mean.csv, compare_to_guard_only_mean.csv, compare_to_shield_only_mean.csv, DECISION.md.
- seed1 final: d0.00 success=0.98 cost=0.00 route=0.990 lane_dev=0.060; d0.08 success=0.88 cost=0.12 route=0.945 lane_dev=0.072; d0.15 success=0.64 cost=0.28 route=0.849 lane_dev=0.102.
- seed2 final: d0.00 success=0.98 cost=0.00 route=0.989 lane_dev=0.101; d0.08 success=0.88 cost=0.08 route=0.969 lane_dev=0.126; d0.15 success=0.62 cost=0.28 route=0.852 lane_dev=0.198.
- Two-seed mean: d0.00 success=0.980 cost=0.000 route=0.990 lane_dev=0.081; d0.08 success=0.880 cost=0.100 route=0.957 lane_dev=0.099; d0.15 success=0.630 cost=0.280 route=0.850 lane_dev=0.150.
- Interpretation: seed1 lateral instability is repaired, but seed2 high-density robustness degrades versus lane1. This candidate fails the promotion gate; do not run seed0.
- Next action: stop risk/lane reward-only retuning for now and test guard-centered/threshold-centered variants, since repeated full-risk retunes do not beat guard_only or shield_only.

## 2026-06-30 launch guard-centered guard_only ttc13/v18 seed1/seed2
- Time: 2026-06-30T23:02:49+0800.
- Roots: outputs/retune_guard_only_ttc13_v18_nenv16_seed1_1m and outputs/retune_guard_only_ttc13_v18_nenv16_seed2_1m.
- Protocol: variant=guard_only, seeds=1/2, n_envs=16, timesteps=1M, horizon=1500, EPISODES=50, DEVICE=cuda.
- Active mechanism: use_action_guard=True, use_risk_reward=False, curriculum=True. Because risk reward is disabled, reward penalty weights are protocol records; behavior-relevant guard parameters are ttc_threshold=13 and target_speed=18.
- Rationale: repeated full-risk/lane retunes failed to beat guard_only/shield_only. A mild guard threshold shift tests whether action-guard-centered tuning can lower high-density cost without the instability previously observed for full-proposed ttc14/v18.
- Gate: promote only if seed1/seed2 keep d0.08 success near guard_only and improve d0.15 cost/route versus guard_only same seeds. Abort or reject if training suppresses route progress or seed2 worsens materially.

## 2026-06-30 guard_only ttc13/v18 config verification
- Time: 2026-06-30T23:03:52+0800.
- Verified both seed1 and seed2 configs: variant=guard_only, n_envs=16, horizon=1500, timesteps=1M, ent_coef=0.01, use_action_guard=True, use_risk_reward=False, curriculum=True.
- Verified behavior-relevant guard parameters: reward_weights.ttc_threshold=13.0 and target_speed_kmh=18.0. Stage gates: stage2_success=0.50, stage2_cost=0.25, demote_cost=0.35.
- Early health around 82k: both processes alive; stage0/warmup route progress present, no launch/config mismatch.

## 2026-06-30 guard_only ttc13/v18 monitor at ~278k
- Time: 2026-06-30T23:06:15+0800.
- seed1 around 278k: stage2, window_success about 0.30-0.35, window_cost about 0.067, window_route about 0.776, rollout success_rate about 0.35. One sampled out_of_road episode appeared, but route progress is healthy.
- seed2 around 278k: stage2, window_success about 0.30, window_cost about 0.133, window_route about 0.855, rollout success_rate about 0.26.
- Decision: continue unchanged. This does not show the progress-suppression failure seen in the over-regularized lane2 run. Final held-out d0.08/d0.15 remains the gate.

## 2026-06-30 guard_only ttc13/v18 monitor at ~410k
- Time: 2026-06-30T23:09:45+0800.
- seed1 around 410k: stage2, window_cost about 0.033, window_route_completion about 0.808, window_success about 0.000-0.033, recent route samples 0.874-0.975, rollout success_rate about 0.02-0.03.
- seed2 around 410k: stage3, window_cost about 0.10, window_route_completion about 0.726, window_success about 0.033, recent route samples 0.533-0.813.
- Interpretation: progress is not suppressed and cost is not exploding, but success window is weak in the middle. Continue unchanged; final held-out evaluation is required before accepting/rejecting ttc13.

## 2026-06-30 guard_only ttc13/v18 monitor at ~600k
- Time: 2026-06-30T23:14:09+0800.
- seed1 around 606k-623k: stage2, window_cost about 0.000, window_route_completion about 0.838-0.847, window_success about 0.133-0.233, rollout success_rate about 0.20.
- seed2 around 590k-606k: stage2, window_cost about 0.000-0.033, window_route_completion about 0.838-0.841, window_success about 0.133-0.267, rollout success_rate about 0.22-0.24. One sampled collision appeared, but the rolling cost window remained low.
- Decision: continue to formal evaluation. ttc13 is not showing obvious training collapse; final d0.15 cost/route versus guard_only same seeds will decide.

## 2026-06-30 guard_only ttc13/v18 near-end training monitor
- Time: 2026-06-30T23:21:35+0800.
- seed1 around 950k-983k: stage2, window_cost 0.000-0.033, window_route about 0.789-0.835, rollout success_rate about 0.10-0.12.
- seed2 around 934k-967k: stage2, window_cost 0.067-0.100, window_route about 0.770-0.810, rollout success_rate about 0.20-0.23, with a sampled collision near 967k.
- Interpretation: no route/cost collapse, but success windows remain weak. Wait for formal evaluation before deciding; likely gate is whether d0.15 cost reduction compensates for possible success loss.

## 2026-06-30 guard_only ttc13/v18 seed1/seed2 diagnostic aggregate completed
- Time: 2026-06-30T23:28:54+0800.
- Aggregate root: outputs/retune_guard_only_ttc13_v18_nenv16_seed1_seed2_diagnostic_aggregate.
- Files: summary_by_seed.csv, mean_by_density.csv, std_by_density.csv, compare_to_guard_only_same_seeds.csv, compare_to_guard_only_seed1_seed2_mean.csv, compare_to_guard_only_three_seed_mean.csv, compare_to_shield_only_three_seed_mean.csv, DECISION.md.
- seed1 final: d0.00 success=0.98 cost=0.00 route=0.990; d0.08 success=0.84 cost=0.08 route=0.954; d0.15 success=0.58 cost=0.20 route=0.857.
- seed2 final: d0.00 success=0.98 cost=0.00 route=0.989; d0.08 success=0.84 cost=0.16 route=0.929; d0.15 success=0.62 cost=0.16 route=0.886.
- Two-seed mean: d0.00 success=0.980 cost=0.000 route=0.990; d0.08 success=0.840 cost=0.120 route=0.941; d0.15 success=0.600 cost=0.180 route=0.872.
- Decision: do not run seed0. ttc13 is mixed parameter-sensitivity evidence, not a promoted guard-centered setting. Default guard_only ttc12/v18 remains the cleaner action-guard baseline.

## 2026-06-30 launch guard-centered guard_only ttc12/v19 seed1/seed2
- Time: 2026-06-30T23:29:27+0800.
- Roots: outputs/retune_guard_only_ttc12_v19_nenv16_seed1_1m and outputs/retune_guard_only_ttc12_v19_nenv16_seed2_1m.
- Protocol: variant=guard_only, seeds=1/2, n_envs=16, timesteps=1M, horizon=1500, EPISODES=50, DEVICE=cuda.
- Active mechanism: use_action_guard=True, use_risk_reward=False, curriculum=True. Behavior-relevant guard parameters: ttc_threshold=12, target_speed=19.
- Rationale: ttc13/v18 reduced some seed2 high-density cost but hurt seed1 and d0.08 success. This orthogonal branch keeps the accepted TTC threshold and relaxes only the overspeed guard target to test whether d0.15 success/route can improve without a large cost penalty.
- Gate: promote only if seed1/seed2 improve d0.15 success or route versus guard_only ttc12/v18 same seeds while keeping d0.08 success/cost close. Reject if high-density cost increases materially or d0.08 degrades.

## 2026-06-30 guard_only ttc12/v19 config verification
- Time: 2026-06-30T23:30:30+0800.
- Verified both seed1 and seed2 configs: variant=guard_only, n_envs=16, horizon=1500, timesteps=1M, ent_coef=0.01, use_action_guard=True, use_risk_reward=False, curriculum=True.
- Verified behavior-relevant guard parameters: reward_weights.ttc_threshold=12.0 and target_speed_kmh=19.0. Stage gates: stage2_success=0.50, stage2_cost=0.25, demote_cost=0.35.
- Early health around 82k: both processes alive; warmup has route progress but sampled out_of_road episodes. Too early to judge; continue to stage transition checks.

## 2026-06-30 guard_only ttc12/v19 monitor at ~300k
- Time: 2026-06-30T23:33:24+0800.
- seed1 around 295k-311k: stage2, window_cost about 0.10-0.133, window_route_completion about 0.809-0.817, window_success about 0.167-0.20, rollout success_rate about 0.28-0.30.
- seed2 around 279k-295k: reached stage3, window_cost about 0.133, window_route_completion about 0.867, window_success about 0.533, rollout success_rate about 0.31.
- Decision: continue unchanged. This branch is not stuck and seed2 is stronger than the ttc13/v18 branch at the same stage; final held-out cost will decide whether the relaxed speed guard is acceptable.

## 2026-06-30 guard_only ttc12/v19 monitor at ~786k/~655k
- Time: 2026-06-30T23:42:23+0800.
- seed1 around 786k: stage2, window_cost about 0.067, window_route_completion about 0.863, window_success about 0.267, rollout success_rate about 0.28. Latest sampled episode had collision cost, but rolling cost remains controlled; continue to final evaluation.
- seed2 around 655k: stage3, window_cost about 0.233, window_route_completion about 0.704, window_success about 0.100, rollout success_rate about 0.11. This is weaker than the early stage3 signal and close to the cost gate; continue but treat as a warning unless final held-out evaluation improves.
- Resource: CPU available about 18GiB; GPU memory used about 1.37GiB / 12.28GiB; protocol remains resource-safe.
- Decision: continue both unchanged. Do not launch seed0 or additional guard-centered runs until seed1/seed2 produce summary.csv and are compared against guard_only ttc12/v18 same seeds.

## 2026-06-30 guard_only ttc12/v19 monitor at ~934k/~754k
- Time: 2026-06-30T23:45:32+0800.
- seed1 around 934k: stage2, window_cost about 0.067, window_route_completion about 0.852, window_success about 0.300, rollout success_rate about 0.34. Latest sampled episode has no cost/collision/out-of-road and route_completion about 0.905. Seed1 is close to final and remains usable.
- seed2 around 754k: stage3, window_cost about 0.233, window_route_completion about 0.720, window_success about 0.067, rollout success_rate about 0.10. Latest sampled episode has collision cost and low route_completion about 0.273. This is a warning against promoting v19 unless final eval recovers strongly.
- Decision: continue to final summaries, but provisional judgement is mixed/weak. Do not launch v19 seed0 before seed1/seed2 final comparison.

## 2026-06-30 guard_only ttc12/v19 seed1/seed2 diagnostic aggregate completed
- Time: 2026-06-30T23:56:10+0800.
- Aggregate root: outputs/retune_guard_only_ttc12_v19_nenv16_seed1_seed2_diagnostic_aggregate.
- Files: summary_by_seed.csv, mean_by_density.csv, std_by_density.csv, compare_to_guard_only_same_seeds.csv, compare_to_guard_only_seed1_seed2_mean.csv, compare_to_guard_only_three_seed_mean.csv, compare_to_shield_only_three_seed_mean.csv, DECISION.md.
- seed1 final: d0.00 success=0.98 cost=0.00 route=0.990; d0.08 success=0.92 cost=0.06 route=0.954; d0.15 success=0.58 cost=0.28 route=0.861.
- seed2 final: d0.00 success=1.00 cost=0.00 route=0.992; d0.08 success=0.84 cost=0.16 route=0.938; d0.15 success=0.72 cost=0.26 route=0.871.
- Two-seed mean: d0.00 success=0.990 cost=0.000 route=0.991; d0.08 success=0.880 cost=0.110 route=0.946; d0.15 success=0.650 cost=0.270 route=0.866.
- Same-seed comparison to default guard_only ttc12/v18 at d0.15: success improves only 0.64 -> 0.65, cost worsens 0.20 -> 0.27, route is essentially unchanged/slightly lower 0.871 -> 0.866.
- Decision: reject target_speed=19 as final guard-centered setting; do not launch seed0. Keep default guard_only ttc12/v18 and shield_only as cleaner action-guard baselines.


## 2026-06-30 launch no_action_guard seed1/seed2 nenv16 ablation completion
- Time: 2026-06-30T23:57:05+0800.
- Roots: outputs/tuned_ablation_no_action_guard_nenv16_seed1_1m and outputs/tuned_ablation_no_action_guard_nenv16_seed2_1m.
- Protocol: variant=no_action_guard, seeds=1/2, n_envs=16, timesteps=1M, horizon=1500, EPISODES=50, DEVICE=cuda, ent_coef=0.01.
- Mechanism: use_risk_reward=True, use_action_guard=False, curriculum=True. This completes the planned three-seed evidence for the dominant action-guard ablation after seed0 collapsed.
- Gate: do not rescue/tune mid-run unless there is a launch/config failure. If both seeds reproduce high cost/low success, aggregate with seed0 and use as strong evidence that action guard is necessary.

## 2026-07-01 no_action_guard seed1/seed2 monitor at ~280k/295k
- Time: 2026-07-01T00:02:05+0800.
- seed1 around 279k: stage0, window_cost=0, window_route_completion about 0.153, window_success=0, rollout success_rate=0, mean_speed about 0.98 km/h, std about 1.01.
- seed2 around 295k: stage0, window_cost=0, window_route_completion about 0.199, window_success=0, rollout success_rate=0, mean_speed about 1.28 km/h, std about 1.00.
- Interpretation: no launch/config failure. The ablation is currently failing to form useful driving behavior rather than crashing; this is relevant mechanism evidence, so continue to final evaluation unless the process fails.
- Resource: GPU memory used about 1.36GiB / 12.28GiB; CPU available about 21GiB. Continue both unchanged.

## 2026-07-01 no_action_guard seed1/seed2 monitor at ~541k/~573k
- Time: 2026-07-01T00:04:33+0800.
- seed1 around 541k: reached stage1, window_cost=0, window_route_completion about 0.674, window_success about 0.467, rollout success_rate about 0.37, mean_speed about 11.6 km/h.
- seed2 around 573k: reached stage1, window_cost about 0.067, window_route_completion about 0.669, window_success about 0.433, rollout success_rate about 0.43, mean_speed about 10.6 km/h.
- Interpretation: unlike seed0 and the early 280k check, these seeds have recovered some driving behavior. Do not claim no_action_guard universally collapses until final held-out evaluation. Continue unchanged and aggregate with seed0 after summaries exist.

## 2026-07-01 no_action_guard seed1/seed2 monitor at ~754k/~786k
- Time: 2026-07-01T00:07:31+0800.
- seed1 around 754k: stage1, window_cost about 0.233, window_route_completion about 0.813, window_success about 0.600, rollout success_rate about 0.39. Latest sampled episode has no cost but route_completion about 0.668.
- seed2 around 786k: stage2, window_cost about 0.033, window_route_completion about 0.895, window_success about 0.667, rollout success_rate about 0.39. Latest sampled episode route_completion about 0.986.
- Interpretation: no_action_guard seed1/2 are not reproducing a simple universal collapse. The final ablation claim must be based on held-out d0.08/d0.15 cost/success and seed variance, not only seed0. Continue to final evaluation unchanged.

## 2026-07-01 no_action_guard seed0/1/2 aggregate completed
- Time: 2026-07-01T00:13:20+0800.
- Aggregate root: outputs/tuned_ablation_no_action_guard_nenv16_seed0_seed1_seed2_aggregate.
- Files: summary_by_seed.csv, mean_by_density.csv, std_by_density.csv, compare_to_full_proposed_mean.csv, compare_to_guard_only_mean.csv, compare_to_shield_only_mean.csv, DECISION.md.
- Three-seed mean: d0.00 success=0.027 cost=0.973 route=0.254; d0.08 success=0.000 cost=1.000 route=0.202; d0.15 success=0.000 cost=1.000 route=0.172.
- Failure mode: low density mostly out_of_road; medium/high density mix collision and out_of_road. seed1/2 had temporary training-window recovery, but held-out evaluation still collapsed.
- Decision: accept as three-seed no_action_guard ablation. Do not rescue/tune this ablation; action-level guard is necessary for stable held-out safety/completion under the current method.


## 2026-07-01 launch wo_lane seed2 and wo_smooth seed2 nenv16 ablation completion
- Time: 2026-07-01T00:14:10+0800.
- Roots: outputs/tuned_ablation_wo_lane_nenv16_seed2_1m and outputs/tuned_ablation_wo_smooth_nenv16_seed2_1m.
- Protocol: variants=proposed_wo_lane/proposed_wo_smooth, seed=2, n_envs=16, timesteps=1M, horizon=1500, EPISODES=50, DEVICE=cuda, ent_coef=0.01.
- Purpose: complete third seed for lane and smooth/accel reward-component ablations after seed0/1 aggregates showed high lane deviation and stability degradation respectively.
- Gate: run to final evaluation unless process/config fails; aggregate with seed0/1 after summaries exist.

## 2026-07-01 invalidated first wo_lane/wo_smooth seed2 launch due wrong ablation weights
- Time: 2026-07-01T00:16:00+0800.
- Issue: initial seed2 launches for proposed_wo_lane and proposed_wo_smooth were passed default reward weights, producing configs with lane=1.0 for wo_lane and smooth=0.02/accel=0.01 for wo_smooth, unlike seed0/seed1 where lane=0.0 or smooth=0.0/accel=0.0.
- Action: stopped the invalid process groups and archived the partial roots with INVALID_DO_NOT_USE.txt. These runs must not enter any table or aggregate.
- Fix: relaunch seed2 using explicit ablation weights: wo_lane with --reward-lane 0.0; wo_smooth with --reward-smooth 0.0 --reward-accel 0.0.

## 2026-07-01 corrected wo_lane/wo_smooth seed2 monitor at ~311k/~360k
- Time: 2026-07-01T00:18:52+0800.
- proposed_wo_lane seed2 around 311k: stage1, window_cost about 0.233, window_route_completion about 0.630, window_success=0, rollout success_rate about 0.03, lane_deviation about 0.463. This is consistent with lane-reward removal causing lateral instability; continue.
- proposed_wo_smooth seed2 around 360k: stage0, window_cost=0, window_route_completion about 0.459, window_success=0, rollout success_rate=0, mean_speed about 3.67 km/h. This is slower than desired but still making route progress; continue to 500k/750k before judging.
- Resource: GPU memory used about 1.35GiB / 12.28GiB. Continue both unchanged.

## 2026-07-01 corrected wo_lane/wo_smooth seed2 monitor at ~573k/~606k
- Time: 2026-07-01T00:21:53+0800.
- proposed_wo_lane seed2 around 573k: stage2, window_cost about 0.133, window_route_completion about 0.842, window_success about 0.300, rollout success_rate about 0.14, lane_deviation about 0.449. Lateral deviation remains high, consistent with lane-reward removal.
- proposed_wo_smooth seed2 around 606k: stage2, window_cost=0, window_route_completion about 0.865, window_success about 0.300, rollout success_rate about 0.34. This recovered from the earlier slow stage0, so final held-out metrics are needed.
- Decision: continue both unchanged to final evaluation and aggregate with seed0/1.

## 2026-07-01 wo_lane and wo_smooth seed2 completed; three-seed aggregates written
- Time: 2026-07-01T00:36:00+0800.
- Corrected seed2 runs used matching ablation weights after invalid first launch was archived.
- wo_lane aggregate root: outputs/tuned_ablation_wo_lane_nenv16_seed0_seed1_seed2_aggregate. Mean d0.15 success=0.607 cost=0.280 route=0.844 lane_dev=0.362. Decision: accept as lane-reward ablation; lane term supports lateral stability/route quality, not dominant raw success.
- wo_smooth aggregate root: outputs/tuned_ablation_wo_smooth_nenv16_seed0_seed1_seed2_aggregate. Mean d0.15 success=0.567 cost=0.287 route=0.821 lane_dev=0.245. Decision: accept as smooth/accel ablation; smooth/accel terms are stabilizers with high seed variance.
- PDF check: seed2 PDFs are under each run figures/ directory; no loose PDFs found for these runs.


## 2026-07-01 launch risk seed1/seed2 nenv16 formal comparator completion
- Time: 2026-07-01T00:37:00+0800.
- Roots: outputs/tuned_compare_risk_nenv16_seed1_1m and outputs/tuned_compare_risk_nenv16_seed2_1m.
- Protocol: variant=risk, seeds=1/2, n_envs=16, timesteps=1M, horizon=1500, EPISODES=50, DEVICE=cuda, ent_coef=0.01.
- Purpose: complete the risk-only comparator after seed0 produced near-zero route/success. This tests whether risk reward alone is enough or whether action guard/curriculum mechanisms dominate.
- Gate: run to final evaluation unless config/process fails; aggregate with seed0 after summaries exist.

## 2026-07-01 risk seed1/seed2 monitor at ~180k
- Time: 2026-07-01T00:39:59+0800.
- seed1 around 180k: success_rate=0, route_completion about 0.025, mean_speed about 0.54 km/h, no cost/collision/out_of_road, std about 1.02.
- seed2 around 180k: success_rate=0, route_completion about 0.043, mean_speed about 0.77 km/h, no cost/collision/out_of_road, std about 1.01.
- Interpretation: risk-only without curriculum is currently low-speed/low-route and resembles seed0 early failure, but it is still early. Continue to 500k before deciding whether the comparator consistently fails.

## 2026-07-01 risk seed1/seed2 monitor at ~475k/~442k
- Time: 2026-07-01T00:44:02+0800.
- seed1 around 475k: success_rate=0, route_completion about 0.017, mean_speed about 0.44 km/h, cost=0. This is low-speed/route-stagnation failure, not useful safety.
- seed2 around 442k: success_rate=0, route_completion about 0.010, mean_speed about 0.44 km/h, cost=0. Same failure mode.
- Interpretation: risk reward + action guard without curriculum is not learning usable driving by mid-training, matching seed0 behavior. Continue to final evaluation for comparator evidence; do not tune this comparator mid-run.



## 2026-07-01 risk seed0/1/2 formal comparator aggregate completed
- Time: 2026-07-01T00:58:42+0800.
- Aggregate root: outputs/tuned_compare_risk_nenv16_seed0_seed1_seed2_aggregate.
- Files: summary_by_seed.csv, mean_by_density.csv, std_by_density.csv, compare_to_full_proposed_mean.csv, compare_to_guard_only_mean.csv, compare_to_shield_only_mean.csv, DECISION.md.
- Three-seed mean: d0.00 success=0.000 cost=0.000 route=0.009 speed=0.013; d0.08 success=0.000 cost=0.000 route=0.009 speed=0.013; d0.15 success=0.000 cost=0.000 route=0.009 speed=0.014.
- Decision: accept as risk-only formal comparator. This is a route-stagnation failure, not a safety success; zero cost is non-informative because the policy barely drives.
- Paper claim boundary: risk reward + action guard without curriculum does not learn usable driving under the formal n_envs=16 protocol. Do not tune this comparator; move to baseline/curriculum seed completion.
- PDF placement: run PDFs are under each single-run figures/ directory; aggregate directory intentionally contains only CSV/Markdown evidence.


## 2026-07-01 launch baseline seed1/seed2 nenv16 formal comparator completion
- Time: 2026-07-01T00:59:54+0800.
- Roots: outputs/tuned_compare_baseline_nenv16_seed1_1m and outputs/tuned_compare_baseline_nenv16_seed2_1m.
- Protocol: variant=baseline, seeds=1/2, n_envs=16, timesteps=1M, horizon=1500, EPISODES=50, DEVICE=cuda, ent_coef=0.01.
- Config check: use_risk_reward=False, use_action_guard=False, curriculum=False for both seed1 and seed2.
- Purpose: complete the baseline comparator symmetry after seed0 only.
- Gate: run to final evaluation unless process/config fails; aggregate with seed0 after summaries exist, then launch curriculum seed1/2.


## 2026-07-01 baseline seed1/seed2 monitor at ~360k
- Time: 2026-07-01T01:07:01+0800.
- seed1 around 360k: recent100 success=0.160, cost=0.840, collision=0.320, out_of_road=0.520, route=0.589, speed=22.950.
- seed2 around 360k: recent100 success=0.250, cost=0.750, collision=0.490, out_of_road=0.260, route=0.668, speed=23.311.
- Interpretation: baseline without guard is learning to drive faster and farther than early stage, but high collision/out_of_road cost is already dominant. Continue unchanged to final held-out evaluation; do not tune this comparator.


## 2026-07-01 baseline seed1/seed2 monitor at ~500k
- Time: 2026-07-01T01:11:04+0800.
- seed1 around 492k: recent100 success=0.030, cost=0.970, collision=0.640, out_of_road=0.330, route=0.439, speed=28.579.
- seed2 around 508k: recent100 success=0.100, cost=0.900, collision=0.560, out_of_road=0.350, route=0.542, speed=26.946.
- Interpretation: unguarded baseline is driving faster but remains unsafe, dominated by collision and out_of_road. Continue unchanged to final held-out evaluation; final paper table must use evaluation summary, not this training window.


## 2026-07-01 baseline seed0/1/2 formal comparator aggregate completed
- Time: 2026-07-01T01:27:33+0800.
- Aggregate root: outputs/tuned_compare_baseline_nenv16_seed0_seed1_seed2_aggregate.
- Files: summary_by_seed.csv, mean_by_density.csv, std_by_density.csv, compare_to_full_proposed_mean.csv, compare_to_guard_only_mean.csv, compare_to_shield_only_mean.csv, DECISION.md.
- Three-seed mean: d0.00 success=0.007 cost=0.993 route=0.303; d0.08 success=0.000 cost=1.000 route=0.242; d0.15 success=0.000 cost=1.000 route=0.190.
- Decision: accept as unguarded lower-bound baseline. It is unsafe at all densities; unlike risk-only stagnation, it moves but fails through collision/out_of_road.
- PDF placement: seed1/seed2 PDFs are under each run figures/ directory; aggregate directory intentionally contains only CSV/Markdown evidence.


## 2026-07-01 launch curriculum seed1/seed2 nenv16 formal comparator completion
- Time: 2026-07-01T01:28:38+0800.
- Roots: outputs/tuned_compare_curriculum_nenv16_seed1_1m and outputs/tuned_compare_curriculum_nenv16_seed2_1m.
- Protocol: variant=curriculum, seeds=1/2, n_envs=16, timesteps=1M, horizon=1500, EPISODES=50, DEVICE=cuda, ent_coef=0.01.
- Config check: use_risk_reward=False, use_action_guard=False, curriculum=True for both seed1 and seed2.
- Purpose: close the remaining main-comparator symmetry gap after baseline and risk aggregates.
- Gate: run to final evaluation unless process/config fails; aggregate with seed0 after summaries exist.


## 2026-07-01 curriculum seed1/seed2 monitor at ~250k
- Time: 2026-07-01T01:31:09+0800.
- seed1 around 262k: recent100 success=0.300, cost=0.580, collision=0.100, out_of_road=0.480, route=0.681, speed=18.027, curriculum_stage about 1.61.
- seed2 around 246k: recent100 success=0.300, cost=0.390, collision=0.140, out_of_road=0.250, route=0.693, speed=15.685, curriculum_stage about 2.05.
- Interpretation: curriculum-only is materially healthier than the unguarded baseline at comparable early/mid training, but final held-out evaluation is still required. Continue unchanged.


## 2026-07-01 curriculum seed1/seed2 monitor at ~425k-492k
- Time: 2026-07-01T01:35:40+0800.
- seed1 around 492k: recent100 success=0.120, cost=0.880, collision=0.670, out_of_road=0.210, route=0.569, speed=30.343, curriculum_stage about 1.74.
- seed2 around 426k: recent100 success=0.140, cost=0.860, collision=0.630, out_of_road=0.230, route=0.572, speed=27.949, curriculum_stage about 2.00.
- Interpretation: after the healthier ~250k window, curriculum-only degrades as speed/collision rise. Continue unchanged to final held-out evaluation; do not tune this comparator mid-run.


## 2026-07-01 curriculum seed1/seed2 monitor at ~705k-770k
- Time: 2026-07-01T01:41:11+0800.
- seed1 around 770k: recent100 success=0.290, cost=0.710, collision=0.420, out_of_road=0.290, route=0.666, speed=28.994, curriculum_stage about 2.00.
- seed2 around 705k: recent100 success=0.240, cost=0.760, collision=0.470, out_of_road=0.290, route=0.615, speed=28.747, curriculum_stage about 2.00.
- Interpretation: curriculum-only partially recovers relative to the ~500k window, but cost remains high. Continue unchanged to final held-out evaluation.


## 2026-07-01 curriculum seed0/1/2 formal comparator aggregate completed
- Time: 2026-07-01T01:51:50+0800.
- Aggregate root: outputs/tuned_compare_curriculum_nenv16_seed0_seed1_seed2_aggregate.
- Files: summary_by_seed.csv, mean_by_density.csv, std_by_density.csv, compare_to_full_proposed_mean.csv, compare_to_baseline_mean.csv, compare_to_guard_only_mean.csv, compare_to_shield_only_mean.csv, DECISION.md.
- Three-seed mean: d0.00 success=0.007 cost=0.993 route=0.349; d0.08 success=0.000 cost=1.000 route=0.236; d0.15 success=0.000 cost=1.000 route=0.177.
- Decision: accept as curriculum-only formal comparator. Curriculum improves some training windows and route progress relative to risk-only stagnation, but without action guard final held-out safety remains poor.
- PDF placement: seed1/seed2 PDFs are under each run figures/ directory; aggregate directory intentionally contains only CSV/Markdown evidence.


## 2026-07-01 stress density 0.20/0.25 nenv16 evaluation completed
- Time: 2026-07-01T02:55:36.125071+08:00.
- Root: outputs/stress_density_020_025_nenv16_20260701_0153.
- Protocol: evaluation-only, densities 0.20 and 0.25, EPISODES=50 per density, n_envs=16, device=cuda, frozen models only.
- Labels/seeds: guard_only, shield_only, retune_proposed_ttc4_cost10_lane1, baseline, curriculum, risk, full_proposed_candidate; each has seeds 0/1/2 and 100 episode rows per seed.
- Execution: all 21 label/seed evals succeeded or were skipped because a valid CSV already existed; no active stress process remains.
- d0.20 means: shield_only success=0.480 cost=0.360 route=0.778; retuned full proposed success=0.453 cost=0.380 route=0.753; guard_only success=0.413 cost=0.407 route=0.733; full proposed candidate success=0.380 cost=0.400 route=0.744.
- d0.25 means: guard_only success=0.267 cost=0.487 route=0.658; full proposed candidate success=0.207 cost=0.587 route=0.587; shield_only success=0.193 cost=0.587 route=0.609; retuned full proposed success=0.173 cost=0.687 route=0.571.
- Failure controls: baseline/curriculum have success=0 and cost=1.0 at both stress densities; risk has near-zero route and zero cost, so it is idle/stagnation rather than safety.
- Decision: accept as frozen high-density stress evidence. Use it to support action-guard-centered robustness and graceful degradation; do not claim risk-reward dominance.


## 2026-07-01 paper evidence tables package written
- Time: 2026-07-01T02:57:35.308647+08:00.
- Root: codex_longrun_iscsic/paper_tables_20260701_0258.
- Files: README_论文证据包.md, main_comparators_nenv16.csv, ablation_mechanism_nenv16.csv, stress_density_020_025.csv, claim_boundary_and_next_decisions.md.
- Purpose: convert completed n_envs=16 main/comparator/ablation/stress evidence into paper-facing tables and explicit claim boundaries.
- Decision: do not open another reward-only retune round by default. Current evidence supports an action-guard/shield-centered paper line; any further method improvement should be a mechanism change, not another weight sweep.


## 2026-07-01 active proposed_gated_risk diagnostics
- Time: 2026-07-01T03:10:01+08:00.
- Active roots: outputs/gated_risk_proposed_nenv16_seed1_1m and outputs/gated_risk_proposed_nenv16_seed2_1m.
- Active PIDs at launch: seed1 parent 109861, seed2 parent 109916.
- Current status at launch check: both configs written with variant=proposed_gated_risk, n_envs=16, horizon=1500, timesteps=1M, use_gated_risk_reward=True, stage2_success=0.50, stage2_cost=0.25, demote_cost=0.35.
- Next action: monitor mid-training windows from monitor CSV/logs, then inspect final evaluation CSVs and decide whether to extend to seed0 or revise the mechanism.


## 2026-07-01 proposed_gated_risk seed1/seed2 monitor at ~472k/~482k
- Time: 2026-07-01T03:12:58+08:00.
- seed1 around 472k env steps: recent100 success=0.090, cost=0.010, collision=0.000, out_of_road=0.010, route=0.292, speed=2.824, risk_gate_rate=0.170, continuous_risk_penalty=35.084, event_risk_penalty=0.100, shield_rate=0.002, curriculum_stage about 0.20.
- seed2 around 482k env steps: recent100 success=0.080, cost=0.080, collision=0.000, out_of_road=0.080, route=0.275, speed=2.441, risk_gate_rate=0.186, continuous_risk_penalty=28.587, event_risk_penalty=0.800, shield_rate=0.001, curriculum_stage about 0.14.
- Interpretation: gated risk is not collapsing into the risk-only near-zero-route failure, and safety/cost is currently low. However speed/stage/route are still conservative versus guard_only/shield_only; do not claim improvement from this window. Continue to final held-out evaluation before deciding on seed0 or mechanism revision.


## 2026-07-01 proposed_gated_risk seed1/seed2 monitor at ~711k/~728k
- Time: 2026-07-01T03:16:32+08:00.
- seed1 around 711k env steps: recent100 success=0.170, cost=0.010, collision=0.000, out_of_road=0.010, route=0.472, speed=6.856, risk_gate_rate=0.269, continuous_risk_penalty=53.112, event_risk_penalty=0.100, shield_rate=0.023, curriculum_stage about 0.68.
- seed2 around 728k env steps: recent100 success=0.170, cost=0.080, collision=0.020, out_of_road=0.060, route=0.473, speed=6.977, risk_gate_rate=0.279, continuous_risk_penalty=46.953, event_risk_penalty=0.800, shield_rate=0.032, curriculum_stage about 0.65.
- Interpretation: this is a recovery from the ~480k conservative window and clearly avoids risk-only route stagnation. Still, training-window metrics remain weaker than the guard/shield-centered best evidence, so continue to final held-out evaluation before deciding whether seed0 is worthwhile.


## 2026-07-01 proposed_gated_risk seed1/seed2 evaluation completed; seed0 launched
- Time: 2026-07-01T03:28:44+08:00.
- Completed roots: outputs/gated_risk_proposed_nenv16_seed1_1m and outputs/gated_risk_proposed_nenv16_seed2_1m.
- Per-seed held-out summary: seed1 d0.00/d0.08/d0.15 success=0.94/0.80/0.62, cost=0.00/0.10/0.28; seed2 success=0.94/0.90/0.56, cost=0.00/0.06/0.28.
- Preliminary two-seed aggregate: outputs/gated_risk_proposed_nenv16_seed1_seed2_prelim_aggregate. Mean d0.00 success=0.940 cost=0.000 route=0.987; d0.08 success=0.850 cost=0.080 route=0.959; d0.15 success=0.590 cost=0.280 route=0.843.
- Decision: gated risk fixes risk-only stagnation and is worth completing as a three-seed mechanism diagnostic, but current two-seed d0.15 does not displace guard_only/shield_only/retuned full. Keep guard/shield-centered paper claim boundary.
- New launch: outputs/gated_risk_proposed_nenv16_seed0_1m pid=111544, same 1M/horizon1500/n_envs16/EPISODES50 protocol with ent_coef=0.01, stage2_success=0.50, stage2_cost=0.25, demote_cost=0.35.


## 2026-07-01 proposed_gated_risk seed0 monitor at ~497k
- Time: 2026-07-01T03:32:54+08:00.
- seed0 around 497k env steps: recent100 success=0.060, cost=0.010, collision=0.000, out_of_road=0.010, route=0.290, speed=2.895, risk_gate_rate=0.189, continuous_risk_penalty=38.136, event_risk_penalty=0.100, shield_rate=0.003, curriculum_stage about 0.26.
- Interpretation: seed0 matches seed1/seed2 mid-training recovery pattern and has no process/config failure. Continue unchanged to late-training and final held-out evaluation.


## 2026-07-01 proposed_gated_risk seed0 monitor at ~744k
- Time: 2026-07-01T03:35:50+08:00.
- seed0 around 744k env steps: recent100 success=0.150, cost=0.010, collision=0.000, out_of_road=0.010, route=0.463, speed=6.460, risk_gate_rate=0.274, continuous_risk_penalty=54.981, event_risk_penalty=0.100, shield_rate=0.024, curriculum_stage about 0.71.
- Interpretation: seed0 has the same late-training recovery pattern as seed1/seed2. Continue unchanged to model save and held-out evaluation.


## 2026-07-01 proposed_gated_risk three-seed aggregate completed
- Time: 2026-07-01T03:46:11+08:00.
- Aggregate root: outputs/gated_risk_proposed_nenv16_seed0_seed1_seed2_aggregate.
- Completed single-run roots: outputs/gated_risk_proposed_nenv16_seed0_1m, outputs/gated_risk_proposed_nenv16_seed1_1m, outputs/gated_risk_proposed_nenv16_seed2_1m.
- Files: summary_by_seed.csv, mean_by_density.csv, std_by_density.csv, compare_to_guard_only_mean.csv, compare_to_shield_only_mean.csv, compare_to_retune_full_mean.csv, compare_to_risk_only_mean.csv, DECISION.md.
- Three-seed mean: d0.00 success=0.940 cost=0.000 route=0.988; d0.08 success=0.867 cost=0.080 route=0.961; d0.15 success=0.600 cost=0.253 route=0.849.
- Mechanism metrics: risk_gate_rate mean is 0.887/0.865/0.764 at d0.00/d0.08/d0.15; out_of_road=0.000 at all formal densities.
- Decision: accept as completed mechanism diagnostic. Gated risk fixes the risk-only stagnation failure, but does not replace the guard_only/shield_only/retuned-full main evidence because d0.15 remains slightly weaker.
- Paper package addendum: codex_longrun_iscsic/paper_tables_20260701_0258/gated_risk_mechanism_addendum.csv and gated_risk_mechanism_addendum.md.
- PDF placement: all generated PDFs are under the single-run figures/ directories; aggregate/addendum directories remain CSV/Markdown only.


## 2026-07-01 proposed_gated_risk stress eval launched
- Time: 2026-07-01T03:48:14+08:00.
- Root: outputs/stress_gated_risk_density_020_025_nenv16_20260701_0346.
- Protocol: frozen proposed_gated_risk seed0/1/2 models, densities 0.20 and 0.25, 50 episodes per density, n_envs=16, device=cuda.
- Execution: serial driver PID 112760, seed0 evaluation confirmed running. Purpose is addendum evidence against the existing 0.20/0.25 stress table, not a new training run.


## 2026-07-01 proposed_gated_risk stress addendum completed
- Time: 2026-07-01T04:00:34+08:00.
- Stress root: outputs/stress_gated_risk_density_020_025_nenv16_20260701_0346.
- Aggregate root: outputs/stress_gated_risk_density_020_025_nenv16_20260701_0346/aggregate.
- Files: status.tsv, evaluations/proposed_gated_risk_ppo_s0.csv, evaluations/proposed_gated_risk_ppo_s1.csv, evaluations/proposed_gated_risk_ppo_s2.csv, aggregate/summary_by_seed.csv, aggregate/mean_by_density.csv, aggregate/std_by_density.csv, aggregate/rank_with_existing_stress.csv, aggregate/DECISION.md.
- Three-seed stress mean: d0.20 success=0.447 cost=0.367 route=0.766; d0.25 success=0.220 cost=0.527 route=0.628.
- Existing stress comparison: at d0.20 proposed_gated_risk ranks behind shield_only and retuned full by success; at d0.25 it ranks second behind guard_only by success/cost/route ordering.
- Paper package addendum: codex_longrun_iscsic/paper_tables_20260701_0258/gated_risk_stress_mean.csv, gated_risk_stress_rank_with_existing.csv, gated_risk_stress_addendum.md.
- Final boundary: conditional risk shaping is useful and improves over risk-only/retuned-full in some stress settings, but does not overturn the guard/shield-centered main claim.
- Process/PDF check: no active training/evaluation process remains; aggregate and paper_table directories contain no PDFs.


## 2026-07-01 reviewer robustness and behavior addenda completed
- Time: 2026-07-01T04:11:29+08:00.
- Updated coverage audit: codex_longrun_iscsic/EXPERIMENT_COVERAGE_AUDIT_20260701_0405.md.
- Reviewer statistics files in paper package: seed_level_robustness_formal.csv, seed_paired_deltas_vs_guard_shield.csv, seed_level_robustness_stress.csv, reviewer_statistics_notes.md.
- Behavior rollout directory: codex_longrun_iscsic/behavior_rollouts_20260701_0406.
- Representative qualitative seed: density=0.15, map_seed=10003. guard_only/shield_only/retuned_full/proposed_gated_risk succeed; no_action_guard fails by collision/high speed; risk_only has near-zero route and zero cost due stagnation.
- Representative plot: codex_longrun_iscsic/behavior_rollouts_20260701_0406/representative_density_0p15_seed10003.pdf.
- Paper package pointer: codex_longrun_iscsic/paper_tables_20260701_0258/behavior_rollout_addendum.md.
- Boundary: behavior plots are qualitative mechanism illustrations only, not replacements for aggregate metrics.

## 2026-07-01 final paper manifest and PDF placement

- Created `codex_longrun_iscsic/final_paper_manifest_20260701_0415`.
- Paper-facing PDFs copied to `codex_longrun_iscsic/final_paper_manifest_20260701_0415/pdf_figures/`.
- Tables/TeX copied or generated in the manifest root; aggregate claim source remains `codex_longrun_iscsic/paper_tables_20260701_0258`.
- Historical run PDFs remain in `outputs/*/figures/` for provenance only.

## 2026-07-01 external seed robustness nenv16 launched

- Time: 2026-07-01T04:27:43.008115+08:00.
- Root: `outputs/external_seed_robustness_nenv16_20260701_0425`.
- Driver: `codex_longrun_iscsic/run_external_seed_robustness_nenv16_20260701_0425.sh`.
- Active PID at launch check: driver `116825`.
- Protocol: frozen completed models, `n_envs=16`, `episodes=50`, densities `0.08/0.15`, external `test_start_seed=20000/30000`.
- Variants: `guard_only`, `shield_only`, `retuned_full`, `proposed_gated_risk`, `risk_only`, `no_action_guard`; seeds `0/1/2` each.
- Purpose: reviewer-facing external scenario-seed validation of the guard/shield-centered paper claim, not new reward tuning.
- Decision rule: aggregate by label/density after each finished unit; if positive methods degrade, report sensitivity instead of hiding it; do not interpret risk-only zero cost without route completion.
