#!/usr/bin/env bash
set -euo pipefail
if [ "$#" -lt 3 ]; then
  echo "usage: $0 VARIANT SEED OUTPUT_ROOT [TIMESTEPS=1000000] [HORIZON=1200] [extra train args...]" >&2
  exit 2
fi
VARIANT="$1"
SEED="$2"
ROOT_OUT="$3"
TIMESTEPS="${4:-1000000}"
HORIZON="${5:-1200}"
shift 5 || true
N_ENVS="${N_ENVS:-16}"
EPISODES="${EPISODES:-50}"
DEVICE="${DEVICE:-cuda}"
ALGO="${ALGO:-ppo}"
PROJECT=/home/aaa/data/qj/stable-baselines3-master/risk_curriculum_metadrive
cd "$PROJECT"
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
mkdir -p "$ROOT_OUT/logs" "$ROOT_OUT/runs" "$ROOT_OUT/evaluations" "$ROOT_OUT/figures"
RUN_NAME="${VARIANT}_${ALGO}_s${SEED}"
RUN_DIR="$ROOT_OUT/runs/$RUN_NAME"
MODEL="$RUN_DIR/model/final_model.zip"
CONFIG="$RUN_DIR/config.json"
echo "start_time=$(date -Is)"
echo "variant=$VARIANT seed=$SEED root=$ROOT_OUT timesteps=$TIMESTEPS horizon=$HORIZON n_envs=$N_ENVS episodes=$EPISODES device=$DEVICE extra_args=$*"
python scripts/train.py \
  --variant "$VARIANT" \
  --algo "$ALGO" \
  --seed "$SEED" \
  --timesteps "$TIMESTEPS" \
  --horizon "$HORIZON" \
  --device "$DEVICE" \
  --output-dir "$ROOT_OUT/runs" \
  --n-envs "$N_ENVS" \
  "$@"
python scripts/evaluate_from_config.py \
  --config-json "$CONFIG" \
  --model "$MODEL" \
  --episodes "$EPISODES" \
  --densities 0.00 0.08 0.15 \
  --output-dir "$ROOT_OUT/evaluations" \
  --device "$DEVICE" \
  --n-envs "$N_ENVS"
python scripts/plot_results.py --input-dir "$ROOT_OUT/evaluations" --output-dir "$ROOT_OUT/figures" --runs-dir "$ROOT_OUT/runs" || true
python scripts/plot_return_figures.py --runs-dir "$ROOT_OUT/runs" --eval-dir "$ROOT_OUT/evaluations" --output-dir "$ROOT_OUT/figures" || true
python scripts/write_run_report.py --experiment-root "$ROOT_OUT" --preset "$(basename "$ROOT_OUT")" || true
echo "end_time=$(date -Is)"
