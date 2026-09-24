# 现有模型证据盘点

更新时间：2026-07-01T16:30:58

## 结论

已有 n_envs=16 三 seed 模型可以作为 IJMLC 第一批冻结模型诊断评估的基础。它们已有 success/cost/route/collision/out-road/TTC/intervention 的正式表，但缺少 IJMLC 新指标：stop ratio、median speed、low-progress、TTC dangerous fraction、latency、intervention per km。

## 方法标签

- baseline: 3/3 models ready; role=lower_bound
- curriculum: 3/3 models ready; role=curriculum_control
- gated_risk: 3/3 models ready; role=refinement
- guard_only: 3/3 models ready; role=action_intervention
- no_action_guard: 3/3 models ready; role=no_guard_negative_control
- retuned_full: 3/3 models ready; role=full_candidate
- risk_only: 3/3 models ready; role=non_motion_negative_control
- shield_only: 3/3 models ready; role=execution_intervention
- wo_lane: 3/3 models ready; role=component_ablation
- wo_smooth: 3/3 models ready; role=component_ablation
- wo_ttc: 3/3 models ready; role=component_ablation

## 缺失或异常
- none for selected core manifest

## 下一步

先对 baseline、risk_only、guard_only、shield_only、gated_risk、no_action_guard 做 d=0.15 冻结模型诊断评估；稳定后扩到 d=0.08/0.20/0.25，并生成 Fig.2/Fig.3/Table7 所需数据。

完整路径见 06_EXISTING_MODEL_MANIFEST.csv。
