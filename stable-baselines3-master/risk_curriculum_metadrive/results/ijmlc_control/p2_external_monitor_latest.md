# P2 External Baseline Monitor

time: 2026-07-01T17:35:42
run_group: ijmlc_p2_external_20260701_1733

## Resource
```
total        used        free      shared  buff/cache   available
内存：       31Gi        11Gi       7.6Gi       170Mi        12Gi        19Gi
交换：         0B          0B          0B
0, 1952, 9925, 14
```

## Watchdog
```
[2026-07-01T17:33:46] mem_available_gib=23.62 gpu_free_mib=10932
[2026-07-01T17:34:01] mem_available_gib=23.62 gpu_free_mib=10932
[2026-07-01T17:34:16] mem_available_gib=23.62 gpu_free_mib=10932
[2026-07-01T17:34:32] mem_available_gib=23.59 gpu_free_mib=10932
[2026-07-01T17:34:47] mem_available_gib=23.61 gpu_free_mib=10940
[2026-07-01T17:35:02] mem_available_gib=19.69 gpu_free_mib=9933
[2026-07-01T17:35:17] mem_available_gib=19.66 gpu_free_mib=9933
[2026-07-01T17:35:32] mem_available_gib=19.67 gpu_free_mib=9925
```

## Processes
```
173373 Ss         00:51 bash results/ijmlc_control/logs/ijmlc_p2_external_20260701_1733_rcpo_train_manager.sh
 173374 Ss         00:51 bash results/ijmlc_control/logs/ijmlc_p2_external_20260701_1733_rss_ttc_eval_manager.sh
 173378 S          00:51 bash results/ijmlc_control/logs/ijmlc_p2_external_20260701_1733_rss_ttc_eval_manager.sh
 173379 S          00:51 bash results/ijmlc_control/logs/ijmlc_p2_external_20260701_1733_rss_ttc_eval_manager.sh
 173381 S          00:51 bash results/ijmlc_control/logs/ijmlc_p2_external_20260701_1733_rss_ttc_eval_manager.sh
 173393 Rl         00:51 /home/aaa/miniconda3/envs/sb3/bin/python scripts/evaluate_ijmlc_diagnostics.py --manifest results/ijmlc_control/p2_external_baselines/p2_rss_ttc_filter_manifest.csv --labels rss_ttc_filter --seeds 0 --densities 0.08 0.15 0.20 0.25 --test-start-seeds 10000 20000 --episodes-per-start 20 --device cuda --run-id ijmlc_p2_external_20260701_1733_rss_ttc_s0 --action-filter rss_ttc
 173394 Rl         00:51 /home/aaa/miniconda3/envs/sb3/bin/python scripts/train.py --variant rcpo_lagrangian --algo ppo --seed 0 --timesteps 1000000 --n-envs 16 --device cuda --rcpo-cost-limit 0.25 --rcpo-lambda-init 20.0 --rcpo-lambda-lr 5.0 --rcpo-lambda-max 200.0 --rcpo-update-window 20 --output-dir outputs/ijmlc_p2_external_baselines/rcpo_lagrangian_1m_nenv16
 173395 Rl         00:51 /home/aaa/miniconda3/envs/sb3/bin/python scripts/evaluate_ijmlc_diagnostics.py --manifest results/ijmlc_control/p2_external_baselines/p2_rss_ttc_filter_manifest.csv --labels rss_ttc_filter --seeds 1 --densities 0.08 0.15 0.20 0.25 --test-start-seeds 10000 20000 --episodes-per-start 20 --device cuda --run-id ijmlc_p2_external_20260701_1733_rss_ttc_s1 --action-filter rss_ttc
 173396 Rl         00:51 /home/aaa/miniconda3/envs/sb3/bin/python scripts/evaluate_ijmlc_diagnostics.py --manifest results/ijmlc_control/p2_external_baselines/p2_rss_ttc_filter_manifest.csv --labels rss_ttc_filter --seeds 2 --densities 0.08 0.15 0.20 0.25 --test-start-seeds 10000 20000 --episodes-per-start 20 --device cuda --run-id ijmlc_p2_external_20260701_1733_rss_ttc_s2 --action-filter rss_ttc
 173495 S          00:49 /home/aaa/miniconda3/envs/sb3/bin/python scripts/train.py --variant rcpo_lagrangian --algo ppo --seed 0 --timesteps 1000000 --n-envs 16 --device cuda --rcpo-cost-limit 0.25 --rcpo-lambda-init 20.0 --rcpo-lambda-lr 5.0 --rcpo-lambda-max 200.0 --rcpo-update-window 20 --output-dir outputs/ijmlc_p2_external_baselines/rcpo_lagrangian_1m_nenv16
 173496 S          00:49 /home/aaa/miniconda3/envs/sb3/bin/python scripts/train.py --variant rcpo_lagrangian --algo ppo --seed 0 --timesteps 1000000 --n-envs 16 --device cuda --rcpo-cost-limit 0.25 --rcpo-lambda-init 20.0 --rcpo-lambda-lr 5.0 --rcpo-lambda-max 200.0 --rcpo-update-window 20 --output-dir outputs/ijmlc_p2_external_baselines/rcpo_lagrangian_1m_nenv16
 173497 S          00:49 /home/aaa/miniconda3/envs/sb3/bin/python scripts/train.py --variant rcpo_lagrangian --algo ppo --seed 0 --timesteps 1000000 --n-envs 16 --device cuda --rcpo-cost-limit 0.25 --rcpo-lambda-init 20.0 --rcpo-lambda-lr 5.0 --rcpo-lambda-max 200.0 --rcpo-update-window 20 --output-dir outputs/ijmlc_p2_external_baselines/rcpo_lagrangian_1m_nenv16
 173498 S          00:49 /home/aaa/miniconda3/envs/sb3/bin/python scripts/train.py --variant rcpo_lagrangian --algo ppo --seed 0 --timesteps 1000000 --n-envs 16 --device cuda --rcpo-cost-limit 0.25 --rcpo-lambda-init 20.0 --rcpo-lambda-lr 5.0 --rcpo-lambda-max 200.0 --rcpo-update-window 20 --output-dir outputs/ijmlc_p2_external_baselines/rcpo_lagrangian_1m_nenv16
 173499 S          00:49 /home/aaa/miniconda3/envs/sb3/bin/python scripts/train.py --variant rcpo_lagrangian --algo ppo --seed 0 --timesteps 1000000 --n-envs 16 --device cuda --rcpo-cost-limit 0.25 --rcpo-lambda-init 20.0 --rcpo-lambda-lr 5.0 --rcpo-lambda-max 200.0 --rcpo-update-window 20 --output-dir outputs/ijmlc_p2_external_baselines/rcpo_lagrangian_1m_nenv16
 173500 S          00:49 /home/aaa/miniconda3/envs/sb3/bin/python scripts/train.py --variant rcpo_lagrangian --algo ppo --seed 0 --timesteps 1000000 --n-envs 16 --device cuda --rcpo-cost-limit 0.25 --rcpo-lambda-init 20.0 --rcpo-lambda-lr 5.0 --rcpo-lambda-max 200.0 --rcpo-update-window 20 --output-dir outputs/ijmlc_p2_external_baselines/rcpo_lagrangian_1m_nenv16
 173501 S          00:49 /home/aaa/miniconda3/envs/sb3/bin/python scripts/train.py --variant rcpo_lagrangian --algo ppo --seed 0 --timesteps 1000000 --n-envs 16 --device cuda --rcpo-cost-limit 0.25 --rcpo-lambda-init 20.0 --rcpo-lambda-lr 5.0 --rcpo-lambda-max 200.0 --rcpo-update-window 20 --output-dir outputs/ijmlc_p2_external_baselines/rcpo_lagrangian_1m_nenv16
 173502 S          00:49 /home/aaa/miniconda3/envs/sb3/bin/python scripts/train.py --variant rcpo_lagrangian --algo ppo --seed 0 --timesteps 1000000 --n-envs 16 --device cuda --rcpo-cost-limit 0.25 --rcpo-lambda-init 20.0 --rcpo-lambda-lr 5.0 --rcpo-lambda-max 200.0 --rcpo-update-window 20 --output-dir outputs/ijmlc_p2_external_baselines/rcpo_lagrangian_1m_nenv16
 173503 S          00:49 /home/aaa/miniconda3/envs/sb3/bin/python scripts/train.py --variant rcpo_lagrangian --algo ppo --seed 0 --timesteps 1000000 --n-envs 16 --device cuda --rcpo-cost-limit 0.25 --rcpo-lambda-init 20.0 --rcpo-lambda-lr 5.0 --rcpo-lambda-max 200.0 --rcpo-update-window 20 --output-dir outputs/ijmlc_p2_external_baselines/rcpo_lagrangian_1m_nenv16
 173504 S          00:49 /home/aaa/miniconda3/envs/sb3/bin/python scripts/train.py --variant rcpo_lagrangian --algo ppo --seed 0 --timesteps 1000000 --n-envs 16 --device cuda --rcpo-cost-limit 0.25 --rcpo-lambda-init 20.0 --rcpo-lambda-lr 5.0 --rcpo-lambda-max 200.0 --rcpo-update-window 20 --output-dir outputs/ijmlc_p2_external_baselines/rcpo_lagrangian_1m_nenv16
 173505 S          00:49 /home/aaa/miniconda3/envs/sb3/bin/python scripts/train.py --variant rcpo_lagrangian --algo ppo --seed 0 --timesteps 1000000 --n-envs 16 --device cuda --rcpo-cost-limit 0.25 --rcpo-lambda-init 20.0 --rcpo-lambda-lr 5.0 --rcpo-lambda-max 200.0 --rcpo-update-window 20 --output-dir outputs/ijmlc_p2_external_baselines/rcpo_lagrangian_1m_nenv16
 173506 S          00:49 /home/aaa/miniconda3/envs/sb3/bin/python scripts/train.py --variant rcpo_lagrangian --algo ppo --seed 0 --timesteps 1000000 --n-envs 16 --device cuda --rcpo-cost-limit 0.25 --rcpo-lambda-init 20.0 --rcpo-lambda-lr 5.0 --rcpo-lambda-max 200.0 --rcpo-update-window 20 --output-dir outputs/ijmlc_p2_external_baselines/rcpo_lagrangian_1m_nenv16
 173507 S          00:49 /home/aaa/miniconda3/envs/sb3/bin/python scripts/train.py --variant rcpo_lagrangian --algo ppo --seed 0 --timesteps 1000000 --n-envs 16 --device cuda --rcpo-cost-limit 0.25 --rcpo-lambda-init 20.0 --rcpo-lambda-lr 5.0 --rcpo-lambda-max 200.0 --rcpo-update-window 20 --output-dir outputs/ijmlc_p2_external_baselines/rcpo_lagrangian_1m_nenv16
 173508 S          00:49 /home/aaa/miniconda3/envs/sb3/bin/python scripts/train.py --variant rcpo_lagrangian --algo ppo --seed 0 --timesteps 1000000 --n-envs 16 --device cuda --rcpo-cost-limit 0.25 --rcpo-lambda-init 20.0 --rcpo-lambda-lr 5.0 --rcpo-lambda-max 200.0 --rcpo-update-window 20 --output-dir outputs/ijmlc_p2_external_baselines/rcpo_lagrangian_1m_nenv16
 173509 S          00:49 /home/aaa/miniconda3/envs/sb3/bin/python scripts/train.py --variant rcpo_lagrangian --algo ppo --seed 0 --timesteps 1000000 --n-envs 16 --device cuda --rcpo-cost-limit 0.25 --rcpo-lambda-init 20.0 --rcpo-lambda-lr 5.0 --rcpo-lambda-max 200.0 --rcpo-update-window 20 --output-dir outputs/ijmlc_p2_external_baselines/rcpo_lagrangian_1m_nenv16
 173510 S          00:49 /home/aaa/miniconda3/envs/sb3/bin/python scripts/train.py --variant rcpo_lagrangian --algo ppo --seed 0 --timesteps 1000000 --n-envs 16 --device cuda --rcpo-cost-limit 0.25 --rcpo-lambda-init 20.0 --rcpo-lambda-lr 5.0 --rcpo-lambda-max 200.0 --rcpo-update-window 20 --output-dir outputs/ijmlc_p2_external_baselines/rcpo_lagrangian_1m_nenv16
 173626 Ss         00:11 bash results/ijmlc_control/logs/ijmlc_p2_external_20260701_1733_rcpo_post_eval_manager.sh
 173676 Ss         00:00 bash -c  cd /home/aaa/data/qj/stable-baselines3-master/risk_curriculum_metadrive RUN_GROUP=ijmlc_p2_external_20260701_1733 for f in results/ijmlc_control/logs/${RUN_GROUP}_rcpo_train_manager.pid results/ijmlc_control/logs/${RUN_GROUP}_rss_ttc_eval_manager.pid results/ijmlc_control/logs/${RUN_GROUP}_rcpo_post_eval_manager.pid results/ijmlc_control/logs/resource_watchdog.pid; do   echo "== $f =="   if [ -f "$f" ]; then pid=$(cat "$f"); ps -p "$pid" -o pid,stat,etime,cmd || true; else echo missing; fi done /home/aaa/miniconda3/envs/sb3/bin/python results/ijmlc_control/p2_external_baselines/monitor_p2_external.py >/dev/null sed -n "1,220p" results/ijmlc_control/p2_external_monitor_latest.md
```

## RCPO Training
- not started or status not written yet

## RSS/TTC Evaluation
- not started or status not written yet
