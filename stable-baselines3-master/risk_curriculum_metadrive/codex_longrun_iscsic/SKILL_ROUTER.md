# SKILL_ROUTER

更新时间：2026-06-29 22:12:15 CST

本阶段按用户要求只使用远程端 `/home/aaa/data/codex` 中的 skill/README 作为路由依据。已扫描 `SKILL.md`/`README.md`。

| skill/source | 入口文件 | 适用阶段 | 本轮使用记录 |
|---|---|---|---|
| academic-research-skills-codex | /home/aaa/data/codex/academic-research-skills-codex/README.md | 研究问题收敛、证据分级、实验规划、反 cherry-picking、复现检查 | 已读取 README；用于本轮审计结构、ledger 分类和 claim 边界。 |
| PaperSpine-main | /home/aaa/data/codex/PaperSpine-main/README.md | 英文 IEEE 初稿、motivation 主线、claim-evidence 段落重写、LaTeX/PDF 组装 | 已读取 README；暂未写英文稿，等 P0 实验补齐后调用。 |
| Supervisor-Skills-main | /home/aaa/data/codex/Supervisor-Skills-main/README.md | 审稿风险、技术论文结构、实验缺口和 benchmark 写法检查 | 已读取 README；用于本轮 missing experiment 与风险清单整理。 |
| scientific-brainstorming-main | /home/aaa/data/codex/scientific-brainstorming-main/SKILL.md | 实验失败后的发散归因、小步调参、下一轮参数搜索 | 已读取 SKILL；暂未启动新调参，待训练/评估结果失败时调用。 |
| CCF-Figure-main / scientific-figure-generator | /home/aaa/data/codex/CCF-Figure-main/SKILL.md | 方法图、结果图、Pareto 图和论文图审美检查 | 已读取 SKILL；当前先生成程序化结果图，论文级图后续再用。 |
| nature-skills-main | /home/aaa/data/codex/nature-skills-main/README.md | 英文摘要、introduction、related work、limitation 润色 | 已读取 README；暂未润色英文稿，等真实结果固定后调用。 |

## 2026-06-30 scientific-brainstorming 使用记录

- 入口：/home/aaa/data/codex/scientific-brainstorming-main/SKILL.md
- 用途：hard stage 失败后的失败归因和小步调参设计。
- 决策：避免继续堆步数或大改 reward；采用可验证的小改动：增加 prehard density=0.12 过渡阶段，放宽 demotion 条件，让 hard stage 失败能回退恢复。

## 2026-06-30 use: scientific-brainstorming-main
- Entry: /home/aaa/data/codex/scientific-brainstorming-main/SKILL.md
- Used for: failure-driven tuning after low-LR and route-gate diagnostics.
- Decision produced: test a targeted hard-stage stabilization hypothesis by tightening stage2 promotion gates, rather than blindly increasing timesteps.

## 2026-06-30 scientific-brainstorming-main used for failed long-step diagnostic
- Skill file read: /home/aaa/data/codex/scientific-brainstorming-main/SKILL.md.
- Use case: after 1.5M longer training worsened held-out metrics, identify next single-mechanism tuning direction rather than blindly increasing timesteps.
- Decision from evidence: treat high-density collision/cost as safety-threshold problem; next screen changes only TTC threshold 12 -> 14 while keeping target speed and curriculum fixed.

## 2026-06-30 scientific-brainstorming-main for reward diagnosis
- Skill: /home/aaa/data/codex/scientific-brainstorming-main/SKILL.md
- Used for: user-raised hypothesis that reward function may be causing proposed hard-stage low success.
- Decision: treat reward as a testable mechanism, not a guess. Current main protocol should finish unchanged; next diagnostics should compare reward/guard ablations and small reward-weight screens focused on progress/success vs safety/overspeed balance.

## 2026-06-30 skill use update
- Skill used: scientific-brainstorming-main (/home/aaa/data/codex/scientific-brainstorming-main/SKILL.md)
- Task: post-screen failure analysis after R1/R2/R3/no_action_guard/proposed_wo_ttc results.
- Decision produced: avoid extreme completion or penalty changes; keep action guard and TTC reward; launch a gentler R5 moderate_completion screen.

## 2026-06-30 skill use update
- Skill used: scientific-brainstorming-main (/home/aaa/data/codex/scientific-brainstorming-main/SKILL.md)
- Task: post-screen failure analysis after R1/R2/R3/no_action_guard/proposed_wo_ttc results.
- Decision produced: avoid extreme completion or penalty changes; keep action guard and TTC reward; launch a gentler R5 moderate_completion screen.
