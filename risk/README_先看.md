# ISCSIC 2026 风险课程 MetaDrive 选题评估包

生成时间：2026-06-29  
远端项目：`/home/aaa/data/qj/stable-baselines3-master/risk_curriculum_metadrive`  
输出目录：`/home/aaa/data/qj/risk`

## 本次调用的技能和资料

- `academic-research-skills-codex`: 用于研究问题收敛、文献检索纪律、证据分级、实验规划和反 cherry-picking 检查。
- `PaperSpine-main`: 用于约束论文主线，核心原则是用户结果为准，不编造数据，不把窄证据膨胀成多重贡献。
- `scientific-brainstorming-main`: 用 SCAMPER、TRIZ、反向假设和形态分析做发散，再做收敛。
- `Supervisor-Skills-main`: 使用 `idea-evaluator`、`tech-paper-template`、`benchmark-paper-template` 的评估框架做创新点、逻辑链和实验缺口审稿。

## 一句话结论

这个题目可以投 ISCSIC 2026，但现在应定位为“面向自动驾驶仿真决策控制的风险感知课程强化学习与防御式 TTC 安全层”工程型技术论文，而不是 SOTA 安全强化学习或真实车辆部署论文。当前状态是 `Accept with Revisions`：想法有可投性，已有结果可支撑中等会议论文，但必须补齐同协议多种子对比、消融、统计表和复现实验记录。

## 当前最强论文主线

推荐主线：

> Risk-aware Curriculum PPO with Defensive TTC Shield for Safe MetaDrive Decision Control

中文表述：

> 面向 MetaDrive 自动驾驶决策控制的风险感知课程 PPO 与防御式 TTC 安全层

主张边界：

- 可以主张：在 MetaDrive 未见地图和中高交通密度下，风险奖励、课程学习和 TTC/速度守护能提高路线完成、安全性和高密度鲁棒性。
- 暂时不能主张：达到真实自动驾驶安全、优于全部 safe RL 方法、SOTA、跨模拟器泛化、真实车辆可部署。

## 最关键证据

已扫描到的完整方法 `proposed` 可用 14 个 seed，每 seed 每密度 50 episodes：

| 测试密度 | 成功率 mean±sd | 路线完成 | 碰撞率 | 越界率 | cost |
|---:|---:|---:|---:|---:|---:|
| 0.00 | 0.840±0.000 | 0.974 | 0.000 | 0.000 | 0.000 |
| 0.08 | 0.747±0.039 | 0.929 | 0.084 | 0.004 | 0.089 |
| 0.15 | 0.467±0.069 | 0.773 | 0.414 | 0.033 | 0.447 |

防御版结果显示更强潜力，但当前证据还不够稳：

- ttc12/v18 重新训练只有 seed25 的完整评估：density 0.15 成功率 0.66，碰撞率 0.18，cost 0.20。
- 旧模型防御层筛查中 ttc12/v18 在 density 0.15 为成功率 0.60，碰撞率 0.10，cost 0.10，但只有 20 episodes，不能直接作为主表。
- ttc8/ttc10/ttc12 混合统计显示防御版总体比原始 proposed 更安全，但不同设置混在一起只能作为探索证据，不能作为最终方法均值。

## 必须优先修的硬缺口

1. 主对比目前只有 seed0，且 `paper_comparison_seed0/runs/proposed_ppo_s0/config.json` 缺失，不能支撑“完整主实验”。
2. 消融目录没有完成结果：`proposed_wo_ttc`、`proposed_wo_lane`、`proposed_wo_smooth` 需要至少 3 seeds。
3. `final_paper_results` 是旧汇总，只包含 proposed 的 seed0/1/3/4，没有纳入 seed5-13，也没有纳入最新防御版。
4. SAC 在代码里有接口，但没有看到可用正式评估表。若论文提 SAC 对比，要补跑；否则从论文中删除。
5. 当前 `config.py` 和实际运行 config 不完全一致，必须以各 run 的 `config.json` 为准，并在论文中写清协议。

## 文件说明

- `01_证据盘点.md`: 代码、结果、已有论文草稿和可复现性问题清点。
- `02_ISCSIC投稿定位_创新点评估.md`: 会议信息、题目可行性、FINER、fatal flaws、五维创新评分。
- `03_头脑风暴_论文主线.md`: 发散方向、推荐主线、论文逻辑骨架。
- `04_实验缺口_对比_消融_改进计划.md`: 投稿前必须补的实验、命令建议、代码改进点。
- `05_论文支撑文献与引用策略.md`: 当前 bib 缺口、建议引用、claim-to-reference 对照。
- `06_审稿风险清单.md`: 模拟审稿人会攻击的问题和对应防御策略。
- `07_论文矩阵_Claim_Evidence_Experiment.md`: 逐段论文矩阵，说明每个 claim 对应什么证据、缺什么实验、怎么写。
- `08_创新点支撑矩阵.md`: 每个创新点的现有支撑、文献支撑、审稿攻击和补强动作。
- `09_4070S_nenv4实验路线图.md`: 按 RTX 4070 SUPER、12 核 CPU、`n_envs=4` 重排的实验优先级、命令和排期。
- `10_优化路线_结果没到最好时怎么迭代.md`: 如何从当前结果继续优化，但避免后验挑选和过拟合。

## 外部来源

- ISCSIC 2026 官网主页和 Call for Papers：<https://www.iscsic.org/>
- ISCSIC 2026 Special Sessions：<https://www.iscsic.org/special>
- ISCSIC 2026 Submission：<https://www.iscsic.org/submission>
- ISCSIC 2026 Publication：<https://www.iscsic.org/publication>
- MetaDrive 论文页：<https://metadriverse.github.io/metadrive/>
- Stable-Baselines3 JMLR 论文：<https://jmlr.org/papers/v22/20-1364.html>
- PPO arXiv：<https://arxiv.org/abs/1707.06347>
- SAC PMLR：<https://proceedings.mlr.press/v80/haarnoja18b.html>
- Curriculum Learning：<https://dl.acm.org/doi/10.1145/1553374.1553380>
- Safe RL survey：<https://jmlr.org/papers/v16/garcia15a.html>
- CPO PMLR：<https://proceedings.mlr.press/v70/achiam17a.html>
- Shielding AAAI：<https://ojs.aaai.org/index.php/AAAI/article/view/11797>
