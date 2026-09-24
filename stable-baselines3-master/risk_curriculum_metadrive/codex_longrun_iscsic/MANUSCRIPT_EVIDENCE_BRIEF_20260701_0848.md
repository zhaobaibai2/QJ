# 论文写作证据简报 2026-07-01

更新时间：2026-07-01T08:47:17+08:00

## 一句话主线

当前 16 环境正式证据支持的论文主线是：在 MetaDrive 密集交通设置中，动作级安全约束/安全屏蔽是稳定安全驾驶的主机制；风险奖励、TTC、车道和平滑项、条件式 gated risk 是对该机制的解释和补强，而不是单独主导性能的来源。

不要把论文写成“risk reward 本身最强”或“full proposed 全面优于所有简化方法”。这会和当前表格冲突。

## 可以写的核心贡献

1. 提出并验证一套 guard/shield-centered safe RL 框架，在 16 环境训练/评估协议下显著改善 dense traffic 中的安全-完成率权衡。
2. 通过 no-action-guard、risk-only、curriculum-only、TTC/lane/smooth ablations 分离机制贡献，证明动作级约束是必要条件，奖励项主要提供行为细化。
3. 通过 stress density 0.20/0.25、external scenario-seed 20000/30000 和代表性轨迹图补充 reviewer-facing robustness 证据。
4. 通过 gated risk addendum 说明风险塑形需要和进度/局部风险条件结合，否则 risk-only 会学成低速停滞的“假安全”。

## 不能写的过度主张

- 不能说 risk-only 是安全最优；它的零 cost 来自几乎不动，d0.15 route completion 约 0.009。
- 不能说 gated risk 显著优于 shield_only；external seed d0.15 Wilson 区间重叠。
- 不能说 full proposed 全密度全面第一；formal/stress/external 表里 guard_only 或 shield_only 经常更强。
- 不能把 stress density 0.20/0.25 写成训练优化目标；它们是 frozen-model robustness probes。
- 不能混用 n_envs=8/10/32 的诊断结果进入正式主表；正式表以 n_envs=16 为准。

## 主表写法

### Table 1: formal main results at density 0.15

文件：`codex_longrun_iscsic/final_paper_manifest_20260701_0415/table1_formal_main_d015.csv`

建议叙述：

- baseline 和 curriculum-only 在 d0.15 均为 success=0、cost=1，说明没有动作级约束时，密集交通 held-out 场景不可用。
- risk-only success=0、cost=0、route≈0.009，说明单纯风险惩罚会产生停滞策略，不能被解释为安全驾驶。
- guard_only d0.15 success=0.633、cost=0.207；shield_only success=0.627、cost=0.227，是最干净的强机制证据。
- full/proposed/gated variants 接近该性能带，但没有稳定超过 guard/shield，因此应该作为完整方法和机制补强呈现。

### Table 2: ablation at density 0.15

文件：`codex_longrun_iscsic/final_paper_manifest_20260701_0415/table2_ablation_d015.csv`

建议叙述：

- no_action_guard d0.15 success=0、cost=1，是动作级约束必要性的最强证据。
- wo_ttc d0.15 success=0.540、cost=0.360，比 guard_only/full 候选更差，支持 TTC 是高密度安全 refinement。
- wo_lane 的 lane deviation 明显上升，说明车道项主要改善横向稳定性，而不是简单提升 success。
- wo_smooth 体现稳定性和 seed variance 问题，适合放在机制解释里，不适合作为主贡献。

### Table 3: stress density 0.20/0.25

文件：`codex_longrun_iscsic/final_paper_manifest_20260701_0415/table3_stress_ranked.csv`

建议叙述：

- density 0.20 下 shield_only 最高 success=0.480，proposed_gated_risk 和 retuned full 接近；说明正方法在 OOD 密度下是 graceful degradation，不是崩溃。
- density 0.25 下 guard_only 是最干净 survivor，success=0.267、cost=0.487；这支持 guard-centered 机制，而不是 full risk-reward dominance。
- risk 在 stress 表中仍是 route≈0.009 的停滞控制，不能被写成“安全”。

### Table 4: external scenario-seed robustness

文件：

- `codex_longrun_iscsic/final_paper_manifest_20260701_0415/table4_external_seed_robustness.csv`
- `codex_longrun_iscsic/final_paper_manifest_20260701_0415/table4_external_seed_robustness_d015_wilson95.csv`

建议叙述：

- 外部 scenario seeds 20000/30000 下，shield_only d0.15 success=0.687、cost=0.207；proposed_gated_risk success=0.663、cost=0.213；guard_only success=0.613、cost=0.240。
- proposed_gated_risk 的成功率 Wilson 95% 区间约为 [0.608, 0.714]，shield_only 约为 [0.632, 0.737]，二者重叠；因此写成“competitive/refinement”，不要写成显著优越。
- no_action_guard 在外部种子下 success=0、cost=1，复现了动作约束必要性。

## 图的用法

图清单：`codex_longrun_iscsic/final_paper_manifest_20260701_0415/figure_manifest.csv`

推荐用法：

- framework diagram：只作为方法结构图，不当作结果证据。
- behavior rollouts d0.15/d0.25：用于解释为什么 no_action_guard 是高速碰撞/偏离，risk-only 是停滞，guard/shield 是完成率与安全折中。
- source_single_seed_metrics：只作为诊断图，不替代 aggregate tables。

## 结果段落骨架

可以按以下顺序写 Results：

1. Formal comparison: dense held-out d0.15 中，baseline/curriculum-only/no-action-guard 失败，guard/shield 形成稳定安全完成率带。
2. Mechanism ablation: 移除 action guard 直接崩溃，移除 TTC/lane/smooth 造成不同维度退化，证明组件不是任意堆叠。
3. Risk-shaping diagnosis: risk-only 停滞，gated risk 恢复 progress，说明风险塑形必须条件化。
4. Robustness: stress density 和 external scenario seeds 下，正方法保持 graceful degradation，负控仍失败。
5. Claim boundary: 全文收束为 action guard/shield-centered robustness，而非 reward-only 或 full-method dominance。

## 当前不建议继续跑的实验

- 不建议继续 TTC-only tuning：`defensive_ttc14_v18_nenv16_tuning` d0.15 success=0.573、cost=0.260，未过 0.60/0.25 gate。
- 不建议继续 reward-only/lane-only micro tuning：已有多个诊断显示 seed trade-off 明显，且不能超过 guard/shield 主线。
- 不建议启动 n_envs=32 正式表：已有诊断指出吞吐更快但 held-out 质量更差，只能保留为资源诊断。

## 如果审稿人追问，优先补的不是训练

1. 给出 seed-level robustness 表和 Wilson 区间，而不是新增随机 tuning。
2. 补充行为轨迹解释 no_action_guard 与 risk-only 的失败模式。
3. 明确 frozen-model stress/external-seed 协议，强调没有用 test seeds 调参。
4. 若必须新增实验，只做窄范围 reviewer validation，例如新增一个 external test_start_seed，而不是改方法参数。

## 远端证据入口

- 完整审计：`codex_longrun_iscsic/EXPERIMENT_COMPLETION_AUDIT_20260701_0845.md`
- 完成矩阵：`codex_longrun_iscsic/EXPERIMENT_REQUIREMENT_MATRIX_20260701_0845.csv`
- 最终 manifest：`codex_longrun_iscsic/final_paper_manifest_20260701_0415/`
- 原始聚合表：`codex_longrun_iscsic/paper_tables_20260701_0258/`
- 行为图：`codex_longrun_iscsic/behavior_rollouts_20260701_0406/`
