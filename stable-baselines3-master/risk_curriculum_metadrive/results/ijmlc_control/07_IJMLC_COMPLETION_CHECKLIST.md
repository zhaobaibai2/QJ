# IJMLC 总完成清单

## A. 已建立的控制面

- [x] IJMLC 大框架：`00_IJMLC_BIG_FRAMEWORK.md`
- [x] 实验矩阵与目的：`01_EXPERIMENT_MATRIX_AND_PURPOSE.md`
- [x] 举证体系：`02_EVIDENCE_SYSTEM.md`
- [x] 运行队列：`03_RUN_QUEUE.md` / `03_RUN_QUEUE.csv`
- [x] 监督协议：`04_SUPERVISION_PROTOCOL.md`
- [x] 当前状态：`05_CURRENT_STATUS.md`
- [x] 现有模型 manifest：`06_EXISTING_MODEL_MANIFEST.csv`
- [x] 资源 watchdog：`watchdog_resource_guard.py`，MemAvailable < 3GB 自动停止当前 IJMLC 队列。
- [x] 资源恢复计划：`RESOURCE_GUARD_RESUME_PLAN.md`，触发后降并行到 8 并只重跑未完成 shard。

## B. 已完成实验/数据

- [x] P1 d=0.15 核心 IJMLC 诊断：6 methods × 3 seeds × 40 episodes = 720 episodes。
- [x] d=0.15 raw：`raw_csv/p1_d015_core_all_episodes.csv`
- [x] d=0.15 aggregate：`summary_tables/p1_d015_core_full_aggregate.csv`
- [x] d=0.15 report：`P1_D015_CORE_DIAGNOSTIC_REPORT.md`

## C. 已完成的长跑监督

- [x] P4 density/stress 扩展：d=0.08/0.20/0.25，6 methods × 3 seeds × 120 episodes。
- [x] 自动监控快照：`density_expand_monitor_latest.md`

## D. 后续必须补的数据

- [x] 合并 d=0.08/0.20/0.25 与 d=0.15，生成完整 density sweep 表。
- [x] 外部 baseline 1：RCPO/PPO-Lagrangian，3 seeds × 1M timesteps，训练使用 `--n-envs 16`。
- [x] 外部 baseline 2：RSS/TTC classical safety filter baseline，3 seeds × 4 densities × 40 episodes。
- [x] sensitivity：ttc_threshold 与 target_speed_kmh 冻结模型 eval 已完成；brake cap 仍作为后续可选扩展，不改正式协议。
- [~] 5-seed 扩展：当前 CI/P2 证据已足够，seed3/seed4 保留为 reviewer-demand 备用；见 `P3_SEED_EXTENSION_DECISION.md`。
- [x] runtime overhead Table 7：`manuscript/table7_runtime_overhead.csv` / `.tex`。
- [x] Wilson / bootstrap CI：`manuscript/table_supp_ci_d015.csv` 与 `table_supp_seed_scatter_d015.csv`。

## E. 后续必须补的图表

- [x] Fig.1 Cybernetic closed-loop runtime intervention architecture：`figures/fig1_runtime_architecture.pdf/png`。
- [x] Fig.2 Non-motion artifact：`figures/fig2_non_motion_artifact.pdf/png`。
- [x] Fig.3 Progress-safety frontier：`figures/fig3_progress_safety_frontier.pdf/png`。
- [x] Fig.4 Mechanism ablation / no-action-guard collapse：`figures/fig4_mechanism_ablation.pdf/png`。
- [x] Fig.5 Density and stress generalization：`figures/fig5_density_stress.pdf/png`。
- [x] Fig.6 Intervention/TTC/speed diagnostics：`figures/fig6_intervention_ttc_speed.pdf/png`。
- [x] Fig.7 Sensitivity analysis：`figures/fig7_sensitivity_ttc_threshold.*` 与 `figures/fig7_sensitivity_target_speed_kmh.*`；runtime overhead 图另见 `fig7_runtime_overhead.*`。

## F. 后续必须补的论文交付

- [ ] Springer IJMLC LaTeX source。
- [ ] 150-250 words abstract。
- [ ] 4-6 keywords。
- [ ] Related Work 扩到 safe RL / shielding / CBF / RSS / reward hacking / MetaDrive closed-loop。
- [ ] Data Availability Statement。
- [ ] Code Availability Statement。
- [ ] Competing Interests。
- [ ] Funding。
- [ ] Author Contributions。
- [ ] claim audit：禁止 formal safety / certified safe / real-world proof。
