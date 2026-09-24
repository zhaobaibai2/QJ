# 监督运行协议

更新时间：2026-07-01T16:30:08

## 1. 每次启动前

- 检查 GPU：显存至少保留 2GB。
- 检查 CPU/RAM：不把机器打满，至少保留 5GB RAM。
- 检查旧进程：不能误杀无关进程；有同类训练时先判断是否冲突。
- 写 run_manifest：没有 manifest 的实验不算正式启动。

## 2. 运行中

- 每 30 分钟以内要能刷新状态文件；长训练要记录 checkpoint、fps、GPU、早期指标。
- 如果出现 success=0，需要先判断是 idle collapse、unsafe crash、reward sign、环境配置还是步数不足。
- 小问题自己处理并记录，不反复询问。

## 3. 运行后

每个实验完成后必须分类：
- accepted_main
- accepted_appendix
- diagnostic_only
- rerun_required
- failed

完成后立即更新：
- 02_EVIDENCE_SYSTEM.md 或 evidence ledger
- 03_RUN_QUEUE.csv
- 05_CURRENT_STATUS.md
- 对应 raw_csv 和 summary_tables

## 4. 调参规则

不能看到一个结果不好就盲目重训。必须先写清楚失败模式：
- risk-only stagnation / non-motion
- no-action unsafe driving
- high-density collision
- overspeed or shield over-trigger
- threshold too conservative
- insufficient training
- logging/config bug

只有失败模式清楚，才启动新的调参分支。

## 5. 论文边界

所有监督记录都要保留 claim boundary：
- stress/external seed 是 frozen-model validation，不是 tuning。
- sensitivity 是 boundary analysis，不是主结果调参。
- runtime overhead 是仿真闭环开销，不是实车部署证明。


## 6. 并行环境说明 2026-07-01T16:37:47.848161

- 正式训练：继续使用远程 `sb3` conda 环境，正式训练命令必须显式 `--n-envs 16`，除非另有单独记录的资源测试结果。
- 普通正式评估：使用 `scripts/evaluate_from_config.py --n-envs 16` 做 VecEnv 并行评估。
- IJMLC 诊断评估：为记录每一步 speed/TTC/latency，单个 shard 使用单环境；为了速度，按 method/seed 拆成多个 shard 同时跑，当前 P1 使用 9 shard 并行。后续可扩到 16 shard，但必须保留 2GB 显存和 5GB RAM 安全余量。
- 任何不是 n_envs=16 的训练或普通评估都不能混入正式主表，除非单独标注为 diagnostic_only。
