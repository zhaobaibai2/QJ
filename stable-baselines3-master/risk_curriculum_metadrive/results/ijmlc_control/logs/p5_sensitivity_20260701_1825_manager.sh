#!/usr/bin/env bash
set -u
cd /home/aaa/data/qj/stable-baselines3-master/risk_curriculum_metadrive
RUN_GROUP=p5_sensitivity_20260701_1825
STATUS=results/ijmlc_control/p5_sensitivity_status.csv
MANIFEST=results/ijmlc_control/06_EXISTING_MODEL_MANIFEST.csv
MAX_PARALLEL=16
mkdir -p results/ijmlc_control/logs results/ijmlc_control/raw_csv results/ijmlc_control/summary_tables
echo "label,seed,axis,value,status,start_time,end_time,exit_code,run_id,raw_csv,summary_csv,log_path" > "$STATUS"
run_one() {
  label=$1; seed=$2; axis=$3; value=$4
  RUN_ID=${RUN_GROUP}_${axis}_${value}_${label}_s${seed}
  LOG=results/ijmlc_control/logs/${RUN_ID}.log
  RAW=results/ijmlc_control/raw_csv/${RUN_ID}_episodes.csv
  SUM=results/ijmlc_control/summary_tables/${RUN_ID}_summary.csv
  START=$(date --iso-8601=seconds)
  if [ -f "$RAW" ] && [ -f "$SUM" ]; then
    END=$(date --iso-8601=seconds)
    echo "$label,$seed,$axis,$value,skipped_existing,$START,$END,0,$RUN_ID,$RAW,$SUM,$LOG" >> "$STATUS"
    return 0
  fi
  extra=""
  if [ "$axis" = "ttc_threshold" ]; then
    extra="--override-ttc-threshold $value --sensitivity-axis ttc_threshold --sensitivity-value $value"
  elif [ "$axis" = "target_speed_kmh" ]; then
    extra="--override-target-speed-kmh $value --sensitivity-axis target_speed_kmh --sensitivity-value $value"
  fi
  /home/aaa/miniconda3/envs/sb3/bin/python scripts/evaluate_ijmlc_diagnostics.py \
    --manifest "$MANIFEST" --labels "$label" --seeds "$seed" \
    --densities 0.15 --test-start-seeds 10000 20000 --episodes-per-start 20 \
    --device cuda --run-id "$RUN_ID" $extra >> "$LOG" 2>&1
  code=$?
  END=$(date --iso-8601=seconds)
  status=done; if [ "$code" -ne 0 ]; then status=failed; fi
  echo "$label,$seed,$axis,$value,$status,$START,$END,$code,$RUN_ID,$RAW,$SUM,$LOG" >> "$STATUS"
  return "$code"
}
throttle() {
  while [ "$(jobs -rp | wc -l)" -ge "$MAX_PARALLEL" ]; do sleep 5; done
}
for label in guard_only shield_only gated_risk; do
  for seed in 0 1 2; do
    for value in 6 8 10 12; do throttle; run_one "$label" "$seed" ttc_threshold "$value" & done
    for value in 15 18 22; do throttle; run_one "$label" "$seed" target_speed_kmh "$value" & done
  done
done
wait
