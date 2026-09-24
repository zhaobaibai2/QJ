# Risk-Aware Curriculum RL for MetaDrive

面向论文实验的 MetaDrive 0.4.3 + Stable-Baselines3 (PyTorch) 工程，实现：

- `PPO` / `SAC` 基线；
- TTC 风险、车道偏离、转向/加速度平滑性和终止事件奖励塑形；
- 基于路线完成度、成功率与安全代价的四阶段自适应课程；
- unseen map、多交通密度评估；
- TensorBoard、CSV、JSON 结果记录和论文图表生成。

当前正式协议使用 pilot 后修正的安全奖励塑形：`base_scale=1.0`，TTC、横向偏离平方、
转向变化、加速度变化和事件代价权重分别为 `2.0/0.10/0.005/0.002/5.0`，
到达终点奖励为 `40`，撞车和驶出道路额外惩罚为 `80/80`。课程使用
warm-up/easy/medium/hard 四阶段，medium/hard 交通密度分别为 `0.08/0.15`，并通过路线完成度、成功率和安全代价推进。
课程默认为单调升级（`allow_demote=False`），避免长训练后从高难度退回低难度导致
最终策略与测试分布不一致。

## 环境

本目录位于 SB3 与 MetaDrive 源码同级工程内。程序优先加载仓库内的
`../metadrive/metadrive`，其版本必须为 `0.4.3`，因此资产可直接使用并且
不依赖用户目录下载。

```bash
source /home/aaa/miniconda3/etc/profile.d/conda.sh
conda activate sb3
export MPLCONFIGDIR=/tmp/mpl-racrl
cd /home/aaa/data/qj/stable-baselines3-master/risk_curriculum_metadrive
python scripts/check_env.py --require-gpu
```

训练与评估默认拒绝 CPU 回退，确保论文结果确实来自 GPU 上运行的 PyTorch
策略网络。MetaDrive 仿真物理本身仍由 CPU 执行，这是模拟器的正常行为。

## 运行

冒烟验证：

```bash
python scripts/run_suite.py --preset smoke --device cuda
```

单种子参数验证（完整方法 100,000 步）：

```bash
python scripts/run_suite.py --preset pilot --device cuda
```

单种子调参验证（完整方法 300,000 步）：

```bash
python scripts/run_suite.py --preset tuning --device cuda
```

四组趋势验证（四个 PPO 方法，每种 500,000 步，复杂道路回合上限 1000 步）：

```bash
python scripts/run_suite.py --preset validation --device cuda
```

完整方法百万步预验证：

```bash
python scripts/run_suite.py --preset million --device cuda
```

正式主实验（四个 PPO 变体，三个随机种子，每模型 1,000,000 步，完成后自动评估和绘图）：

```bash
python scripts/run_suite.py --preset paper --device cuda
```

加入 SAC 对比：

```bash
python scripts/run_suite.py --preset paper --include-sac --device cuda
```

风险项消融：

```bash
python scripts/run_suite.py --preset ablation --device cuda
```

单次训练、评估和绘图：

```bash
python scripts/train.py --variant proposed --algo ppo --seed 0 --timesteps 1000000 --device cuda
python scripts/evaluate.py --model outputs/runs/proposed_ppo_s0/model/final_model.zip --variant proposed --algo ppo --seed 0 --device cuda
python scripts/plot_results.py --input-dir outputs/evaluations --output-dir outputs/figures
```

## 研究变体

| 变体 | 风险奖励 | 课程策略 | 用途 |
| --- | --- | --- | --- |
| `baseline` | 否 | 否 | PPO/SAC 基线 |
| `risk` | 是 | 否 | 奖励塑形消融 |
| `curriculum` | 否 | 是 | 课程策略消融 |
| `proposed` | 是 | 是 | 完整方法 |
| `proposed_wo_ttc` | 是，TTC 权重为 0 | 是 | TTC 消融 |
| `proposed_wo_lane` | 是，车道偏离权重为 0 | 是 | 车道偏离消融 |
| `proposed_wo_smooth` | 是，转向/加速度平滑权重为 0 | 是 | 控制平滑消融 |

## 输出

- `outputs/<preset>/runs/<run>/tensorboard/`: TensorBoard event 文件；
- `outputs/<preset>/runs/<run>/monitor.monitor.csv`: 训练 episode 指标；
- `outputs/<preset>/runs/<run>/model/`: 最终和检查点模型；
- `outputs/<preset>/evaluations/*.csv`: 每 episode 测试数据；
- `outputs/<preset>/evaluations/summary.csv`: 汇总结果表；
- `outputs/<preset>/figures/`: 该实验套件对应的 PDF/PNG 图，训练曲线优先由 TensorBoard 标量生成；
- `paper/main_zh.tex`: 中文论文初稿。

TensorBoard：

```bash
tensorboard --logdir outputs/paper/runs --port 6006
```

训练中将车道偏离作为密集风险惩罚，但只有真正驶离道路才以越界终止回合
（`on_continuous_line_done=False`，`out_of_road_done=True`），以避免触碰道路标线造成
过早终止并掩盖可学习的控制行为。
