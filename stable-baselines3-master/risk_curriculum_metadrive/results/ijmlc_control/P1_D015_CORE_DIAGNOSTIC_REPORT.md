# P1 d=0.15 核心 IJMLC 诊断报告

更新时间：2026-07-01T16:49:40

## 数据范围

- raw episode CSV: `results/ijmlc_control/raw_csv/p1_d015_core_all_episodes.csv`
- aggregate CSV: `results/ijmlc_control/summary_tables/p1_d015_core_full_aggregate.csv`
- seed summary CSV: `results/ijmlc_control/summary_tables/p1_d015_core_seed_summary.csv`
- episode rows: 720
- labels: risk_only, baseline, no_action_guard, guard_only, shield_only, gated_risk
- 每个 label: 3 个 training seeds，每个 seed 40 episodes，density=0.15。
- 这是冻结模型诊断评估，不是重新训练，也不是调参。

## 关键表

| method | episodes | success | cost | route | collision | out-road | mean speed | stop ratio | low-progress | TTC danger | intervention/100 steps | control loop ms |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| risk_only | 120 | 0.000 | 0.000 | 0.009 | 0.000 | 0.000 | 0.013 | 1.000 | 1.000 | 0.000 | 0.000 | 4.119 |
| baseline | 120 | 0.000 | 1.000 | 0.207 | 0.633 | 0.367 | 41.053 | 0.001 | 0.575 | 0.604 | 0.000 | 10.290 |
| no_action_guard | 120 | 0.008 | 1.000 | 0.217 | 0.533 | 0.467 | 36.832 | 0.002 | 0.558 | 0.487 | 0.000 | 6.204 |
| guard_only | 120 | 0.592 | 0.208 | 0.864 | 0.183 | 0.025 | 15.802 | 0.024 | 0.000 | 0.118 | 69.646 | 8.373 |
| shield_only | 120 | 0.625 | 0.192 | 0.857 | 0.158 | 0.033 | 15.887 | 0.028 | 0.008 | 0.114 | 70.751 | 7.984 |
| gated_risk | 120 | 0.617 | 0.183 | 0.869 | 0.183 | 0.000 | 15.303 | 0.035 | 0.008 | 0.114 | 67.872 | 7.732 |

## 初步判断

- `risk_only` 支撑 non-motion artifact：success=0.000，cost=0.000，route=0.009，stop_ratio=1.000，low_progress=1.000。这说明低 cost 来自不动，不是安全驾驶。
- `no_action_guard` 支撑 unsafe collapse 负控制：success=0.008，cost=1.000，route=0.217，collision=0.533，out_road=0.467。
- `guard_only` 支撑 action-side intervention：success=0.592，route=0.864，cost=0.208，intervention/100 steps=69.646。
- `shield_only` 是 execution-side intervention 对照：success=0.625，route=0.857，cost=0.192。后续和 guard_only/gated_risk 共同写 guard vs shield 差异。
- `gated_risk` 是 progress-gated risk refinement：success=0.617，route=0.869，cost=0.183。后续不能夸大为 universally dominant，只能写 refinement/balance。

## 可写入 IJMLC 的证据用途

- Fig. 2 Non-motion artifact：risk_only 的 stop_ratio=1.0 与 route≈0，和 guard/shield/gated 对比。
- Fig. 3 Progress-safety frontier：x=route_completion，y=cost，点大小=success，颜色=method。
- Fig. 4 Mechanism ablation：no_action_guard 的 cost=1.0 和 low route，guard_only 的恢复。
- Table 7 Runtime overhead：policy/control-loop wall-clock latency；注意这只是仿真闭环开销，不是实车部署证明。

## 下一步

1. 扩展同样诊断到 d=0.08、0.20、0.25。
2. 补外部 baseline：simple PPO-Lagrangian/RCPO 与 RSS/TTC classical filter。
3. 如果正文统计仍显薄，再按 n_envs=16 训练 seed3/seed4。
