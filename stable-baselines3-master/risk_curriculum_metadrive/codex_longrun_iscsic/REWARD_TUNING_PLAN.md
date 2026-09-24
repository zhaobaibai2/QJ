# REWARD_TUNING_PLAN

更新时间：2026-06-30

## 目的

针对当前 `proposed` 在 hard/high-density 阶段 success 偏低的问题，系统检查 reward 权重是否导致“安全/限速/guard 过强，完成率激励不足”。所有调参必须可追溯到命令、config.json、CSV、日志和结论。

## 当前主线 RewardWeights

```text
base_scale=0.5
ttc=2.0
lane=0.5
smooth=0.02
accel=0.01
cost=20.0
overspeed=2.0
target_speed_kmh=20.0
progress=30.0
idle_penalty=0.15
min_speed_kmh=2.0
success_bonus=40.0
crash_penalty=80.0
out_of_road_penalty=80.0
ttc_threshold=5.0
```

## 当前观察

- `risk` seeds 1/2：低/中密度稳定，高密度 success 0.40/0.46 且 cost 0.52，说明 risk reward+guard 可工作但高密度碰撞仍明显。
- `proposed` seed0/1：d0.15 差异大，seed0 success 0.60，seed1 success 0.32。
- `proposed` seed2 训练中：进入 stage3/4 后 success_rate 下降到约 0.08-0.24，route 约 0.70-0.73，cost 约 0.33-0.38，提示 hard-stage reward 权衡可能不合适。

## 调参原则

1. 不中途修改正在跑的正式主协议 run。
2. 每个 screen 独立目录，命名包含 changed mechanism。
3. 每次优先改 1-3 个直接相关 reward 权重，避免解释不清。
4. 先用 500k screen seed2 或 seed28，n_envs=10，eval_n_envs=10，episodes=30/50；通过后再扩展到 1.0M/1.5M 和多 seed。
5. 所有结果记录到 `REWARD_TUNING_LEDGER.md`，失败记录到 `FAILED_RUNS.md`。
6. 正式论文主表只用完整协议；screen 只能作为调参证据或附录诊断。

## 第一批候选 screens

### R1 completion_boost

假设：progress/success 激励不足，策略在 hard stage 安全行驶但不完成。

参数：
- `--reward-progress 45`
- `--reward-success-bonus 80`
- 其他 reward/guard/stage 不变。

预期：提高 route/success；若 cost 大幅上升，则说明 completion 奖励过猛。

### R2 safety_soften

假设：安全/限速惩罚压制完成率。

参数：
- `--reward-cost 15`
- `--reward-overspeed 1.0`
- `--reward-crash-penalty 80` 保持不变。

预期：success 上升；若 collision/cost 上升过多，则不采用。

### R3 completion_plus_safety

假设：单纯提 completion 会增加碰撞，需要同时提高完成激励和终端事故惩罚。

参数：
- `--reward-progress 45`
- `--reward-success-bonus 80`
- `--reward-crash-penalty 120`
- `--reward-out-of-road-penalty 120`

预期：比 R1 更安全；若仍低 success，则 reward 不是唯一瓶颈，需看 guard/curriculum。

### R4 guard_ablation_priority

不是 reward weight screen，而是机制消融：
- `variant=no_action_guard`
- 默认 reward weights。

目的：区分 action guard 是否压制 hard-stage completion。

## 当前执行队列

1. 等当前 `proposed seed2` 正式 run 完成并评估。
2. 若 proposed seed2 final d0.15 仍弱，先跑 R1 500k screen。
3. 根据 R1 结果决定 R2/R3/R4 的顺序。
