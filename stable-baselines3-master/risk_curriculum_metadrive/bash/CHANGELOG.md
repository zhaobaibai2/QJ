# bash 修改记录

## 2026-05-28

- **新增脚本体系**: 在 `bash/` 下新增统一运行入口，覆盖环境检查、smoke、pilot、tuning、validation、million、paper、paper+SAC、ablation、单独训练、单独评估、绘图、轨迹图、论文编译和 TensorBoard。
- **统一环境**: 所有脚本通过 `common.sh` 先激活 `sb3` conda 环境，并默认使用 `cuda`。
- **统一命名**: 套件脚本直接使用 `outputs/<preset>/`；单独训练/评估使用 `PRESET` 指定输出分组。
- **运行记录**: 每次运行自动写入 `bash/RUN_HISTORY.md`，并在 `bash/logs/<run_id>/` 保存环境、GPU、git 状态、代码 diff 和命令日志。
