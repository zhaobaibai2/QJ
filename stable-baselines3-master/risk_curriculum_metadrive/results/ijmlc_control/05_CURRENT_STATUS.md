# IJMLC 当前状态

更新时间：2026-07-01T16:30:08

## 已完成

- 已读取用户指定 pasted text，确认目标从短稿升级为 IJMLC 期刊版。
- 已确认远程 aaa 可连接，GPU 空闲，当前没有 MetaDrive 训练/评估进程。
- 已确认主要代码根目录：/home/aaa/data/qj/stable-baselines3-master/risk_curriculum_metadrive。
- 已确认远程 skill 根目录和可用 skill：/home/aaa/data/codex 与 /home/aaa/.codex/skills。
- 已确认旧 n_envs=16 evidence package 存在，但 IJMLC 新指标仍需补评估。
- 已建立 IJMLC 控制面目录：results/ijmlc_control。

## 当前判断

旧工作足以支撑短稿或会议式 guard/shield story，但 IJMLC 需要更完整的期刊证据：
- non-motion artifact 指标不足。
- runtime latency 表不足。
- 外部 baseline 不够。
- seed 数需要从 3 向 5 扩展，至少核心方法补齐。
- Springer 论文结构和声明还未完成。

## 下一步

1. 验证控制面文件完整。
2. 补一个稳定的 IJMLC 诊断评估脚本。
3. 先跑冻结模型 P1 诊断评估，补 stop ratio / low-progress / latency。
4. 根据诊断结果决定是否立即启动外部 baseline 实现或 seed 扩展训练。


## P1 启动记录 2026-07-01T16:33:11

- run_id: p1_d015_core_diag_20260701_1635
- 内容: baseline/risk_only/guard_only/shield_only/gated_risk/no_action_guard, seeds 0/1/2, density 0.15, test_start_seed 10000/20000, each 20 episodes.
- 目的: 补 non-motion artifact、progress-safety、TTC、intervention per km、runtime wall-clock diagnostics。
- 日志: results/ijmlc_control/logs/p1_d015_core_diag_20260701_1635.log


## P1 监督修正 2026-07-01T16:35:48

- 已中断 run_id=p1_d015_core_diag_20260701_1635。
- 原因：旧启动方式日志被 conda run 缓冲，脚本也只在最终结束时写 CSV，不利于长评估监督和恢复。
- 处理：evaluate_ijmlc_diagnostics.py 已增加每个模型完成后的 partial episode CSV 和 partial summary CSV。
- 下一步：用 conda run --no-capture-output 和 python -u 重新启动 P1。


## P1 重启 2026-07-01T16:36:07

- run_id: p1_d015_nonmotion_diag_20260701_1640
- 内容: risk_only / guard_only / no_action_guard, seeds 0/1/2, density 0.15, scenario starts 10000/20000, each 20 episodes。
- 目的: 先补 non-motion artifact 和 no-action-guard collapse 的 IJMLC 指标。
- partial 输出: raw_csv 和 summary_tables 下的 .partial.csv 文件。
- 日志: results/ijmlc_control/logs/p1_d015_nonmotion_diag_20260701_1640.log


## P1 并行重启 2026-07-01T16:36:58

- run_group: p1_d015_nonmotion_parallel_20260701_1645
- 已停止此前串行 run_id=p1_d015_nonmotion_diag_20260701_1640。
- 新策略：risk_only / guard_only / no_action_guard × seed0/1/2 共 9 个 shard 同时跑。
- 每个 shard: density=0.15, test_start_seed=10000/20000, episodes_per_start=20。
- 目的：加速 non-motion artifact 与 no-action-guard collapse 诊断，同时保留逐步 speed/TTC/latency 指标。
- 说明：训练协议和普通正式评估仍按 n_envs=16；这个 IJMLC 诊断采用 shard 并行而不是单个 VecEnv，因为需要 per-step 行为和 latency 统计。


## P1 第二批并行启动 2026-07-01T16:39:20.818498

- run_group: p1_d015_core_parallel2_20260701_1648
- 内容: baseline / shield_only / gated_risk × seed0/1/2，共 9 个 shard。
- 与第一批剩余 risk_only/guard_only 6 个 shard 并行，总并行约 15 个评估进程。
- 目的: 尽快补齐 d=0.15 的核心 non-motion/progress-safety/runtime 诊断表。


## P1 d=0.15 核心诊断完成 2026-07-01T16:49:40

- 完成 18 个 shard，720 episodes。
- 汇总表: results/ijmlc_control/summary_tables/p1_d015_core_full_aggregate.csv
- 报告: results/ijmlc_control/P1_D015_CORE_DIAGNOSTIC_REPORT.md
- 初步结论：risk_only 是 non-motion，no_action_guard 是 unsafe collapse，guard/shield/gated 提供 progress-safety 证据。


## P1 密度扩展启动 2026-07-01T16:50:09

- run_group: p1_density_expand_20260701_1655
- 内容: baseline/risk_only/guard_only/shield_only/gated_risk/no_action_guard × seed0/1/2 × density 0.08/0.20/0.25。
- 每个 label-density 目标 episodes: 3 seeds × 2 starts × 20 = 120。
- 并行上限: 16 shard。
- 目的: 生成 IJMLC Fig.5 density/stress generalization 和 Table 6。
- manager: results/ijmlc_control/logs/p1_density_expand_20260701_1655_manager.sh


## 资源 watchdog 已启动 2026-07-01T16:54:50

- 规则：CPU/RAM 侧 `MemAvailable < 3.0 GiB` 立即停止当前 IJMLC 诊断队列。
- 同时保留 GPU 保护：GPU free < 2048 MiB 也停止。
- 当前 watchdog: `results/ijmlc_control/watchdog_resource_guard.py`。
- 日志: `results/ijmlc_control/logs/resource_watchdog.log`。
- 说明：Linux 的 free 内存会被缓存占用，所以用 MemAvailable 判断真实可用内存。


## 资源保护恢复脚本已生成 2026-07-01T16:55:29

- 如果 MemAvailable < 3GB，watchdog 会停止当前 IJMLC 诊断队列。
- 已生成 `results/ijmlc_control/resume_density_expand_incomplete.py`，用于只重跑未完成 shard。
- 恢复并行上限会从 16 降到 8。
- 恢复计划文件：`results/ijmlc_control/RESOURCE_GUARD_RESUME_PLAN.md`。


## P1 全密度诊断完成 2026-07-01T17:24:32

- 完成 d=0.08/0.15/0.20/0.25 的核心诊断，合计 2880 episodes。
- 全密度汇总: results/ijmlc_control/summary_tables/p1_all_density_core_aggregate.csv
- 全密度报告: results/ijmlc_control/P1_ALL_DENSITY_CORE_DIAGNOSTIC_REPORT.md
- watchdog 未触发，资源保护全程有效。
- 下一步转入 P2 外部 baseline 审计/实现。


## P2 外部 baseline 已启动 2026-07-01T17:37:04

- RCPO/PPO-Lagrangian：正式训练已启动，seed0/1/2 顺序跑，每个 seed `--n-envs 16 --timesteps 1000000`。
- RSS/TTC classical filter：已启动 3 个 seed 诊断 shard，使用 `--action-filter rss_ttc`，不改变训练模型。
- 监督：`resource_watchdog` 已覆盖 P2 训练/诊断；MemAvailable < 3 GiB 或 GPU free < 2048 MiB 会停当前 P2 任务。
- post-manager：RCPO 三个 seed 训练完成后自动运行 `evaluate_from_config.py --n-envs 16` 和 IJMLC 诊断评估。


## P2 外部 baseline 完成 2026-07-01T18:23:26

- RCPO/PPO-Lagrangian：3 个 seed 全部完成，训练均为 `--n-envs 16 --timesteps 1000000`。
- RCPO 正式 eval：3 个 seed 已完成 `evaluate_from_config.py --n-envs 16`。
- RCPO IJMLC 诊断：480 episodes 已完成。
- RSS/TTC classical filter：480 episodes 已完成。
- Table4：`results/ijmlc_control/manuscript/table4_external_baselines_d015.csv`。
- 结论边界：RCPO 训练型 baseline 在 d=0.15 失败，RSS/TTC 有效但弱于 Guard/Shield/Gated；这支持 runtime intervention 主线。


## P5 sensitivity 启动 2026-07-01T18:25:14

- run_group: p5_sensitivity_20260701_1825。
- 内容: guard_only / shield_only / gated_risk × seed0/1/2 × ttc_threshold(6,8,10,12) 与 target_speed_kmh(15,18,22)。
- 每个 shard: density=0.15, starts=10000/20000, episodes_per_start=20。
- 目标: `table_supp_sensitivity.csv` 和 `fig7_sensitivity_*.pdf/png`。
- 监督: watchdog 已覆盖 p5 manager；MemAvailable < 3 GiB 或 GPU free < 2048 MiB 会停当前 P5 任务。


## P5 sensitivity 完成 2026-07-01T19:12:50

- 完成 63/63 shards，合计 2520 episodes。
- raw: `results/ijmlc_control/raw_csv/p5_sensitivity_all_episodes.csv`。
- aggregate: `results/ijmlc_control/summary_tables/p5_sensitivity_aggregate.csv`。
- table: `results/ijmlc_control/manuscript/table_supp_sensitivity.csv`。
- figures: `fig7_sensitivity_ttc_threshold.*` 与 `fig7_sensitivity_target_speed_kmh.*`。
- watchdog 未触发。


## P6 manuscript package complete 2026-07-01T19:27:06

- Springer Nature official template package downloaded; `sn-jnl.cls` and `.bst` files copied into `results/ijmlc_control/manuscript_ijmlc_20260701`.
- Generated `main.tex`, `references.bib`, `claim_evidence_map.md`, `writing_rationale_matrix.md`, `submission_checklist.md`, and `README_先看.md`.
- Figures copied to the same level as `main.tex` for Springer submission compatibility.
- `latexmk` compiled `main.pdf` successfully: 13 pages, abstract word count 217, return code 0.
- Final manuscript still uses anonymous author placeholders and needs final author/funding/contribution/public-repository details before real submission.


## P6 citation verification complete 2026-07-01T19:29:37

- `references.bib` updated with URL/DOI/arXiv/PMLR/JMLR/AAAI-backed metadata.
- `citation_verification_report.md` generated in `results/ijmlc_control/manuscript_ijmlc_20260701`.
- Recompiled `main.pdf` successfully after bibliography update; latexmk return code 0.


## Publication table/figure revision

- Revised report: `results/ijmlc_control/FIGURE_TABLE_REVISION_REPORT.md`
- New figure directory: `results/ijmlc_control/figures_publication`
- New table directory: `results/ijmlc_control/tables_publication`
- Main manuscript now uses complete diagnostic tables and six redesigned publication figures.


## Publication table/figure revision

- Revised report: `results/ijmlc_control/FIGURE_TABLE_REVISION_REPORT.md`
- New figure directory: `results/ijmlc_control/figures_publication`
- New table directory: `results/ijmlc_control/tables_publication`
- Main manuscript now uses complete diagnostic tables and six redesigned publication figures.


## Publication table/figure revision

- Revised report: `results/ijmlc_control/FIGURE_TABLE_REVISION_REPORT.md`
- New figure directory: `results/ijmlc_control/figures_publication`
- New table directory: `results/ijmlc_control/tables_publication`
- Main manuscript now uses complete diagnostic tables and six redesigned publication figures.


## Publication table/figure revision

- Revised report: `results/ijmlc_control/FIGURE_TABLE_REVISION_REPORT.md`
- New figure directory: `results/ijmlc_control/figures_publication`
- New table directory: `results/ijmlc_control/tables_publication`
- Main manuscript now uses complete diagnostic tables and six redesigned publication figures.


## Publication table/figure revision

- Revised report: `results/ijmlc_control/FIGURE_TABLE_REVISION_REPORT.md`
- New figure directory: `results/ijmlc_control/figures_publication`
- New table directory: `results/ijmlc_control/tables_publication`
- Main manuscript now uses complete diagnostic tables and six redesigned publication figures.


## Publication table/figure revision

- Revised report: `results/ijmlc_control/FIGURE_TABLE_REVISION_REPORT.md`
- New figure directory: `results/ijmlc_control/figures_publication`
- New table directory: `results/ijmlc_control/tables_publication`
- Main manuscript now uses complete diagnostic tables and six redesigned publication figures.


## Publication table/figure revision

- Revised report: `results/ijmlc_control/FIGURE_TABLE_REVISION_REPORT.md`
- New figure directory: `results/ijmlc_control/figures_publication`
- New table directory: `results/ijmlc_control/tables_publication`
- Main manuscript now uses complete diagnostic tables and six redesigned publication figures.


## Publication table/figure revision

- Revised report: `results/ijmlc_control/FIGURE_TABLE_REVISION_REPORT.md`
- New figure directory: `results/ijmlc_control/figures_publication`
- New table directory: `results/ijmlc_control/tables_publication`
- Main manuscript now uses complete diagnostic tables and six redesigned publication figures.


## IJMLC journalization revision

- Generated: 2026-07-01T20:01:33
- Manuscript: `results/ijmlc_control/manuscript_ijmlc_20260701/main.tex` and `main.pdf`
- Report: `results/ijmlc_control/IJMLC_JOURNALIZATION_REPORT.md`
- Generator: `results/ijmlc_control/scripts/build_ijmlc_journal_revision.py`
- Key changes: IJMLC cybernetic-feedback framing, expanded related work, formal method equations, Algorithm 1, claim-to-evidence table, mechanism-decomposition table, revised Fig. 1/Fig. 2/Fig. 5/Fig. 6, no rotated tables.
- Known evidence boundary: current raw CSVs are episode-level; representative step-level trace figure requires a future diagnostic run with per-step logging.

<!-- IJMLC_JOURNAL_REVISION_FINAL_START -->

## IJMLC journal revision final status (2026-07-01 20:10:22)

- Manuscript package: `results/ijmlc_control/manuscript_ijmlc_20260701`.
- Final compiled PDF: `manuscript_ijmlc_20260701/main.pdf`, 26 pages, 34 references.
- Table orientation fix: all generated main-text and appendix tables are portrait `table` floats; generated manuscript/table files contain no `sidewaystable`, `landscape`, `resizebox`, or `rotatebox` commands.
- Table interpretation fix: main and appendix metric headers now mark desired directions, e.g. success/route `up`, cost/collision/out/TTC/stop/low-progress `down`; density summary reports `Cost red.` and `Route gain` explicitly.
- Visual polish: paragraph-style tables use ragged-right columns to avoid stretched text and ugly forced hyphenation; Fig. 1 and Fig. 2 label overlaps were removed.
- Evidence scope: training/ordinary evaluation use 16 SB3 parallel environments; IJMLC diagnostics are per-seed shards for episode-level TTC/speed/stop/intervention/route/latency traceability.
- Supervision: resource watchdog remains the required guard; it stops IJMLC jobs when Linux MemAvailable is below 3.0 GiB or free GPU memory is below 2048 MiB.
- Limitation retained: current raw CSVs are episode-level, not step-level; no representative route/speed/TTC time-series trace was fabricated.

<!-- IJMLC_JOURNAL_REVISION_FINAL_END -->
