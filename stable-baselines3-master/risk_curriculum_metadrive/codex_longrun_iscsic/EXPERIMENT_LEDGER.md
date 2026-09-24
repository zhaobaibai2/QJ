
## tuning_lr1e4_prehard_nenv10_1p5m / proposed PPO seed1
- Status: stopped early at ~1.064M after demotion and degradation; final training not used as paper result.
- Checkpoint evaluation: checkpoint_750000_steps.zip, n_envs=10, 50 episodes per density, CSV outputs/tuning_lr1e4_prehard_nenv10_1p5m/checkpoint_evaluations/s1_750k/proposed_ppo_s1.csv.
- Metrics: d0.00 success 0.86 cost 0.00 route 0.980; d0.08 success 0.74 cost 0.12 route 0.927; d0.15 success 0.34 cost 0.62 route 0.713.
- Decision: low LR 1e-4 does not solve seed1 high-density instability; try intermediate LR 2e-4 rather than simply increasing total timesteps.

## tuning_lr2e4_prehard_nenv10_1p5m / proposed PPO seed1
- Status: stopped after checkpoint_1125000_steps.zip because hard stage was reached twice but not maintained.
- Checkpoint evaluation: checkpoint_1125000_steps.zip, n_envs=10, 50 episodes per density, CSV outputs/tuning_lr2e4_prehard_nenv10_1p5m/checkpoint_evaluations/s1_1125k/proposed_ppo_s1.csv.
- Metrics: d0.00 success 0.74 cost 0.00 route 0.973; d0.08 success 0.74 cost 0.10 route 0.939; d0.15 success 0.38 cost 0.52 route 0.767.
- Decision: 2e-4 is better than 1e-4 on high density but still worse than the old risk seed1 1M high-density result and does not solve hard-stage instability. Do not solve by blindly increasing steps.

## tuning_stage2strict035_prehard_nenv10_1p5m / proposed PPO seed1
- Status: stopped after checkpoint_1125000_steps.zip plus monitoring to ~1.239M because it stayed in stage3 and did not enter hard under stricter gates.
- Config: n_envs=10, ent_coef=0.01, learning_rate=3e-4, stage2_success=0.35, stage2_cost=0.35.
- Checkpoint evaluation: checkpoint_1125000_steps.zip, n_envs=10, 50 episodes/density, CSV outputs/tuning_stage2strict035_prehard_nenv10_1p5m/checkpoint_evaluations/s1_1125k/proposed_ppo_s1.csv.
- Metrics: d0.00 success 0.76 cost 0.00 route 0.976; d0.08 success 0.78 cost 0.04 route 0.974; d0.15 success 0.38 cost 0.52 route 0.732.
- Decision: strict stage2 gate improves d0.08 over lr2e-4 and default seed1, but high-density d0.15 remains weak. Gate tuning alone is insufficient; next direction should target defensive safety/high-density collisions.

## defensive_ttc12_v18_nenv10_final / seed26
- Status: completed train + evaluation + figures/report.
- Command: scripts/run_one_defensive_proposed.py --seed 26 --n-envs 10 --timesteps 1000000 --root outputs/defensive_ttc12_v18_nenv10_final --ttc-threshold 12.0 --target-speed 18.0 --device cuda.
- Config: n_envs=10, horizon=1500, ttc_threshold=12.0, target_speed_kmh=18.0, stage2_success=0.50, stage2_cost=0.25.
- CSV: outputs/defensive_ttc12_v18_nenv10_final/evaluations/defensive_proposed_ppo_s26.csv; eval_n_envs=10.
- Metrics: d0.00 success 0.98 cost 0.00 route 0.990; d0.08 success 0.88 cost 0.10 route 0.954; d0.15 success 0.60 cost 0.28 route 0.848.
- Decision: promising fixed defensive protocol; expand to another seed under same n_envs=10 protocol.

## defensive_ttc12_v18_nenv10_final / seed27
- Status: completed train + evaluation + figures/report.
- Command: scripts/run_one_defensive_proposed.py --seed 27 --n-envs 10 --timesteps 1000000 --root outputs/defensive_ttc12_v18_nenv10_final --ttc-threshold 12.0 --target-speed 18.0 --device cuda.
- Config: n_envs=10, horizon=1500, ttc_threshold=12.0, target_speed_kmh=18.0, stage2_success=0.50, stage2_cost=0.25.
- CSV: outputs/defensive_ttc12_v18_nenv10_final/evaluations/defensive_proposed_ppo_s27.csv; eval_n_envs=10.
- Two-seed summary after seed26/27: d0.00 success 0.96, d0.08 success 0.87, d0.15 success 0.60; d0.15 cost/collision about 0.29.
- Decision: strong reproducibility across two seeds; launch seed28 to reach the required 3-seed defensive fixed-protocol minimum.

## defensive_ttc12_v18_nenv10_final / seed28
- Status: completed train+eval+figures/report.
- Command: scripts/run_one_defensive_proposed.py --seed 28 --n-envs 10 --timesteps 1000000 --root outputs/defensive_ttc12_v18_nenv10_final --ttc-threshold 12.0 --target-speed 18.0 --device cuda.
- Config: n_envs=10, horizon=1500, ttc_threshold=12.0, target_speed_kmh=18.0, lr=3e-4, stages warmup/easy/medium/prehard/hard.
- CSV: outputs/defensive_ttc12_v18_nenv10_final/evaluations/defensive_proposed_ppo_s28.csv; eval_n_envs=10; 150 episodes.
- Results: d0.00 success=0.98 cost=0.00 route=0.989 collision=0.00; d0.08 success=0.88 cost=0.10 route=0.954 collision=0.08; d0.15 success=0.72 cost=0.20 route=0.885 collision=0.20.
- Three-seed fixed-protocol summary (s26/s27/s28): d0.00 success=0.967+-0.023 cost=0.000 route=0.989; d0.08 success=0.873+-0.012 cost=0.087+-0.023 route=0.958+-0.007; d0.15 success=0.640+-0.069 cost=0.260+-0.053 route=0.852+-0.031.
- Convergence interpretation: longer training may help high-density robustness because seed28 improves to 0.72 at d0.15, but training logs still finish at stage2 with low rollout success/window_success, so this is not a clean monotonic convergence case. Need a controlled longer-step diagnostic before scaling all final runs.

## defensive_ttc12_v18_nenv10_steps_diag_1p5m / seed28
- Status: completed train+eval+figures/report; diagnostic only, not final benchmark.
- Purpose: test whether increasing timesteps from 1M to 1.5M improves the fixed defensive protocol.
- Command: scripts/run_one_defensive_proposed.py --seed 28 --n-envs 10 --timesteps 1500000 --root outputs/defensive_ttc12_v18_nenv10_steps_diag_1p5m --ttc-threshold 12.0 --target-speed 18.0 --device cuda.
- Config: n_envs=10, horizon=1500, ttc_threshold=12.0, target_speed_kmh=18.0, lr=3e-4, stage2_success=0.5, stage2_cost=0.25.
- CSV: outputs/defensive_ttc12_v18_nenv10_steps_diag_1p5m/evaluations/defensive_proposed_ppo_s28.csv; eval_n_envs=10; 150 episodes.
- Results: d0.00 success=0.96 cost=0.00 route=0.991 collision=0.00; d0.08 success=0.78 cost=0.16 route=0.911 collision=0.08; d0.15 success=0.58 cost=0.36 route=0.825 collision=0.32.
- Comparison to same seed 1M: worsened at d0.08 (0.88 -> 0.78 success) and d0.15 (0.72 -> 0.58 success; cost 0.20 -> 0.36). Conclusion: do not adopt blind longer training; investigate checkpoint selection/early stopping or curriculum tuning.

## tuning_ttc14_v18_nenv10_500k / seed28
- Status: completed train+eval; screening failed, do not expand.
- Command: scripts/run_one_defensive_proposed.py --seed 28 --n-envs 10 --timesteps 500000 --root outputs/tuning_ttc14_v18_nenv10_500k --ttc-threshold 14.0 --target-speed 18.0 --device cuda.
- CSV: outputs/tuning_ttc14_v18_nenv10_500k/evaluations/defensive_proposed_ppo_s28.csv; eval_n_envs=10; 150 episodes.
- Results: d0.00 success=1.00 cost=0.00 route=0.991; d0.08 success=0.78 cost=0.20 route=0.888 collision=0.20; d0.15 success=0.48 cost=0.32 route=0.829 collision=0.32.
- Interpretation: higher TTC threshold alone was too conservative/unstable and worsened both d0.08 and d0.15 versus ttc12/v18 seed28.

## tuning_ttc12_v16_nenv10_500k / seed28
- Status: completed train+eval; screening failed, do not expand.
- Command: scripts/run_one_defensive_proposed.py --seed 28 --n-envs 10 --timesteps 500000 --root outputs/tuning_ttc12_v16_nenv10_500k --ttc-threshold 12.0 --target-speed 16.0 --device cuda.
- CSV: outputs/tuning_ttc12_v16_nenv10_500k/evaluations/defensive_proposed_ppo_s28.csv; eval_n_envs=10; 150 episodes.
- Results: d0.00 success=0.84 cost=0.00 route=0.975; d0.08 success=0.76 cost=0.08 route=0.944 collision=0.08; d0.15 success=0.52 cost=0.22 route=0.857 collision=0.22.
- Interpretation: lower target speed reduces speed and keeps collision moderate, but success drops too much versus ttc12/v18.

## iscsic_main_nenv10_1p5m_ent001 / baseline seed1
- Status: completed train+eval.
- Command: scripts/train.py --variant baseline --algo ppo --seed 1 --timesteps 1500000 --horizon 1200 --n-envs 10 --ent-coef 0.01 --device cuda --output-dir outputs/iscsic_main_nenv10_1p5m_ent001/runs; then evaluate_from_config episodes=50 densities=0.00/0.08/0.15 n_envs=10.
- Config: outputs/iscsic_main_nenv10_1p5m_ent001/runs/baseline_ppo_s1/config.json.
- Model: outputs/iscsic_main_nenv10_1p5m_ent001/runs/baseline_ppo_s1/model/final_model.zip.
- CSV: outputs/iscsic_main_nenv10_1p5m_ent001/evaluations/baseline_ppo_s1.csv; eval_n_envs=10; 150 episodes.
- Results: d0.00 success=0.00 cost=1.00 route=0.327 collision=0.00 out=1.00; d0.08 success=0.00 cost=1.00 route=0.223 collision=0.50 out=0.50; d0.15 success=0.00 cost=1.00 route=0.213 collision=0.68 out=0.32.
- Interpretation: baseline learned high-speed unsafe behavior and fails all held-out evaluations. Preserve as main comparator, not a failed run.

## iscsic_main_nenv10_1p5m_ent001 / baseline seed2
- Status: completed train+eval.
- Command: scripts/train.py --variant baseline --algo ppo --seed 2 --timesteps 1500000 --horizon 1200 --n-envs 10 --ent-coef 0.01 --device cuda --output-dir outputs/iscsic_main_nenv10_1p5m_ent001/runs; then evaluate_from_config episodes=50 densities=0.00/0.08/0.15 n_envs=10.
- Config: outputs/iscsic_main_nenv10_1p5m_ent001/runs/baseline_ppo_s2/config.json.
- Model: outputs/iscsic_main_nenv10_1p5m_ent001/runs/baseline_ppo_s2/model/final_model.zip.
- CSV: outputs/iscsic_main_nenv10_1p5m_ent001/evaluations/baseline_ppo_s2.csv; eval_n_envs=10; 150 episodes.
- Results: d0.00 success=0.00 cost=1.00 route=0.345 collision=0.00 out=1.00; d0.08 success=0.14 cost=0.86 route=0.410 collision=0.30 out=0.56; d0.15 success=0.04 cost=0.96 route=0.360 collision=0.58 out=0.38.
- Interpretation: baseline seed2 has slight held-out success at nonzero densities but remains very unsafe/high-cost. Preserve as main comparator.

## iscsic_main_nenv10_1p5m_ent001 / current CSV audit snapshot
- Existing current-protocol evaluation CSVs: baseline_ppo_s1.csv, baseline_ppo_s2.csv, proposed_ppo_s0.csv, proposed_ppo_s1.csv; all eval_n_envs=10, 50 episodes per density.
- Proposed seed0: d0.00 success=0.820 cost=0.000 route=0.978; d0.08 success=0.760 cost=0.120 route=0.929; d0.15 success=0.600 cost=0.340 route=0.856.
- Proposed seed1: d0.00 success=0.880 cost=0.000 route=0.984; d0.08 success=0.760 cost=0.100 route=0.917; d0.15 success=0.320 cost=0.620 route=0.703.
- Baseline seed1/2 are recorded above and remain high-cost unsafe comparators.
- Note: proposed seed-level high-density variance is large; final reporting must keep seed-level table or mean/std and cannot claim only the best seed.

## iscsic_main_nenv10_1p5m_ent001 / curriculum seed1
- Status: completed train+eval.
- Command: scripts/train.py --variant curriculum --algo ppo --seed 1 --timesteps 1500000 --horizon 1200 --n-envs 10 --ent-coef 0.01 --device cuda --output-dir outputs/iscsic_main_nenv10_1p5m_ent001/runs; then evaluate_from_config episodes=50 densities=0.00/0.08/0.15 n_envs=10.
- Config: outputs/iscsic_main_nenv10_1p5m_ent001/runs/curriculum_ppo_s1/config.json.
- Model: outputs/iscsic_main_nenv10_1p5m_ent001/runs/curriculum_ppo_s1/model/final_model.zip.
- CSV: outputs/iscsic_main_nenv10_1p5m_ent001/evaluations/curriculum_ppo_s1.csv; eval_n_envs=10; 150 episodes.
- Results: d0.00 success=0.02 cost=0.98 route=0.323 collision=0.00 out=0.98; d0.08 success=0.00 cost=1.00 route=0.247 collision=0.40 out=0.60; d0.15 success=0.00 cost=1.00 route=0.225 collision=0.52 out=0.48.
- Interpretation: curriculum-only is a weak comparator under the current candidate protocol; it reached stage3 late but failed held-out evaluation with high out-of-road/collision cost.

## iscsic_main_nenv10_1p5m_ent001 / risk seed1
- Status: completed train+eval.
- Command: scripts/train.py --variant risk --algo ppo --seed 1 --timesteps 1500000 --horizon 1200 --n-envs 10 --ent-coef 0.01 --device cuda --output-dir outputs/iscsic_main_nenv10_1p5m_ent001/runs; then evaluate_from_config episodes=50 densities=0.00/0.08/0.15 n_envs=10.
- Config: outputs/iscsic_main_nenv10_1p5m_ent001/runs/risk_ppo_s1/config.json.
- Model: outputs/iscsic_main_nenv10_1p5m_ent001/runs/risk_ppo_s1/model/final_model.zip.
- CSV: outputs/iscsic_main_nenv10_1p5m_ent001/evaluations/risk_ppo_s1.csv; eval_n_envs=10; 150 episodes.
- Results: d0.00 success=0.90 cost=0.00 route=0.983 collision=0.00 out=0.00; d0.08 success=0.70 cost=0.14 route=0.911 collision=0.12 out=0.02; d0.15 success=0.40 cost=0.52 route=0.741 collision=0.50 out=0.02.
- Shield/intervention: shield_intervention_rate=0.867/0.850/0.725 at d0.00/d0.08/d0.15; overspeed_guard_rate=0.867/0.843/0.675.
- Interpretation: risk reward+guard is strong at low/medium density but still collision-limited under d0.15; useful as main comparator and seed-level claim boundary.

## iscsic_main_nenv10_1p5m_ent001 / risk seed2
- Status: completed train+eval.
- Command: scripts/train.py --variant risk --algo ppo --seed 2 --timesteps 1500000 --horizon 1200 --n-envs 10 --ent-coef 0.01 --device cuda --output-dir outputs/iscsic_main_nenv10_1p5m_ent001/runs; then evaluate_from_config episodes=50 densities=0.00/0.08/0.15 n_envs=10.
- Config: outputs/iscsic_main_nenv10_1p5m_ent001/runs/risk_ppo_s2/config.json.
- Model: outputs/iscsic_main_nenv10_1p5m_ent001/runs/risk_ppo_s2/model/final_model.zip.
- CSV: outputs/iscsic_main_nenv10_1p5m_ent001/evaluations/risk_ppo_s2.csv; eval_n_envs=10; 150 episodes.
- Results: d0.00 success=0.90 cost=0.00 route=0.985 collision=0.00 out=0.00; d0.08 success=0.74 cost=0.14 route=0.936 collision=0.14 out=0.00; d0.15 success=0.46 cost=0.52 route=0.808 collision=0.52 out=0.00.
- Shield/intervention: shield_intervention_rate=0.866/0.859/0.762 at d0.00/d0.08/d0.15; overspeed_guard_rate=0.866/0.856/0.726.
- Interpretation: risk seed2 closely matches seed1, confirming stable low/medium-density performance and persistent high-density collision limitation.

## 2026-06-30 P0 main proposed seed2 complete
- Protocol: variant=proposed, algo=PPO, seed=2, timesteps=1,500,000, horizon=1200, n_envs=10, ent_coef=0.01, eval_n_envs=10, episodes=50 per density.
- Output: outputs/iscsic_main_nenv10_1p5m_ent001/evaluations/proposed_ppo_s2.csv
- d0.00: success=0.76, cost=0.00, route=0.967, collision=0.00, out=0.00, shield=0.865
- d0.08: success=0.70, cost=0.14, route=0.927, collision=0.14, out=0.00, shield=0.847
- d0.15: success=0.54, cost=0.40, route=0.755, collision=0.40, out=0.00, shield=0.756
- Interpretation: proposed beats risk on high-density success for this seed, but still has substantial collision/cost and seed variance; continue reward tuning.

## 2026-06-30 P0 main curriculum seed2 complete
- Protocol: variant=curriculum, algo=PPO, seed=2, timesteps=1,500,000, horizon=1200, n_envs=10, ent_coef=0.01, eval_n_envs=10, episodes=50 per density.
- Output: outputs/iscsic_main_nenv10_1p5m_ent001/evaluations/curriculum_ppo_s2.csv
- d0.00: success=0.02, cost=0.98, route=0.399, collision=0.00, out=0.98, shield=0.000
- d0.08: success=0.00, cost=1.00, route=0.252, collision=0.48, out=0.52, shield=0.000
- d0.15: success=0.02, cost=0.98, route=0.250, collision=0.62, out=0.36, shield=0.000
- Interpretation: confirms curriculum-only failure and supports need for risk reward/action guard.


## 2026-06-30 launched nenv8 defensive ttc12/v18 seed26
- Time: 2026-06-30T14:00:53+08:00
- Protocol: scripts/run_one_defensive_proposed.py --seed 26 --n-envs 8 --timesteps 1000000 --root outputs/defensive_ttc12_v18_nenv8_final --ttc-threshold 12.0 --target-speed 18.0 --device cuda.
- Purpose: first 8-env migration check for the strongest current self-method branch; compare with existing nenv10 seed26 result before scaling to seed27/28 or changing parameters.
- Log: outputs/defensive_ttc12_v18_nenv8_final/logs/defensive_s26_nenv8_20260630_140018.log
- PID: 7802; PGID: 7795.
- Initial health: process and 8 VecEnv workers are running; early log shows n_envs=8 and fps around 2500-2700.

## 2026-06-30 nenv8 defensive seed26 monitor at ~319k
- Time: 2026-06-30T14:03:04+08:00
- Checkpoint: checkpoint_250000_steps.zip exists.
- Health: process still running with 8 workers; GPU memory about 922 MiB, fps about 2220-2245.
- Training signal: reached stage1 by ~311k; latest success_rate about 0.07, route_completion sample up to 0.865, std about 0.68, no collision/out-of-road in sampled tail.
- Decision: continue; not an idle-collapse run. Recheck around 500k.

## 2026-06-30 nenv8 defensive seed26 monitor at ~459k
- Time: 2026-06-30T14:05:05+08:00
- Health: process still running with 8 workers; GPU memory about 922 MiB, fps recently 1729-1915.
- Training signal: reached stage2; success_rate peaked around 0.44 near 401k and later fluctuated around 0.16-0.26; route_completion has high samples around 0.96-0.98.
- Risk signal: one sampled out_of_road at ~442k and window_cost rose to about 0.30, so the run is learning but unstable.
- Decision: continue to 500k/750k; no intervention yet because this is not idle collapse and still has route/success learning.

## 2026-06-30 nenv8 defensive seed26 monitor at ~614k
- Time: 2026-06-30T14:07:45+08:00
- Checkpoint: checkpoint_500000_steps.zip exists.
- Health: process still running with 8 workers; GPU memory about 922 MiB; fps recently about 1466-1555.
- Training signal: stage2, success_rate about 0.27, window_success around 0.20-0.37, window_route_completion around 0.80-0.85.
- Risk signal: one sampled collision near ~598k, but window_cost stayed low around 0.07-0.10 afterward.
- Decision: continue to final; do not interrupt because there is meaningful learning and no collapse.

## 2026-06-30 nenv8 defensive seed26 monitor at ~786k
- Time: 2026-06-30T14:12:58+08:00
- Checkpoint: checkpoint_750000_steps.zip exists.
- Health: process still running with 8 workers; GPU memory about 896 MiB; fps recently about 1285-1367.
- Training signal: still stage2; success_rate roughly 0.14-0.19 in latest tail, window_success about 0.10-0.27, route_completion has high samples near 0.99 but instability remains.
- Risk signal: recent sampled collision/out_of_road events exist; std down to about 0.44 but not a full idle collapse.
- Decision: let seed26 finish and judge by final 3-density evaluation, because the earlier nenv10 defensive protocol also had imperfect training-stage logs but strong held-out eval.


## 2026-06-30 launched nenv8 defensive ttc12/v18 seed27
- Time: 2026-06-30T14:21:39+08:00
- Protocol: scripts/run_one_defensive_proposed.py --seed 27 --n-envs 8 --timesteps 1000000 --root outputs/defensive_ttc12_v18_nenv8_final --ttc-threshold 12.0 --target-speed 18.0 --device cuda.
- Rationale: seed26 nenv8 is usable (d0.15 success=0.60/cost=0.24) but d0.08 dropped versus nenv10; seed27 tests whether that is seed/noise or protocol degradation before tuning.
- Log: outputs/defensive_ttc12_v18_nenv8_final/logs/defensive_s27_nenv8_20260630_142139.log
- Launcher PID: 10678; main PID: 10685; PGID: 10678.


## 2026-06-30 protocol change to nenv16
- Time: 2026-06-30T14:24:15+08:00
- User requirement: switch experiments to n_envs=16; keep at least 4GB CPU memory and 2GB GPU memory free.
- Action: stopped the in-progress seed27 nenv8 run and archived partial artifacts under outputs/interrupted_nenv8_protocol_change_to_nenv16_20260630_142415.
- Stopped PGID: 10678.
- Note: completed nenv8 seed26 remains diagnostic only; new formal runs use nenv16 directories and TARGET_N_ENVS=16 summaries.


## 2026-06-30 launched nenv16 defensive ttc12/v18 seed26
- Time: 2026-06-30T14:25:31+08:00
- Protocol: scripts/run_one_defensive_proposed.py --seed 26 --n-envs 16 --timesteps 1000000 --root outputs/defensive_ttc12_v18_nenv16_final --ttc-threshold 12.0 --target-speed 18.0 --device cuda.
- Safety requirement: keep at least 4GB available CPU memory and 2GB free GPU memory.
- Rationale: first nenv16 migration check on strongest current self-method branch; compare with nenv8/nenv10 seed26 before expanding seeds.
- Log: outputs/defensive_ttc12_v18_nenv16_final/logs/defensive_s26_nenv16_20260630_142531.log
- Launcher PID: 11385; main PID: 11392; PGID: 11385.

## 2026-06-30 nenv16 defensive seed26 monitor at ~393k
- Time: 2026-06-30T14:29:12+08:00
- Safety: CPU available about 24GiB; GPU free about 10.9GiB, above the required 4GB CPU / 2GB GPU headroom.
- Checkpoint: checkpoint_250000_steps.zip exists.
- Training signal: reached stage2 by ~311k; success_rate peaked around 0.41 near 295k and is about 0.19 at 393k; window_success about 0.30, window_cost about 0.067, route_completion samples near 0.98.
- Decision: continue. nenv16 is currently safe and learning faster than the interrupted nenv8 seed27 and comparable/better than nenv8 seed26 early curve.

## 2026-06-30 nenv16 defensive seed26 monitor at ~524k
- Time: 2026-06-30T14:31:18+08:00
- Safety: CPU available about 23GiB; GPU free about 10.9GiB, above the required 4GB CPU / 2GB GPU headroom.
- Checkpoint: checkpoint_500000_steps.zip exists.
- Training signal: still stage2; route window about 0.75, latest cost window 0, std about 0.63. Success rate dropped from the earlier 0.35-0.41 peak to about 0.06-0.10.
- Decision: continue to 750k/final. Not an idle collapse because route progress remains high, cost is controlled, and exploration std has not collapsed.

## 2026-06-30 nenv16 defensive seed26 monitor at ~721k
- Time: 2026-06-30T14:34:03+08:00
- Safety: CPU available about 23GiB; GPU free about 10.9GiB, above the required 4GB CPU / 2GB GPU headroom.
- Training signal: still stage2; after a mid-run dip, latest success_rate recovered to about 0.19-0.20, window_success about 0.20-0.23, window_cost about 0.10-0.17, route window about 0.75-0.82.
- Decision: continue to final evaluation; no resource or collapse reason to stop.

## 2026-06-30 nenv16 defensive seed26 completed
- Time: 2026-06-30T14:42:35+08:00
- Evaluation CSV: outputs/defensive_ttc12_v18_nenv16_final/evaluations/defensive_proposed_ppo_s26.csv; eval_n_envs=16; 50 episodes per density.
- d0.00: success=0.92, cost=0.00, collision=0.00, route=0.990.
- d0.08: success=0.86, cost=0.08, collision=0.08, route=0.946.
- d0.15: success=0.66, cost=0.10, collision=0.10, route=0.930.
- Comparison: nenv16 improves high-density over nenv8 seed26 (0.60/0.24 cost) and nenv10 seed26 (0.60/0.28 cost), while staying near nenv10 at d0.08.
- Decision: adopt nenv16 as the current formal protocol and expand to seed27 before any new reward/defensive parameter tuning.


## 2026-06-30 launched nenv16 defensive ttc12/v18 seed27
- Time: 2026-06-30T14:42:40+08:00
- Protocol: scripts/run_one_defensive_proposed.py --seed 27 --n-envs 16 --timesteps 1000000 --root outputs/defensive_ttc12_v18_nenv16_final --ttc-threshold 12.0 --target-speed 18.0 --device cuda.
- Purpose: confirm the strong seed26 nenv16 result is reproducible before expanding to seed28 or tuning.
- Log: outputs/defensive_ttc12_v18_nenv16_final/logs/defensive_s27_nenv16_20260630_144235.log
- Launcher PID: 13808; main PID: 13815; PGID: 13808.


## 2026-06-30 protocol change to nenv32
- Time: 2026-06-30T14:44:48+08:00
- User requirement: try n_envs=32 because CPU/GPU memory are still largely free; keep at least 4GB available CPU memory and 2GB free GPU memory.
- Action: stopped the in-progress nenv16 seed27 run and archived partial artifacts under outputs/interrupted_nenv16_protocol_change_to_nenv32_20260630_144448.
- Stopped PGID: 13808.
- Note: completed nenv16 seed26 remains valid comparison evidence; new formal runs use nenv32 directories and TARGET_N_ENVS=32 summaries.


## 2026-06-30 launched nenv32 defensive ttc12/v18 seed26
- Time: 2026-06-30T14:45:56+08:00
- Protocol: scripts/run_one_defensive_proposed.py --seed 26 --n-envs 32 --timesteps 1000000 --root outputs/defensive_ttc12_v18_nenv32_final --ttc-threshold 12.0 --target-speed 18.0 --device cuda.
- Safety requirement: keep at least 4GB available CPU memory and 2GB free GPU memory.
- Purpose: test whether nenv32 improves throughput/results beyond the strong completed nenv16 seed26 result.
- Log: outputs/defensive_ttc12_v18_nenv32_final/logs/defensive_s26_nenv32_20260630_144548.log
- Launcher PID: 14217; main PID: 14224; PGID: 14217.

## 2026-06-30 nenv32 defensive seed26 monitor at ~393k
- Time: 2026-06-30T14:48:05+08:00
- Safety: CPU available about 24GiB; GPU free about 10.9GiB, above the required 4GB CPU / 2GB GPU headroom.
- Throughput: fps about 3600-4000, clearly faster than nenv16/nenv8.
- Checkpoint: checkpoint_249984_steps.zip exists.
- Training signal: still stage0 at ~393k; route window about 0.50, cost window 0, std about 0.88, success_rate 0.
- Decision: continue to 500k/750k. nenv32 is resource-safe and fast, but learning speed is not yet clearly better than nenv16, so final eval will decide protocol adoption.

## 2026-06-30 nenv32 defensive seed26 monitor at ~655k
- Time: 2026-06-30T14:50:07+08:00
- Safety: CPU available about 23GiB; GPU free about 10.95GiB, above the required 4GB CPU / 2GB GPU headroom.
- Throughput: fps about 2800-3100 in mid-run, still faster than nenv16.
- Checkpoints: checkpoint_249984_steps.zip and checkpoint_499968_steps.zip exist; non-round names are expected from callback frequency with 32 envs.
- Training signal: after slow stage0 start, reached stage2; success_rate peaked around 0.54 and latest stage2 has window_success about 0.30, window_cost about 0.033, route window about 0.836.
- Decision: continue to final evaluation; nenv32 is both safe and promising enough to finish.

## 2026-06-30 nenv32 defensive seed26 monitor at ~918k
- Time: 2026-06-30T14:53:37+08:00
- Safety: CPU available about 22GiB; GPU free about 10.95GiB, above the required 4GB CPU / 2GB GPU headroom.
- Throughput: nenv32 is faster than nenv16 early/mid-run; fps peaked around 3600-4000 and later dropped to about 2000-2200 as episodes became longer/harder.
- Training signal: reached stage3 multiple times; success_rate peaked around 0.68 at ~852k and later fluctuated to about 0.31 at ~918k; latest std about 0.59.
- Decision: continue to final evaluation. nenv32 is fast and resource-safe; final held-out metrics will decide whether it replaces nenv16.

## 2026-06-30 nenv32 defensive seed26 completed and rejected as final protocol
- Time: 2026-06-30T14:59:07+08:00
- Evaluation CSV: outputs/defensive_ttc12_v18_nenv32_final/evaluations/defensive_proposed_ppo_s26.csv; eval_n_envs=32; 50 episodes per density.
- nenv32 results: d0.00 success=1.00 cost=0.00 route=0.991; d0.08 success=0.78 cost=0.18 route=0.914; d0.15 success=0.54 cost=0.24 route=0.854.
- Same-seed comparison: nenv16 seed26 had d0.08 success=0.86 cost=0.08 and d0.15 success=0.66 cost=0.10.
- Interpretation: nenv32 is faster (about 3600-4000 fps early) and resource-safe, but degrades held-out medium/high-density success and safety.
- Decision: keep nenv32 as a throughput diagnostic only; restore formal default protocol to nenv16 and continue seed expansion there.


## 2026-06-30 relaunched nenv16 defensive ttc12/v18 seed27 after nenv32 diagnostic
- Time: 2026-06-30T14:59:49+08:00
- Protocol: scripts/run_one_defensive_proposed.py --seed 27 --n-envs 16 --timesteps 1000000 --root outputs/defensive_ttc12_v18_nenv16_final --ttc-threshold 12.0 --target-speed 18.0 --device cuda.
- Purpose: expand the best current formal protocol after nenv32 proved faster but worse on held-out metrics.
- Log: outputs/defensive_ttc12_v18_nenv16_final/logs/defensive_s27_nenv16_20260630_145943.log
- Launcher PID: 15496; main PID: 15503; PGID: 15496.

## 2026-06-30 created experiment master plan and nenv16 runner
- Time: 2026-06-30T15:26:00+08:00
- User requirement: after the current run, plan and execute all paper experiments deeply, including other innovations, ablations, comparisons, and per-run parameter/result review.
- Created: codex_longrun_iscsic/EXPERIMENT_MASTER_PLAN_20260630.md.
- Created: codex_longrun_iscsic/run_formal_variant_nenv16.sh.
- Created inventory: codex_longrun_iscsic/RESULT_INVENTORY_20260630.tsv with historical CSV status.
- Formal resource rule: keep CPU available >=4GB and GPU free >=2GB.
- Formal protocol for new runs: train/eval n_envs=16, densities 0.00/0.08/0.15, 50 eval episodes.
- Immediate decision: do not start new baseline/ablation training until defensive seed28 finishes; then evaluate whether Branch A freezes or needs targeted tuning before launching Branch B/C.

## 2026-06-30 nenv16 defensive seeds26-28 completed, gate failed
- Time: 2026-06-30T15:34:00+08:00
- Protocol: defensive ttc12/v18, n_envs=16, timesteps=1M, horizon=1500, eval_n_envs=16, 50 episodes per density.
- Seed26: d0.15 success=0.66 cost=0.10 collision=0.10 route=0.930.
- Seed27: d0.15 success=0.56 cost=0.34 collision=0.34 route=0.815.
- Seed28: d0.15 success=0.48 cost=0.38 collision=0.38 route=0.751.
- Three-seed mean: d0.00 success=0.960 cost=0.000 route=0.990; d0.08 success=0.873 cost=0.080 route=0.950; d0.15 success=0.567 cost=0.273 route=0.832.
- Decision: Branch A does not pass freeze gate (d0.15 success <0.60 and cost >0.25). Treat ttc12/v18 as diagnostic/current baseline, not final main result.
- Next action: targeted tuning T1, same seed28/n_envs16/1M/horizon1500, ttc_threshold=14.0, target_speed=18.0. Goal: reduce d0.15 cost while preserving d0.08 success/cost.

## 2026-06-30 user clarified retain nenv16 formal protocol
- Time: 2026-06-30T15:53:00+08:00
- Clarification: user questioned switching to 8 because previous empirical tests had moved to 16.
- Current state: defaults remain n_envs=16; no files were changed to 8.
- Decision: keep n_envs=16 as formal protocol. n_envs=8 is not adopted unless the user explicitly re-requests it despite the quality tradeoff.
- T1 result: ttc14/v18 seed28 improved high-density from ttc12/v18 seed28 d0.15 success=0.48/cost=0.38 to success=0.66/cost=0.20; d0.08 changed from success=0.88/cost=0.08 to success=0.86/cost=0.12.
- Decision: T1 passes single-seed screen and should be expanded to weak-seed validation, starting with seed27.

## 2026-06-30 ttc14/v18 nenv16 weak-seed validation status
- Time: 2026-06-30T16:09:19
- Protocol: scripts/run_one_defensive_proposed.py, n_envs=16, timesteps=1M, horizon=1500, ttc_threshold=14.0, target_speed=18.0, eval_n_envs=16.
- Seed27: d0.08 success=0.86 cost=0.06; d0.15 success=0.44 cost=0.38 collision=0.32 route=0.777.
- Seed28: d0.08 success=0.86 cost=0.12; d0.15 success=0.66 cost=0.20 collision=0.20 route=0.897.
- Current 2-seed mean d0.08: success=0.860, cost=0.090.
- Current 2-seed mean d0.15: success=0.550, cost=0.290.
- Decision: seed27 reduces high-density cost but does not improve success; seed28 improves both. Need seed26 before freezing or rejecting ttc14/v18, because two-seed mean is too narrow for paper-facing claim.
- Launched seed26 ttc14/v18 nenv16 at 2026-06-30 16:08 CST; log under outputs/defensive_ttc14_v18_nenv16_tuning/logs/launcher_s26_ttc14_v18_20260630_160822.out.

## 2026-06-30 correction on ttc14/v18 seed27 interpretation
- Time: 2026-06-30T16:09:40
- Correction: the earlier summary row with seed=27.5 was the aggregate over seed27 and seed28, not seed27 alone.
- Actual seed27 ttc14/v18: d0.08 success=0.86 cost=0.06; d0.15 success=0.44 cost=0.38 collision=0.32 route=0.777.
- Compared with ttc12/v18 seed27 (d0.15 success=0.56 cost=0.34), ttc14/v18 worsens this weak seed. Seed28 improved, so the tuning is unstable rather than ready to freeze.
- Decision: keep the already launched seed26 run only to complete evidence. Do not freeze ttc14/v18 unless the three-seed mean clearly passes and the weak-seed failure can be explained. If not, next tuning should target robustness instead of only raising TTC threshold.

## 2026-06-30 ttc14/v18 seed26 monitor at ~393k
- Time: 2026-06-30T16:12:01
- Health: process alive with 16 workers; GPU free about 10.9GB and CPU available about 23GB, above safety headroom.
- Checkpoint: checkpoint_250000_steps.zip exists.
- Training signal: stage1, total_timesteps about 393k, success_rate recently about 0.22-0.32, window_route_completion about 0.626, window_cost back to 0, std about 0.709.
- Decision: continue to 500k/750k. This is not idle collapse; still need final held-out d0.08/d0.15 before deciding whether ttc14/v18 is viable.

## 2026-06-30 ttc14/v18 seed26 monitor at ~622k
- Time: 2026-06-30T16:14:57
- Health: still alive with 16 workers; GPU free about 10.9GB.
- Checkpoint: checkpoint_500000_steps.zip exists.
- Training signal: reached stage2 by ~622k. Recent success_rate about 0.27; window_success about 0.433; window_route_completion about 0.754.
- Risk signal: window_cost about 0.30 and one sampled out_of_road episode appeared. This is not a crash/idle-collapse run, but ttc14/v18 is showing instability.
- Decision: continue to 750k/final evaluation; do not freeze ttc14/v18 from training curves alone. Final held-out d0.15 will decide.

## 2026-06-30 ttc14/v18 seed26 monitor at ~885k
- Time: 2026-06-30T16:18:55
- Checkpoint: checkpoint_750000_steps.zip exists.
- Training signal: around 835k-885k, stage2 briefly appeared but then demoted to stage1; recent success_rate about 0.05-0.11, route samples vary from 0.56 to 0.95.
- Risk signal: window_cost reached about 0.433 and sampled out_of_road occurred earlier. This suggests ttc14/v18 is unstable for seed26 as well.
- Decision: do not stop because the run is close to completion and final held-out CSV is needed for evidence. Expect likely diagnostic-only unless evaluation contradicts the training curve.


## 2026-06-30 ttc14/v18 nenv16 tuning completed and rejected
- Time: 2026-06-30T16:29:52+08:00
- Protocol: scripts/run_one_defensive_proposed.py, n_envs=16, timesteps=1M, horizon=1500, ttc_threshold=14.0, target_speed=18.0, eval_n_envs=16, 50 episodes per density.
- Evidence: outputs/defensive_ttc14_v18_nenv16_tuning/evaluations/summary.csv and per-seed CSVs for seeds 26/27/28.
- seed26 d0.15: success=0.62 cost=0.20 collision=0.20 out=0.00 route=0.842.
- seed27 d0.15: success=0.44 cost=0.38 collision=0.32 out=0.06 route=0.777.
- seed28 d0.15: success=0.66 cost=0.20 collision=0.20 out=0.00 route=0.897.
- mean d0.00: success=0.973 cost=0.000 collision=0.000 out=0.000 route=0.990.
- mean d0.08: success=0.867 cost=0.093 collision=0.087 out=0.007 route=0.953.
- mean d0.15: success=0.573 cost=0.260 collision=0.240 out=0.020 route=0.839.
- Gate result: FAIL. The d0.15 three-seed mean success=0.573 is below the 0.60 minimum and mean cost=0.260 is above the 0.25 ceiling.
- Interpretation: raising TTC threshold to 14 helps seed26/28 relative to the weakest ttc12/v18 cases but worsens seed27 success and remains unstable; improvement over ttc12/v18 mean is too small for a paper-facing final claim.
- Decision: keep ttc14/v18 as diagnostic parameter-sensitivity evidence only. Do not freeze it as Branch A. Move to Branch B standard comparison with n_envs=16 and start from the full proposed method, while retaining defensive results for appendix/tuning discussion.

## 2026-06-30 launch Branch B proposed seed0 nenv16
- Time: 2026-06-30T16:30:49+08:00
- Decision basis: previous n_envs=10 candidate protocol used ent_coef=0.01 after idle-collapse diagnostics; current user requirement is to rerun formal evidence with n_envs=16. Keep ent_coef=0.01 and move only the environment parallelism/protocol to n_envs=16.
- Command: N_ENVS=16 EPISODES=50 DEVICE=cuda codex_longrun_iscsic/run_formal_variant_nenv16.sh proposed 0 outputs/iscsic_main_nenv16_v2 1500000 1200 --ent-coef 0.01
- Protocol: Branch B standard main comparison, proposed full method, seed=0, horizon=1200, train/eval n_envs=16, densities=0.00/0.08/0.15, 50 eval episodes per density.
- Review target: if final d0.15 is underfit or safety-success tradeoff cannot serve the paper main line, inspect training stages/config and run targeted reward/gate/timestep diagnostics before expanding all seeds.

## 2026-06-30 actual Branch B proposed seed0 nenv16 launch
- Time: 2026-06-30T16:31:15+08:00
- Note: previous local wrapper attempt only wrote the decision note; the training launch is performed by this remote script.
- Command: N_ENVS=16 EPISODES=50 DEVICE=cuda codex_longrun_iscsic/run_formal_variant_nenv16.sh proposed 0 outputs/iscsic_main_nenv16_v2 1500000 1200 --ent-coef 0.01
- Expected artifacts: outputs/iscsic_main_nenv16_v2/runs/proposed_ppo_s0/config.json, final_model.zip, evaluations/proposed_ppo_s0.csv, figures, and run report.

## 2026-06-30 proposed seed0 nenv16 early health check
- Time: 2026-06-30T16:31:59+08:00
- Run: outputs/iscsic_main_nenv16_v2/runs/proposed_ppo_s0.
- Config verified: variant=proposed, seed=0, timesteps=1.5M, horizon=1200, n_envs=16, ent_coef=0.01, learning_rate=3e-4, curriculum/risk_reward/action_guard all enabled.
- Early log: reached about 49k timesteps, fps about 2500, stage=0, no crash/cost signal yet, low route completion as expected during warmup.
- Resource check: GPU free about 10.9GB, CPU available about 24GB, disk free about 35GB. Continue to 250k checkpoint before making quality decision.

## 2026-06-30 proposed seed0 nenv16 monitor at ~344k
- Time: 2026-06-30T16:34:18+08:00
- Health: process alive with 16 workers; GPU free about 10.9GB, above safety headroom.
- Training signal: reached stage1 around 327k with window_success about 0.50, window_route_completion about 0.732, window_cost about 0.033; then demoted to stage0 by 344k with window_success about 0.033, route window about 0.526, window_cost about 0.10.
- Interpretation: this is not idle collapse because success and route progress have appeared, but the policy is unstable after first promotion.
- Decision: continue to 500k/750k before tuning. If repeated demotion persists or final held-out d0.15 fails, inspect stage gates/reward safety balance before expanding all proposed seeds.

## 2026-06-30 proposed seed0 nenv16 monitor at ~475k
- Time: 2026-06-30T16:35:45+08:00
- Health: process alive with 16 workers; GPU free about 10.9GB; checkpoint_374992_steps.zip exists.
- Training signal: progressed beyond early instability and reached stage3 by about 475k. Recent window_success about 0.367 and window_route_completion about 0.736.
- Risk signal: stage3 window_cost about 0.233 and one out-of-road/cost sample appeared near 442k. This is acceptable to continue but not yet safe enough to expand all seeds blindly.
- Decision: continue to 750k/final. Main criterion is held-out d0.08/d0.15 cost and success after full eval; no parameter edit yet.

## 2026-06-30 proposed seed0 nenv16 monitor at ~557k
- Time: 2026-06-30T16:37:23+08:00
- Health: process alive; GPU free about 10.9GB; checkpoint_374992_steps.zip exists.
- Training signal: after reaching stage3 around 475k, current log around 557k is stage2 with window_route_completion about 0.718 and window_success about 0.133.
- Risk signal: window_cost fluctuated up to 0.400 around 540k and then fell to about 0.233 by 557k; ttc_risk begins to appear at hard enough traffic.
- Interpretation: standard proposed is learning but safety is not yet stable. Continue because mid-run stage demotion/cost spikes are informative but final held-out evaluation is the decisive evidence.
- Decision: keep running to 750k/final. If final d0.15 cost remains high, likely next diagnostic is safety-weight/gate tuning rather than more seeds only.

## 2026-06-30 proposed seed0 nenv16 monitor at ~672k
- Time: 2026-06-30T16:39:17+08:00
- Health: process alive; GPU free about 10.9GB.
- Training signal: recovered from earlier stage2/cost spike and reached stage4 hard around 655k. Recent window_cost about 0.067, window_route_completion about 0.837, success_rate about 0.34.
- Mechanism note: the full proposed method is now exposing hard-density TTC risk while keeping current sampled cost at zero, which is the intended safety-curriculum behavior.
- Decision: continue to 1M/1.5M and final evaluation. If held-out d0.15 is acceptable, expand Branch B seeds/variants under the same n_envs=16 + ent_coef=0.01 protocol.

## 2026-06-30 proposed seed0 nenv16 monitor at ~770k
- Time: 2026-06-30T16:41:41+08:00
- Health: process alive; checkpoint_749984_steps.zip now exists.
- Training signal: after a good stage4 window at ~655k, the policy is back at stage3 by ~770k with window_route_completion about 0.687 and window_success about 0.10.
- Risk signal: two recent collision/cost samples appeared near ~754k and ~770k; window_cost is about 0.167. This is below the earlier 0.40 spike but not yet paper-grade stable.
- Decision: continue to final evaluation for authoritative d0.08/d0.15 metrics. If final cost is high, next action should be targeted reward/gate tuning before broad seed expansion.

## 2026-06-30 proposed seed0 nenv16 monitor at ~885k
- Time: 2026-06-30T16:44:06+08:00
- Health: process alive; GPU free about 10.9GB; checkpoints at ~375k and ~750k exist.
- Training signal: still stage3 near 885k; route window about 0.749 but success window only about 0.033-0.10 in recent logs.
- Risk signal: window_cost fluctuates from about 0.133 to 0.333; recent sampled episodes can achieve high route completion, but held-out safety stability is uncertain.
- Decision: continue to final eval. Do not expand Branch B seeds until proposed seed0 final CSV is inspected. Likely next diagnostic, if final d0.15 is poor, is reward/gate safety tuning rather than just more timesteps.

## 2026-06-30 proposed seed0 nenv16 monitor at ~1.0M
- Time: 2026-06-30T16:47:02+08:00
- Health: process alive; checkpoints at ~375k and ~750k exist.
- Training signal: around 966k-999k the run is stage4 hard, with recent success samples but unstable success window.
- Risk signal: window_cost reached about 0.400 at ~999k, including recent crash_vehicle/cost samples. This is a warning sign for the final d0.15 safety claim.
- Decision: continue to 1.5M and final held-out eval. Do not expand additional proposed seeds until final CSV is checked; if cost remains high, next step is safety reward/gate tuning.

## 2026-06-30 proposed seed0 nenv16 monitor at ~1.15M
- Time: 2026-06-30T16:50:48+08:00
- Health: process alive; checkpoint_1124976_steps.zip now exists.
- Training signal: around 1.15M still mostly stage3, with route window about 0.707 and success window about 0.067 in the latest logged block.
- Risk signal: window_cost spiked to about 0.533 near 1.11M and then recovered to about 0.133 by 1.15M. Safety remains unstable, even though sampled episodes often have no immediate cost.
- Decision: finish the scheduled 1.5M and evaluate. Treat this as a pending quality gate, not accepted main evidence yet.

## 2026-06-30 proposed seed0 nenv16 monitor at ~1.36M
- Time: 2026-06-30T16:55:13+08:00
- Health: process alive; GPU free about 10.9GB; final checkpoint not yet written, but 1.125M checkpoint exists.
- Training signal: latest blocks around 1.31M-1.36M remain stage3, with route window around 0.77-0.81 and success window around 0.13-0.20.
- Risk signal: window_cost improved from earlier spikes to about 0.067-0.133. Safety has improved late, but success/stage progression remain weaker than ideal.
- Decision: finish and inspect final evaluation CSV before deciding whether to expand seeds or launch a safety/target-speed/TTC tuning diagnostic.

## 2026-06-30 proposed seed0 nenv16 training completed, evaluation running
- Time: 2026-06-30T16:58:37+08:00
- Training status: completed 1.5M scheduled timesteps and saved outputs/iscsic_main_nenv16_v2/runs/proposed_ppo_s0/model/final_model.zip plus checkpoint_1499968_steps.zip.
- Final training signal: still stage3 near 1.507M, window_route_completion about 0.794, window_success about 0.20, window_cost about 0.20. Not a clean training-curve pass, so held-out eval is decisive.
- Evaluation status: scripts/evaluate_from_config.py is running with eval_n_envs=16, densities 0.00/0.08/0.15, 50 episodes per density.

## 2026-06-30 Branch B proposed seed0 nenv16 completed and failed main gate
- Time: 2026-06-30T17:03:41+08:00
- Run: outputs/iscsic_main_nenv16_v2/runs/proposed_ppo_s0.
- Protocol: proposed full method, seed0, train/eval n_envs=16, timesteps=1.5M, horizon=1200, ent_coef=0.01, eval 50 episodes per density.
- Evaluation CSV: outputs/iscsic_main_nenv16_v2/evaluations/proposed_ppo_s0.csv; summary: outputs/iscsic_main_nenv16_v2/evaluations/summary.csv.
- d0.00: success=0.90 cost=0.00 collision=0.00 out=0.00 route=0.984 shield=0.862.
- d0.08: success=0.76 cost=0.12 collision=0.12 out=0.00 route=0.929 shield=0.842.
- d0.15: success=0.48 cost=0.42 collision=0.40 out=0.02 route=0.791 shield=0.749.
- Gate result: FAIL for paper main line. High-density cost/collision is too high and success is below target; do not expand this exact protocol to seed1/seed2 as the main proposed method.
- Decision: launch targeted safety tuning using stronger TTC/collision penalties and lower target speed, based on defensive branch evidence and prior reward screens showing completion-only tuning worsens high-density collision.

## 2026-06-30 launch proposed safety-tuned seed0 nenv16 screen
- Time: 2026-06-30T17:03:41+08:00
- Output root: outputs/tuning_proposed_safety_ttc12_v18_nenv16_1m.
- Command: N_ENVS=16 EPISODES=50 DEVICE=cuda codex_longrun_iscsic/run_formal_variant_nenv16.sh proposed 0 outputs/tuning_proposed_safety_ttc12_v18_nenv16_1m 1000000 1200 --ent-coef 0.01 --reward-ttc 6 --reward-cost 40 --reward-overspeed 3 --reward-target-speed 18 --reward-progress 40 --reward-success-bonus 55 --reward-crash-penalty 120 --reward-out-of-road-penalty 120 --reward-ttc-threshold 12 --stage2-success 0.40 --stage2-cost 0.25 --demote-cost 0.35
- Hypothesis: stronger TTC/cost/crash penalties and lower target speed should reduce d0.15 collision/cost relative to standard proposed seed0, while preserving enough route completion for a safety-success tradeoff.
- Promotion rule: only expand if d0.15 cost is materially below 0.42 and preferably <=0.25 without collapsing d0.08 success.

## 2026-06-30 safety-tuned proposed seed0 nenv16 early health check
- Time: 2026-06-30T17:04:21+08:00
- Run: outputs/tuning_proposed_safety_ttc12_v18_nenv16_1m/runs/proposed_ppo_s0.
- Config verified: n_envs=16, timesteps=1M, horizon=1200, ent_coef=0.01, reward_ttc=6, reward_cost=40, target_speed=18, progress=40, success_bonus=55, crash/out=120, ttc_threshold=12, stage2_success=0.40, stage2_cost=0.25, demote_cost=0.35.
- Early log: about 32k timesteps, stage0, no cost/collision yet; low route completion is expected during warmup.
- Resource check: GPU free about 10.8GB, CPU available about 24GB, disk free about 41GB. Continue to 250k/500k quality checks.

## 2026-06-30 safety-tuned proposed seed0 monitor at ~311k
- Time: 2026-06-30T17:06:20+08:00
- Health: process alive; checkpoint_250000_steps.zip exists; GPU free about 10.9GB.
- Training signal: reached stage1 by about 278k-311k. Success window remains low at about 0.067; route window dropped from about 0.600 to 0.436, while sampled route can reach about 0.604.
- Risk signal: window_cost ranges about 0.067-0.200. Safety pressure is working, but the run may be too conservative/slow early.
- Decision: continue to 500k before changing parameters. Watch whether route/success recover under the lower target speed and stronger TTC/cost penalties.

## 2026-06-30 safety-tuned proposed seed0 monitor at ~508k
- Time: 2026-06-30T17:08:24+08:00
- Health: process alive; checkpoints at 250k and 500k exist; GPU free about 10.9GB.
- Training signal: still stage1 around 508k. Route window improved to about 0.685, success window about 0.133; sampled route can reach about 0.829 but an out-of-road cost sample appeared.
- Risk/benefit: stronger safety tuning is slowing curriculum progress but may reduce high-density collision relative to standard proposed. It is not idle collapse.
- Decision: continue to 750k/final evaluation. If final d0.15 cost improves but success collapses, next diagnostic should relax completion/speed slightly rather than revert to standard reward.

## 2026-06-30 safety-tuned proposed seed0 monitor at ~704k
- Time: 2026-06-30T17:11:14+08:00
- Health: process alive; checkpoints at 250k and 500k exist; GPU free about 10.9GB.
- Training signal: recovered from slow early stage1 and reached stage3 by about 688k. Window_route_completion peaked around 0.862 and window_success about 0.467; current sampled route remains moderate to high.
- Risk signal: window_cost is 0.0 in the recent stage2/stage3 blocks, a clear improvement over the standard proposed run's high-cost training windows.
- Decision: continue to final evaluation. This screen remains promising for reducing d0.15 cost; final success tradeoff will decide promotion.

## 2026-06-30 safety-tuned proposed seed0 monitor at ~918k
- Time: 2026-06-30T17:14:47+08:00
- Health: process alive; checkpoints at 250k/500k/750k exist.
- Training signal: after reaching stage3 earlier, latest log near 918k is stage2 with route window about 0.749 and success window about 0.067.
- Risk signal: recent window_cost is low, about 0.033-0.067, much lower than standard proposed, but success appears under pressure.
- Decision: finish and evaluate. If final d0.15 cost drops strongly but success is too low, next tuning should relax success/completion pressure or reduce safety strength slightly.

## 2026-06-30 safety-tuned proposed seed0 training completed, evaluation running
- Time: 2026-06-30T17:17:50+08:00
- Training status: completed 1M scheduled timesteps and saved outputs/tuning_proposed_safety_ttc12_v18_nenv16_1m/runs/proposed_ppo_s0/model/final_model.zip plus checkpoint_1000000_steps.zip.
- Final training signal: stage2 near 1.016M, window_route_completion about 0.743, window_success about 0.167, window_cost about 0.133.
- Interpretation before eval: much lower apparent cost than standard proposed, but success/stage progression is weaker. Held-out eval will decide whether this is a useful safety-success tradeoff.
- Evaluation status: evaluate_from_config.py is running with eval_n_envs=16, densities 0.00/0.08/0.15, 50 episodes per density.

## 2026-06-30 safety-tuned proposed seed0 nenv16 screen completed and rejected
- Time: 2026-06-30T17:21:05+08:00
- Run: outputs/tuning_proposed_safety_ttc12_v18_nenv16_1m/runs/proposed_ppo_s0.
- Protocol: proposed seed0, train/eval n_envs=16, timesteps=1M, horizon=1200, ent_coef=0.01, reward_ttc=6, cost=40, target_speed=18, progress=40, success_bonus=55, crash/out=120, ttc_threshold=12, stage2_success=0.40, stage2_cost=0.25, demote_cost=0.35.
- Evaluation CSV: outputs/tuning_proposed_safety_ttc12_v18_nenv16_1m/evaluations/proposed_ppo_s0.csv.
- d0.00: success=0.70 cost=0.00 collision=0.00 out=0.00 route=0.969 shield=0.860.
- d0.08: success=0.64 cost=0.12 collision=0.10 out=0.02 route=0.935 shield=0.839.
- d0.15: success=0.28 cost=0.40 collision=0.34 out=0.06 route=0.704 shield=0.699.
- Gate result: FAIL. Compared with standard proposed seed0 d0.15 success=0.48/cost=0.42, cost only improves slightly while success collapses. Do not expand this configuration.
- Decision: launch defensive-like horizon1500 cost50 diagnostic, because prior defensive branch suggests horizon1500 + stricter progression gives better high-density tradeoff than horizon1200 safety penalty alone.

## 2026-06-30 launch defensive-like proposed h1500 cost50 seed0 nenv16 screen
- Time: 2026-06-30T17:21:05+08:00
- Output root: outputs/tuning_proposed_defensive_h1500_cost50_nenv16_1m.
- Command: N_ENVS=16 EPISODES=50 DEVICE=cuda codex_longrun_iscsic/run_formal_variant_nenv16.sh proposed 0 outputs/tuning_proposed_defensive_h1500_cost50_nenv16_1m 1000000 1500 --ent-coef 0.01 --reward-ttc 6 --reward-cost 50 --reward-overspeed 3 --reward-target-speed 18 --reward-progress 40 --reward-success-bonus 55 --reward-crash-penalty 120 --reward-out-of-road-penalty 120 --reward-ttc-threshold 12 --stage2-success 0.50 --stage2-cost 0.25 --demote-cost 0.35
- Hypothesis: horizon=1500 and stricter stage2 gate should preserve route/success better than the failed horizon1200 safety screen, while cost=50 attempts to push d0.15 cost below the defensive ttc12/v18 mean.
- Promotion rule: must beat standard proposed seed0 on d0.15 cost by a clear margin and avoid the safety-tuned screen's success collapse.

## 2026-06-30 defensive-like h1500 cost50 seed0 early health check
- Time: 2026-06-30T17:21:39+08:00
- Run: outputs/tuning_proposed_defensive_h1500_cost50_nenv16_1m/runs/proposed_ppo_s0.
- Config verified: n_envs=16, timesteps=1M, horizon=1500, ent_coef=0.01, reward_ttc=6, reward_cost=50, target_speed=18, progress=40, success_bonus=55, crash/out=120, ttc_threshold=12, stage2_success=0.50, stage2_cost=0.25, demote_cost=0.35.
- Early log: about 32k timesteps, stage0, no cost/collision, low route completion as expected.
- Resource check: GPU free about 10.8GB, CPU available about 24GB, disk free about 41GB. Continue to 250k/500k checks.

## 2026-06-30 defensive-like h1500 cost50 seed0 monitor at ~295k
- Time: 2026-06-30T17:23:35+08:00
- Health: process alive; checkpoint_250000_steps.zip exists; GPU free about 10.8GB.
- Training signal: reached stage1 by ~278k. Recent window_success rose to about 0.233, with route window around 0.528-0.607.
- Risk signal: window_cost is 0.0-0.10 in early stage1, better than the failed horizon1200 safety screen at comparable progress.
- Decision: continue to 500k/750k. This diagnostic is still viable because horizon1500 appears to preserve early success better while keeping cost low.

## 2026-06-30 defensive-like h1500 cost50 seed0 monitor at ~508k
- Time: 2026-06-30T17:26:11+08:00
- Health: process alive; checkpoints at 250k and 500k exist.
- Training signal: around 508k still stage1, but route window is strong at about 0.813 and success window about 0.267. This is better route/success behavior than the failed horizon1200 safety screen.
- Risk signal: window_cost rose to about 0.233, near the intended stage2 cost ceiling. It is not yet clean enough to freeze.
- Decision: continue to 750k/final. Need final d0.15 cost to decide whether cost50 helps or just trades instability for route.

## 2026-06-30 defensive-like h1500 cost50 seed0 monitor at ~688k
- Time: 2026-06-30T17:28:58+08:00
- Health: process alive; checkpoints at 250k and 500k exist.
- Training signal: reached stage2 by about 672k. Window_route_completion about 0.854, window_success about 0.30, and success samples appear.
- Risk signal: cost spiked around 622k-639k up to window_cost about 0.30, then improved to about 0.10 by 672k-688k.
- Decision: continue to 750k/final. This is now the most promising tuning screen so far because it preserves route/success better than the horizon1200 safety screen while recovering cost.

## 2026-06-30 defensive-like h1500 cost50 seed0 monitor at ~918k
- Time: 2026-06-30T17:32:16+08:00
- Health: process alive; checkpoints at 250k/500k/750k exist.
- Training signal: around 900k-918k the run is stage2 and success_rate increases, but route samples are mixed.
- Risk signal: window_cost worsened to about 0.333-0.467, mainly out-of-road samples, despite cost50. This is a serious warning sign.
- Decision: continue to final held-out eval for evidence, but do not treat this diagnostic as promotable unless the CSV unexpectedly shows much lower d0.15 cost.

## 2026-06-30 defensive-like h1500 cost50 seed0 training completed, evaluation running
- Time: 2026-06-30T17:35:19+08:00
- Training status: completed 1M scheduled timesteps and saved outputs/tuning_proposed_defensive_h1500_cost50_nenv16_1m/runs/proposed_ppo_s0/model/final_model.zip plus checkpoint_1000000_steps.zip.
- Final training signal: stage2 near 1.016M, window_route_completion about 0.776, window_success about 0.467, window_cost about 0.20.
- Interpretation before eval: better success/route than the horizon1200 safety screen, but out-of-road/cost instability remains. Held-out eval decides promotion or rejection.
- Evaluation status: evaluate_from_config.py is running with eval_n_envs=16, densities 0.00/0.08/0.15, 50 episodes per density.

## 2026-06-30 defensive-like h1500 cost50 seed0 screen completed: improved but failed
- Time: 2026-06-30T17:38:31+08:00
- Run: outputs/tuning_proposed_defensive_h1500_cost50_nenv16_1m/runs/proposed_ppo_s0.
- Protocol: proposed seed0, n_envs=16, timesteps=1M, horizon=1500, ent_coef=0.01, reward_ttc=6, cost=50, target_speed=18, progress=40, success_bonus=55, crash/out=120, ttc_threshold=12, stage2_success=0.50, stage2_cost=0.25.
- Evaluation CSV: outputs/tuning_proposed_defensive_h1500_cost50_nenv16_1m/evaluations/proposed_ppo_s0.csv.
- d0.00: success=0.96 cost=0.00 collision=0.00 out=0.00 route=0.986 shield=0.867.
- d0.08: success=0.84 cost=0.12 collision=0.10 out=0.02 route=0.936 shield=0.846.
- d0.15: success=0.54 cost=0.34 collision=0.24 out=0.10 route=0.815 shield=0.716.
- Gate result: FAIL but improved. Compared with standard proposed seed0, d0.15 improved from success=0.48/cost=0.42 to success=0.54/cost=0.34, but cost remains too high and out_of_road=0.10 is a new bottleneck.
- Decision: next tuning should target lane/out-of-road control, not just global cost. Launch h1500 lane/out diagnostic with lower target speed and stronger lane/out penalties.

## 2026-06-30 launch defensive-like h1500 lane/out seed0 nenv16 screen
- Time: 2026-06-30T17:38:31+08:00
- Output root: outputs/tuning_proposed_defensive_h1500_lane2_v16_cost50_nenv16_1m.
- Command: N_ENVS=16 EPISODES=50 DEVICE=cuda codex_longrun_iscsic/run_formal_variant_nenv16.sh proposed 0 outputs/tuning_proposed_defensive_h1500_lane2_v16_cost50_nenv16_1m 1000000 1500 --ent-coef 0.01 --reward-ttc 6 --reward-cost 50 --reward-overspeed 3 --reward-target-speed 16 --reward-progress 40 --reward-lane 2.0 --reward-success-bonus 55 --reward-crash-penalty 120 --reward-out-of-road-penalty 150 --reward-ttc-threshold 12 --stage2-success 0.50 --stage2-cost 0.25 --demote-cost 0.35
- Hypothesis: h1500/cost50 improved success but left high out_of_road and lane deviation; stronger lane/out penalty plus target_speed=16 should reduce d0.15 cost without repeating the horizon1200 success collapse.
- Promotion rule: must reduce d0.15 cost below 0.34 and preferably <=0.25 while keeping success near or above 0.50.

## 2026-06-30 defensive-like h1500 lane/out seed0 early health check
- Time: 2026-06-30T17:39:05+08:00
- Run: outputs/tuning_proposed_defensive_h1500_lane2_v16_cost50_nenv16_1m/runs/proposed_ppo_s0.
- Config verified: n_envs=16, timesteps=1M, horizon=1500, ent_coef=0.01, reward_ttc=6, reward_cost=50, reward_lane=2.0, target_speed=16, progress=40, success_bonus=55, crash=120, out=150, ttc_threshold=12, stage2_success=0.50, stage2_cost=0.25.
- Early log: about 32k timesteps, stage0, no cost/collision; shaped reward is much lower because lane penalty is stronger.
- Resource check: GPU free about 10.8GB, CPU available about 24GB, disk free about 41GB. Continue to 250k; watch for over-conservative/low-motion collapse.

## 2026-06-30 defensive-like h1500 lane2/v16 seed0 early rejected
- Time: 2026-06-30T17:41:32+08:00
- Run: outputs/tuning_proposed_defensive_h1500_lane2_v16_cost50_nenv16_1m/runs/proposed_ppo_s0.
- Status at about 311k: still stage0, window_route_completion about 0.077-0.082, window_success=0, window_cost=0, mean_speed about 0.5-0.6 km/h.
- Interpretation: reward_lane=2.0 plus target_speed=16 and strong out penalty makes the policy too conservative/low-motion. This is early idle/slow-motion collapse, not a useful paper candidate.
- Decision: terminate this run early and do not evaluate it. Launch a milder lane/out diagnostic: lane=1.0, target_speed=18, out penalty=150, keeping horizon1500 and cost50.

## 2026-06-30 launch defensive-like h1500 lane1/out150 seed0 nenv16 screen
- Time: 2026-06-30T17:41:32+08:00
- Output root: outputs/tuning_proposed_defensive_h1500_lane1_out150_cost50_nenv16_1m.
- Command: N_ENVS=16 EPISODES=50 DEVICE=cuda codex_longrun_iscsic/run_formal_variant_nenv16.sh proposed 0 outputs/tuning_proposed_defensive_h1500_lane1_out150_cost50_nenv16_1m 1000000 1500 --ent-coef 0.01 --reward-ttc 6 --reward-cost 50 --reward-overspeed 3 --reward-target-speed 18 --reward-progress 40 --reward-lane 1.0 --reward-success-bonus 55 --reward-crash-penalty 120 --reward-out-of-road-penalty 150 --reward-ttc-threshold 12 --stage2-success 0.50 --stage2-cost 0.25 --demote-cost 0.35
- Hypothesis: a moderate lane penalty and stronger out penalty may reduce out_of_road without the lane2/v16 low-motion collapse.

## 2026-06-30 defensive-like h1500 lane1/out150 seed0 screen completed: promoted to candidate
- Time: 2026-06-30T17:57:38+08:00
- Run: outputs/tuning_proposed_defensive_h1500_lane1_out150_cost50_nenv16_1m/runs/proposed_ppo_s0.
- Protocol: proposed seed0, n_envs=16, timesteps=1M, horizon=1500, ent_coef=0.01, reward_ttc=6, reward_cost=50, reward_lane=1.0, target_speed=18, progress=40, success_bonus=55, crash=120, out=150, ttc_threshold=12, stage2_success=0.50, stage2_cost=0.25, demote_cost=0.35.
- Evaluation CSV: outputs/tuning_proposed_defensive_h1500_lane1_out150_cost50_nenv16_1m/evaluations/proposed_ppo_s0.csv; summary.csv exists.
- d0.00: success=0.96 cost=0.00 collision=0.00 out=0.00 route=0.988 shield=0.868.
- d0.08: success=0.88 cost=0.10 collision=0.10 out=0.00 route=0.965 shield=0.850.
- d0.15: success=0.70 cost=0.24 collision=0.22 out=0.02 route=0.872 shield=0.712.
- Comparison: vs standard proposed seed0 d0.15 improved from success=0.48/cost=0.42/route=0.791 to success=0.70/cost=0.24/route=0.872. Vs h1500 cost50 seed0 improved from success=0.54/cost=0.34/out=0.10 to success=0.70/cost=0.24/out=0.02.
- Interpretation: moderate lane penalty plus stronger out-of-road penalty fixes the lane2/v16 low-motion failure and materially reduces high-density cost while preserving route completion. The remaining d0.15 failures are mostly collision (0.22), not out-of-road.
- Gate result: PROMOTE TO CANDIDATE, not final. Expand seeds 1 and 2 with the same n_envs=16 protocol before freezing paper-facing results. If seed1/2 mean d0.15 remains success>=0.60 and cost<=0.28, use this as the main proposed setting and start ablations/comparisons against it.

## 2026-06-30 launch candidate lane1/out150 seed1-2 nenv16 replication
- Time: 2026-06-30T17:58:25+08:00
- Roots: outputs/candidate_lane1_out150_cost50_nenv16_seed1_1m and outputs/candidate_lane1_out150_cost50_nenv16_seed2_1m.
- Protocol: proposed seeds 1 and 2, n_envs=16, timesteps=1M, horizon=1500, ent_coef=0.01, reward_ttc=6, reward_cost=50, reward_lane=1.0, target_speed=18, progress=40, success_bonus=55, crash=120, out=150, ttc_threshold=12, stage2_success=0.50, stage2_cost=0.25, demote_cost=0.35.
- Reason: seed0 promoted to candidate with d0.15 success=0.70/cost=0.24/out=0.02, but paper-facing main proposed setting requires multi-seed replication.
- Run policy: use independent roots for seed1/seed2 to avoid parallel root-level figure/report write conflicts; aggregate after both finish.

## 2026-06-30 candidate lane1/out150 seed1-2 monitor at ~600k
- Time: 2026-06-30T18:04:12+08:00
- Roots: outputs/candidate_lane1_out150_cost50_nenv16_seed1_1m and outputs/candidate_lane1_out150_cost50_nenv16_seed2_1m.
- Resource status: parallel n_envs=16 + n_envs=16 remains safe; GPU free about 10.5GB, CPU memory available about 21GB.
- Seed1 status: checkpoint_500000_steps.zip exists; by ~590k reached stage2, window_success about 0.667 at one check, rollout success_rate about 0.40, cost near 0.00-0.03.
- Seed2 status: checkpoint_500000_steps.zip exists; by ~590k reached stage2 once, then stage1/2 fluctuation; rollout success_rate about 0.28-0.32, cost about 0.10.
- Interpretation: both seeds had a slow stage0 start but recovered, so this is not the lane2/v16 idle collapse. Continue to 750k/final held-out evaluation.

## 2026-06-30 candidate lane1/out150 seed0-2 aggregate completed
- Time: 2026-06-30T18:17:01+08:00
- Aggregate root: outputs/candidate_lane1_out150_cost50_nenv16_aggregate.
- Files: summary_by_seed.csv, mean_by_density.csv, DECISION.md.
- Sources: seed0 from outputs/tuning_proposed_defensive_h1500_lane1_out150_cost50_nenv16_1m/evaluations/summary.csv; seed1/2 from outputs/candidate_lane1_out150_cost50_nenv16_seed1_1m and seed2_1m.
- d0.00 mean: success=0.973, cost=0.000, route=0.989.
- d0.08 mean: success=0.833, cost=0.133, collision=0.127, out=0.007, route=0.929.
- d0.15 mean: success=0.620, cost=0.247, collision=0.233, out=0.013, route=0.865.
- Variance warning: d0.15 success std=0.122 and seed2 is weak (success=0.48, cost=0.32). This is acceptable as current best only because the three-seed mean passes the promotion gate, not because every seed is clean.
- Decision: keep lane1/out150/cost50 as current main-method candidate and start ablations/comparisons around it. Remaining bottleneck is high-density collision, not out-of-road.

## 2026-06-30 launch tuned-protocol comparison/ablation seed0 batch A
- Time: 2026-06-30T18:18:25+08:00
- Runs launched: baseline seed0 and proposed_wo_ttc seed0.
- Roots: outputs/tuned_compare_baseline_nenv16_seed0_1m and outputs/tuned_ablation_wo_ttc_nenv16_seed0_1m.
- Protocol: n_envs=16, timesteps=1M, horizon=1500, ent_coef=0.01, target_speed=18, progress=40, cost=50, lane=1.0 where applicable, success_bonus=55, crash=120, out=150, stage2_success=0.50, stage2_cost=0.25, demote_cost=0.35.
- Important ablation detail: proposed_wo_ttc intentionally omits --reward-ttc so get_variant_config keeps TTC weight at 0.0; all other tuned reward/curriculum settings match the candidate.
- Purpose: baseline tests vanilla PPO under same horizon; proposed_wo_ttc tests whether TTC risk term is needed for the high-density safety-success tradeoff.

## 2026-06-30 tuned-protocol proposed_wo_ttc seed0 nenv16 completed
- Time: 2026-06-30T18:38:32.
- Root: outputs/tuned_ablation_wo_ttc_nenv16_seed0_1m.
- Protocol: proposed_wo_ttc seed0, n_envs=16, timesteps=1M, horizon=1500, ent_coef=0.01, target_speed=18, progress=40, cost=50, lane=1.0, success_bonus=55, crash=120, out=150, stage2_success=0.50, stage2_cost=0.25, demote_cost=0.35.
- Config check: reward_ttc=0.0 by variant; action guard and curriculum stay enabled. This is the intended TTC reward ablation, not a mistaken low-TTC full method.
- CSV: outputs/tuned_ablation_wo_ttc_nenv16_seed0_1m/evaluations/summary.csv.
- d0.00: success=1.00 cost=0.00 collision=0.00 out=0.00 route=0.992.
- d0.08: success=0.92 cost=0.04 collision=0.04 out=0.00 route=0.975.
- d0.15: success=0.44 cost=0.54 collision=0.54 out=0.00 route=0.743.
- Comparison to full tuned proposed seed0: full d0.15 success=0.70 cost=0.24 collision=0.22 out=0.02 route=0.872; removing TTC drops success by 0.26 and increases collision/cost by about 0.30.
- Interpretation: TTC reward is important specifically for dense-traffic collision suppression. The ablation can look strong at easy/medium density, but it fails the paper-relevant high-density safety-success tradeoff.
- Decision: keep TTC in the main method. Do not expand proposed_wo_ttc to more seeds until baseline/risk/curriculum/no_action_guard seed0 comparisons are available, unless the paper explicitly needs a three-seed TTC ablation table.

## 2026-06-30 tuned-protocol baseline seed0 nenv16 completed
- Time: 2026-06-30T18:44:31.
- Root: outputs/tuned_compare_baseline_nenv16_seed0_1m.
- Protocol: baseline seed0, n_envs=16, timesteps=1M, horizon=1500, ent_coef=0.01, same evaluation densities and episode budget as tuned proposed.
- Config check: use_risk_reward=False, use_action_guard=False, curriculum=False. Reward CLI values are recorded for protocol parity but are not active in baseline shaping.
- CSV: outputs/tuned_compare_baseline_nenv16_seed0_1m/evaluations/summary.csv.
- d0.00: success=0.02 cost=0.98 collision=0.00 out=0.98 route=0.302.
- d0.08: success=0.00 cost=1.00 collision=0.40 out=0.60 route=0.234.
- d0.15: success=0.00 cost=1.00 collision=0.62 out=0.38 route=0.177.
- Comparison to full tuned proposed seed0: full d0.15 success=0.70 cost=0.24 route=0.872; baseline d0.15 success=0.00 cost=1.00 route=0.177.
- Interpretation: vanilla PPO under this 1M/h1500/n_envs16 protocol fails even at easy density, mostly by leaving the road at d0.00 and by mixed collision/out failures under traffic. This is a strong main-comparison baseline, not a competitive candidate.
- Decision: do not expand baseline seeds immediately. Next batch should isolate mechanisms: risk without curriculum and no_action_guard under the same tuned reward/curriculum settings.

## 2026-06-30 launch tuned-protocol comparison/ablation seed0 batch B
- Time: 2026-06-30T18:45:43.
- Runs launched: risk seed0 and no_action_guard seed0.
- Roots: outputs/tuned_compare_risk_nenv16_seed0_1m and outputs/tuned_ablation_no_action_guard_nenv16_seed0_1m.
- Protocol: n_envs=16, timesteps=1M, horizon=1500, ent_coef=0.01, reward_ttc=6, reward_cost=50, overspeed=3, target_speed=18, progress=40, lane=1.0, success_bonus=55, crash=120, out=150, ttc_threshold=12, stage2_success=0.50, stage2_cost=0.25, demote_cost=0.35.
- Purpose: risk tests risk reward + action guard without curriculum; no_action_guard tests tuned reward + curriculum without action guard. Together with baseline and proposed_wo_ttc, these isolate the main paper mechanisms.
- Resource check after launch: two n_envs=16 jobs active; GPU and system memory remain within safe range.
- Next monitor: verify config JSON/logs, then check early learning around 100k/250k. Kill early only if a true collapse appears (idle/zero-route or config mismatch), otherwise evaluate to final CSV.

## 2026-06-30 batch B early config and health check
- Time: 2026-06-30T18:47:22.
- risk config verified: variant=risk, n_envs=16, horizon=1500, timesteps=1M, ent_coef=0.01, use_risk_reward=True, use_action_guard=True, curriculum=False, reward_ttc=6, cost=50, lane=1.0, target_speed=18, progress=40, success_bonus=55, crash=120, out=150, ttc_threshold=12.
- no_action_guard config verified: variant=no_action_guard, n_envs=16, horizon=1500, timesteps=1M, ent_coef=0.01, use_risk_reward=True, use_action_guard=False, curriculum=True, same tuned reward weights.
- risk early signal around 115k: mean_speed below 1 km/h, route about 0.058, success=0, cost=0. This may be low-motion collapse caused by risk/guard without curriculum; wait until 250k-300k before deciding.
- no_action_guard early signal around 180k: stage0, route about 0.19-0.25, speed about 1.4 km/h, success=0, window_cost about 0.10. Slow but not yet a confirmed collapse.
- Decision: continue both to the next monitor. Do not tune parameters mid-run because these are mechanism comparisons; only stop early if the trajectory remains idle/zero-route and cannot produce meaningful paper evidence.

## 2026-06-30 batch B monitor at risk~328k no_action_guard~475k
- Time: 2026-06-30T18:50:26.
- risk: checkpoint_250000 exists; around 295k-328k still no curriculum, success_rate=0, episode length near 1500, mean_speed about 0.5-0.6 km/h, route about 0.02-0.03, cost=0. This is low-motion collapse, likely because risk reward + guard without curriculum over-penalizes motion.
- Decision for risk: continue to final CSV rather than kill, because the failure itself is a useful comparison showing why curriculum/staging is needed.
- no_action_guard: checkpoint_250000 exists; around 442k-475k reached stage2, rollout success_rate about 0.30-0.38, speed about 8-10 km/h, recent cost=0, route samples around 0.45-0.78.
- Decision for no_action_guard: continue to final CSV. It is viable enough that the key question is high-density collision/cost without the guard, not learning collapse.

## 2026-06-30 batch B completed: risk and no_action_guard seed0 nenv16
- Time: 2026-06-30T19:03:02.
- risk root: outputs/tuned_compare_risk_nenv16_seed0_1m; summary CSV exists.
- risk config: use_risk_reward=True, use_action_guard=True, curriculum=False. It isolates risk reward + guard without curriculum.
- risk d0.00/d0.08/d0.15: success=0.00 at all densities, cost=0.00 at all densities, route about 0.009, speed about 0.013 km/h, episode_length=1500. Interpretation: low-motion/idle collapse, not a usable policy. Curriculum/staging is necessary to make the risk+guard mechanism move.
- no_action_guard root: outputs/tuned_ablation_no_action_guard_nenv16_seed0_1m; summary CSV exists.
- no_action_guard config: use_risk_reward=True, use_action_guard=False, curriculum=True. It isolates action guard removal under the tuned reward/curriculum protocol.
- no_action_guard d0.00: success=0.08 cost=0.92 collision=0.00 out=0.92 route=0.295.
- no_action_guard d0.08: success=0.00 cost=1.00 collision=0.32 out=0.68 route=0.177.
- no_action_guard d0.15: success=0.00 cost=1.00 collision=0.46 out=0.54 route=0.171.
- Comparison to full tuned proposed seed0 d0.15: full success=0.70 cost=0.24 route=0.872; no_action_guard success=0.00 cost=1.00 route=0.171; risk success=0.00 cost=0.00 route=0.008.
- Paper interpretation: action guard is necessary to prevent high-speed out-of-road/collision evaluation failure, while curriculum is necessary to prevent risk+guard from becoming an idle safe-but-useless policy.
- Decision: do not expand risk or no_action_guard seeds now. Next run curriculum-only and guard_only to complete mechanism decomposition before deciding which ablations need multi-seed replication.

## 2026-06-30 launch tuned-protocol comparison/ablation seed0 batch C
- Time: 2026-06-30T19:03:49.
- Runs launched: curriculum seed0 and guard_only seed0.
- Roots: outputs/tuned_compare_curriculum_nenv16_seed0_1m and outputs/tuned_ablation_guard_only_nenv16_seed0_1m.
- Protocol: n_envs=16, timesteps=1M, horizon=1500, ent_coef=0.01, same tuned reward CLI values and evaluation protocol as the current main candidate.
- Purpose: curriculum isolates staged learning without risk reward/action guard; guard_only isolates action guard + curriculum without risk reward. These complete the seed0 mechanism decomposition with baseline, risk, no_action_guard, and proposed_wo_ttc.
- Next monitor: verify configs and early learning; continue unless there is a config mismatch or persistent zero-motion collapse.

## 2026-06-30 batch C early config and health check
- Time: 2026-06-30T19:05:45.
- curriculum config verified: use_risk_reward=False, use_action_guard=False, curriculum=True; n_envs=16, horizon=1500, timesteps=1M.
- guard_only config verified: use_risk_reward=False, use_action_guard=True, curriculum=True; n_envs=16, horizon=1500, timesteps=1M.
- curriculum around 213k: stage2 reached, window_success about 0.53, route window about 0.84, but recent out_of_road cost appears. It learns movement faster than baseline/risk but may lack safety control.
- guard_only around 197k: stage2 reached, window_success about 0.57, route window about 0.76, but recent out_of_road also appears. Guard helps movement relative to risk-only, but risk reward contribution still needs final eval.
- Decision: continue both to final CSV. These are mechanism comparisons and should not be tuned mid-run.

## 2026-06-30 batch C monitor at ~475k
- Time: 2026-06-30T19:11:41.
- curriculum: around 425k-475k, success_rate rises to about 0.50, stage2 reached, but window_cost is high (about 0.33-0.57) with both out_of_road and collision samples. Interpretation: curriculum alone can induce movement/success but lacks safety shaping/guarding.
- guard_only: around 425k-475k, stage3 reached with long route samples and low immediate cost, but rollout success_rate remains low around 0.04-0.06. Interpretation: guard+curriculum without risk reward may be safer than curriculum-only but has weak completion/success behavior.
- Decision: continue both to final CSV. The mid-run difference is mechanistically useful and should be verified under held-out density evaluation.

## 2026-06-30 batch C completed: curriculum and guard_only seed0 nenv16
- Time: 2026-06-30T19:26:49.
- curriculum root: outputs/tuned_compare_curriculum_nenv16_seed0_1m; summary CSV exists.
- curriculum config: use_risk_reward=False, use_action_guard=False, curriculum=True.
- curriculum d0.00: success=0.02 cost=0.98 collision=0.00 out=0.98 route=0.350.
- curriculum d0.08: success=0.00 cost=1.00 collision=0.32 out=0.68 route=0.256.
- curriculum d0.15: success=0.00 cost=1.00 collision=0.56 out=0.44 route=0.176.
- Interpretation: curriculum alone induces movement during training, but final evaluation fails by high-speed out-of-road/collision. Curriculum is not sufficient without the guard/safety mechanism.
- guard_only root: outputs/tuned_ablation_guard_only_nenv16_seed0_1m; summary CSV exists.
- guard_only config: use_risk_reward=False, use_action_guard=True, curriculum=True.
- guard_only d0.00: success=1.00 cost=0.00 route=0.992 shield_intervention_rate=0.872.
- guard_only d0.08: success=0.86 cost=0.08 collision=0.08 out=0.00 route=0.954 shield_intervention_rate=0.852.
- guard_only d0.15: success=0.62 cost=0.22 collision=0.20 out=0.02 route=0.861 shield_intervention_rate=0.728.
- Comparison to full tuned proposed seed0: full d0.15 success=0.70 cost=0.24 route=0.872. Guard_only is close: slightly lower success (-0.08), slightly lower cost (-0.02), similar route.
- Paper-risk interpretation: the guard+curriculum component explains a large part of the current seed0 gain. The risk reward contribution is positive on seed0 for high-density success, but not yet proven robust enough as a standalone claim.
- Decision: promote guard_only to critical comparison. Run guard_only seeds 1 and 2 before claiming the full method beats simpler guard+curriculum. If guard_only mean matches/exceeds full proposed, either retune the full risk reward or shift the paper claim toward guard/curriculum as the main mechanism.

## 2026-06-30 launch critical guard_only seed1-2 replication
- Time: 2026-06-30T19:27:33.
- Reason: guard_only seed0 is close to full tuned proposed seed0, so this is no longer a routine ablation. It must be replicated before writing the paper mechanism claim.
- Roots: outputs/tuned_ablation_guard_only_nenv16_seed1_1m and outputs/tuned_ablation_guard_only_nenv16_seed2_1m.
- Protocol: guard_only seeds 1 and 2, n_envs=16, timesteps=1M, horizon=1500, ent_coef=0.01, same tuned CLI reward values/evaluation protocol as full proposed candidate.
- Decision rule: compare three-seed guard_only aggregate against full proposed aggregate at d0.15. If guard_only mean is comparable or better, retune the full method or rewrite the claim so the core mechanism is guard+curriculum rather than risk reward alone.

## 2026-06-30 guard_only seed1-2 early config and health check
- Time: 2026-06-30T19:29:29.
- seed1 config verified: variant=guard_only, use_risk_reward=False, use_action_guard=True, curriculum=True, n_envs=16, horizon=1500, timesteps=1M.
- seed2 config verified: same protocol and switches as seed1.
- seed1 around 197k: reached stage2, window_success about 0.53, window_cost about 0.07, route window about 0.78. Healthy early learning.
- seed2 around 213k: still stage1, window_success about 0.17-0.30, window_cost about 0.37, route window about 0.59. Higher early cost than seed1 but not a confirmed collapse.
- Decision: continue both to final evaluation; guard_only is a critical comparison, so do not stop on ordinary seed variability.

## 2026-06-30 guard_only seed1-2 monitor at ~557k
- Time: 2026-06-30T19:35:56.
- seed1: around 524k-557k, stage2, window_cost about 0.03, route window about 0.82-0.83, rollout success_rate about 0.14-0.18, long route samples but many non-success timeouts.
- seed2: around 524k-557k, stage2, window_cost about 0.03-0.07, route window about 0.82-0.84, rollout success_rate about 0.12-0.18.
- Interpretation: both seeds show a guard_only pattern of low cost and long route completion, but weak success conversion at mid-training. This makes final held-out evaluation decisive.
- Decision: continue both to final CSV and aggregate guard_only seed0-2 before changing the main claim.

## 2026-06-30 guard_only seed0-2 aggregate completed
- Time: 2026-06-30T19:53:00.
- Aggregate root: outputs/tuned_ablation_guard_only_nenv16_aggregate.
- Files: summary_by_seed.csv, mean_by_density.csv, std_by_density.csv, compare_to_full_proposed_mean.csv, DECISION.md.
- Guard_only d0.00 mean: success=0.973 cost=0.000 route=0.990.
- Guard_only d0.08 mean: success=0.873 cost=0.093 collision=0.093 out=0.000 route=0.940.
- Guard_only d0.15 mean: success=0.633 cost=0.207 collision=0.200 out=0.007 route=0.868.
- Comparison to full proposed aggregate: at d0.15 guard_only is +0.013 success, -0.040 cost, +0.003 route, -0.033 collision, -0.007 out_of_road relative to current full proposed.
- Interpretation: the current full risk-reward setting does not beat guard+curriculum. The paper claim must not state that the risk reward is the dominant improvement under the current evidence.
- Decision: launch a light-risk full proposed retuning screen. Goal: retain the stability of guard_only while recovering any high-density success gain from a milder TTC/cost reward. If light-risk does not beat guard_only, reframe the main method around guard+curriculum and treat risk reward as optional/diagnostic.

## 2026-06-30 launch light-risk full proposed seed0 and seed2
- Time: 2026-06-30T19:53:49.
- Reason: guard_only seed0-2 aggregate matches/exceeds the current full proposed aggregate, so the full risk reward setting must be retuned before paper claims are frozen.
- Roots: outputs/tuning_proposed_light_risk_ttc3_cost25_lane03_nenv16_seed0_1m and outputs/tuning_proposed_light_risk_ttc3_cost25_lane03_nenv16_seed2_1m.
- Protocol: proposed seeds 0 and 2, n_envs=16, timesteps=1M, horizon=1500, ent_coef=0.01.
- Light-risk weights: ttc=3, cost=25, lane=0.3, crash=80, out=150, overspeed=3, target_speed=18, progress=40, success_bonus=55, ttc_threshold=12, stage2_success=0.50, stage2_cost=0.25, demote_cost=0.35.
- Purpose: keep guard+curriculum stability while adding milder risk shaping. Seed0 checks that the strong seed is not harmed; seed2 targets the weak seed in the current full proposed aggregate.
- Promotion rule: light-risk must beat guard_only aggregate at d0.15 or at least improve full proposed seed2 materially without hurting seed0. Otherwise the paper main line should pivot toward guard+curriculum.

## 2026-06-30 light-risk seed0/2 early config and health check
- Time: 2026-06-30T19:55:48.
- Config verified for both seeds: variant=proposed, use_risk_reward=True, use_action_guard=True, curriculum=True, n_envs=16, horizon=1500, timesteps=1M.
- Light-risk weights verified: ttc=3, cost=25, lane=0.3, crash=80, out=150, target_speed=18, progress=40, success_bonus=55.
- seed0 around 246k: stage1, window_cost about 0.03, route window about 0.60, rollout success_rate about 0.10. It is slower than guard_only but not collapsed.
- seed2 around 246k: still stage0, window_success=0, route window about 0.44, cost fluctuating but not catastrophic. This is weaker than desired and must be watched closely.
- Decision: continue to 500k before judging. If seed2 remains stage0/zero-success at 500k, light-risk is likely not solving the weak-seed issue.

## 2026-06-30 light-risk full proposed seed0/2 completed and rejected as main setting
- Time: 2026-06-30T20:15:44+08:00.
- Aggregate root: outputs/tuning_proposed_light_risk_ttc3_cost25_lane03_nenv16_aggregate.
- Files: summary_by_seed.csv, mean_by_density.csv, std_by_density.csv, compare_to_full_proposed_mean.csv, compare_to_guard_only_mean.csv, DECISION.md.
- Final seed0: d0.00 success=0.98 cost=0.00 route=0.991; d0.08 success=0.90 cost=0.06 collision=0.06 route=0.956; d0.15 success=0.64 cost=0.28 collision=0.26 out=0.02 route=0.859.
- Final seed2: d0.00 success=0.96 cost=0.00 route=0.990; d0.08 success=0.86 cost=0.12 collision=0.12 route=0.930; d0.15 success=0.52 cost=0.30 collision=0.30 out=0.00 route=0.821.
- Light-risk mean over seeds 0 and 2: d0.00 success=0.970 cost=0.000 route=0.990; d0.08 success=0.880 cost=0.090 route=0.943; d0.15 success=0.580 cost=0.290 collision=0.280 out=0.010 route=0.840.
- Comparison to guard_only 3-seed aggregate: at d0.08 light-risk is roughly comparable/slightly higher success, but at d0.15 it is worse (success 0.580 vs 0.633, cost 0.290 vs 0.207, collision 0.280 vs 0.200, route 0.840 vs 0.868).
- Comparison to current full proposed 3-seed aggregate: light-risk improves d0.08 but worsens d0.15 (success 0.580 vs 0.620, cost 0.290 vs 0.247, route 0.840 vs 0.865).
- Interpretation: milder TTC/cost/lane risk shaping did not solve the high-density weak-seed issue. The current evidence still says guard+curriculum is the robust mechanism; risk reward is not ready to be claimed as the dominant gain.
- Decision: do not promote this light-risk full setting. Run missing reward-component ablations next (`proposed_wo_lane`, `proposed_wo_smooth`) under the tuned full-proposed protocol, with CLI overrides chosen so the intended zeroed reward terms are not accidentally restored.

## 2026-06-30 launch reward-component ablations wo_lane and wo_smooth seed0
- Time: 2026-06-30T20:17:25+08:00.
- Roots: outputs/tuned_ablation_wo_lane_nenv16_seed0_1m and outputs/tuned_ablation_wo_smooth_nenv16_seed0_1m.
- Protocol: n_envs=16, timesteps=1M, horizon=1500, EPISODES=50, DEVICE=cuda, ent_coef=0.01, stage2_success=0.50, stage2_cost=0.25, demote_cost=0.35.
- Shared tuned full-proposed weights: ttc=6, cost=50, overspeed=3, target_speed=18, progress=40, success_bonus=55, crash=120, out_of_road=150, ttc_threshold=12.
- proposed_wo_lane config verified: variant=proposed_wo_lane, use_risk_reward=True, use_action_guard=True, curriculum=True, lane=0.0, smooth=0.02, accel=0.01.
- proposed_wo_smooth config verified: variant=proposed_wo_smooth, use_risk_reward=True, use_action_guard=True, curriculum=True, lane=1.0, smooth=0.0, accel=0.0.
- Early health at about 82k: both runs alive on GPU, still stage0 with success=0 and low route completion. This is treated as normal cold start; next checkpoint is around 250k before intervention.
- Purpose: complete reward-component ablations without accidentally restoring the ablated CLI weights. These results will support whether lane keeping and smoothness terms are material or mostly cosmetic relative to TTC/cost/guard/curriculum.

## 2026-06-30 reward-component ablations monitor at ~350k
- Time: 2026-06-30T20:19:59+08:00.
- proposed_wo_lane: around 344k, stage1, window_success about 0.30, rollout success_rate about 0.35, route window about 0.62, window_cost about 0.17. It is learning despite lane=0, but lane_deviation is visibly high in samples (about 0.4-1.0), so final eval should reveal whether lane reward mainly improves tracking/stability rather than raw success.
- proposed_wo_smooth: around 393k, still stage0, window_success=0, route window about 0.23, speed about 1.5 km/h, no cost yet. This looks like a real ablation degradation from removing smooth/accel regularization, not a launch/config failure.
- Decision: do not tune or rescue these ablations mid-run, because the purpose is to measure component removal under the same tuned full-proposed protocol. Continue to final held-out summary.csv and then decide whether to replicate with more seeds.

## 2026-06-30 reward-component ablation seed0 completed
- Time: 2026-06-30T20:35:35+08:00.
- Aggregate root: outputs/tuned_reward_component_ablation_seed0_aggregate.
- Files: seed0_component_ablation_summary.csv, deltas_vs_full_seed0.csv, DECISION.md.
- full_proposed seed0 d0.15: success=0.70, cost=0.24, collision=0.22, route=0.872.
- wo_ttc seed0 d0.15: success=0.44, cost=0.54, collision=0.54, route=0.743.
- wo_lane seed0 d0.15: success=0.60, cost=0.28, collision=0.28, route=0.862, lane_deviation=0.348.
- wo_smooth seed0 d0.15: success=0.58, cost=0.24, collision=0.24, route=0.849.
- Interpretation: TTC removal is the strongest reward-term degradation; lane removal mainly harms lateral tracking and high-density safety/success; smooth/accel removal weakens high-density success and training conversion but is less catastrophic than expected from mid-run.
- Decision: replicate at least wo_ttc beyond seed0 and add shield_only seed0 next. Do not overclaim reward terms from a single-seed table.

## 2026-06-30 launch wo_ttc seed1 and shield_only seed0
- Time: 2026-06-30T20:37:50+08:00.
- Roots: outputs/tuned_ablation_wo_ttc_nenv16_seed1_1m and outputs/tuned_compare_shield_only_nenv16_seed0_1m.
- proposed_wo_ttc seed1 config verified: use_risk_reward=True, use_action_guard=True, curriculum=True, n_envs=16, horizon=1500, timesteps=1M, ttc=0.0, lane=1.0, cost=50, crash=120, out=150.
- shield_only seed0 config verified: use_risk_reward=False, use_action_guard=True, curriculum=False, n_envs=16, horizon=1500, timesteps=1M.
- Early health: both alive on GPU. proposed_wo_ttc is still stage0/cold-start around 115k. shield_only has no curriculum and already shows the expected low-speed/low-route pattern: route about 0.06-0.07, success=0, one out-of-road sample.
- Purpose: replicate the strongest reward-term negative effect beyond seed0 and isolate whether the action guard alone can work without curriculum.
- Decision: continue both to final evaluation; do not tune shield_only because its role is a mechanism control, not a candidate method.

## 2026-06-30 wo_ttc seed1 and shield_only seed0 completed
- Time: 2026-06-30T21:00:21+08:00.
- wo_ttc aggregate root: outputs/tuned_ablation_wo_ttc_nenv16_seed0_seed1_aggregate.
- proposed_wo_ttc seed1 d0.15: success=0.66, cost=0.20, collision=0.20, route=0.905. This contradicts the seed0-only interpretation that TTC removal always collapses high-density performance.
- proposed_wo_ttc seed0-1 mean d0.15: success=0.550, cost=0.370, collision=0.370, route=0.824.
- shield_only seed0: d0.00 success=1.00 cost=0.00 route=0.992; d0.08 success=0.96 cost=0.04 collision=0.02 out=0.02 route=0.975; d0.15 success=0.56 cost=0.32 collision=0.32 out=0.00 route=0.833.
- Interpretation: action guard alone is a major mechanism and is very strong up to medium density, but high-density safety/success still lags guard_only/full. TTC reward contribution is high-variance across seeds and must not be overclaimed from seed0.
- Decision: launch proposed_wo_ttc seed2 and shield_only seed1 next. This resolves TTC variance and checks shield_only stability.

## 2026-06-30 launch wo_ttc seed2 and shield_only seed1
- Time: 2026-06-30T21:02:21+08:00.
- Roots: outputs/tuned_ablation_wo_ttc_nenv16_seed2_1m and outputs/tuned_compare_shield_only_nenv16_seed1_1m.
- proposed_wo_ttc seed2 config verified: use_risk_reward=True, use_action_guard=True, curriculum=True, n_envs=16, horizon=1500, timesteps=1M, ttc=0.0, lane=1.0, cost=50, crash=120, out=150.
- shield_only seed1 config verified: use_risk_reward=False, use_action_guard=True, curriculum=False, n_envs=16, horizon=1500, timesteps=1M.
- Early health: both runs alive on GPU. proposed_wo_ttc seed2 is cold-start stage0 around 131k. shield_only seed1 is still early and shows lower stability than seed0 with out-of-road samples; this is not yet a final judgement.
- Purpose: resolve the high variance between wo_ttc seed0 and seed1, and test whether shield_only seed0's strong medium-density result is seed-stable.


## 2026-06-30 wo_ttc seed2 completed and three-seed aggregate written
- Time: 2026-06-30T21:20:19+08:00.
- New aggregate root: outputs/tuned_ablation_wo_ttc_nenv16_seed0_seed1_seed2_aggregate.
- Files: summary_by_seed.csv, mean_by_density.csv, std_by_density.csv, compare_to_full_proposed_mean.csv, compare_to_guard_only_mean.csv, DECISION.md.
- proposed_wo_ttc seed2 final: d0.00 success=0.96 cost=0.00 route=0.990; d0.08 success=0.96 cost=0.04 collision=0.04 route=0.959; d0.15 success=0.52 cost=0.34 collision=0.34 route=0.821.
- Three-seed wo_ttc mean: d0.00 success=0.987 cost=0.000 route=0.991; d0.08 success=0.900 cost=0.067 collision=0.067 route=0.950; d0.15 success=0.540 cost=0.360 collision=0.360 route=0.823.
- Comparison to full proposed aggregate at d0.15: success 0.540 vs 0.620, cost 0.360 vs 0.247, route 0.823 vs 0.865. Removing TTC is worse on average in dense traffic.
- Comparison to guard_only aggregate at d0.15: success 0.540 vs 0.633, cost 0.360 vs 0.207, route 0.823 vs 0.868. The TTC-ablated full method is also weaker than guard+curriculum in dense traffic.
- Interpretation: TTC reward contribution is high-variance but negative when removed at d0.15. Claim boundary: TTC reward helps dense-traffic robustness on average; do not claim it is universally necessary or that risk reward dominates guard+curriculum.
- Active run still in progress: outputs/tuned_compare_shield_only_nenv16_seed1_1m. Current decision is to wait for shield_only seed1 before starting shield_only seed2 or additional reward ablation seeds.

## 2026-06-30 shield_only seed1 completed and seed0-1 interim aggregate written
- Time: 2026-06-30T21:25:29+08:00.
- New aggregate root: outputs/tuned_compare_shield_only_nenv16_seed0_seed1_aggregate.
- Files: summary_by_seed.csv, mean_by_density.csv, std_by_density.csv, compare_to_full_proposed_mean.csv, compare_to_guard_only_mean.csv, DECISION.md.
- shield_only seed1 final: d0.00 success=0.98 cost=0.00 route=0.991; d0.08 success=0.92 cost=0.08 collision=0.06 out=0.02 route=0.944; d0.15 success=0.56 cost=0.22 collision=0.22 route=0.867.
- shield_only seed0-1 mean: d0.00 success=0.990 cost=0.000 route=0.991; d0.08 success=0.940 cost=0.060 collision=0.040 out=0.020 route=0.960; d0.15 success=0.560 cost=0.270 collision=0.270 route=0.850.
- Interpretation: action guard alone is seed-stable enough to require a seed2 follow-up. It is very strong at easy/medium densities and still meaningful at high density, though high-density success remains below full proposed/guard_only means.
- Decision: launch shield_only seed2 next. Also begin proposed_wo_lane seed1 while the GPU is free, because lane reward ablation currently has only seed0 evidence.

## 2026-06-30 launch/config check shield_only seed2 and wo_lane seed1
- Time: 2026-06-30T21:27:13+08:00.
- Active roots: outputs/tuned_compare_shield_only_nenv16_seed2_1m and outputs/tuned_ablation_wo_lane_nenv16_seed1_1m.
- Launch protocol: n_envs=16, timesteps=1M, horizon=1500, EPISODES=50, DEVICE=cuda, ent_coef=0.01.
- shield_only seed2 config verified: variant=shield_only, seed=2, use_risk_reward=False, use_action_guard=True, curriculum=False. This completes the planned third seed for the action-guard-only mechanism control.
- proposed_wo_lane seed1 config verified: variant=proposed_wo_lane, seed=1, use_risk_reward=True, use_action_guard=True, curriculum=True, reward_weights.lane=0.0, ttc=6.0, smooth=0.02, accel=0.01, cost=50.0, crash=120.0, out=150.0.
- Early health: both processes alive. shield_only seed2 is in normal cold-start low-speed/low-route behavior. wo_lane seed1 shows high lane deviation/out-of-road risk early, which is expected for lane reward removal and should not be rescued mid-run unless it becomes a launch/config failure.
- Next checkpoint: inspect around 250k-350k timesteps for stage transition, cost window, and route/success trend; do not retune these controls before final evaluation unless the run crashes or config is wrong.

## 2026-06-30 mid-run health shield_only seed2 and wo_lane seed1
- Time: 2026-06-30T21:31:54+08:00.
- shield_only seed2 around 344k: no config/process issue; success_rate about 0.30, route samples up to about 0.99, some out-of-road/cost remains. This matches the seed0/1 recovery pattern and should continue to final evaluation.
- proposed_wo_lane seed1 around 623k: reached curriculum stage2, window_success about 0.30, window_cost about 0.067, window_route about 0.82. Lane deviation remains high in samples (roughly 0.38-0.50 recently, max up to 2.0), which is expected evidence for lane reward removal rather than a launch failure.
- Decision: continue both runs unchanged. No reward rescue or retune before final summaries because both are mechanism/ablation controls.

## 2026-06-30 wo_lane seed1 completed and seed0-1 aggregate written
- Time: 2026-06-30T21:43:33+08:00.
- New aggregate root: outputs/tuned_ablation_wo_lane_nenv16_seed0_seed1_aggregate.
- Files: summary_by_seed.csv, mean_by_density.csv, std_by_density.csv, compare_to_full_proposed_mean.csv, DECISION.md.
- proposed_wo_lane seed1 final: d0.00 success=0.88 cost=0.00 route=0.987 lane_dev=0.347; d0.08 success=0.90 cost=0.10 collision=0.10 route=0.971 lane_dev=0.322; d0.15 success=0.62 cost=0.28 collision=0.28 route=0.856 lane_dev=0.340.
- wo_lane seed0-1 mean: d0.00 success=0.940 cost=0.000 route=0.990 lane_dev=0.347; d0.08 success=0.900 cost=0.080 collision=0.080 route=0.964 lane_dev=0.341; d0.15 success=0.610 cost=0.280 collision=0.280 route=0.859 lane_dev=0.344.
- Interpretation: lane reward removal is seed-stable. It does not collapse success, but it consistently produces much higher lane deviation and slightly worse high-density cost/route than full proposed.
- Decision: do not tune wo_lane. Next reward-component replication priority is proposed_wo_smooth seed1, while shield_only seed2 continues to final evaluation.

## 2026-06-30 launch/config check wo_smooth seed1
- Time: 2026-06-30T21:44:26+08:00.
- Root: outputs/tuned_ablation_wo_smooth_nenv16_seed1_1m.
- Launch protocol: proposed_wo_smooth seed1, n_envs=16, timesteps=1M, horizon=1500, EPISODES=50, DEVICE=cuda, ent_coef=0.01.
- Config verified: use_risk_reward=True, use_action_guard=True, curriculum=True, reward_weights.ttc=6.0, lane=1.0, smooth=0.0, accel=0.0, cost=50.0, crash=120.0, out=150.0.
- Early health: alive, stage0/cold-start, success_rate=0. This is expected for a new reward-component ablation and should not be rescued before mid-run evidence.
- Active concurrent run: shield_only seed2 is still training and should be evaluated/aggregated when complete.

## 2026-06-30 shield_only seed2 completed and three-seed aggregate written
- Time: 2026-06-30T21:50:06+08:00.
- New aggregate root: outputs/tuned_compare_shield_only_nenv16_seed0_seed1_seed2_aggregate.
- Files: summary_by_seed.csv, mean_by_density.csv, std_by_density.csv, compare_to_full_proposed_mean.csv, compare_to_guard_only_mean.csv, DECISION.md.
- shield_only seed2 final: d0.00 success=1.00 cost=0.00 route=0.992; d0.08 success=0.86 cost=0.08 collision=0.06 out=0.02 route=0.958; d0.15 success=0.76 cost=0.14 collision=0.14 route=0.913.
- shield_only seed0-2 mean: d0.00 success=0.993 cost=0.000 route=0.992; d0.08 success=0.913 cost=0.067 collision=0.047 out=0.020 route=0.959; d0.15 success=0.627 cost=0.227 collision=0.227 route=0.871.
- Comparison to full proposed aggregate at d0.15: shield_only success 0.627 vs full 0.620, cost 0.227 vs 0.247, route 0.871 vs 0.865. Action guard alone matches/slightly exceeds the current full proposed mean.
- Comparison to guard_only at d0.15: shield_only success 0.627 vs guard_only 0.633, cost 0.227 vs 0.207, route 0.871 vs 0.868. Shield-only is close to guard+curriculum.
- Interpretation: action guard is the dominant verified mechanism. Current results do not support a risk-reward-dominant paper claim. Risk/reward components should be framed as high-density refinements unless a new retuned full variant clearly improves beyond shield/guard.
- Active run: proposed_wo_smooth seed1 continues; wait for final summary and aggregate with seed0.

## 2026-06-30 launch/config check proposed retune ttc4-cost10-lane1 seed2
- Time: 2026-06-30T21:51:22+08:00.
- Root: outputs/retune_proposed_ttc4_cost10_lane1_nenv16_seed2_1m.
- Rationale: shield_only three-seed aggregate matches/slightly exceeds current full proposed, so a conservative retune is needed. This candidate preserves action guard/curriculum/lane stability while reducing risk-reward aggressiveness.
- Protocol: proposed seed2, n_envs=16, timesteps=1M, horizon=1500, EPISODES=50, DEVICE=cuda, ent_coef=0.01.
- Config verified: use_risk_reward=True, use_action_guard=True, curriculum=True, reward_weights.ttc=4.0, lane=1.0, smooth=0.02, accel=0.01, cost=10.0, crash=100.0, out=150.0, ttc_threshold=12.0.
- Evaluation rule: this candidate is only useful if seed2 improves over the current full proposed seed2 and approaches shield_only seed2 at d0.15 without hurting d0.00/d0.08. Otherwise keep the paper claim pivot toward action guard dominance.
- Active concurrent run: proposed_wo_smooth seed1 continues.

## 2026-06-30 mid-run health wo_smooth seed1 and retune seed2
- Time: 2026-06-30T21:57:05+08:00.
- proposed_wo_smooth seed1 around 967k: still training near the end, stage2, success_rate about 0.10, window_success about 0.167, window_cost about 0.10, route window about 0.785. This looks weaker than desired and may confirm that removing smooth/accel harms training stability, but final held-out evaluation is required.
- retune proposed ttc4-cost10-lane1 seed2 around 623k: reached stage2, window_success about 0.333, window_cost about 0.10, window_route about 0.791. It is not collapsed and appears healthier than the original weak full-proposed seed2 at comparable mid-run points, but final d0.15 evaluation against shield_only seed2 is the gate.
- Decision: continue both unchanged. Do not promote retune until formal summary.csv exists.

## 2026-06-30 wo_smooth seed1 completed and seed0-1 aggregate written
- Time: 2026-06-30T22:03:11+08:00.
- New aggregate root: outputs/tuned_ablation_wo_smooth_nenv16_seed0_seed1_aggregate.
- Files: summary_by_seed.csv, mean_by_density.csv, std_by_density.csv, compare_to_full_proposed_mean.csv, DECISION.md.
- proposed_wo_smooth seed1 final: d0.00 success=1.00 cost=0.00 route=0.991; d0.08 success=0.80 cost=0.18 collision=0.16 out=0.02 route=0.879; d0.15 success=0.48 cost=0.42 collision=0.40 out=0.02 route=0.736.
- wo_smooth seed0-1 mean: d0.00 success=0.990 cost=0.000 route=0.990; d0.08 success=0.820 cost=0.160 collision=0.150 out=0.010 route=0.909; d0.15 success=0.530 cost=0.330 collision=0.320 out=0.010 route=0.792.
- Interpretation: removing smooth/accel materially hurts stability and high-density evaluation. Smooth/accel terms are not the dominant mechanism, but they should remain in the full setting.
- Decision: continue retune proposed ttc4-cost10-lane1 seed2 to final evaluation before launching more experiments.

## 2026-06-30 proposed retune ttc4-cost10-lane1 seed2 completed and promoted to multi-seed candidate
- Time: 2026-06-30T22:11:54+0800.
- Root: outputs/retune_proposed_ttc4_cost10_lane1_nenv16_seed2_1m.
- Protocol: proposed seed2, n_envs=16, 1M steps, horizon=1500, EPISODES=50, reward ttc=4, cost=10, lane=1, smooth=0.02, accel=0.01, crash=100, out=150.
- Formal final: d0.00 success=1.00 cost=0.00 route=0.991; d0.08 success=0.86 cost=0.10 route=0.951; d0.15 success=0.68 cost=0.16 collision=0.14 out=0.02 route=0.871.
- Compared with old full-proposed seed2 at d0.15: success improves 0.48 -> 0.68, cost 0.32 -> 0.16, route 0.826 -> 0.871.
- Compared with shield_only seed2 at d0.15: still lower success/route (0.68/0.871 vs 0.76/0.913), but better than current full-proposed seed2 and competitive with shield_only three-seed mean.
- Decision: promote to multi-seed candidate and launch seed0/seed1. Do not claim final method superiority until the three-seed aggregate exists.

## 2026-06-30 launch retune proposed ttc4-cost10-lane1 seed0/seed1
- Time: 2026-06-30T22:13:15+0800.
- Roots: outputs/retune_proposed_ttc4_cost10_lane1_nenv16_seed0_1m and outputs/retune_proposed_ttc4_cost10_lane1_nenv16_seed1_1m.
- Protocol: variant=proposed, seeds=0/1, n_envs=16, timesteps=1M, horizon=1500, EPISODES=50, DEVICE=cuda.
- Reward args: ent_coef=0.01, ttc=4, cost=10, overspeed=3, target_speed=18, progress=40, lane=1.0, success_bonus=55, crash_penalty=100, out_of_road_penalty=150, ttc_threshold=12, stage2_success=0.50, stage2_cost=0.25, demote_cost=0.35.
- Purpose: complete the three-seed stability test for the promising retuned full-proposed candidate after seed2 improved the weak original full-proposed seed2.
- Early launch check: processes alive; formal config verification to follow after config files are fully written.

## 2026-06-30 retune proposed ttc4-cost10-lane1 seed0/1 completed and three-seed aggregate written
- Time: 2026-06-30T22:32:54+0800.
- New aggregate root: outputs/retune_proposed_ttc4_cost10_lane1_nenv16_seed0_seed1_seed2_aggregate.
- Files: summary_by_seed.csv, mean_by_density.csv, std_by_density.csv, compare_to_full_proposed_mean.csv, compare_to_guard_only_mean.csv, compare_to_shield_only_mean.csv, DECISION.md.
- seed0 final: d0.00 success=0.94 cost=0.00 route=0.991 lane_dev=0.071; d0.08 success=0.98 cost=0.02 route=0.986 lane_dev=0.081; d0.15 success=0.56 cost=0.26 route=0.819 lane_dev=0.118.
- seed1 final: d0.00 success=0.96 cost=0.00 route=0.991 lane_dev=0.263; d0.08 success=0.82 cost=0.10 route=0.923 lane_dev=0.273; d0.15 success=0.62 cost=0.30 route=0.869 lane_dev=0.359.
- three-seed mean: d0.00 success=0.967 cost=0.000 route=0.991; d0.08 success=0.887 cost=0.073 route=0.953; d0.15 success=0.620 cost=0.240 route=0.853 lane_dev=0.207.
- Interpretation: medium-density result improves over old full proposed, but high-density mean does not beat shield_only or guard_only and lane deviation worsens, especially seed1. Do not promote as final main method.
- Next tuning direction: keep lower risk penalty but strengthen lateral/smooth regularization, or formally pivot claims toward action-guard dominance if the next candidate fails.

## 2026-06-30 launch lateral/smooth retune ttc4-cost10-lane2-smooth004-accel002 seed1/seed2
- Time: 2026-06-30T22:34:02+0800.
- Roots: outputs/retune_proposed_ttc4_cost10_lane2_smooth004_accel002_nenv16_seed1_1m and outputs/retune_proposed_ttc4_cost10_lane2_smooth004_accel002_nenv16_seed2_1m.
- Protocol: proposed, seeds=1/2, n_envs=16, timesteps=1M, horizon=1500, EPISODES=50, DEVICE=cuda.
- Reward args: ent_coef=0.01, ttc=4, cost=10, lane=2.0, smooth=0.04, accel=0.02, overspeed=3, target_speed=18, progress=40, success_bonus=55, crash_penalty=100, out_of_road_penalty=150, ttc_threshold=12.
- Rationale: previous ttc4-cost10-lane1 aggregate improved d0.08 but failed to beat guard/shield at d0.15 and had high lane deviation, especially seed1. This run tests whether stronger lateral/smooth regularization fixes that failure without losing seed2 high-density behavior.
- Gate: promote only if seed1 lane deviation drops materially and d0.15 success/route/cost improve without seed2 collapsing.

## 2026-06-30 abort lateral/smooth retune lane2-smooth004-accel002 seed1/seed2
- Time: 2026-06-30T22:38:56+0800.
- Roots: outputs/retune_proposed_ttc4_cost10_lane2_smooth004_accel002_nenv16_seed1_1m and seed2_1m.
- Abort reason: mid-run evidence showed severe progress suppression. At about 524k/540k timesteps both runs remained in stage0 with window_route_completion about 0.10/0.09 and success_rate 0. This is much worse than the preceding ttc4-cost10-lane1 retune, which had already reached stage1/2 by this point.
- Diagnosis: lane=2.0 plus smooth=0.04/accel=0.02 over-regularizes motion and should not be completed as a formal candidate.
- Decision: stop these diagnostic runs and launch a gentler lateral retune instead: lane around 1.25, smooth 0.03, accel 0.015, with slightly higher progress reward to preserve motion.

## 2026-06-30 launch moderate lateral retune ttc4-cost10-lane125-smooth003-accel0015-progress45 seed1/seed2
- Time: 2026-06-30T22:39:26+0800.
- Roots: outputs/retune_proposed_ttc4_cost10_lane125_smooth003_accel0015_progress45_nenv16_seed1_1m and seed2_1m.
- Protocol: proposed, seeds=1/2, n_envs=16, timesteps=1M, horizon=1500, EPISODES=50, DEVICE=cuda.
- Reward args: ent_coef=0.01, ttc=4, cost=10, lane=1.25, smooth=0.03, accel=0.015, progress=45, overspeed=3, target_speed=18, success_bonus=55, crash_penalty=100, out_of_road_penalty=150, ttc_threshold=12.
- Rationale: lane2/smooth004 over-regularized and suppressed progress; this is a gentler lateral-stability retune with extra progress reward to preserve motion.
- Gate: seed1 must reduce lane deviation versus lane1 retune without losing d0.15 success/route; seed2 must remain competitive with its previous d0.15 result.

## 2026-06-30 moderate lateral retune seed1/seed2 diagnostic aggregate completed
- Time: 2026-06-30T23:00:54+0800.
- Aggregate root: outputs/retune_proposed_ttc4_cost10_lane125_smooth003_accel0015_progress45_nenv16_seed1_seed2_diagnostic_aggregate.
- Files: summary_by_seed.csv, mean_by_density.csv, std_by_density.csv, compare_to_lane1_same_seeds.csv, compare_to_lane1_seed1_seed2_mean.csv, compare_to_guard_only_mean.csv, compare_to_shield_only_mean.csv, DECISION.md.
- seed1 final: d0.00 success=0.98 cost=0.00 route=0.990 lane_dev=0.060; d0.08 success=0.88 cost=0.12 route=0.945 lane_dev=0.072; d0.15 success=0.64 cost=0.28 route=0.849 lane_dev=0.102.
- seed2 final: d0.00 success=0.98 cost=0.00 route=0.989 lane_dev=0.101; d0.08 success=0.88 cost=0.08 route=0.969 lane_dev=0.126; d0.15 success=0.62 cost=0.28 route=0.852 lane_dev=0.198.
- Two-seed mean: d0.00 success=0.980 cost=0.000 route=0.990 lane_dev=0.081; d0.08 success=0.880 cost=0.100 route=0.957 lane_dev=0.099; d0.15 success=0.630 cost=0.280 route=0.850 lane_dev=0.150.
- Interpretation: seed1 lateral instability is repaired, but seed2 high-density robustness degrades versus lane1. This candidate fails the promotion gate; do not run seed0.
- Next action: stop risk/lane reward-only retuning for now and test guard-centered/threshold-centered variants, since repeated full-risk retunes do not beat guard_only or shield_only.

## 2026-06-30 launch guard-centered guard_only ttc13/v18 seed1/seed2
- Time: 2026-06-30T23:02:49+0800.
- Roots: outputs/retune_guard_only_ttc13_v18_nenv16_seed1_1m and outputs/retune_guard_only_ttc13_v18_nenv16_seed2_1m.
- Protocol: variant=guard_only, seeds=1/2, n_envs=16, timesteps=1M, horizon=1500, EPISODES=50, DEVICE=cuda.
- Active mechanism: use_action_guard=True, use_risk_reward=False, curriculum=True. Because risk reward is disabled, reward penalty weights are protocol records; behavior-relevant guard parameters are ttc_threshold=13 and target_speed=18.
- Rationale: repeated full-risk/lane retunes failed to beat guard_only/shield_only. A mild guard threshold shift tests whether action-guard-centered tuning can lower high-density cost without the instability previously observed for full-proposed ttc14/v18.
- Gate: promote only if seed1/seed2 keep d0.08 success near guard_only and improve d0.15 cost/route versus guard_only same seeds. Abort or reject if training suppresses route progress or seed2 worsens materially.

## 2026-06-30 guard_only ttc13/v18 config verification
- Time: 2026-06-30T23:03:52+0800.
- Verified both seed1 and seed2 configs: variant=guard_only, n_envs=16, horizon=1500, timesteps=1M, ent_coef=0.01, use_action_guard=True, use_risk_reward=False, curriculum=True.
- Verified behavior-relevant guard parameters: reward_weights.ttc_threshold=13.0 and target_speed_kmh=18.0. Stage gates: stage2_success=0.50, stage2_cost=0.25, demote_cost=0.35.
- Early health around 82k: both processes alive; stage0/warmup route progress present, no launch/config mismatch.

## 2026-06-30 guard_only ttc13/v18 monitor at ~278k
- Time: 2026-06-30T23:06:15+0800.
- seed1 around 278k: stage2, window_success about 0.30-0.35, window_cost about 0.067, window_route about 0.776, rollout success_rate about 0.35. One sampled out_of_road episode appeared, but route progress is healthy.
- seed2 around 278k: stage2, window_success about 0.30, window_cost about 0.133, window_route about 0.855, rollout success_rate about 0.26.
- Decision: continue unchanged. This does not show the progress-suppression failure seen in the over-regularized lane2 run. Final held-out d0.08/d0.15 remains the gate.

## 2026-06-30 guard_only ttc13/v18 monitor at ~410k
- Time: 2026-06-30T23:09:45+0800.
- seed1 around 410k: stage2, window_cost about 0.033, window_route_completion about 0.808, window_success about 0.000-0.033, recent route samples 0.874-0.975, rollout success_rate about 0.02-0.03.
- seed2 around 410k: stage3, window_cost about 0.10, window_route_completion about 0.726, window_success about 0.033, recent route samples 0.533-0.813.
- Interpretation: progress is not suppressed and cost is not exploding, but success window is weak in the middle. Continue unchanged; final held-out evaluation is required before accepting/rejecting ttc13.

## 2026-06-30 guard_only ttc13/v18 monitor at ~600k
- Time: 2026-06-30T23:14:09+0800.
- seed1 around 606k-623k: stage2, window_cost about 0.000, window_route_completion about 0.838-0.847, window_success about 0.133-0.233, rollout success_rate about 0.20.
- seed2 around 590k-606k: stage2, window_cost about 0.000-0.033, window_route_completion about 0.838-0.841, window_success about 0.133-0.267, rollout success_rate about 0.22-0.24. One sampled collision appeared, but the rolling cost window remained low.
- Decision: continue to formal evaluation. ttc13 is not showing obvious training collapse; final d0.15 cost/route versus guard_only same seeds will decide.

## 2026-06-30 guard_only ttc13/v18 near-end training monitor
- Time: 2026-06-30T23:21:35+0800.
- seed1 around 950k-983k: stage2, window_cost 0.000-0.033, window_route about 0.789-0.835, rollout success_rate about 0.10-0.12.
- seed2 around 934k-967k: stage2, window_cost 0.067-0.100, window_route about 0.770-0.810, rollout success_rate about 0.20-0.23, with a sampled collision near 967k.
- Interpretation: no route/cost collapse, but success windows remain weak. Wait for formal evaluation before deciding; likely gate is whether d0.15 cost reduction compensates for possible success loss.

## 2026-06-30 guard_only ttc13/v18 seed1/seed2 diagnostic aggregate completed
- Time: 2026-06-30T23:28:54+0800.
- Aggregate root: outputs/retune_guard_only_ttc13_v18_nenv16_seed1_seed2_diagnostic_aggregate.
- Files: summary_by_seed.csv, mean_by_density.csv, std_by_density.csv, compare_to_guard_only_same_seeds.csv, compare_to_guard_only_seed1_seed2_mean.csv, compare_to_guard_only_three_seed_mean.csv, compare_to_shield_only_three_seed_mean.csv, DECISION.md.
- seed1 final: d0.00 success=0.98 cost=0.00 route=0.990; d0.08 success=0.84 cost=0.08 route=0.954; d0.15 success=0.58 cost=0.20 route=0.857.
- seed2 final: d0.00 success=0.98 cost=0.00 route=0.989; d0.08 success=0.84 cost=0.16 route=0.929; d0.15 success=0.62 cost=0.16 route=0.886.
- Two-seed mean: d0.00 success=0.980 cost=0.000 route=0.990; d0.08 success=0.840 cost=0.120 route=0.941; d0.15 success=0.600 cost=0.180 route=0.872.
- Decision: do not run seed0. ttc13 is mixed parameter-sensitivity evidence, not a promoted guard-centered setting. Default guard_only ttc12/v18 remains the cleaner action-guard baseline.

## 2026-06-30 launch guard-centered guard_only ttc12/v19 seed1/seed2
- Time: 2026-06-30T23:29:27+0800.
- Roots: outputs/retune_guard_only_ttc12_v19_nenv16_seed1_1m and outputs/retune_guard_only_ttc12_v19_nenv16_seed2_1m.
- Protocol: variant=guard_only, seeds=1/2, n_envs=16, timesteps=1M, horizon=1500, EPISODES=50, DEVICE=cuda.
- Active mechanism: use_action_guard=True, use_risk_reward=False, curriculum=True. Behavior-relevant guard parameters: ttc_threshold=12, target_speed=19.
- Rationale: ttc13/v18 reduced some seed2 high-density cost but hurt seed1 and d0.08 success. This orthogonal branch keeps the accepted TTC threshold and relaxes only the overspeed guard target to test whether d0.15 success/route can improve without a large cost penalty.
- Gate: promote only if seed1/seed2 improve d0.15 success or route versus guard_only ttc12/v18 same seeds while keeping d0.08 success/cost close. Reject if high-density cost increases materially or d0.08 degrades.

## 2026-06-30 guard_only ttc12/v19 config verification
- Time: 2026-06-30T23:30:30+0800.
- Verified both seed1 and seed2 configs: variant=guard_only, n_envs=16, horizon=1500, timesteps=1M, ent_coef=0.01, use_action_guard=True, use_risk_reward=False, curriculum=True.
- Verified behavior-relevant guard parameters: reward_weights.ttc_threshold=12.0 and target_speed_kmh=19.0. Stage gates: stage2_success=0.50, stage2_cost=0.25, demote_cost=0.35.
- Early health around 82k: both processes alive; warmup has route progress but sampled out_of_road episodes. Too early to judge; continue to stage transition checks.

## 2026-06-30 guard_only ttc12/v19 monitor at ~300k
- Time: 2026-06-30T23:33:24+0800.
- seed1 around 295k-311k: stage2, window_cost about 0.10-0.133, window_route_completion about 0.809-0.817, window_success about 0.167-0.20, rollout success_rate about 0.28-0.30.
- seed2 around 279k-295k: reached stage3, window_cost about 0.133, window_route_completion about 0.867, window_success about 0.533, rollout success_rate about 0.31.
- Decision: continue unchanged. This branch is not stuck and seed2 is stronger than the ttc13/v18 branch at the same stage; final held-out cost will decide whether the relaxed speed guard is acceptable.

## 2026-06-30 guard_only ttc12/v19 monitor at ~786k/~655k
- Time: 2026-06-30T23:42:23+0800.
- seed1 around 786k: stage2, window_cost about 0.067, window_route_completion about 0.863, window_success about 0.267, rollout success_rate about 0.28. Latest sampled episode had collision cost, but rolling cost remains controlled; continue to final evaluation.
- seed2 around 655k: stage3, window_cost about 0.233, window_route_completion about 0.704, window_success about 0.100, rollout success_rate about 0.11. This is weaker than the early stage3 signal and close to the cost gate; continue but treat as a warning unless final held-out evaluation improves.
- Resource: CPU available about 18GiB; GPU memory used about 1.37GiB / 12.28GiB; protocol remains resource-safe.
- Decision: continue both unchanged. Do not launch seed0 or additional guard-centered runs until seed1/seed2 produce summary.csv and are compared against guard_only ttc12/v18 same seeds.

## 2026-06-30 guard_only ttc12/v19 monitor at ~934k/~754k
- Time: 2026-06-30T23:45:32+0800.
- seed1 around 934k: stage2, window_cost about 0.067, window_route_completion about 0.852, window_success about 0.300, rollout success_rate about 0.34. Latest sampled episode has no cost/collision/out-of-road and route_completion about 0.905. Seed1 is close to final and remains usable.
- seed2 around 754k: stage3, window_cost about 0.233, window_route_completion about 0.720, window_success about 0.067, rollout success_rate about 0.10. Latest sampled episode has collision cost and low route_completion about 0.273. This is a warning against promoting v19 unless final eval recovers strongly.
- Decision: continue to final summaries, but provisional judgement is mixed/weak. Do not launch v19 seed0 before seed1/seed2 final comparison.

## 2026-06-30 guard_only ttc12/v19 seed1/seed2 diagnostic aggregate completed
- Time: 2026-06-30T23:56:10+0800.
- Aggregate root: outputs/retune_guard_only_ttc12_v19_nenv16_seed1_seed2_diagnostic_aggregate.
- Files: summary_by_seed.csv, mean_by_density.csv, std_by_density.csv, compare_to_guard_only_same_seeds.csv, compare_to_guard_only_seed1_seed2_mean.csv, compare_to_guard_only_three_seed_mean.csv, compare_to_shield_only_three_seed_mean.csv, DECISION.md.
- seed1 final: d0.00 success=0.98 cost=0.00 route=0.990; d0.08 success=0.92 cost=0.06 route=0.954; d0.15 success=0.58 cost=0.28 route=0.861.
- seed2 final: d0.00 success=1.00 cost=0.00 route=0.992; d0.08 success=0.84 cost=0.16 route=0.938; d0.15 success=0.72 cost=0.26 route=0.871.
- Two-seed mean: d0.00 success=0.990 cost=0.000 route=0.991; d0.08 success=0.880 cost=0.110 route=0.946; d0.15 success=0.650 cost=0.270 route=0.866.
- Same-seed comparison to default guard_only ttc12/v18 at d0.15: success improves only 0.64 -> 0.65, cost worsens 0.20 -> 0.27, route is essentially unchanged/slightly lower 0.871 -> 0.866.
- Decision: reject target_speed=19 as final guard-centered setting; do not launch seed0. Keep default guard_only ttc12/v18 and shield_only as cleaner action-guard baselines.


## 2026-06-30 launch no_action_guard seed1/seed2 nenv16 ablation completion
- Time: 2026-06-30T23:57:05+0800.
- Roots: outputs/tuned_ablation_no_action_guard_nenv16_seed1_1m and outputs/tuned_ablation_no_action_guard_nenv16_seed2_1m.
- Protocol: variant=no_action_guard, seeds=1/2, n_envs=16, timesteps=1M, horizon=1500, EPISODES=50, DEVICE=cuda, ent_coef=0.01.
- Mechanism: use_risk_reward=True, use_action_guard=False, curriculum=True. This completes the planned three-seed evidence for the dominant action-guard ablation after seed0 collapsed.
- Gate: do not rescue/tune mid-run unless there is a launch/config failure. If both seeds reproduce high cost/low success, aggregate with seed0 and use as strong evidence that action guard is necessary.

## 2026-07-01 no_action_guard seed1/seed2 monitor at ~280k/295k
- Time: 2026-07-01T00:02:05+0800.
- seed1 around 279k: stage0, window_cost=0, window_route_completion about 0.153, window_success=0, rollout success_rate=0, mean_speed about 0.98 km/h, std about 1.01.
- seed2 around 295k: stage0, window_cost=0, window_route_completion about 0.199, window_success=0, rollout success_rate=0, mean_speed about 1.28 km/h, std about 1.00.
- Interpretation: no launch/config failure. The ablation is currently failing to form useful driving behavior rather than crashing; this is relevant mechanism evidence, so continue to final evaluation unless the process fails.
- Resource: GPU memory used about 1.36GiB / 12.28GiB; CPU available about 21GiB. Continue both unchanged.

## 2026-07-01 no_action_guard seed1/seed2 monitor at ~541k/~573k
- Time: 2026-07-01T00:04:33+0800.
- seed1 around 541k: reached stage1, window_cost=0, window_route_completion about 0.674, window_success about 0.467, rollout success_rate about 0.37, mean_speed about 11.6 km/h.
- seed2 around 573k: reached stage1, window_cost about 0.067, window_route_completion about 0.669, window_success about 0.433, rollout success_rate about 0.43, mean_speed about 10.6 km/h.
- Interpretation: unlike seed0 and the early 280k check, these seeds have recovered some driving behavior. Do not claim no_action_guard universally collapses until final held-out evaluation. Continue unchanged and aggregate with seed0 after summaries exist.

## 2026-07-01 no_action_guard seed1/seed2 monitor at ~754k/~786k
- Time: 2026-07-01T00:07:31+0800.
- seed1 around 754k: stage1, window_cost about 0.233, window_route_completion about 0.813, window_success about 0.600, rollout success_rate about 0.39. Latest sampled episode has no cost but route_completion about 0.668.
- seed2 around 786k: stage2, window_cost about 0.033, window_route_completion about 0.895, window_success about 0.667, rollout success_rate about 0.39. Latest sampled episode route_completion about 0.986.
- Interpretation: no_action_guard seed1/2 are not reproducing a simple universal collapse. The final ablation claim must be based on held-out d0.08/d0.15 cost/success and seed variance, not only seed0. Continue to final evaluation unchanged.

## 2026-07-01 no_action_guard seed0/1/2 aggregate completed
- Time: 2026-07-01T00:13:20+0800.
- Aggregate root: outputs/tuned_ablation_no_action_guard_nenv16_seed0_seed1_seed2_aggregate.
- Files: summary_by_seed.csv, mean_by_density.csv, std_by_density.csv, compare_to_full_proposed_mean.csv, compare_to_guard_only_mean.csv, compare_to_shield_only_mean.csv, DECISION.md.
- Three-seed mean: d0.00 success=0.027 cost=0.973 route=0.254; d0.08 success=0.000 cost=1.000 route=0.202; d0.15 success=0.000 cost=1.000 route=0.172.
- Failure mode: low density mostly out_of_road; medium/high density mix collision and out_of_road. seed1/2 had temporary training-window recovery, but held-out evaluation still collapsed.
- Decision: accept as three-seed no_action_guard ablation. Do not rescue/tune this ablation; action-level guard is necessary for stable held-out safety/completion under the current method.


## 2026-07-01 launch wo_lane seed2 and wo_smooth seed2 nenv16 ablation completion
- Time: 2026-07-01T00:14:10+0800.
- Roots: outputs/tuned_ablation_wo_lane_nenv16_seed2_1m and outputs/tuned_ablation_wo_smooth_nenv16_seed2_1m.
- Protocol: variants=proposed_wo_lane/proposed_wo_smooth, seed=2, n_envs=16, timesteps=1M, horizon=1500, EPISODES=50, DEVICE=cuda, ent_coef=0.01.
- Purpose: complete third seed for lane and smooth/accel reward-component ablations after seed0/1 aggregates showed high lane deviation and stability degradation respectively.
- Gate: run to final evaluation unless process/config fails; aggregate with seed0/1 after summaries exist.

## 2026-07-01 invalidated first wo_lane/wo_smooth seed2 launch due wrong ablation weights
- Time: 2026-07-01T00:16:00+0800.
- Issue: initial seed2 launches for proposed_wo_lane and proposed_wo_smooth were passed default reward weights, producing configs with lane=1.0 for wo_lane and smooth=0.02/accel=0.01 for wo_smooth, unlike seed0/seed1 where lane=0.0 or smooth=0.0/accel=0.0.
- Action: stopped the invalid process groups and archived the partial roots with INVALID_DO_NOT_USE.txt. These runs must not enter any table or aggregate.
- Fix: relaunch seed2 using explicit ablation weights: wo_lane with --reward-lane 0.0; wo_smooth with --reward-smooth 0.0 --reward-accel 0.0.

## 2026-07-01 corrected wo_lane/wo_smooth seed2 monitor at ~311k/~360k
- Time: 2026-07-01T00:18:52+0800.
- proposed_wo_lane seed2 around 311k: stage1, window_cost about 0.233, window_route_completion about 0.630, window_success=0, rollout success_rate about 0.03, lane_deviation about 0.463. This is consistent with lane-reward removal causing lateral instability; continue.
- proposed_wo_smooth seed2 around 360k: stage0, window_cost=0, window_route_completion about 0.459, window_success=0, rollout success_rate=0, mean_speed about 3.67 km/h. This is slower than desired but still making route progress; continue to 500k/750k before judging.
- Resource: GPU memory used about 1.35GiB / 12.28GiB. Continue both unchanged.

## 2026-07-01 corrected wo_lane/wo_smooth seed2 monitor at ~573k/~606k
- Time: 2026-07-01T00:21:53+0800.
- proposed_wo_lane seed2 around 573k: stage2, window_cost about 0.133, window_route_completion about 0.842, window_success about 0.300, rollout success_rate about 0.14, lane_deviation about 0.449. Lateral deviation remains high, consistent with lane-reward removal.
- proposed_wo_smooth seed2 around 606k: stage2, window_cost=0, window_route_completion about 0.865, window_success about 0.300, rollout success_rate about 0.34. This recovered from the earlier slow stage0, so final held-out metrics are needed.
- Decision: continue both unchanged to final evaluation and aggregate with seed0/1.

## 2026-07-01 wo_lane and wo_smooth seed2 completed; three-seed aggregates written
- Time: 2026-07-01T00:36:00+0800.
- Corrected seed2 runs used matching ablation weights after invalid first launch was archived.
- wo_lane aggregate root: outputs/tuned_ablation_wo_lane_nenv16_seed0_seed1_seed2_aggregate. Mean d0.15 success=0.607 cost=0.280 route=0.844 lane_dev=0.362. Decision: accept as lane-reward ablation; lane term supports lateral stability/route quality, not dominant raw success.
- wo_smooth aggregate root: outputs/tuned_ablation_wo_smooth_nenv16_seed0_seed1_seed2_aggregate. Mean d0.15 success=0.567 cost=0.287 route=0.821 lane_dev=0.245. Decision: accept as smooth/accel ablation; smooth/accel terms are stabilizers with high seed variance.
- PDF check: seed2 PDFs are under each run figures/ directory; no loose PDFs found for these runs.


## 2026-07-01 launch risk seed1/seed2 nenv16 formal comparator completion
- Time: 2026-07-01T00:37:00+0800.
- Roots: outputs/tuned_compare_risk_nenv16_seed1_1m and outputs/tuned_compare_risk_nenv16_seed2_1m.
- Protocol: variant=risk, seeds=1/2, n_envs=16, timesteps=1M, horizon=1500, EPISODES=50, DEVICE=cuda, ent_coef=0.01.
- Purpose: complete the risk-only comparator after seed0 produced near-zero route/success. This tests whether risk reward alone is enough or whether action guard/curriculum mechanisms dominate.
- Gate: run to final evaluation unless config/process fails; aggregate with seed0 after summaries exist.

## 2026-07-01 risk seed1/seed2 monitor at ~180k
- Time: 2026-07-01T00:39:59+0800.
- seed1 around 180k: success_rate=0, route_completion about 0.025, mean_speed about 0.54 km/h, no cost/collision/out_of_road, std about 1.02.
- seed2 around 180k: success_rate=0, route_completion about 0.043, mean_speed about 0.77 km/h, no cost/collision/out_of_road, std about 1.01.
- Interpretation: risk-only without curriculum is currently low-speed/low-route and resembles seed0 early failure, but it is still early. Continue to 500k before deciding whether the comparator consistently fails.

## 2026-07-01 risk seed1/seed2 monitor at ~475k/~442k
- Time: 2026-07-01T00:44:02+0800.
- seed1 around 475k: success_rate=0, route_completion about 0.017, mean_speed about 0.44 km/h, cost=0. This is low-speed/route-stagnation failure, not useful safety.
- seed2 around 442k: success_rate=0, route_completion about 0.010, mean_speed about 0.44 km/h, cost=0. Same failure mode.
- Interpretation: risk reward + action guard without curriculum is not learning usable driving by mid-training, matching seed0 behavior. Continue to final evaluation for comparator evidence; do not tune this comparator mid-run.



## 2026-07-01 risk seed0/1/2 formal comparator aggregate completed
- Time: 2026-07-01T00:58:42+0800.
- Aggregate root: outputs/tuned_compare_risk_nenv16_seed0_seed1_seed2_aggregate.
- Files: summary_by_seed.csv, mean_by_density.csv, std_by_density.csv, compare_to_full_proposed_mean.csv, compare_to_guard_only_mean.csv, compare_to_shield_only_mean.csv, DECISION.md.
- Three-seed mean: d0.00 success=0.000 cost=0.000 route=0.009 speed=0.013; d0.08 success=0.000 cost=0.000 route=0.009 speed=0.013; d0.15 success=0.000 cost=0.000 route=0.009 speed=0.014.
- Decision: accept as risk-only formal comparator. This is a route-stagnation failure, not a safety success; zero cost is non-informative because the policy barely drives.
- Paper claim boundary: risk reward + action guard without curriculum does not learn usable driving under the formal n_envs=16 protocol. Do not tune this comparator; move to baseline/curriculum seed completion.
- PDF placement: run PDFs are under each single-run figures/ directory; aggregate directory intentionally contains only CSV/Markdown evidence.


## 2026-07-01 launch baseline seed1/seed2 nenv16 formal comparator completion
- Time: 2026-07-01T00:59:54+0800.
- Roots: outputs/tuned_compare_baseline_nenv16_seed1_1m and outputs/tuned_compare_baseline_nenv16_seed2_1m.
- Protocol: variant=baseline, seeds=1/2, n_envs=16, timesteps=1M, horizon=1500, EPISODES=50, DEVICE=cuda, ent_coef=0.01.
- Config check: use_risk_reward=False, use_action_guard=False, curriculum=False for both seed1 and seed2.
- Purpose: complete the baseline comparator symmetry after seed0 only.
- Gate: run to final evaluation unless process/config fails; aggregate with seed0 after summaries exist, then launch curriculum seed1/2.


## 2026-07-01 baseline seed1/seed2 monitor at ~360k
- Time: 2026-07-01T01:07:01+0800.
- seed1 around 360k: recent100 success=0.160, cost=0.840, collision=0.320, out_of_road=0.520, route=0.589, speed=22.950.
- seed2 around 360k: recent100 success=0.250, cost=0.750, collision=0.490, out_of_road=0.260, route=0.668, speed=23.311.
- Interpretation: baseline without guard is learning to drive faster and farther than early stage, but high collision/out_of_road cost is already dominant. Continue unchanged to final held-out evaluation; do not tune this comparator.


## 2026-07-01 baseline seed1/seed2 monitor at ~500k
- Time: 2026-07-01T01:11:04+0800.
- seed1 around 492k: recent100 success=0.030, cost=0.970, collision=0.640, out_of_road=0.330, route=0.439, speed=28.579.
- seed2 around 508k: recent100 success=0.100, cost=0.900, collision=0.560, out_of_road=0.350, route=0.542, speed=26.946.
- Interpretation: unguarded baseline is driving faster but remains unsafe, dominated by collision and out_of_road. Continue unchanged to final held-out evaluation; final paper table must use evaluation summary, not this training window.


## 2026-07-01 baseline seed0/1/2 formal comparator aggregate completed
- Time: 2026-07-01T01:27:33+0800.
- Aggregate root: outputs/tuned_compare_baseline_nenv16_seed0_seed1_seed2_aggregate.
- Files: summary_by_seed.csv, mean_by_density.csv, std_by_density.csv, compare_to_full_proposed_mean.csv, compare_to_guard_only_mean.csv, compare_to_shield_only_mean.csv, DECISION.md.
- Three-seed mean: d0.00 success=0.007 cost=0.993 route=0.303; d0.08 success=0.000 cost=1.000 route=0.242; d0.15 success=0.000 cost=1.000 route=0.190.
- Decision: accept as unguarded lower-bound baseline. It is unsafe at all densities; unlike risk-only stagnation, it moves but fails through collision/out_of_road.
- PDF placement: seed1/seed2 PDFs are under each run figures/ directory; aggregate directory intentionally contains only CSV/Markdown evidence.


## 2026-07-01 launch curriculum seed1/seed2 nenv16 formal comparator completion
- Time: 2026-07-01T01:28:38+0800.
- Roots: outputs/tuned_compare_curriculum_nenv16_seed1_1m and outputs/tuned_compare_curriculum_nenv16_seed2_1m.
- Protocol: variant=curriculum, seeds=1/2, n_envs=16, timesteps=1M, horizon=1500, EPISODES=50, DEVICE=cuda, ent_coef=0.01.
- Config check: use_risk_reward=False, use_action_guard=False, curriculum=True for both seed1 and seed2.
- Purpose: close the remaining main-comparator symmetry gap after baseline and risk aggregates.
- Gate: run to final evaluation unless process/config fails; aggregate with seed0 after summaries exist.


## 2026-07-01 curriculum seed1/seed2 monitor at ~250k
- Time: 2026-07-01T01:31:09+0800.
- seed1 around 262k: recent100 success=0.300, cost=0.580, collision=0.100, out_of_road=0.480, route=0.681, speed=18.027, curriculum_stage about 1.61.
- seed2 around 246k: recent100 success=0.300, cost=0.390, collision=0.140, out_of_road=0.250, route=0.693, speed=15.685, curriculum_stage about 2.05.
- Interpretation: curriculum-only is materially healthier than the unguarded baseline at comparable early/mid training, but final held-out evaluation is still required. Continue unchanged.


## 2026-07-01 curriculum seed1/seed2 monitor at ~425k-492k
- Time: 2026-07-01T01:35:40+0800.
- seed1 around 492k: recent100 success=0.120, cost=0.880, collision=0.670, out_of_road=0.210, route=0.569, speed=30.343, curriculum_stage about 1.74.
- seed2 around 426k: recent100 success=0.140, cost=0.860, collision=0.630, out_of_road=0.230, route=0.572, speed=27.949, curriculum_stage about 2.00.
- Interpretation: after the healthier ~250k window, curriculum-only degrades as speed/collision rise. Continue unchanged to final held-out evaluation; do not tune this comparator mid-run.


## 2026-07-01 curriculum seed1/seed2 monitor at ~705k-770k
- Time: 2026-07-01T01:41:11+0800.
- seed1 around 770k: recent100 success=0.290, cost=0.710, collision=0.420, out_of_road=0.290, route=0.666, speed=28.994, curriculum_stage about 2.00.
- seed2 around 705k: recent100 success=0.240, cost=0.760, collision=0.470, out_of_road=0.290, route=0.615, speed=28.747, curriculum_stage about 2.00.
- Interpretation: curriculum-only partially recovers relative to the ~500k window, but cost remains high. Continue unchanged to final held-out evaluation.


## 2026-07-01 curriculum seed0/1/2 formal comparator aggregate completed
- Time: 2026-07-01T01:51:50+0800.
- Aggregate root: outputs/tuned_compare_curriculum_nenv16_seed0_seed1_seed2_aggregate.
- Files: summary_by_seed.csv, mean_by_density.csv, std_by_density.csv, compare_to_full_proposed_mean.csv, compare_to_baseline_mean.csv, compare_to_guard_only_mean.csv, compare_to_shield_only_mean.csv, DECISION.md.
- Three-seed mean: d0.00 success=0.007 cost=0.993 route=0.349; d0.08 success=0.000 cost=1.000 route=0.236; d0.15 success=0.000 cost=1.000 route=0.177.
- Decision: accept as curriculum-only formal comparator. Curriculum improves some training windows and route progress relative to risk-only stagnation, but without action guard final held-out safety remains poor.
- PDF placement: seed1/seed2 PDFs are under each run figures/ directory; aggregate directory intentionally contains only CSV/Markdown evidence.


## 2026-07-01 stress density 0.20/0.25 nenv16 evaluation completed
- Time: 2026-07-01T02:55:36.125071+08:00.
- Root: outputs/stress_density_020_025_nenv16_20260701_0153.
- Protocol: evaluation-only, densities 0.20 and 0.25, EPISODES=50 per density, n_envs=16, device=cuda, frozen models only.
- Labels/seeds: guard_only, shield_only, retune_proposed_ttc4_cost10_lane1, baseline, curriculum, risk, full_proposed_candidate; each has seeds 0/1/2 and 100 episode rows per seed.
- Execution: all 21 label/seed evals succeeded or were skipped because a valid CSV already existed; no active stress process remains.
- d0.20 means: shield_only success=0.480 cost=0.360 route=0.778; retuned full proposed success=0.453 cost=0.380 route=0.753; guard_only success=0.413 cost=0.407 route=0.733; full proposed candidate success=0.380 cost=0.400 route=0.744.
- d0.25 means: guard_only success=0.267 cost=0.487 route=0.658; full proposed candidate success=0.207 cost=0.587 route=0.587; shield_only success=0.193 cost=0.587 route=0.609; retuned full proposed success=0.173 cost=0.687 route=0.571.
- Failure controls: baseline/curriculum have success=0 and cost=1.0 at both stress densities; risk has near-zero route and zero cost, so it is idle/stagnation rather than safety.
- Decision: accept as frozen high-density stress evidence. Use it to support action-guard-centered robustness and graceful degradation; do not claim risk-reward dominance.


## 2026-07-01 paper evidence tables package written
- Time: 2026-07-01T02:57:35.308647+08:00.
- Root: codex_longrun_iscsic/paper_tables_20260701_0258.
- Files: README_论文证据包.md, main_comparators_nenv16.csv, ablation_mechanism_nenv16.csv, stress_density_020_025.csv, claim_boundary_and_next_decisions.md.
- Purpose: convert completed n_envs=16 main/comparator/ablation/stress evidence into paper-facing tables and explicit claim boundaries.
- Decision: do not open another reward-only retune round by default. Current evidence supports an action-guard/shield-centered paper line; any further method improvement should be a mechanism change, not another weight sweep.


## 2026-07-01 proposed_gated_risk mechanism added and seed1/seed2 launched
- Time: 2026-07-01T03:10:01+08:00.
- Code change: added variant=proposed_gated_risk with use_risk_reward=True, use_action_guard=True, curriculum=True, and use_gated_risk_reward=True.
- Mechanism: continuous TTC/lane/smooth/accel/overspeed penalties are gated by meaningful motion/progress plus local risk; event cost, crash penalty, out-of-road penalty, progress reward, idle penalty, and action guard remain active. This targets the observed risk-reward idle/stagnation failure without changing the formal n_envs=16 evaluation protocol.
- Static/smoke verification: py_compile passed; config instantiation passed; short n_envs=16 smoke root outputs/smoke_proposed_gated_risk_20260701_0308 trained/evaluated and produced risk_gate_rate/continuous_risk_penalty/event_risk_penalty columns. Smoke is diagnostic only and must not enter paper tables.
- Formal diagnostic launches: outputs/gated_risk_proposed_nenv16_seed1_1m pid=109861 and outputs/gated_risk_proposed_nenv16_seed2_1m pid=109916.
- Protocol: timesteps=1M, horizon=1500, n_envs=16, EPISODES=50, DEVICE=cuda, ent_coef=0.01, stage2_success=0.50, stage2_cost=0.25, demote_cost=0.35.
- Gate: run seed1/seed2 to held-out evaluation unless process/config fails; decide on seed0 only after inspecting final metrics and failure mode versus guard_only/shield_only/retuned full proposed.


## 2026-07-01 proposed_gated_risk seed1/seed2 monitor at ~472k/~482k
- Time: 2026-07-01T03:12:58+08:00.
- seed1 around 472k env steps: recent100 success=0.090, cost=0.010, collision=0.000, out_of_road=0.010, route=0.292, speed=2.824, risk_gate_rate=0.170, continuous_risk_penalty=35.084, event_risk_penalty=0.100, shield_rate=0.002, curriculum_stage about 0.20.
- seed2 around 482k env steps: recent100 success=0.080, cost=0.080, collision=0.000, out_of_road=0.080, route=0.275, speed=2.441, risk_gate_rate=0.186, continuous_risk_penalty=28.587, event_risk_penalty=0.800, shield_rate=0.001, curriculum_stage about 0.14.
- Interpretation: gated risk is not collapsing into the risk-only near-zero-route failure, and safety/cost is currently low. However speed/stage/route are still conservative versus guard_only/shield_only; do not claim improvement from this window. Continue to final held-out evaluation before deciding on seed0 or mechanism revision.


## 2026-07-01 proposed_gated_risk seed1/seed2 monitor at ~711k/~728k
- Time: 2026-07-01T03:16:32+08:00.
- seed1 around 711k env steps: recent100 success=0.170, cost=0.010, collision=0.000, out_of_road=0.010, route=0.472, speed=6.856, risk_gate_rate=0.269, continuous_risk_penalty=53.112, event_risk_penalty=0.100, shield_rate=0.023, curriculum_stage about 0.68.
- seed2 around 728k env steps: recent100 success=0.170, cost=0.080, collision=0.020, out_of_road=0.060, route=0.473, speed=6.977, risk_gate_rate=0.279, continuous_risk_penalty=46.953, event_risk_penalty=0.800, shield_rate=0.032, curriculum_stage about 0.65.
- Interpretation: this is a recovery from the ~480k conservative window and clearly avoids risk-only route stagnation. Still, training-window metrics remain weaker than the guard/shield-centered best evidence, so continue to final held-out evaluation before deciding whether seed0 is worthwhile.


## 2026-07-01 proposed_gated_risk seed1/seed2 evaluation completed; seed0 launched
- Time: 2026-07-01T03:28:44+08:00.
- Completed roots: outputs/gated_risk_proposed_nenv16_seed1_1m and outputs/gated_risk_proposed_nenv16_seed2_1m.
- Per-seed held-out summary: seed1 d0.00/d0.08/d0.15 success=0.94/0.80/0.62, cost=0.00/0.10/0.28; seed2 success=0.94/0.90/0.56, cost=0.00/0.06/0.28.
- Preliminary two-seed aggregate: outputs/gated_risk_proposed_nenv16_seed1_seed2_prelim_aggregate. Mean d0.00 success=0.940 cost=0.000 route=0.987; d0.08 success=0.850 cost=0.080 route=0.959; d0.15 success=0.590 cost=0.280 route=0.843.
- Decision: gated risk fixes risk-only stagnation and is worth completing as a three-seed mechanism diagnostic, but current two-seed d0.15 does not displace guard_only/shield_only/retuned full. Keep guard/shield-centered paper claim boundary.
- New launch: outputs/gated_risk_proposed_nenv16_seed0_1m pid=111544, same 1M/horizon1500/n_envs16/EPISODES50 protocol with ent_coef=0.01, stage2_success=0.50, stage2_cost=0.25, demote_cost=0.35.


## 2026-07-01 proposed_gated_risk seed0 monitor at ~497k
- Time: 2026-07-01T03:32:54+08:00.
- seed0 around 497k env steps: recent100 success=0.060, cost=0.010, collision=0.000, out_of_road=0.010, route=0.290, speed=2.895, risk_gate_rate=0.189, continuous_risk_penalty=38.136, event_risk_penalty=0.100, shield_rate=0.003, curriculum_stage about 0.26.
- Interpretation: seed0 matches seed1/seed2 mid-training recovery pattern and has no process/config failure. Continue unchanged to late-training and final held-out evaluation.


## 2026-07-01 proposed_gated_risk seed0 monitor at ~744k
- Time: 2026-07-01T03:35:50+08:00.
- seed0 around 744k env steps: recent100 success=0.150, cost=0.010, collision=0.000, out_of_road=0.010, route=0.463, speed=6.460, risk_gate_rate=0.274, continuous_risk_penalty=54.981, event_risk_penalty=0.100, shield_rate=0.024, curriculum_stage about 0.71.
- Interpretation: seed0 has the same late-training recovery pattern as seed1/seed2. Continue unchanged to model save and held-out evaluation.


## 2026-07-01 proposed_gated_risk three-seed aggregate completed
- Time: 2026-07-01T03:46:11+08:00.
- Aggregate root: outputs/gated_risk_proposed_nenv16_seed0_seed1_seed2_aggregate.
- Completed single-run roots: outputs/gated_risk_proposed_nenv16_seed0_1m, outputs/gated_risk_proposed_nenv16_seed1_1m, outputs/gated_risk_proposed_nenv16_seed2_1m.
- Files: summary_by_seed.csv, mean_by_density.csv, std_by_density.csv, compare_to_guard_only_mean.csv, compare_to_shield_only_mean.csv, compare_to_retune_full_mean.csv, compare_to_risk_only_mean.csv, DECISION.md.
- Three-seed mean: d0.00 success=0.940 cost=0.000 route=0.988; d0.08 success=0.867 cost=0.080 route=0.961; d0.15 success=0.600 cost=0.253 route=0.849.
- Mechanism metrics: risk_gate_rate mean is 0.887/0.865/0.764 at d0.00/d0.08/d0.15; out_of_road=0.000 at all formal densities.
- Decision: accept as completed mechanism diagnostic. Gated risk fixes the risk-only stagnation failure, but does not replace the guard_only/shield_only/retuned-full main evidence because d0.15 remains slightly weaker.
- Paper package addendum: codex_longrun_iscsic/paper_tables_20260701_0258/gated_risk_mechanism_addendum.csv and gated_risk_mechanism_addendum.md.
- PDF placement: all generated PDFs are under the single-run figures/ directories; aggregate/addendum directories remain CSV/Markdown only.


## 2026-07-01 proposed_gated_risk stress eval launched
- Time: 2026-07-01T03:48:14+08:00.
- Root: outputs/stress_gated_risk_density_020_025_nenv16_20260701_0346.
- Protocol: frozen proposed_gated_risk seed0/1/2 models, densities 0.20 and 0.25, 50 episodes per density, n_envs=16, device=cuda.
- Execution: serial driver PID 112760, seed0 evaluation confirmed running. Purpose is addendum evidence against the existing 0.20/0.25 stress table, not a new training run.


## 2026-07-01 proposed_gated_risk stress addendum completed
- Time: 2026-07-01T04:00:34+08:00.
- Stress root: outputs/stress_gated_risk_density_020_025_nenv16_20260701_0346.
- Aggregate root: outputs/stress_gated_risk_density_020_025_nenv16_20260701_0346/aggregate.
- Files: status.tsv, evaluations/proposed_gated_risk_ppo_s0.csv, evaluations/proposed_gated_risk_ppo_s1.csv, evaluations/proposed_gated_risk_ppo_s2.csv, aggregate/summary_by_seed.csv, aggregate/mean_by_density.csv, aggregate/std_by_density.csv, aggregate/rank_with_existing_stress.csv, aggregate/DECISION.md.
- Three-seed stress mean: d0.20 success=0.447 cost=0.367 route=0.766; d0.25 success=0.220 cost=0.527 route=0.628.
- Existing stress comparison: at d0.20 proposed_gated_risk ranks behind shield_only and retuned full by success; at d0.25 it ranks second behind guard_only by success/cost/route ordering.
- Paper package addendum: codex_longrun_iscsic/paper_tables_20260701_0258/gated_risk_stress_mean.csv, gated_risk_stress_rank_with_existing.csv, gated_risk_stress_addendum.md.
- Final boundary: conditional risk shaping is useful and improves over risk-only/retuned-full in some stress settings, but does not overturn the guard/shield-centered main claim.
- Process/PDF check: no active training/evaluation process remains; aggregate and paper_table directories contain no PDFs.


## 2026-07-01 reviewer robustness and behavior addenda completed
- Time: 2026-07-01T04:11:29+08:00.
- Updated coverage audit: codex_longrun_iscsic/EXPERIMENT_COVERAGE_AUDIT_20260701_0405.md.
- Reviewer statistics files in paper package: seed_level_robustness_formal.csv, seed_paired_deltas_vs_guard_shield.csv, seed_level_robustness_stress.csv, reviewer_statistics_notes.md.
- Behavior rollout directory: codex_longrun_iscsic/behavior_rollouts_20260701_0406.
- Representative qualitative seed: density=0.15, map_seed=10003. guard_only/shield_only/retuned_full/proposed_gated_risk succeed; no_action_guard fails by collision/high speed; risk_only has near-zero route and zero cost due stagnation.
- Representative plot: codex_longrun_iscsic/behavior_rollouts_20260701_0406/representative_density_0p15_seed10003.pdf.
- Paper package pointer: codex_longrun_iscsic/paper_tables_20260701_0258/behavior_rollout_addendum.md.
- Boundary: behavior plots are qualitative mechanism illustrations only, not replacements for aggregate metrics.

## 2026-07-01 final paper manifest and PDF placement

- Created `codex_longrun_iscsic/final_paper_manifest_20260701_0415`.
- Paper-facing PDFs copied to `codex_longrun_iscsic/final_paper_manifest_20260701_0415/pdf_figures/`.
- Tables/TeX copied or generated in the manifest root; aggregate claim source remains `codex_longrun_iscsic/paper_tables_20260701_0258`.
- Historical run PDFs remain in `outputs/*/figures/` for provenance only.

## 2026-07-01 external seed robustness nenv16 launched

- Time: 2026-07-01T04:27:43.008115+08:00.
- Root: `outputs/external_seed_robustness_nenv16_20260701_0425`.
- Driver: `codex_longrun_iscsic/run_external_seed_robustness_nenv16_20260701_0425.sh`.
- Active PID at launch check: driver `116825`.
- Protocol: frozen completed models, `n_envs=16`, `episodes=50`, densities `0.08/0.15`, external `test_start_seed=20000/30000`.
- Variants: `guard_only`, `shield_only`, `retuned_full`, `proposed_gated_risk`, `risk_only`, `no_action_guard`; seeds `0/1/2` each.
- Purpose: reviewer-facing external scenario-seed validation of the guard/shield-centered paper claim, not new reward tuning.
- Decision rule: aggregate by label/density after each finished unit; if positive methods degrade, report sensitivity instead of hiding it; do not interpret risk-only zero cost without route completion.


## 2026-07-01 external seed robustness integrated into paper package

- Time: 2026-07-01T08:39:24+08:00.
- Source root: outputs/external_seed_robustness_nenv16_20260701_0425.
- Added paper package files: external_seed_robustness_addendum.md, external_seed_robustness_mean.csv, external_seed_robustness_rank_d015.csv, external_seed_robustness_by_test_start.csv, external_seed_robustness_eval_units.csv.
- Added final manifest table: final_paper_manifest_20260701_0415/table4_external_seed_robustness.csv and table_manifest.csv row.
- Latest density 0.15 conclusion: shield_only success=0.687/cost=0.207, proposed_gated_risk success=0.663/cost=0.213, guard_only success=0.613/cost=0.240; no_action_guard has success=0/cost=1 and risk_only has near-zero route completion.
- Decision: keep guard/shield-centered paper claim; treat gated risk as refinement/addendum; do not open another reward-only retune from this result.

## 2026-07-01 external seed Wilson interval statistics added

- Time: 2026-07-01T08:40:52+08:00.
- Added `codex_longrun_iscsic/paper_tables_20260701_0258/external_seed_robustness_wilson95.csv` and `external_seed_robustness_d015_wilson95.csv` from episode-level external-seed rows.
- Added final manifest copy `final_paper_manifest_20260701_0415/table4_external_seed_robustness_d015_wilson95.csv` and table_manifest row.
- Interpretation: at d0.15 shield_only and proposed_gated_risk have overlapping success intervals, so use the result as robustness/refinement evidence, not as a superiority claim.

## 2026-07-01 defensive ttc14/v18 aggregate closed

- Time: 2026-07-01T08:44:46+08:00.
- Source root: outputs/defensive_ttc14_v18_nenv16_tuning.
- Added aggregate files under outputs/defensive_ttc14_v18_nenv16_tuning/aggregate.
- Three-seed d0.15 mean: success=0.573, cost=0.260, route=0.839; compared with ttc12/v18 success=0.567, cost=0.273.
- Decision: diagnostic only, because d0.15 success remains below 0.60 and d0.15 cost remains above 0.25. Do not promote or open more TTC-only tuning from this branch.

## 2026-07-01 experiment completion audit written

- Time: 2026-07-01T08:45:49+08:00.
- Wrote EXPERIMENT_COMPLETION_AUDIT_20260701_0845.md and EXPERIMENT_REQUIREMENT_MATRIX_20260701_0845.csv.
- Verification: 33 accepted model configs checked with bad_count=0; 72 episode eval CSVs checked with bad_count=0; paper table source missing_count=0.
- Decision: evidence package is ready for conservative guard/shield-centered manuscript writing; no blind new reward/TTC tuning should be started.

## 2026-07-01 manuscript evidence brief and supervisor script added

- Time: 2026-07-01T08:48:51+08:00.
- Added manuscript-facing evidence brief: codex_longrun_iscsic/MANUSCRIPT_EVIDENCE_BRIEF_20260701_0848.md.
- Added repeatable supervisor script: codex_longrun_iscsic/check_supervision_status.py.
- Latest supervisor snapshot: codex_longrun_iscsic/supervision_status_latest.md.
- Verification: check_supervision_status.py --write returned Status=OK_IDLE, active experiment processes=0, accepted configs=33 bad=0, episode eval CSVs=72 bad=0, and all key paper tables met expected row counts.
- Decision: do not start broad new training from idle GPU alone. Current next action is manuscript/table/figure packaging or a narrowly scoped reviewer validation if a concrete gap appears.

