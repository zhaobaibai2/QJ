# 举证体系与文件规范

更新时间：2026-07-01T16:30:08

## 1. 目录结构

远程控制面：results/ijmlc_control

固定子目录：
- raw_csv：每个实验/评估的 episode-level 和必要 step-level 原始 CSV。
- summary_tables：按 label、density、seed 聚合的 CSV 和 LaTeX 表。
- figures：论文图 PDF/PNG/SVG。
- logs：训练、评估、监督、错误日志。
- configs：每个 run 的 config.json 快照和命令快照。
- manuscript：后续 Springer LaTeX、results section、claim text。
- run_manifests：每个实验的 manifest，记录模型、命令、状态、用途。

## 2. 每个实验必须有的证据

每个 train/eval 单元必须记录：
1. run_id
2. label/method
3. variant/algo/seed/density
4. config_json 路径
5. model 路径
6. eval command 或 train command
7. raw episode CSV
8. summary CSV
9. log 路径
10. status：running / done / failed / diagnostic_only / accepted_main / accepted_appendix / rerun_required
11. claim_supported：这个结果支持哪一个论文 claim
12. boundary_note：不能用这个结果证明什么

## 3. 证据等级

accepted_main：可以进正文主表或主图。
accepted_appendix：可进附录或补充材料。
diagnostic_only：只用于调参/失败归因，不作为论文主结论。
rerun_required：协议、日志或指标不完整，需要重跑。
blocked：远程连接、环境或代码阻塞。

## 4. 现有结果复用原则

可以复用：已有 n_envs=16 frozen model 的正式三 seed 结果、外部 seed robustness、stress density 结果。

必须补评估：stop ratio、median speed、low-progress、TTC dangerous fraction、latency、intervention per km。因为旧 CSV 不完整记录这些 IJMLC 新指标。

不能直接复用为主证据：旧的 tuning、failed、interrupted、diagnostic_failed、n_envs 协议不一致结果。它们只能作为调参日志或失败分析。

## 5. Claim 到证据映射

Claim 1：reward-only safety can create non-motion artifact。
需要证据：risk-only 的 low route completion、low mean/median speed、高 stop ratio；同时 cost 低或 collision 低。

Claim 2：action-level runtime intervention changes the failure mode。
需要证据：guard/shield/gated-risk 与 no_action_guard 的 success/cost/route/TTC/intervention 对比。

Claim 3：GuardShield improves progress-safety balance under tested MetaDrive densities。
需要证据：density sweep、external seed robustness、progress-safety frontier。

Claim 4：runtime overhead is small in simulation closed-loop evaluation。
需要证据：policy/guard/shield/total latency p50/p95/p99。

Claim 5：method has boundaries under higher density and threshold changes。
需要证据：d=0.20/0.25 stress、threshold sensitivity、failure cases。
