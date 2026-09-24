# SB3 MetaDrive 论文实验持续工作记录

更新时间：2026-05-29 22:28 CST

## 用户目标

- 项目目录：`/root/autodl-tmp/projects/sb3/stable-baselines3-master/risk_curriculum_metadrive`
- 环境：`conda activate sb3` 或 `/root/autodl-tmp/envs/sb3/bin/python`
- 输出统一放在：`risk_curriculum_metadrive/outputs`
- 使用 GPU1，尽可能快地训练和评估；目前 CVCI/CARLA 已结束，可以更积极使用 CPU/GPU。
- 论文目标：不要造指标，但需要尽量提高主结果；若 0.95 不现实，可以稍降目标，同时增加创新点、消融、图、表和 LaTeX，最终服务于投稿质量。

## 当前核心判断

1. 纯 PPO + 风险奖励 + 课程学习在 hard density=0.15 下目前成功率仍偏低，seed0/seed1 约 0.42-0.56。
2. 仅继续 PPO 步数可能提升有限；需要增加方法创新：风险感知密集奖励、自适应课程学习、TTC/车道/速度触发的 safety shield、专家策略或 IDM 风险接管、多种子统计、消融实验、压力测试。
3. 论文写法要诚实：主表用相对稳定且表现较好的设置；高密度/事故作为压力测试，不把低结果伪装成高结果。
4. 如果专家/专家接管能显著提高成功率，就把最终方法定义为 `Risk-aware Curriculum PPO with Expert Safety Shield`，报告接管率，作为创新点之一。

## CVCI 已完成状态

CVCI/DriveTransformer 已完成 144/144 场景测试，无 CARLA/leaderboard 进程残留。

目录：`/root/autodl-tmp/projects/CVCI_Benchmark/CVCI_BenchMark/runs/drivetransformer_large_cvci_full`

关键输出：`summary.md`、`summary.json`、`cvci_144_final_report.md`、`cvci_144_final_routes.csv`

结果摘要：Evaluated routes 144/144；Successful evaluated routes 20/144；Success rate 0.1389；Missing routes 0；Bad result files 0；Mean `score_route` 57.7635；Mean `score_challenge` 31.9697。

## 已完成 SB3 代码修改

### `racrl/config.py`

- medium traffic density 改为 `0.08`，hard traffic density 改为 `0.15`。
- `ExperimentConfig.n_envs` 支持多环境并行。
- 当前 reward 权重：`ttc=4.0`，`cost=30.0`，`overspeed=2.5`，`target_speed_kmh=20.0`，`progress=35.0`，`success_bonus=50.0`，`crash_penalty=100.0`，`out_of_road_penalty=100.0`，`ttc_threshold=6.0`。

### `racrl/envs.py`

- 支持 `SubprocVecEnv` 多 worker。
- 修复 SubprocVecEnv reset seed 超出 MetaDrive scenario range 的问题。
- 加入 TTC shield：`min_ttc < 3.5` 强制 brake 到 `-1.0`，`min_ttc < 6.0` brake 到 `-0.6`。
- 加入速度守护：超过目标速度限制油门，超过目标速度 5 km/h 强制轻刹。
- 观测 lidar `num_others=4`，让策略看到周围交通车。

### `racrl/experiment.py`

- `train(..., load_model_path=None)` 支持从已有模型继续训练。
- checkpoint 频率按 `n_envs` 修正。

### 新增/使用脚本

- `scripts/plot_framework_diagram.py`
- `scripts/plot_return_figures.py`
- `scripts/launch_stage1000_true_proposed.py`
- `scripts/launch_stage1000_true_proposed_seeds12.py`
- `scripts/launch_stage1000_stable_proposed.py`
- `scripts/launch_stage1000_stable_proposed_seeds12.py`
- `scripts/launch_stage1000_true_proposed_s4s5_nenv16.py`
- `scripts/evaluate_parallel_shield.py`

## 已完成 SB3 结果

### `outputs/stage1000_true_proposed_s0`

true 100w seed0，评估 50 episodes：density 0.00 success 0.84，density 0.08 success 0.78，density 0.15 success 0.42。

### `outputs/stage1000_true_proposed_multiseed`

seed1 true 100w：density 0.00 success 0.84，density 0.08 success 0.74，density 0.15 success 0.56。seed2 当前仍在跑。

### `outputs/stage1000_final_candidate`

ckpt702 + conservative TTC shield：density 0.00 success 0.84，density 0.08 success 0.74，density 0.15 success 0.48。

### `outputs/paper_comparison_seed0`

baseline/risk/curriculum/proposed seed0 对比已完成，能作为论文初始对比，但不是最终主表。

## 当前正在跑的任务

### seed2 true 100w

- 目录：`outputs/stage1000_true_proposed_multiseed`
- 日志：`outputs/stage1000_true_proposed_multiseed/logs/seeds12_20260529_201826.log`
- 进程：`scripts/launch_stage1000_true_proposed_seeds12.py`
- 最新已看到进度：约 46w/100w（2026-05-29 22:14）

### seed3 true 100w, n_envs=8

- 目录：`outputs/stage1000_true_proposed_s3_nenv8`
- 日志：`outputs/stage1000_true_proposed_s3_nenv8/logs/run_20260529_215935.log`
- 最新已看到进度：约 41w/100w（2026-05-29 22:14）
- 速度约 700-800 fps。

### seed4/seed5 true 100w, n_envs=16

- 目录：`outputs/stage1000_true_proposed_s4s5_nenv16`
- 日志：`outputs/stage1000_true_proposed_s4s5_nenv16/logs/run_20260529_222258.log`
- 进程 PID：`844216`
- seed4 已启动，速度约 1400 fps。

### shield/expert 并行评估

- 目录：`outputs/policy_shield_screen`
- 脚本：`scripts/evaluate_parallel_shield.py`
- 日志：`outputs/policy_shield_screen/logs/eval_20260529_222410.log`
- 进程 PID：`844319`
- 设置：50 episodes，36 workers，horizon 1200。
- 评估方法：`expert_only/expert`，`rl_s0_100w/rl`，`rl_s0_100w/shield_expert`，`rl_s1_100w/rl`，`rl_s1_100w/shield_expert`，`rl_ckpt702/rl`，`rl_ckpt702/shield_expert`。
- 输出：`outputs/policy_shield_screen/evaluations/shield_screen.csv`，`outputs/policy_shield_screen/evaluations/summary.csv`，partial 文件 `shield_screen_partial.csv`。

## 资源状态记录

2026-05-29 22:24 左右：CPU 192 核，内存约 1.0TiB，可用约 894GB。GPU0 基本空闲，GPU1 显存约 1.3GB，利用率 6-23%。MetaDrive/PPO 主要受 CPU 仿真限制。

## 接下来必须做

1. 等 `evaluate_parallel_shield.py` 完成，读取 `outputs/policy_shield_screen/evaluations/summary.csv`。
2. 如果 `shield_expert` 或 `expert_only` 成功率显著更高：把最终方法改为 `Risk-aware Curriculum PPO with Expert Safety Shield`，增加 success/collision/route/takeover_rate 图，论文解释风险触发接管率。
3. 等 seed2/seed3/seed4/seed5 完成，整理所有 true 100w seeds。
4. 合并主结果目录，建议新建 `outputs/final_paper_results`，包含 `evaluations/`、`figures/`、`tables/`、运行记录。
5. 重画图：training return、test success、collision、base return、shaped return、robustness control、curriculum stage、framework diagram、shield takeover rate。
6. 修改 `paper/main_zh.tex`：同步真实权重、density、horizon=1200、多种子、expert safety shield、最终图路径。
7. 更新 `paper/generated_results.tex`。
8. 编译 `paper/main_zh.pdf`；如果 xelatex 不存在，记录原因。

## 后续命令参考

检查任务状态：

```bash
cd /root/autodl-tmp/projects/sb3/stable-baselines3-master/risk_curriculum_metadrive
ps -eo pid,ppid,stat,pcpu,pmem,etime,args | egrep "launch_stage1000|evaluate_parallel_shield|train.py|CarlaUE4|leaderboard" | grep -v egrep
nvidia-smi
```

查看训练进度：

```bash
grep -E "total_timesteps|saved_report|Traceback|Error" outputs/stage1000_true_proposed_multiseed/logs/seeds12_20260529_201826.log | tail -80
grep -E "total_timesteps|saved_report|Traceback|Error" outputs/stage1000_true_proposed_s3_nenv8/logs/run_20260529_215935.log | tail -80
grep -E "total_timesteps|saved_report|Traceback|Error" outputs/stage1000_true_proposed_s4s5_nenv16/logs/run_20260529_222258.log | tail -80
```

查看 shield 评估：

```bash
tail -120 outputs/policy_shield_screen/logs/eval_20260529_222410.log
cat outputs/policy_shield_screen/evaluations/summary.csv
```

## 注意

- 不要把低成功率改写成高成功率；论文可以通过降低主测试难度、增加压力测试、增加安全接管创新点来成立，但不能伪造。
- `Completed` 不等于 success，评估脚本里的 `is_success` 才是最终成功率。
- GPU 利用率低是 SB3 MLP + MetaDrive 仿真的正常现象，真正瓶颈是 CPU 环境步。
- 后续如果继续开更大并行，先看 load average，建议不超过 120-150，避免把系统打满。

## 2026-05-29 22:35 资源加速更新

用户反馈 htop 只看到少数 Python。我检查后确认：顶层 launcher 看起来少，但实际 SB3 Python 进程数为 69；之后又启动 seed6/seed7 独立训练后，Python 进程数达到 119。

新增失败尝试：`scripts/launch_stage1000_true_proposed_s6s7_parallel_nenv24.py` 用 Python multiprocessing fork 同时启两个 CUDA 训练，报错 `Cannot re-initialize CUDA in forked subprocess`。该任务已退出，没有持续占资源。结论：多 CUDA 训练不能用 fork 方式并行，要用独立 nohup 进程或 spawn。

新增成功任务：

- 脚本：`scripts/run_one_true_proposed.py`
- 目录：`outputs/stage1000_true_proposed_s6s7_independent_nenv24`
- seed6 日志：`outputs/stage1000_true_proposed_s6s7_independent_nenv24/logs/seed6_20260529_223353.log`
- seed7 日志：`outputs/stage1000_true_proposed_s6s7_independent_nenv24/logs/seed7_20260529_223353.log`
- seed6 PID：`844965`
- seed7 PID：`844967`
- 设置：每个 seed 1,000,000 steps，`n_envs=24`，horizon 1200，GPU1。
- 初始速度：约 1100-1500 fps。

资源状态：2026-05-29 22:34，Python 进程数 119，GPU1 显存约 2281MiB，瞬时 GPU 利用率约 78%，load average 约 43/192，内存仍非常充足。当前利用率比之前明显提高，但还未接近系统上限。

## 2026-05-29 22:46 shield 评估问题

`evaluate_parallel_shield.py` 的 full/fast 两组 ProcessPool 评估卡住：日志保持 0 字节，worker 长时间处于 `do_select`，CPU 很低，没有产出 partial CSV。判断为 MetaDrive/专家策略在该 ProcessPool 并行方式下不稳定或阻塞。已停止相关进程：full PID `844319`，fast PID `845286/845283`。后续不要再用这个脚本的大 ProcessPool 方式；改成独立 nohup 子进程或顺序评估，并加入单 episode 超时与逐 episode 写 CSV。

补充：停止父进程后 fast 评估遗留孤儿 worker，已清理；当前没有 `evaluate_parallel_shield.py` 进程。

## 2026-05-29 DriveTransformer 一轮训练脚本确认

DriveTransformer 训练脚本仍在：`/root/autodl-tmp/projects/code/DriveTransformer/runs/cvci_drivetransformer_train/run_cvci_train.sh`。
配置文件：`/root/autodl-tmp/projects/code/DriveTransformer/runs/cvci_drivetransformer_train/cvci_finetune_large.py`。
README：`/root/autodl-tmp/projects/code/DriveTransformer/runs/cvci_drivetransformer_train/README_TRAIN.md`。

训练数据 info：`/root/autodl-tmp/projects/code/DriveTransformer/data/infos/cvci_infos_drivetransformer_meta.pkl`，`total_lenth=39584`，`routes_names=141`。两张 GPU、每 GPU batch=1 时，严格一轮约 `ceil(39584 / 2) = 19792` iter。脚本默认 `MAX_ITERS=20000`，基本就是一轮，且方便保存 `iter_20000.pth`。

注意：README 记录 `BATCH_SIZE=2` 在 4090D pair 上 OOM，所以安全最大资源建议保持 `BATCH_SIZE=1`，通过 `GPUS=2`、较高 `WORKERS_PER_GPU` 和 `OMP_NUM_THREADS` 提高吞吐。

推荐一轮训练命令：

```bash
cd /root/autodl-tmp/projects/code/DriveTransformer
CUDA_VISIBLE_DEVICES=0,1 GPUS=2 BATCH_SIZE=1 WORKERS_PER_GPU=16 OMP_NUM_THREADS=16 MKL_NUM_THREADS=16 MAX_ITERS=20000 CHECKPOINT_INTERVAL=1000 MASTER_PORT=35229 bash runs/cvci_drivetransformer_train/run_cvci_train.sh
```

严格 19792 iter 版本：

```bash
cd /root/autodl-tmp/projects/code/DriveTransformer
CUDA_VISIBLE_DEVICES=0,1 GPUS=2 BATCH_SIZE=1 WORKERS_PER_GPU=16 OMP_NUM_THREADS=16 MKL_NUM_THREADS=16 MAX_ITERS=19792 CHECKPOINT_INTERVAL=9896 MASTER_PORT=35229 bash runs/cvci_drivetransformer_train/run_cvci_train.sh
```

## 2026-05-29 23:05 继续加速

当前 seed3 已完成并出评估；seed4 已出评估；seed5 开始训练；seed6/seed7 训练已到 100w，进入评估阶段。由于 Python 进程降到约 24、load 约 19/192，又启动 seed8/seed9 双独立训练。

新增任务：

- 目录：`outputs/stage1000_true_proposed_s8s9_independent_nenv32`
- seed8 PID：`846488`，日志：`outputs/stage1000_true_proposed_s8s9_independent_nenv32/logs/seed8_20260529_230547.log`
- seed9 PID：`846490`，日志：`outputs/stage1000_true_proposed_s8s9_independent_nenv32/logs/seed9_20260529_230547.log`
- 设置：每个 seed 1,000,000 steps，`n_envs=32`，horizon 1200，GPU1。


## 2026-05-29 23:08 继续扩并行

seed8/seed9 正常启动后，资源仍安全：Python 约 90，GPU1 瞬时约 77%，load 约 31/192。继续启动 seed10/seed11：

- 目录：
- 设置：每个 seed 1,000,000 steps，，horizon 1200，GPU1。
- 后续需要检查日志： 和 。

## 2026-05-29 23:08 继续扩并行（修正版）

seed8/seed9 正常启动后，资源仍安全：Python 约 90，GPU1 瞬时约 77%，load 约 31/192。继续启动 seed10/seed11。

- 目录：`outputs/stage1000_true_proposed_s10s11_independent_nenv32`
- seed10 PID：`846782`，日志：`outputs/stage1000_true_proposed_s10s11_independent_nenv32/logs/seed10_20260529_230747.log`
- seed11 PID：`846784`，日志：`outputs/stage1000_true_proposed_s10s11_independent_nenv32/logs/seed11_20260529_230747.log`
- 设置：每个 seed 1,000,000 steps，`n_envs=32`，horizon 1200，GPU1。

注意：本段上一条追加时因远端 shell 双引号导致 Markdown 反引号被展开，可能出现少量 shell 报错；训练启动成功，已用本段修正记录。

## 2026-05-29 23:09 启用 GPU0

用户明确要求不再只用一张 GPU。当前 GPU1 瞬时利用率高、GPU0 空闲，因此新增 seed12/seed13 到 GPU0。

- 目录：`outputs/stage1000_true_proposed_s12s13_gpu0_nenv24`
- seed12 PID：`846945`，日志：`outputs/stage1000_true_proposed_s12s13_gpu0_nenv24/logs/seed12_20260529_230837.log`
- seed13 PID：`846947`，日志：`outputs/stage1000_true_proposed_s12s13_gpu0_nenv24/logs/seed13_20260529_230837.log`
- 设置：每个 seed 1,000,000 steps，`n_envs=24`，horizon 1200，`CUDA_VISIBLE_DEVICES=0`。

## 2026-05-29 23:10 高密度安全守护优化

修改 `racrl/envs.py`：TTC action guard 不再固定用 3.5/6.0 秒，而是根据 `reward_weights.ttc_threshold` 自动缩放：

- `hard_ttc = max(3.5, ttc_threshold * 0.60)` 时强制 brake `-1.0`
- `soft_ttc = max(6.0, ttc_threshold)` 时保守 brake `-0.6`

这样后续可在评估或新训练中设置更高 `ttc_threshold`（例如 8-10 秒）形成更保守的 defensive shield，目标是降低 density=0.15 的碰撞率。已通过 `python -m py_compile racrl/envs.py`。

## 2026-05-29 23:25 新增防御版训练脚本

新增 `scripts/run_one_defensive_proposed.py`。该版本不是简单复评，而是重新训练防御版方法：

- horizon 1500
- `ttc_threshold=8.0`
- `target_speed_kmh=18.0`
- `ttc=6.0`
- `cost=40.0`
- `overspeed=3.0`
- `progress=40.0`
- `crash/out_of_road_penalty=120.0`
- `stage2_cost=0.25`

目标：降低 density=0.15 高密度碰撞，同时保持 0.08 主任务成功率。

## 2026-05-29 23:29 启动防御版训练

启动防御版 `defensive_proposed` 训练，目标不是盲目增加 seed，而是验证新方法是否能降低高密度碰撞。

- 目录：`outputs/defensive_proposed_s20s21_nenv32`
- seed20：GPU0，PID `847978`，日志 `outputs/defensive_proposed_s20s21_nenv32/logs/seed20_gpu0_20260529_232928.log`
- seed21：GPU1，PID `847980`，日志 `outputs/defensive_proposed_s20s21_nenv32/logs/seed21_gpu1_20260529_232928.log`
- 设置：每个 seed 1,000,000 steps，`n_envs=32`，horizon 1500，`ttc_threshold=8.0`，`target_speed=18.0`。

## 2026-05-29 23:44 启动第二组防御版训练 ttc10/v18

旧模型筛查显示 `ttc10/v18` 是当前较好的安全-效率折中：density=0.15 success 约 0.60、collision 约 0.15。为避免只用后处理，启动重新训练版本。

- 目录：`outputs/defensive_proposed_ttc10v18_s22s23_nenv32`
- seed22：GPU0，PID `848593`，日志 `outputs/defensive_proposed_ttc10v18_s22s23_nenv32/logs/seed22_gpu0_20260529_234355.log`
- seed23：GPU1，PID `848595`，日志 `outputs/defensive_proposed_ttc10v18_s22s23_nenv32/logs/seed23_gpu1_20260529_234355.log`
- 设置：每个 seed 1,000,000 steps，`n_envs=32`，horizon 1500，`ttc_threshold=10.0`，`target_speed=18.0`。

## 2026-05-29 23:54 启动第三组防御版训练 ttc12/v18

防御筛查显示 `ttc12/v18` 是当前最好安全-效率折中：density=0.15 success 约 0.60，collision 约 0.10，out_of_road 0，cost 0.10。启动重新训练版本。

- 目录：`outputs/defensive_proposed_ttc12v18_s24s25_nenv32`
- seed24：GPU0，PID `849103`，日志 `outputs/defensive_proposed_ttc12v18_s24s25_nenv32/logs/seed24_gpu0_20260529_235428.log`
- seed25：GPU1，PID `849105`，日志 `outputs/defensive_proposed_ttc12v18_s24s25_nenv32/logs/seed25_gpu1_20260529_235428.log`
- 设置：每个 seed 1,000,000 steps，`n_envs=32`，horizon 1500，`ttc_threshold=12.0`，`target_speed=18.0`。

## 2026-05-29 23:58 防御层筛查结论

旧模型 seed1 上的防御层参数筛查完成。主要结果：

- `ttc8/v18`: density=0.15 success 0.65, collision 0.30, cost 0.30
- `ttc10/v16`: density=0.15 success 0.55, collision 0.10, cost 0.15
- `ttc10/v18`: density=0.15 success 0.60, collision 0.15, cost 0.25
- `ttc12/v18`: density=0.15 success 0.60, collision 0.10, cost 0.10; density=0.08 success 0.80, collision 0.05
- `ttc8/v20`: density=0.15 success 0.55, collision 0.35, cost 0.35

结论：`ttc12/v18` 是目前最适合论文安全层的 Pareto 点。它牺牲少量效率但显著降低高密度碰撞。最终论文应把原始 RAC-PPO 作为无防御对照，把 Defensive RAC-PPO (`ttc12/v18`) 作为主方法候选；density=0.15 作为压力测试，不能声称接近 0.95。
