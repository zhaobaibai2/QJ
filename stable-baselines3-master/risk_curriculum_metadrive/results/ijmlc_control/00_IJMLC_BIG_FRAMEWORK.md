# IJMLC 大框架与工作路线

更新时间：2026-07-01T16:30:08

## 1. 目标期刊定位

目标不是继续按 7 页 IEEE 短文讲一个规则 shield，而是改写成机器学习与控制论交叉的期刊论文：

题目建议：GuardShield-Runtime: Cybernetic Runtime Action Intervention for Progress-Preserving Safe Reinforcement Learning in Dense Traffic

期刊叙事关键词：
- system-environment interaction
- cybernetic closed-loop feedback
- progress-safety ambiguity
- runtime action intervention
- safe reinforcement learning
- dense traffic autonomous driving

## 2. 不能越界的 claim

禁止写：
- proven safety
- formal guarantee
- certified safe
- deployment-ready
- real-world validation/proof
- solved dense-traffic generalization
- statistically significant superiority，除非置信区间和检验支持

允许写：
- simulator-bounded evidence
- mechanism-level finding
- action-level runtime feedback is a key stabilizing mechanism under tested MetaDrive protocols
- reward-only safety can create non-motion artifacts in this setup
- high-density stress remains a limitation

## 3. 论文结构

1 Introduction：dense traffic 是闭环 system-environment interaction，提出 progress-safety ambiguity。
2 Related Work：safe RL、runtime shielding/filtering、CBF/RSS/MPC-style safety filters、autonomous driving RL、closed-loop evaluation、reward hacking/non-motion artifact。
3 Problem Formulation：定义 raw action、guarded action、executed action、progress、cost、intervention loci。
4 GuardShield-Runtime：learning-side risk shaping、action-side soft guard、execution-side hard shield、logging diagnostics。
5 Experimental Design：环境、baseline、seed protocol、metrics、统计方法、实现细节。
6 Results：按问题组织，而不是堆表。
7 Discussion：机制发现、guard vs shield、为什么 reward-only 不够、为什么不是 formal safety。
8 Limitations and Future Work：仿真边界、高密度失败、阈值人工设置、无真实车证明。
9 Conclusion：短结论，保守 claim。

## 4. 后续工作分阶段

Phase A 证据盘点与控制面固定：完成已有结果复用边界、实验矩阵、运行队列、状态脚本。

Phase B IJMLC 诊断补评估：不重训，先用冻结模型重评估 non-motion artifact、stop ratio、low-progress、TTC 分布、latency 和 intervention per km。

Phase C 外部 baseline 补齐：先做轻量可实现 baseline，包括 PPO vanilla、risk-only、PPO-Lagrangian 或 RCPO 简化版、RSS/TTC classical filter、hard-shield-only、soft-action-filter/guard。

Phase D seed 扩展：核心方法从 3 个 training seeds 扩展到至少 5 个，优先 d=0.15 和核心对比。

Phase E 密度和扰动泛化：d=0.00/0.08/0.15/0.20/0.25；后续再加 action delay、lidar noise、target speed 等扰动。

Phase F sensitivity：tau_soft、tau_hard、soft brake、hard brake、target speed。先做冻结模型 eval sensitivity，必要时再训练。

Phase G runtime overhead：policy inference、guard TTC computation、shield decision、total action latency、p50/p95/p99。

Phase H 图表和 Springer 稿件：生成 Springer 单栏/双栏适配图表、author-year 引用、Data/Code Availability、Funding、Competing Interests、Author Contributions。
