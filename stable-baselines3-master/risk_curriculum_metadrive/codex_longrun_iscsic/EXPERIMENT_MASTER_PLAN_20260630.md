# EXPERIMENT_MASTER_PLAN_20260630

更新时间：2026-06-30 CST
当前正式资源约束：CPU available >= 4GB；GPU free >= 2GB。当前正式并行协议：train/eval n_envs=16。n_envs=32 已完成同 seed 诊断，吞吐更快但 held-out d0.08/d0.15 质量更差，只保留为吞吐诊断，不进正式结果表。

## 论文主线

目标不是单纯提高平均成功率，而是证明：风险感知奖励 + 自适应课程 + 动作安全约束/defensive shield 可以在交通密度升高时降低碰撞/代价，同时尽量保持 route completion 和 success。所有实验都要回答一个论文问题：

1. 主方法是否比 vanilla PPO、risk-only、curriculum-only 更好？
2. TTC 风险项、车道/平滑项、动作 guard/shield、课程推进分别贡献了什么？
3. defensive fixed branch 是否在高密度下提供更强 safety-success tradeoff？
4. 结果是否跨 seed 稳定，还是只靠单 seed？
5. 参数变化是否解释了方法机制，而不是偶然调参？

## 正式协议

### 通用评估口径

- densities: 0.00, 0.08, 0.15
- episodes: 50 per density
- eval_n_envs: 16
- 结果文件必须包含 eval_n_envs=16 或由对应 config/run 明确证明。
- 旧结果只有当 train_n_envs/eval_n_envs/horizon/timesteps 与当前任务一致时才能进正式表；否则只能进 historical/diagnostic appendix。

### Branch A: defensive final branch

- output root: outputs/defensive_ttc12_v18_nenv16_final
- script: scripts/run_one_defensive_proposed.py
- seeds: 26, 27, 28 first; if variance high, extend 29, 30.
- timesteps: 1,000,000
- horizon: 1500
- target_speed_kmh: 18.0
- ttc_threshold: 12.0
- key reward changes: ttc=6, cost=40, overspeed=3, progress=40, success_bonus=55, crash/out=120.
- acceptance gate after seed28:
  - d0.08 mean success >= 0.85 and mean cost <= 0.12 preferred.
  - d0.15 mean success >= 0.60 and mean cost <= 0.25 minimum.
  - If d0.15 mean cost > 0.25 or success < 0.60, do not freeze; run targeted tuning.

### Branch B: standard main comparison

- output root: outputs/iscsic_main_nenv16_v2
- runner: codex_longrun_iscsic/run_formal_variant_nenv16.sh
- variants: baseline, risk, curriculum, proposed
- seeds: 0, 1, 2
- timesteps: start with 1,000,000; if proposed/risk underfit at d0.15, run 1,500,000 diagnostic for the weak variant/seed before replacing protocol.
- horizon: 1200
- purpose:
  - baseline: vanilla PPO reference.
  - risk: risk reward without curriculum, tests safety shaping alone.
  - curriculum: curriculum without risk reward/guard, tests exposure schedule alone.
  - proposed: full standard method, tests synergy.
- expected pattern:
  - baseline may have lower safety at d0.08/d0.15.
  - risk should reduce cost/collision relative to baseline, possibly with success tradeoff.
  - curriculum should improve route/success relative to baseline at higher density.
  - proposed should improve safety-success tradeoff over all three.

### Branch C: component ablation

- output root: outputs/iscsic_ablation_nenv16_v2
- runner: codex_longrun_iscsic/run_formal_variant_nenv16.sh
- P0 variants: proposed_wo_ttc, no_action_guard
- P1 variants: proposed_wo_lane, proposed_wo_smooth, reward_only, guard_only, shield_only
- seeds: 0, 1, 2
- timesteps: 1,000,000 initial; rerun only if the ablation result is unstable or contradicts mechanism expectations.
- horizon: 1200
- expected pattern:
  - proposed_wo_ttc should worsen medium/high-density safety.
  - no_action_guard should strongly worsen safety/completion; previous screen showed collapse.
  - reward_only vs guard_only separates reward shaping from action-level intervention.
  - proposed_wo_lane/proposed_wo_smooth should affect lane deviation/smoothness more than raw success.

### Branch D: robustness and stress evaluation

Run only after Branch A/B/C candidate models are fixed.

- evaluation-only densities: 0.20 and 0.25, no retraining.
- purpose: appendix/stress table; not used to tune primary claims unless the main protocol is already accepted.
- include route_completion, cost, collision, out_of_road, shield rates.

### Branch E: parameter sensitivity

Run only when a result fails its gate or needs mechanism explanation.

Candidate defensive screens:

- ttc_threshold: 10, 12, 14
- target_speed_kmh: 16, 18, 20
- cost weight: 40, 50, 60
- stage2 gate: success 0.40/0.50 and cost 0.20/0.25

Use 500k or 1M single-seed screens first; promote only if it beats current branch on d0.15 without damaging d0.08.

## Per-run review protocol

每个 run 完成后必须做以下检查，再决定下一步：

1. Protocol check: train_n_envs, eval_n_envs, timesteps, horizon, densities, episodes 是否符合本 plan。
2. Resource check: 是否保持 CPU/GPU 安全线；若低于安全线，降并行或停止新启动。
3. Metric check: density-wise success/cost/collision/out/route/shield rates。
4. Mechanism check: 结果是否符合该 variant 的预期机制；若不符合，检查日志、config 和是否 seed 方差。
5. Decision:
   - accept: 进入正式表/均值。
   - diagnostic only: 保留但不进正式表。
   - rerun same protocol: 怀疑 seed 方差或异常。
   - tune: 明确指出要改哪个参数以及为什么。

## 当前立即任务

1. 等 outputs/defensive_ttc12_v18_nenv16_final seed28 完整训练和评估。
2. 计算 defensive seed26/27/28 三种子均值。
3. 若 defensive gate 通过，冻结 Branch A 并启动 Branch B 的 baseline/risk/curriculum/proposed。
4. 若 defensive gate 不通过，先做 Branch E 的针对性 tuning，不把当前 branch 当最终主方法。
5. 无论 Branch A 是否冻结，Branch B/C 都要补，因为论文需要对比和消融证据。
