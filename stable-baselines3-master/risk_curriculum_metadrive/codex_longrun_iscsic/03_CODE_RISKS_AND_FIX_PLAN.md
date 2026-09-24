# 03_CODE_RISKS_AND_FIX_PLAN

更新时间：2026-06-29 22:12:15 CST

## 已修复

- `racrl/config.py`: 删除重复 `success_bonus`，加入正式字段 `n_envs: int = 1`。
- `racrl/config.py`: 加入 `use_risk_reward` 与 `use_action_guard`，保留 `risk_reward` 作为兼容上层开关。
- `racrl/envs.py`: action guard 从 `risk_reward` 拆出，由 `use_action_guard` 控制；reward shaping 由 `use_risk_reward` 控制。
- `racrl/envs.py` 和 `racrl/experiment.py`: 新增 `shield_intervention`, `shield_soft`, `shield_hard`, `overspeed_guard` 及对应 rate。
- `scripts/run_one_defensive_proposed.py`: 硬编码 Python 路径替换为 `sys.executable`。
- 新增 `scripts/evaluate_from_config.py`: 从 run 的 `config.json` 恢复配置再评估。
- `scripts/build_final_outputs.py`: 改为 glob 扫描，输出 final ISCSIC 的 episode/seed/method 汇总、表格和图。

## 仍需注意

- 老 CSV 没有 shield rate，只有后续用新代码评估/训练的 defensive 结果才有完整 intervention rate。
- `risk_reward=True` 的旧 run 在兼容读取时会被解释为 reward+guard 同时启用，这是为了忠实复现旧模型；后续消融必须依赖新字段区分。
- 聚合脚本会把协议分为 `final_benchmark`, `screening`, `preliminary`, `inconsistent_protocol`，论文写作必须按该标签控制 claim。

## 验证

- 远程 `python -m py_compile` 已通过核心文件与脚本。
- `scripts/evaluate_from_config.py --help` 与 `scripts/train.py --help` 已通过。
- `scripts/build_final_outputs.py` 已成功生成 `outputs/final_iscsic_results` 全部要求文件。

## 2026-06-29 协议变更：n_envs=10

用户要求全部改为 10 个环境训练/测试。此前 n_envs=4 的 risk seed1 已停止并移动到 interrupted 目录，不进入正式汇总。

后续 P0 主协议：

- train n_envs: 10
- eval n_envs: 10
- timesteps: 1000000
- horizon: 1200 for main/ablation; 1500 for fixed defensive
- eval episodes: 50
- densities: 0.00, 0.08, 0.15

正式输出目录：

- outputs/iscsic_main_nenv10
- outputs/iscsic_ablation_nenv10
- outputs/defensive_ttc12_v18_nenv10_final

## 2026-06-30 curriculum density alignment

- Problem observed: proposed seed0 n_envs=10 collapsed after entering stage 3; logs showed window_success=0, window_cost around 0.73-0.77, route around 0.39-0.42.
- Root cause hypothesis: default curriculum hard traffic_density=0.22 is harder than the formal stress evaluation density=0.15, so the last curriculum stage over-trains on an out-of-protocol regime and destabilizes the policy.
- Change: DEFAULT_STAGES medium density changed from 0.10 to 0.08; hard density changed from 0.22 to 0.15. Reward weights, shield logic and PPO settings are unchanged.
- Validation: py_compile passed for config/env/experiment/train/evaluate_from_config.

## 2026-06-30 hard-stage evaluation alignment

- Problem observed after density alignment: stage 3 no longer had severe cost explosion, but success stayed at zero and route remained around 0.5-0.65.
- Code audit found mismatch: training hard stage still used accident_prob=0.02 and horizon=1000, while formal evaluation uses accident_prob=0.0 and horizon=1200.
- Change: DEFAULT_STAGES hard stage set to traffic_density=0.15, accident_prob=0.0, horizon=1200. Medium remains density=0.08.
- Reward weights, action guard, PPO hyperparameters and evaluation script are unchanged.
- Validation: py_compile passed.

## 2026-06-30 curriculum gate relaxation

- Problem observed: with hard stage aligned to evaluation, proposed seed0 still remained in stage 2 until around 993k because stage2_success=0.50 was rarely met.
- Change: stage2_success lowered from 0.50 to 0.25; allow_demote enabled; demote_grace_episodes lowered from 60 to 40.
- Rationale: ensure enough hard-density exposure while allowing recovery if the hard stage is temporarily too difficult. Environment density, accident_prob, reward weights, action guard and PPO hyperparameters are unchanged.
- Validation: py_compile passed.

## 2026-06-30 prehard curriculum and demotion logic

- Failure evidence: gate-relaxed proposed seed0 entered hard stage, but window_success stayed around 0 while route fell to about 0.50-0.65 and cost rose to about 0.56.
- Change 1: inserted a `prehard` curriculum stage at traffic_density=0.12, map_blocks=6, accident_prob=0.0, horizon=1100 between medium=0.08 and hard=0.15.
- Change 2: demotion now triggers when success is below demote_success and either route is below demote_route_completion or cost exceeds demote_cost, after grace episodes. Previously route/cost/success all had to fail simultaneously, so recovery almost never triggered.
- Change 3: demote_route_completion=0.65, demote_cost=0.45, stage2_cost=0.45.
- Validation: py_compile passed.

## 2026-06-30 train.py curriculum gate CLI support
- Added explicit `scripts/train.py` CLI options for curriculum promotion/demotion gates, including `--stage2-success`, `--stage2-cost`, stage1 gate overrides, demotion gate overrides, and `--no-demote`.
- Reason: targeted tuning runs must store changed curriculum gates in `config.json`; temporary source edits would be hard to trace and could contaminate later protocol comparisons.
- Verification: `python -m py_compile scripts/train.py` passed; `python scripts/train.py --help` shows `--stage2-success` and demotion options; launched strict-gate run wrote `stage2_success=0.35`, `stage2_cost=0.35`, `n_envs=10` to config.json.

## 2026-06-30 defensive evaluation n_envs fix
- Fixed `scripts/run_one_defensive_proposed.py` so its post-training evaluation passes `n_envs=args.n_envs` into `evaluate(...)`.
- Reason: user updated protocol to 10 environments for both training and testing; previous script trained with n_envs but evaluated with default eval_n_envs=1.
- Verification: `python -m py_compile scripts/run_one_defensive_proposed.py` passed and the evaluate call now includes `n_envs=args.n_envs`.
