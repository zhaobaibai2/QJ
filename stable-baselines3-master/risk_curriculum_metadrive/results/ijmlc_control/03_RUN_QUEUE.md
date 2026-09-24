# 运行队列

更新时间：2026-07-01T16:30:08

本队列先保证“为什么跑”清楚，再跑。当前先不盲目铺满所有训练，因为旧 n_envs=16 已有很多冻结模型，IJMLC 首先缺的是诊断指标和举证链。

## 立即执行顺序

1. P1 frozen-model IJMLC diagnostic evaluation。
   方法：baseline、risk-only、guard_only、shield_only、proposed_gated_risk、no_action_guard。
   密度：先 d=0.15；如果脚本稳定，扩 d=0.08、0.20、0.25。
   目标：stop ratio、median speed、low-progress、TTC dangerous fraction、intervention per km、latency。

2. P1 runtime overhead。
   使用同一诊断评估记录 policy inference、guard/shield decision、total action latency。
   目标：Table 7。

3. P2 外部 baseline 实现前审计。
   检查远程 sb3 环境是否有 sb3-contrib；如果有，优先 PPO-Lagrangian/RCPO；如果没有，实现 simple PPO-Lagrangian 并明确命名。
   同时实现 RSS/TTC classical filter baseline。

4. P3 seed extension。
   只有当 P1/P2 证明当前三 seed 统计不足时，启动 seed3/seed4；否则先把期刊表格和 CI 补完整。

5. P4/P5 robustness and sensitivity。
   在不改正式协议的前提下做 reviewer-facing checks，不作为调参重新选最优。

## 当前队列 CSV

详见 03_RUN_QUEUE.csv。
