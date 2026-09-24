#!/usr/bin/env bash
set -euo pipefail
cd /home/aaa/data/qj/stable-baselines3-master/risk_curriculum_metadrive
if [ -f "$HOME/miniconda3/etc/profile.d/conda.sh" ]; then
  source "$HOME/miniconda3/etc/profile.d/conda.sh"
elif [ -f "$HOME/anaconda3/etc/profile.d/conda.sh" ]; then
  source "$HOME/anaconda3/etc/profile.d/conda.sh"
elif [ -f "/opt/conda/etc/profile.d/conda.sh" ]; then
  source "/opt/conda/etc/profile.d/conda.sh"
else
  echo "conda.sh not found" >&2
  exit 1
fi
conda activate sb3
export PYTHONUNBUFFERED=1
python scripts/run_one_defensive_proposed.py \
  --seed 26 \
  --n-envs 16 \
  --timesteps 1000000 \
  --root outputs/defensive_ttc12_v18_nenv16_final \
  --ttc-threshold 12.0 \
  --target-speed 18.0 \
  --device cuda
TARGET_N_ENVS=16 FINAL_OUTPUT_DIR=final_iscsic_results_nenv16 python scripts/build_final_outputs.py
