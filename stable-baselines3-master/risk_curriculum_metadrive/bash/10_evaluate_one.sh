#!/usr/bin/env bash
SCRIPT_NAME="10_evaluate_one"
source "$(dirname "$0")/common.sh"
run_main
VARIANT="${VARIANT:-proposed}"
ALGO="${ALGO:-ppo}"
SEED="${SEED:-0}"
EPISODES="${EPISODES:-30}"
HORIZON="${HORIZON:-1000}"
PRESET="${PRESET:-manual}"
DENSITIES="${DENSITIES:-0.00 0.10 0.25}"
MODEL="${MODEL:-outputs/${PRESET}/runs/${VARIANT}_${ALGO}_s${SEED}/model/final_model.zip}"
OUTPUT_DIR="outputs/${PRESET}/evaluations"
record_command "${RUN_LOG_DIR}/evaluate_${VARIANT}_${ALGO}_s${SEED}.log" python scripts/evaluate.py --model "${MODEL}" --variant "${VARIANT}" --algo "${ALGO}" --seed "${SEED}" --episodes "${EPISODES}" --horizon "${HORIZON}" --densities ${DENSITIES} --device "${DEVICE}" --output-dir "${OUTPUT_DIR}"
finish_run completed
