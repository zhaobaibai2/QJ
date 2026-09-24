# P1 全密度核心 IJMLC 诊断报告

更新时间：2026-07-01T17:24:32

## 数据范围

- raw episode CSV: `results/ijmlc_control/raw_csv/p1_all_density_core_episodes.csv`
- aggregate CSV: `results/ijmlc_control/summary_tables/p1_all_density_core_aggregate.csv`
- seed summary CSV: `results/ijmlc_control/summary_tables/p1_all_density_core_seed_summary.csv`
- total episodes: 2880
- methods: baseline, risk_only, guard_only, shield_only, gated_risk, no_action_guard
- densities: 0.08, 0.15, 0.20, 0.25；每个 method-density 为 3 seeds × 40 episodes = 120 episodes。

## Density 0.08

| method | success | cost | route | collision | out-road | stop ratio | low-progress | TTC danger | interv/100 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| risk_only | 0.000 | 0.000 | 0.009 | 0.000 | 0.000 | 1.000 | 1.000 | 0.000 | 0.000 |
| baseline | 0.000 | 1.000 | 0.258 | 0.433 | 0.567 | 0.001 | 0.425 | 0.555 | 0.000 |
| no_action_guard | 0.025 | 0.975 | 0.287 | 0.358 | 0.617 | 0.001 | 0.433 | 0.404 | 0.000 |
| guard_only | 0.850 | 0.050 | 0.968 | 0.025 | 0.025 | 0.005 | 0.000 | 0.138 | 84.512 |
| shield_only | 0.833 | 0.067 | 0.965 | 0.067 | 0.000 | 0.005 | 0.000 | 0.103 | 84.686 |
| gated_risk | 0.850 | 0.042 | 0.969 | 0.042 | 0.000 | 0.006 | 0.000 | 0.134 | 84.164 |

## Density 0.15

| method | success | cost | route | collision | out-road | stop ratio | low-progress | TTC danger | interv/100 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| risk_only | 0.000 | 0.000 | 0.009 | 0.000 | 0.000 | 1.000 | 1.000 | 0.000 | 0.000 |
| baseline | 0.000 | 1.000 | 0.207 | 0.633 | 0.367 | 0.001 | 0.575 | 0.604 | 0.000 |
| no_action_guard | 0.008 | 1.000 | 0.217 | 0.533 | 0.467 | 0.002 | 0.558 | 0.487 | 0.000 |
| guard_only | 0.592 | 0.208 | 0.864 | 0.183 | 0.025 | 0.024 | 0.000 | 0.118 | 69.646 |
| shield_only | 0.625 | 0.192 | 0.857 | 0.158 | 0.033 | 0.028 | 0.008 | 0.114 | 70.751 |
| gated_risk | 0.617 | 0.183 | 0.869 | 0.183 | 0.000 | 0.035 | 0.008 | 0.114 | 67.872 |

## Density 0.2

| method | success | cost | route | collision | out-road | stop ratio | low-progress | TTC danger | interv/100 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| risk_only | 0.000 | 0.000 | 0.009 | 0.000 | 0.000 | 1.000 | 1.000 | 0.000 | 0.000 |
| baseline | 0.000 | 1.000 | 0.189 | 0.683 | 0.317 | 0.002 | 0.675 | 0.601 | 0.000 |
| no_action_guard | 0.000 | 1.000 | 0.203 | 0.658 | 0.342 | 0.002 | 0.667 | 0.505 | 0.000 |
| guard_only | 0.525 | 0.267 | 0.775 | 0.267 | 0.000 | 0.053 | 0.025 | 0.082 | 59.311 |
| shield_only | 0.475 | 0.333 | 0.764 | 0.308 | 0.025 | 0.051 | 0.000 | 0.082 | 58.941 |
| gated_risk | 0.392 | 0.325 | 0.754 | 0.325 | 0.000 | 0.052 | 0.025 | 0.072 | 57.070 |

## Density 0.25

| method | success | cost | route | collision | out-road | stop ratio | low-progress | TTC danger | interv/100 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| risk_only | 0.000 | 0.000 | 0.009 | 0.000 | 0.000 | 1.000 | 1.000 | 0.000 | 0.000 |
| baseline | 0.000 | 1.000 | 0.173 | 0.692 | 0.308 | 0.002 | 0.742 | 0.567 | 0.000 |
| no_action_guard | 0.000 | 1.000 | 0.168 | 0.692 | 0.308 | 0.002 | 0.733 | 0.577 | 0.000 |
| guard_only | 0.300 | 0.433 | 0.641 | 0.400 | 0.033 | 0.080 | 0.042 | 0.074 | 50.624 |
| shield_only | 0.250 | 0.500 | 0.646 | 0.458 | 0.042 | 0.082 | 0.050 | 0.083 | 52.020 |
| gated_risk | 0.183 | 0.525 | 0.613 | 0.517 | 0.008 | 0.084 | 0.042 | 0.090 | 48.157 |

## IJMLC 结论边界

- risk_only 在所有密度均用于支撑 non-motion artifact，而不是安全驾驶有效性。
- no_action_guard/baseline 用于 unsafe lower-bound/negative control。
- guard_only/shield_only/gated_risk 用于说明 runtime action/execution intervention 改变 progress-safety failure mode。
- 高密度 d=0.20/0.25 是 stress-boundary evidence，不作为调参后主胜利结论。
- 这些都是 frozen-model diagnostic evaluation，不是新训练。

## 下一步

1. 生成 Fig.2/Fig.3/Fig.5/Table7 的 CSV/图。
2. 审计并实现外部 baseline：PPO-Lagrangian/RCPO 与 RSS/TTC classical filter。
3. 根据外部 baseline 后的统计缺口，再决定 seed3/seed4 是否按 `--n-envs 16` 补训练。
