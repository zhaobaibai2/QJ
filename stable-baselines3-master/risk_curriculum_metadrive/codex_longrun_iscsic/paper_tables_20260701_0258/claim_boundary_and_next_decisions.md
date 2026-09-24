# Claim Boundary And Next Decisions

时间：2026-07-01T02:57:35.308647+08:00

## 当前主线判断

当前最强、最稳的论文主线不是“risk reward 主导”，而是：

**action-level guard / shield 是主要稳定机制；risk reward、TTC、lane、smooth/curriculum 是辅助 refinement，用于解释特定失败模式和组件贡献。**

这个边界来自四类证据：

1. 主对照：baseline/curriculum/risk 三种子正式对照都失败；guard_only/shield_only 是强对照。
2. 消融：no_action_guard 三种子 held-out 失败最明显，说明 action guard 是必要机制。
3. reward component：wo_ttc/wo_lane/wo_smooth 支持 TTC、lane、smooth 是 refinement，但不是主导因素。
4. stress：0.20/0.25 下 guard/shield 仍是最好或最稳，full proposed/retune 没有超过 guard/shield。

## 不能写的 claim

- 不能写“risk reward 是主要性能来源”。risk-only 三种子几乎不动，zero cost 是 idle/stagnation。
- 不能写“full proposed 显著优于 guard_only/shield_only”。当前 full proposed 和 retune 在 d0.15/stress 都没有稳定超过 guard/shield。
- 不能用训练窗口 success 替代 held-out formal evaluation。baseline/curriculum 都出现过训练窗口短暂恢复，但最终评估失败。

## 可以写的 claim

- Action guard/shield 在密度提升时提供了主要稳定性。
- 去除 action guard 会导致 held-out 安全和完成度崩溃。
- TTC reward、lane reward、smooth/accel reward 改善特定维度，但贡献是 refinement。
- 高密度 stress 显示 guard-centered 方法有 graceful degradation，而 unguarded controls 失败。

## 是否继续调参

不建议继续做“只改 reward 权重”的 full proposed retune。理由：

- 多轮 full-risk retune 已经反复未超过 guard/shield。
- stress 下 retuned full proposed 在 d0.20 接近强基线，但 d0.25 比 guard_only 差。
- 继续微调 reward 很可能增加工作量但不改变论文主线。

如果必须继续提升自己的方法，下一轮不能只是改权重，应该改机制，例如：

1. 把 action guard 正式提升为主方法组件，重命名为 guard-centered method。
2. 设计 risk reward 的 gated/conditional 版本，只在 guard 允许且交通风险真实存在时作用，避免和完成度/稳定性冲突。
3. 先用 seed1/2 诊断小规模验证，再决定是否扩展 seed0，不再盲目全量三种子。

## 当前推荐写法

正文主线：

- Main method / mechanism: guard-centered safe policy optimization.
- Core evidence: guard_only/shield_only strong, no_action_guard fails, baseline/curriculum/risk fail.
- Full proposed: present as integrated candidate or refinement,但必须承认其相对 guard/shield 的优势不稳定。
- Stress: 0.20/0.25 作为 appendix robustness，强调 action guard graceful degradation。


## 2026-07-01 gated-risk addendum
- Added `gated_risk_mechanism_addendum.csv` and `gated_risk_mechanism_addendum.md`.
- Claim boundary: use gated-risk as mechanism evidence that conditional risk shaping avoids risk-only stagnation; do not replace the guard/shield-centered main result.


## 2026-07-01 gated-risk stress addendum
- Added `gated_risk_stress_mean.csv`, `gated_risk_stress_rank_with_existing.csv`, and `gated_risk_stress_addendum.md`.
- Stress boundary: proposed_gated_risk is competitive under 0.20/0.25 but does not overturn the guard/shield-centered main claim.


## 2026-07-01 behavior rollout addendum
- Added `behavior_rollout_addendum.md`, pointing to `codex_longrun_iscsic/behavior_rollouts_20260701_0406`.
- These trajectory plots are qualitative mechanism evidence only; aggregate formal/stress tables remain the quantitative source of truth.
