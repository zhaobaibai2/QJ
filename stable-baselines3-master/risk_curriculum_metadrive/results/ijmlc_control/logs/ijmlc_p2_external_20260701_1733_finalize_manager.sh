#!/usr/bin/env bash
set -u
cd /home/aaa/data/qj/stable-baselines3-master/risk_curriculum_metadrive
RUN_GROUP=ijmlc_p2_external_20260701_1733
STATUS=results/ijmlc_control/p2_external_baselines/p2_finalize_status.txt
echo "started $(date --iso-8601=seconds)" > "$STATUS"
for pidfile in results/ijmlc_control/logs/${RUN_GROUP}_rss_ttc_eval_manager.pid results/ijmlc_control/logs/${RUN_GROUP}_rcpo_post_eval_manager.pid; do
  while true; do
    if [ -f "$pidfile" ]; then
      pid=$(cat "$pidfile" 2>/dev/null || true)
      if [ -n "$pid" ] && ps -p "$pid" >/dev/null 2>&1; then sleep 60; continue; fi
    fi
    break
  done
done
/home/aaa/miniconda3/envs/sb3/bin/python results/ijmlc_control/scripts/build_p2_external_tables.py >> results/ijmlc_control/logs/${RUN_GROUP}_finalize_manager.out 2>&1
code=$?
echo "finished $(date --iso-8601=seconds) exit=$code" >> "$STATUS"
exit $code
