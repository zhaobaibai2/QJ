#!/usr/bin/env bash
set -u
cd /home/aaa/data/qj/stable-baselines3-master/risk_curriculum_metadrive
RUN_GROUP=p1_density_expand_resume_max8_20260701_165529
MAX_JOBS=8
PID_FILE=/home/aaa/data/qj/stable-baselines3-master/risk_curriculum_metadrive/results/ijmlc_control/logs/p1_density_expand_resume_max8_20260701_165529.pids
: > "$PID_FILE"
launch_one() {
  local label="$1"
  local seed="$2"
  local run_id=${RUN_GROUP}_${label}_s${seed}
  local log=results/ijmlc_control/logs/${run_id}.log
  (
    /home/aaa/miniconda3/bin/conda run --no-capture-output -n sb3 python -u scripts/evaluate_ijmlc_diagnostics.py --labels "$label" --seeds "$seed" --densities 0.08 0.20 0.25 --test-start-seeds 10000 20000 --episodes-per-start 20 --run-id "$run_id"
    rc=$?
    echo "EXIT_CODE=${rc}" >> "$log"
    exit $rc
  ) > "$log" 2>&1 &
  echo "$! $run_id $log" >> "$PID_FILE"
}
while [ "$(jobs -rp | wc -l)" -ge "$MAX_JOBS" ]; do sleep 10; done
launch_one risk_only 0
while [ "$(jobs -rp | wc -l)" -ge "$MAX_JOBS" ]; do sleep 10; done
launch_one risk_only 1
while [ "$(jobs -rp | wc -l)" -ge "$MAX_JOBS" ]; do sleep 10; done
launch_one risk_only 2
while [ "$(jobs -rp | wc -l)" -ge "$MAX_JOBS" ]; do sleep 10; done
launch_one guard_only 0
while [ "$(jobs -rp | wc -l)" -ge "$MAX_JOBS" ]; do sleep 10; done
launch_one guard_only 1
while [ "$(jobs -rp | wc -l)" -ge "$MAX_JOBS" ]; do sleep 10; done
launch_one guard_only 2
while [ "$(jobs -rp | wc -l)" -ge "$MAX_JOBS" ]; do sleep 10; done
launch_one shield_only 0
while [ "$(jobs -rp | wc -l)" -ge "$MAX_JOBS" ]; do sleep 10; done
launch_one shield_only 1
while [ "$(jobs -rp | wc -l)" -ge "$MAX_JOBS" ]; do sleep 10; done
launch_one shield_only 2
while [ "$(jobs -rp | wc -l)" -ge "$MAX_JOBS" ]; do sleep 10; done
launch_one gated_risk 0
while [ "$(jobs -rp | wc -l)" -ge "$MAX_JOBS" ]; do sleep 10; done
launch_one gated_risk 1
while [ "$(jobs -rp | wc -l)" -ge "$MAX_JOBS" ]; do sleep 10; done
launch_one gated_risk 2
while [ "$(jobs -rp | wc -l)" -ge "$MAX_JOBS" ]; do sleep 10; done
launch_one no_action_guard 0
while [ "$(jobs -rp | wc -l)" -ge "$MAX_JOBS" ]; do sleep 10; done
launch_one no_action_guard 1
while [ "$(jobs -rp | wc -l)" -ge "$MAX_JOBS" ]; do sleep 10; done
launch_one no_action_guard 2
wait
