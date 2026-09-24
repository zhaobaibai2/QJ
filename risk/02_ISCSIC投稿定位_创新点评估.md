# 02 ISCSIC 2026 投稿定位与创新点评估

## 会议信息核对

根据 ISCSIC 官网：

- 会议名：2026 8th International Symposium on Computer Science and Intelligent Control。
- 时间地点：2026-09-11 至 2026-09-13，Chongqing, China。
- 官网主页写明：Submission Deadline 为 2026-07-15，Abstract Deadline 为 2026-07-01。
- Submission 页面说明：Full Paper 至少 5 页，Article 必须是英文，未出版并符合 IEEE 模板；摘要只参加 oral/poster，不进入 proceedings。
- Publication 页面说明：注册并展示的完整论文会进入 conference proceedings，并提交 IEEE Xplore，最终以 scope 和 quality review 为准。

注意：官网不同页面存在日期不一致。主页显示 Full Paper 2026-07-15，但 Submission 页面中 Full Paper Deadline 显示 2026-06-15。当前日期是 2026-06-29，因此必须以投稿系统或会务邮件为准。如果 July 15 生效，仍有约 16 天；如果 June 15 生效，常规 full paper 已过期，只能问 special/session 或 late submission。

可匹配 special/session：

- Safe and Resilient Distributed Control for Autonomous Multi-Agent Systems: special session deadline 2026-07-15。
- Frontiers of AI-Driven Control and Decision-Making for Autonomous Systems: special session deadline 2026-07-15。
- Advanced Intelligent Control for Multi-Agent Systems: special session deadline 2026-07-31。
- Intelligent Decision-Making and Control for Multi-Agent Systems: special session deadline 2026-07-31。

项目主题和这些方向匹配度较高，尤其是 autonomous systems、decision-making、safe control、intelligent control。

## 论文类型定位

不建议定位为 benchmark paper。当前工作没有新的 benchmark construction pipeline，也没有系统化 taxonomy/data card/benchmark maintenance plan。

建议定位为技术论文：

> Technique Paper: 在 MetaDrive 自动驾驶仿真中，用风险奖励、课程学习和防御式 TTC 安全层改进 PPO 决策控制。

更准确的副定位：

> Applied Safe RL / Intelligent Control paper for autonomous driving simulation.

## FINER 评估

| Criterion | Score | 依据 |
|---|---:|---|
| Feasible | 4/5 | 代码和结果已经存在，MetaDrive/SB3 工程可运行；缺口主要是补实验和汇总，不是从零实现。 |
| Interesting | 4/5 | 自动驾驶 RL 的安全探索、未见地图泛化和高密度交通鲁棒性是清晰问题。 |
| Novel | 3/5 | 风险奖励、课程学习、TTC shield 单独都不是新概念；创新要靠组合、协议和实证洞察，而不是声称理论新方法。 |
| Ethical | 4/5 | 仿真实验，无真人/真实车辆风险；但必须避免暗示真实部署安全。 |
| Relevant | 4/5 | ISCSIC 的 intelligent control/autonomous systems 范围契合。 |
| Average | 3.8/5 | 可投，但要收窄主张。 |

结论：题目可行，但不应包装成“突破性安全强化学习”。更适合作为工程严谨、证据清楚的 ISCSIC 技术论文。

## Fatal flaws audit

| # | Flaw | Severity | 证据 | Defense |
|---|---|---|---|---|
| 1 | Baseline is not the real baseline | MAJOR | 当前主对比只有 PPO seed0，SAC 未正式结果，CPO/shield-only/安全 RL baseline 缺失。 | 至少补三种子 PPO baseline/risk/curriculum/proposed；若时间不足，删除 SAC 主张并加入 shield-only 或 PPO+rule shield 对照。 |
| 2 | Unverifiable claim | MAJOR | 若写“课程显著提升”，当前 seed0 下 proposed 在 density 0.08 并不优于 risk；课程贡献还没有多种子统计。 | 把主 claim 改成“风险奖励是主要提升源，课程在高密度压力下提供额外稳定性”，并补消融。 |
| 3 | Scope creep | MINOR to MAJOR | 草稿同时写 reward、curriculum、SAC、消融、trajectory、defensive shield，但不是全都完成。 | 最终论文只保留已经完成或一周内能补完的贡献，其他放入 future work。 |

没有发现必须放弃的 CRITICAL flaw。当前版本是 `Accept with Revisions`。

## 五维创新评分

| Dimension | Score | 依据 | 论文中应强调 |
|---|---:|---|---|
| Higher | 7 | proposed 在 seed0 对比中显著优于 baseline/curriculum；14 seeds 中 density 0.08 成功率约 0.747。 | 强调中等密度未见地图成功率和 route completion。 |
| Faster | 3 | 不是效率论文；并行环境只是训练工程。 | 不要把训练加速写成贡献。 |
| Stronger | 8 | 0.15 高密度压力测试、防御式 TTC 层降低碰撞的证据是最有价值的点。 | 主打 robustness/safety under density shift。 |
| Cheaper | 5 | 不需要人工标注和新数据，但训练仿真成本仍高。 | 可作为工程优势，不作为核心贡献。 |
| Broader | 5 | 方法可迁移到其他仿真器是推断，尚无跨模拟器实验。 | 只能写“potentially extensible”，不能写 verified transfer。 |

主论文轴：`Stronger + Higher`。不要主打 Faster 或 Broader。

## 推荐题目

英文题目候选：

1. `Risk-Aware Curriculum PPO with Defensive TTC Shield for Safe MetaDrive Decision Control`
2. `Improving Safety and Density Robustness of PPO Driving Policies via Risk-Aware Curriculum Learning`
3. `A Lightweight Risk-Curriculum Reinforcement Learning Framework for MetaDrive Autonomous Driving Control`

中文题目候选：

1. `面向 MetaDrive 自动驾驶决策控制的风险感知课程 PPO 与防御式 TTC 安全层`
2. `基于风险感知课程学习的自动驾驶仿真决策控制方法`

首选第 1 个，因为它把真正可区分的创新点都放进了标题：risk-aware、curriculum、TTC shield、decision control。

## 可写贡献

建议贡献控制在 3 条：

1. 提出一个轻量级风险感知 PPO 训练框架，将 TTC 预碰撞风险、车道偏离、控制平滑、事件 cost 和 route progress 统一为密集学习信号。
2. 设计 outcome-gated curriculum，根据 route completion、success 和 safety cost 自适应提升 MetaDrive 场景难度，面向未见地图泛化。
3. 引入 defensive TTC/overspeed shield，并用多密度、多 seed、模块消融和高密度压力测试分析安全-效率权衡。

不建议写的贡献：

- “首次提出 TTC 风险奖励”。TTC 和 reward shaping 都不是首次。
- “显著优于所有安全强化学习方法”。没有对比。
- “可直接用于真实车辆”。没有 sim-to-real。

## ISCSIC 适配判断

| 维度 | 判断 |
|---|---|
| 主题契合 | 高。自动驾驶、智能控制、决策控制、安全鲁棒性都契合。 |
| 结果强度 | 中。能支撑会议论文，但不是顶会级。 |
| 时间风险 | 高。若 July 15 截稿，必须快速补齐实验和英文稿。 |
| 最大审稿风险 | baseline/ablation 不足、claim 过大、代码参数和论文不一致。 |
| 推荐动作 | 走 special session 或 main full paper；用稳健工程论文写法，不做夸张 SOTA 叙事。 |
