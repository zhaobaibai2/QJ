#!/usr/bin/env bash
SCRIPT_NAME="15_tensorboard"
source "$(dirname "$0")/common.sh"
run_main
PRESET="${PRESET:-paper}"
PORT="${PORT:-6006}"
record_command "${RUN_LOG_DIR}/tensorboard_${PRESET}.log" tensorboard --logdir "outputs/${PRESET}/runs" --port "${PORT}" --host 0.0.0.0
finish_run completed
