#!/usr/bin/env bash
set -u
cd /home/aaa/data/qj/stable-baselines3-master/risk_curriculum_metadrive
RUN_GROUP=ijmlc_p2_external_20260701_1733
MANIFEST=results/ijmlc_control/p2_external_baselines/p2_rss_ttc_filter_manifest.csv
STATUS=results/ijmlc_control/p2_external_baselines/rss_ttc_eval_status.csv
mkdir -p results/ijmlc_control/p2_external_baselines results/ijmlc_control/logs
echo "seed,status,start_time,end_time,exit_code,run_id,raw_csv,summary_csv,log_path" > "$STATUS"
for seed in 0 1 2; do
  (
    RUN_ID=${RUN_GROUP}_rss_ttc_s${seed}
    LOG=results/ijmlc_control/logs/${RUN_ID}.log
    RAW=results/ijmlc_control/raw_csv/${RUN_ID}_episodes.csv
    SUM=results/ijmlc_control/summary_tables/${RUN_ID}_summary.csv
    START=$(date --iso-8601=seconds)
    echo "[$START] start rss_ttc_filter seed=$seed" | tee -a "$LOG"
    if [ -f "$RAW" ] && [ -f "$SUM" ]; then
      END=$(date --iso-8601=seconds)
      echo "$seed,skipped_existing,$START,$END,0,$RUN_ID,$RAW,$SUM,$LOG" >> "$STATUS"
      exit 0
    fi
    /home/aaa/miniconda3/envs/sb3/bin/python scripts/evaluate_ijmlc_diagnostics.py \
      --manifest "$MANIFEST" --labels rss_ttc_filter --seeds "$seed" \
      --densities 0.08 0.15 0.20 0.25 --test-start-seeds 10000 20000 --episodes-per-start 20 \
      --device cuda --run-id "$RUN_ID" --action-filter rss_ttc >> "$LOG" 2>&1
    code=$?
    END=$(date --iso-8601=seconds)
    status=done
    if [ "$code" -ne 0 ]; then status=failed; fi
    echo "$seed,$status,$START,$END,$code,$RUN_ID,$RAW,$SUM,$LOG" >> "$STATUS"
  ) &
done
wait
