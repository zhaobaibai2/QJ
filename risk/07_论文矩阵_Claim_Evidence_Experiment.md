# 07 论文矩阵：Claim - Evidence - Experiment

用途：这份矩阵把论文每一段要说的话、当前证据、缺口实验和最终写法绑定起来。后面写英文稿时，不要脱离这张表扩 claim。

## 总控主张

| 项目 | 内容 |
|---|---|
| 推荐题目 | Risk-Aware Curriculum PPO with Defensive TTC Shield for Safe MetaDrive Decision Control |
| 论文类型 | Technique paper / applied intelligent control paper |
| 核心问题 | 标准 PPO 在 MetaDrive 未见地图和高密度交通下缺少提前安全反馈、难度递进机制和运行时防御层。 |
| 核心方法 | Risk-aware dense reward + outcome-gated curriculum + defensive TTC/overspeed shield。 |
| 最终主张边界 | 改善 MetaDrive 仿真中的安全性和密度鲁棒性；不声称真实车部署、不声称形式化安全保证、不声称 SOTA。 |

## 论文写作执行矩阵

| Row | Manuscript unit | 该段功能 | 可写 claim | 当前证据 anchor | 缺口 | 最终写法检查 |
|---|---|---|---|---|---|---|
| M0 | Whole paper frame | 定义整篇主线 | 本文研究的是安全关键自动驾驶仿真决策控制，不是单纯 reward 最大化。 | MetaDrive 项目、已有多密度评估、collision/cost 指标。 | 英文稿需统一用 `safe decision control in simulation`。 | 不写 real-world deployment。 |
| M1 | Abstract sentence 1 | 说明问题 | RL driving policies need to balance task completion and safety under unseen maps and traffic density shifts. | proposed 14 seeds 在 0.08/0.15 下有明显 density degradation。 | 无。 | 必须出现 density shift 和 safety events。 |
| M2 | Abstract method | 简述方法 | We propose RAC-PPO with risk reward, outcome-gated curriculum, and defensive TTC shield. | `racrl/envs.py`、`callbacks.py`、defensive runs。 | shield intervention rate 尚未记录。 | 若 intervention rate 未补，只写 shield rule，不写 quantified takeover。 |
| M3 | Abstract results | 给核心数字 | RAC-PPO reaches 0.747±0.039 success at density 0.08; high-density remains challenging; defensive variant shows potential. | proposed 14 seeds；defensive ttc12/v18 seed25。 | Defensive 需要 3 seeds 才能进 abstract。 | 只放已完成多 seed 数字。 |
| M4 | Introduction para 1 | 背景和重要性 | Autonomous decision control must handle stochastic roads and surrounding vehicles. | MetaDrive 文献、safe RL 文献。 | 需补引用。 | 背景不能泛泛写“AI revolution”。 |
| M5 | Introduction para 2 | prior limitation | Sparse terminal penalties are late safety signals; fixed training difficulty misses density robustness. | baseline/curriculum 单独结果差；risk reward 提升明显。 | 需要多 seed baseline/risk/curriculum。 | 写“in our setting”而不是领域普遍结论。 |
| M6 | Introduction para 3 | key idea | Combine risk shaping, outcome-gated curriculum, and TTC shield without changing PPO backbone. | 代码实现存在。 | 拆分 reward-only 与 guard-only 更好。 | 明确是 lightweight framework。 |
| M7 | Contributions | 三点贡献 | 1 risk reward, 2 curriculum, 3 defensive safety analysis and evaluation protocol. | 已有部分证据。 | 消融缺失。 | 贡献不能超过 3 条。 |
| M8 | Related work: RL driving | 铺垫平台和算法 | MetaDrive supports diverse generated driving scenarios; PPO/SAC are standard baselines. | `references.bib` 已有 MetaDrive/PPO/SAC。 | SB3 引用缺失。 | SAC 未跑就不写实验对比。 |
| M9 | Related work: safe RL | 支撑安全动机 | Safe RL studies risk constraints and shielding; our shield is heuristic runtime safety, not formal verification. | Safe RL survey、CPO、shielding 文献。 | 文献需补入 bib。 | 不写 formal guarantee。 |
| M10 | Method: problem | 定义 MDP 和指标 | State/action/reward in MetaDrive; metrics include success, route, collision, out-of-road, cost. | evaluate CSV 字段完整。 | 无。 | 指标定义要和 CSV 列一致。 |
| M11 | Method: risk reward | 方法核心 | TTC、lane deviation、smoothness、event cost、progress 构成 dense signal。 | `envs.py` 中 `_ttc_risk`, `_lane_deviation`, reward equation。 | reward-only 消融缺。 | 写公式并列权重来自 run config。 |
| M12 | Method: curriculum | 方法模块 | Difficulty progresses based on recent success/route/cost. | `callbacks.py` 和 run config。 | 课程贡献需要多 seed 验证。 | 不说课程一定提升所有密度。 |
| M13 | Method: shield | 方法模块 | TTC/overspeed guard suppresses unsafe acceleration and triggers braking. | `envs.py` action guard；defensive scripts。 | intervention rate 未记录；reward/guard 耦合。 | 写 heuristic shield，承认无形式化 guarantee。 |
| M14 | Experiments setup | 复现协议 | 200 train scenarios, 100 unseen test scenarios, density 0/0.08/0.15, 50 episodes per seed. | run config 和 CSV。 | `n_envs` 未写入 config。 | 论文表注写清硬件和 n_envs。 |
| M15 | Main comparison | 验证 RQ1/RQ2 | Risk reward is the main source of improvement; curriculum may help high-density robustness. | seed0 四方法对比。 | baseline/risk/curriculum seed1/2 缺失。 | 未补前只能写 preliminary。 |
| M16 | Multi-seed stability | 支撑完整方法稳定性 | RAC-PPO has stable density 0.08 performance across 14 seeds. | proposed 14 seeds。 | 对比方法不等量。 | 可作为 RAC-PPO stability analysis，不可替代 main comparison。 |
| M17 | Defensive analysis | 支撑安全层 | ttc12/v18 appears to improve high-density safety; ttc8 has higher success but more collision. | shield screen、defensive seed25。 | ttc12/v18 需 3 seeds；intervention rate 缺。 | 写 Pareto tradeoff，不写最优定论。 |
| M18 | Ablation | 支撑创新点 | TTC, lane, smoothness, guard each contribute differently. | 目前没有正式结果。 | 必须补。 | 未补则删掉 ablation claim。 |
| M19 | Discussion | 解释不足 | High density remains failure-prone; learned policy still needs stronger safety handling. | density 0.15 success 0.467/collision 0.414。 | 无。 | 这段要诚实写，会增加可信度。 |
| M20 | Limitations | 限定范围 | Simulation only, heuristic shield, no formal safety, no real-world validation. | 当前工作事实。 | 无。 | 必须单独写。 |

## Claim 强度分级

| Claim | 当前可写强度 | 何时升级 |
|---|---|---|
| RAC-PPO improves over PPO baseline | 暂时：seed0 preliminary | baseline/risk/curriculum/proposed 都有 3 seeds 后升级为 main claim。 |
| Risk reward is important | 中等强 | `proposed_wo_ttc`、reward-only/no-guard 补齐后升级。 |
| Curriculum improves robustness | 弱到中等 | risk vs proposed 三种子 high-density 结果明确后升级。 |
| Defensive TTC shield improves safety | 探索性 | ttc12/v18 至少 3 seeds + intervention rate 后升级。 |
| Method is suitable for real cars | 不能写 | 除非真实车或高保真闭环验证，不建议升级。 |

## 最小可投稿矩阵

如果时间有限，最终英文稿至少要满足：

| 必要元素 | 最低证据 |
|---|---|
| Main table | 4 方法 × 3 seeds × 3 density。 |
| Stability table | proposed 14 seeds，可作为附加。 |
| Ablation | 至少 `wo_ttc` 和 `no_action_guard`。 |
| Defensive table | fixed ttc12/v18 × 3 seeds，或降级为 discussion/preliminary。 |
| Figure | success/collision vs density、training curves、curriculum stage、shield Pareto。 |

