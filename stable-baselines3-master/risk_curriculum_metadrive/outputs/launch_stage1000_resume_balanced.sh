#!/usr/bin/env bash
set -euo pipefail

cd /root/autodl-tmp/projects/sb3/stable-baselines3-master/risk_curriculum_metadrive
source /root/miniconda3/etc/profile.d/conda.sh
conda activate sb3

export CUDA_VISIBLE_DEVICES=1
export OMP_NUM_THREADS=2
export MKL_NUM_THREADS=2
export NUMEXPR_MAX_THREADS=2
export MPLCONFIGDIR=/tmp/mpl-racrl

ROOT=outputs/stage1000_resume_balanced_safety
BASE=outputs/stage600_nenv4_guarded/runs/proposed_ppo_s0/model/final_model.zip
mkdir -p "$ROOT/logs" "$ROOT/evaluations" "$ROOT/figures"

python scripts/train.py \
  --variant proposed \
  --algo ppo \
  --seed 0 \
  --timesteps 400000 \
  --horizon 1200 \
  --device cuda \
  --n-envs 4 \
  --load-model "$BASE" \
  --output-dir "$ROOT/runs"

python scripts/evaluate.py \
  --model "$ROOT/runs/proposed_ppo_s0/model/final_model.zip" \
  --variant proposed \
  --algo ppo \
  --seed 0 \
  --episodes 50 \
  --horizon 1200 \
  --device cuda \
  --densities 0.00 0.08 0.15 \
  --output-dir "$ROOT/evaluations"

python scripts/plot_results.py \
  --input-dir "$ROOT/evaluations" \
  --output-dir "$ROOT/figures" \
  --runs-dir "$ROOT/runs"

python scripts/write_run_report.py \
  --experiment-root "$ROOT" \
  --preset stage1000_resume_balanced_safety
