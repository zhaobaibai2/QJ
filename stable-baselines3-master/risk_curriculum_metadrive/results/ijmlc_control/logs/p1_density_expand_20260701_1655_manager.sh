#!/usr/bin/env bash
set -u
cd /home/aaa/data/qj/stable-baselines3-master/risk_curriculum_metadrive
RUN_GROUP=p1_density_expand_20260701_1655
MAX_JOBS=16
PID_FILE=results/ijmlc_control/logs/${RUN_GROUP}.pids
: > "$PID_FILE"
launch_one() {
  local label="$1"
  local seed="$2"
  local run_id=${RUN_GROUP}_${label}_s${seed}
  local log=results/ijmlc_control/logs/${run_id}.log
  (
    /home/aaa/miniconda3/bin/conda run --no-capture-output -n sb3 python -u scripts/evaluate_ijmlc_diagnostics.py       --labels "$label" --seeds "$seed" --densities 0.08 0.20 0.25       --test-start-seeds 10000 20000 --episodes-per-start 20 --run-id "$run_id"
    rc=$?
    echo "EXIT_CODE=${rc}" >> "$log"
    exit $rc
  ) > "$log" 2>&1 &
  echo "$! $run_id $log" >> "$PID_FILE"
}
for label in baseline risk_only guard_only shield_only gated_risk no_action_guard; do
  for seed in 0 1 2; do
    while [ "$(jobs -rp | wc -l)" -ge "$MAX_JOBS" ]; do
      sleep 10
    done
    launch_one "$label" "$seed"
  done
done
wait
