#!/usr/bin/env bash
set -euo pipefail

CVCI_RUN=/root/autodl-tmp/projects/CVCI_Benchmark/CVCI_BenchMark/runs/drivetransformer_large_cvci_full
SB3_ROOT=/root/autodl-tmp/projects/sb3/stable-baselines3-master/risk_curriculum_metadrive
LOG_DIR="$SB3_ROOT/outputs/stage1000_true_proposed_s0/logs"
mkdir -p "$LOG_DIR"

done_flag() {
  local task="$1"
  /root/miniconda3/envs/drivetransformer/bin/python - "$CVCI_RUN/results/cvci_${task}.json" <<'PY'
import json, sys
try:
    data=json.load(open(sys.argv[1]))
    progress=data.get('_checkpoint',{}).get('progress',[0,72])
    print("1" if len(progress)>=2 and int(progress[0]) >= int(progress[1]) else "0")
except Exception:
    print("0")
PY
}

while true; do
  d0="$(done_flag 0)"
  d1="$(done_flag 1)"
  echo "[$(date '+%F %T')] wait CVCI done: task0=$d0 task1=$d1"
  if [[ "$d0" == "1" && "$d1" == "1" ]]; then
    break
  fi
  sleep 300
done

cd "$SB3_ROOT"
source /root/miniconda3/etc/profile.d/conda.sh
conda activate sb3
export CUDA_VISIBLE_DEVICES=1
export OMP_NUM_THREADS=2
export MKL_NUM_THREADS=2
export NUMEXPR_MAX_THREADS=2
export MPLCONFIGDIR=/tmp/mpl-racrl

exec nice -n 10 /root/autodl-tmp/envs/sb3/bin/python scripts/launch_stage1000_true_proposed.py
