#!/usr/bin/env bash
SCRIPT_NAME="09_train_one"
source "$(dirname "$0")/common.sh"
run_main
VARIANT="${VARIANT:-proposed}"
ALGO="${ALGO:-ppo}"
SEED="${SEED:-0}"
TIMESTEPS="${TIMESTEPS:-300000}"
HORIZON="${HORIZON:-1000}"
PRESET="${PRESET:-manual}"
OUTPUT_DIR="outputs/${PRESET}/runs"
record_command "${RUN_LOG_DIR}/train_${VARIANT}_${ALGO}_s${SEED}.log" python scripts/train.py --variant "${VARIANT}" --algo "${ALGO}" --seed "${SEED}" --timesteps "${TIMESTEPS}" --horizon "${HORIZON}" --device "${DEVICE}" --output-dir "${OUTPUT_DIR}"
finish_run completed
