# bash 实验脚本说明

本目录保存所有可复现实验入口、运行日志和修改记录。

## 统一规则

- **环境**: 所有脚本都会先执行 `conda activate sb3`。
- **GPU**: 默认 `GPU_ID=0`，并传入 `--device cuda`。
- **日志**: 每次运行都会创建 `bash/logs/<时间戳>_<脚本名>/`。
- **记录**: 每次运行会追加到 `bash/RUN_HISTORY.md`。
- **代码快照**: 每次运行会保存 `environment.txt`、`git_status.txt`、`code_diff.patch` 和命令输出。

## 常用命令

```bash
bash bash/00_check_env.sh
bash bash/03_tuning.sh
bash bash/04_validation.sh
bash bash/06_paper.sh
bash bash/08_ablation.sh
```

## 指定 GPU

```bash
GPU_ID=1 bash bash/03_tuning.sh
```

## 单独训练

```bash
VARIANT=proposed ALGO=ppo SEED=0 TIMESTEPS=300000 PRESET=manual_tuning bash bash/09_train_one.sh
```

## 单独评估

```bash
MODEL=outputs/manual_tuning/runs/proposed_ppo_s0/model/final_model.zip VARIANT=proposed ALGO=ppo SEED=0 PRESET=manual_tuning bash bash/10_evaluate_one.sh
```

## 输出目录

- **套件训练**: `outputs/<preset>/runs/`
- **套件评估**: `outputs/<preset>/evaluations/`
- **套件图表**: `outputs/<preset>/figures/`
- **bash 日志**: `bash/logs/`
