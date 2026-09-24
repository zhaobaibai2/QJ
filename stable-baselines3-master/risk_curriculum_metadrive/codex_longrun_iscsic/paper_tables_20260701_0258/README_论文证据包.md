# 论文证据表包 2026-07-01

生成时间：2026-07-01T02:57:35.308647+08:00

这个目录把当前 n_envs=16 的正式实验结果整理成论文可用表格。所有数值都来自远端已完成 aggregate 或 stress evaluation，不包含训练中间窗口。

## 文件

- `main_comparators_nenv16.csv`：主对照表，包含 baseline / curriculum / risk / guard_only / shield_only / full proposed candidate / retuned full proposed。
- `ablation_mechanism_nenv16.csv`：机制消融表，包含 no_action_guard / wo_ttc / wo_lane / wo_smooth / guard_only。
- `stress_density_020_025.csv`：冻结模型 stress evaluation，密度 0.20 和 0.25。
- `claim_boundary_and_next_decisions.md`：中文结论、主线边界、下一步是否继续调参的决策。

## 使用原则

1. 正文主表优先使用 `main_comparators_nenv16.csv` 中 density 0.00/0.08/0.15 的三种子均值。
2. 消融表优先使用 `ablation_mechanism_nenv16.csv`，尤其是 no_action_guard 的失败和 guard_only/shield_only 的强表现。
3. stress 表只能作为额外鲁棒性/外推分析，不作为调参目标。
4. 不要写成 risk reward 主导。当前证据支持 action guard / shield 是主机制。


## 2026-07-01 gated-risk addendum
- Added `gated_risk_mechanism_addendum.csv` and `gated_risk_mechanism_addendum.md`.
- Claim boundary: use gated-risk as mechanism evidence that conditional risk shaping avoids risk-only stagnation; do not replace the guard/shield-centered main result.


## 2026-07-01 gated-risk stress addendum
- Added `gated_risk_stress_mean.csv`, `gated_risk_stress_rank_with_existing.csv`, and `gated_risk_stress_addendum.md`.
- Stress boundary: proposed_gated_risk is competitive under 0.20/0.25 but does not overturn the guard/shield-centered main claim.


## 2026-07-01 behavior rollout addendum
- Added `behavior_rollout_addendum.md`, pointing to `codex_longrun_iscsic/behavior_rollouts_20260701_0406`.
- These trajectory plots are qualitative mechanism evidence only; aggregate formal/stress tables remain the quantitative source of truth.


## 2026-07-01 final paper manifest
- Added `final_manifest_addendum.md`, pointing to `../final_paper_manifest_20260701_0415`.
- Curated paper-facing PDFs are under `../final_paper_manifest_20260701_0415/pdf_figures/`; historical run PDFs remain under their source `outputs/*/figures/` directories.
