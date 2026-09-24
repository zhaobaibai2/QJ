# IJMLC 补实验矩阵与目的

更新时间：2026-07-01T16:30:08

## 第一优先级：non-motion artifact 诊断

目的：证明 reward-only 或 risk-only 的低 cost 可能来自不动，而不是安全驾驶。

对比方法：
- PPO vanilla / baseline：无安全干预，下界。
- risk-only：reward-level safety，重点看 stop ratio 和 route completion。
- guard_only：action-side soft guard，验证动作层干预。
- shield_only：execution-side hard shield，验证最终执行层干预。
- proposed_gated_risk：progress-gated risk shaping 作为 refinement。
- no_action_guard：负控制，验证去掉 guard 后 failure mode 改变。

必须指标：success、cost、route completion、collision、out_of_road、mean speed、median speed、stop ratio、low-progress rate、progress per cost、min/mean TTC、TTC dangerous fraction、intervention count/rate/per km。

论文用途：Fig. 2 Non-motion artifact；Fig. 3 progress-safety frontier；Table 3 primary d=0.15；Results 6.1 和 6.2。

## 第二优先级：外部 baseline

目的：降低审稿人质疑“只是内部消融，没有外部对比”的风险。

需要补：
- PPO vanilla：已有，可复用并补诊断指标。
- PPO + risk penalty / risk-only：已有，可复用并补诊断指标。
- PPO-Lagrangian 或 RCPO 简化版：如果代码中没有，先实现最稳定的 cost multiplier 版本，并清楚标注 simple PPO-Lagrangian baseline。
- RSS/TTC classical filter：不训练或少训练，基于 TTC/RSS-style safety filter 对 PPO policy 做执行时过滤。
- hard shield only：已有 shield_only，可复用并补诊断指标。
- action filter / guard only：已有 guard_only，可复用并补诊断指标。

论文用途：Table 4 External baseline comparison；审稿回复“not only internal ablation”。

## 第三优先级：seed 扩展

目的：把当前三 seed 结果扩展到期刊更稳的统计证据。

最低目标：核心方法至少 5 training seeds。
核心方法：baseline、risk-only、guard_only、shield_only、proposed_gated_risk、no_action_guard。若算力紧，先 d=0.15，后扩 d=0.08/0.20/0.25。

论文用途：Wilson 95 CI、bootstrap CI、per-seed scatter。

## 第四优先级：密度与压力泛化

目的：证明不是只在 d=0.15 调参。

密度：0.00、0.08、0.15、0.20、0.25。
核心评估：success/cost/route/collision/out-road/stop ratio/intervention/TTC。

论文用途：Fig. 5 Density and stress generalization；Table 6 density sweep。

## 第五优先级：threshold sensitivity

目的：回应“阈值是不是手调出来的”。

变量：
- tau_soft: 8, 10, 12, 14
- tau_hard: 5, 7.2, 9
- soft braking cap: -0.4, -0.6, -0.8
- hard braking cap: -0.8, -1.0
- target speed: 15, 18, 22 km/h

先做冻结模型 sensitivity，不把 sensitivity 当主结果，也不反向选择最优数值替换正式协议。

论文用途：appendix 或 Fig. 7。

## 第六优先级：runtime overhead

目的：既然方法叫 runtime，必须说明开销。

指标：policy inference ms、guard TTC computation ms、shield decision ms、total action latency ms、p50/p95/p99、control-loop step ms。

论文用途：Table 7 Runtime overhead；Discussion 中说明只证明仿真闭环实时性，不证明实车实时部署。
