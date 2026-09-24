# 资源保护后恢复计划

更新时间：2026-07-01T16:55:29

- 原始 run_group: `p1_density_expand_20260701_1655`
- 恢复 run_group: `p1_density_expand_resume_max8_20260701_165529`
- 恢复并行上限: 8
- 未完成 shard 数: 15
- manager script: `/home/aaa/data/qj/stable-baselines3-master/risk_curriculum_metadrive/results/ijmlc_control/logs/p1_density_expand_resume_max8_20260701_165529_manager.sh`

如果 watchdog 因 MemAvailable < 3GB 停止当前队列，后续使用这个 manager 只重跑未完成 shard。

待恢复 shard:
- risk_only seed0
- risk_only seed1
- risk_only seed2
- guard_only seed0
- guard_only seed1
- guard_only seed2
- shield_only seed0
- shield_only seed1
- shield_only seed2
- gated_risk seed0
- gated_risk seed1
- gated_risk seed2
- no_action_guard seed0
- no_action_guard seed1
- no_action_guard seed2
