# Failed / stopped runs

## 2026-06-30 route-gate 0.85 diagnostic stopped
- Run: outputs/tuning_routegate_prehard_nenv10_1p5m/runs/proposed_ppo_s1
- Command: proposed seed1, 1.5M, n_envs=10, stage2_route_completion=0.85.
- Stop reason: by ~768k timesteps it remained in stage2. Window route completion reached ~0.843 but did not cross 0.85; success around 0.22-0.27 and cost 0.07-0.13. The gate delayed prehard exposure too much.
- Diagnosis: route gate idea is plausible, but 0.85 is too strict for seed1 medium-stage variance.
- Fix action: lower stage2_route_completion to 0.80 and rerun same seed diagnostic.

## 2026-06-30 route-gate 0.80 diagnostic stopped
- Run: outputs/tuning_routegate080_prehard_nenv10_1p5m/runs/proposed_ppo_s1
- Command: proposed seed1, 1.5M, n_envs=10, stage2_route_completion=0.80.
- Stop reason: although it reached stage3 around ~461k, it later suffered repeated collisions/cost spikes and demoted all the way to stage0 by ~727k-809k. Window route completion collapsed to ~0.06 and success to 0.
- Diagnosis: route-gated promotion alone does not stabilize seed1; it can delay exposure but does not prevent later catastrophic policy drift.
- Fix action: restore pre-route-gate curriculum code from backups. Treat 0.80 and 0.85 as failed diagnostics, not final benchmark.

## 2026-06-30 stopped: tuning_lr1e4_prehard_nenv10_1p5m seed1
- Command: proposed PPO seed1, 1.5M planned, n_envs=10, ent_coef=0.01, learning_rate=1e-4.
- Stopped at about 1.064M steps because training demoted from stage3 to stage2 and window metrics degraded: window_success 0.0333, window_cost 0.433, window_route_completion 0.649.
- Failure interpretation: low LR is not simply under-trained; it slowed adaptation and still showed policy drift/cost growth. Next diagnostic is checkpoint evaluation at 750k to test whether earlier checkpoints are better than continued training.

## 2026-06-30 stopped: tuning_lr2e4_prehard_nenv10_1p5m seed1
- Command: proposed PPO seed1, n_envs=10, ent_coef=0.01, learning_rate=2e-4, planned 1.5M.
- Stopped after checkpoint_1125000_steps.zip because run entered hard stage around 829k and 1.044M but could not maintain stable hard-stage success; latest stage3 window around 1.157M had success 0.10, cost 0.20, route 0.769.
- Failure interpretation: 2e-4 improves curriculum speed over 1e-4 but does not solve hard-stage instability. Evaluate 1.125M checkpoint as diagnostic.

## 2026-06-30 stopped: tuning_stage2strict035_prehard_nenv10_1p5m seed1
- Command: proposed PPO seed1, n_envs=10, ent_coef=0.01, stage2_success=0.35, stage2_cost=0.35, planned 1.5M.
- Stopped around ~1.239M because the run remained in stage3 and did not enter hard; latest window: success about 0.167, route about 0.766, cost about 0.20.
- Interpretation: stricter promotion avoided early hard-stage collapse and improved safety/route stability, but did not solve prehard success-rate insufficiency. Evaluate checkpoint_1125000_steps.zip as diagnostic.

## 2026-06-30 ttc14/v18 500k screening did not improve safety-success tradeoff
- Command: python scripts/run_one_defensive_proposed.py --seed 28 --n-envs 10 --timesteps 500000 --root outputs/tuning_ttc14_v18_nenv10_500k --ttc-threshold 14.0 --target-speed 18.0 --device cuda.
- Purpose: increase TTC threshold from 12 to 14 while keeping target_speed=18 to reduce high-density collision/cost.
- Result: d0.00 success=1.00 cost=0.00 route=0.991; d0.08 success=0.78 cost=0.20 route=0.888 collision=0.20; d0.15 success=0.48 cost=0.32 route=0.829 collision=0.32.
- Comparison: ttc12/v18 seed28 1M had d0.08 success=0.88 cost=0.10 and d0.15 success=0.72 cost=0.20.
- Decision: ttc14/v18 is worse and should not be expanded. Next screen changes target_speed only: ttc12/v16.

## 2026-06-30 ttc12/v16 500k screening did not improve overall tradeoff
- Command: python scripts/run_one_defensive_proposed.py --seed 28 --n-envs 10 --timesteps 500000 --root outputs/tuning_ttc12_v16_nenv10_500k --ttc-threshold 12.0 --target-speed 16.0 --device cuda.
- Purpose: lower target speed from 18 to 16 while keeping TTC threshold 12 to reduce high-density collision/cost.
- Result: d0.00 success=0.84 cost=0.00 route=0.975; d0.08 success=0.76 cost=0.08 route=0.944 collision=0.08; d0.15 success=0.52 cost=0.22 route=0.857 collision=0.22.
- Comparison: ttc12/v18 seed28 1M had d0.00 success=0.98, d0.08 success=0.88, d0.15 success=0.72 with cost=0.20.
- Decision: target_speed=16 slightly controls high-density cost but sacrifices success too much. Do not expand.

## 2026-06-30 abort lateral/smooth retune lane2-smooth004-accel002 seed1/seed2
- Time: 2026-06-30T22:38:56+0800.
- Roots: outputs/retune_proposed_ttc4_cost10_lane2_smooth004_accel002_nenv16_seed1_1m and seed2_1m.
- Abort reason: mid-run evidence showed severe progress suppression. At about 524k/540k timesteps both runs remained in stage0 with window_route_completion about 0.10/0.09 and success_rate 0. This is much worse than the preceding ttc4-cost10-lane1 retune, which had already reached stage1/2 by this point.
- Diagnosis: lane=2.0 plus smooth=0.04/accel=0.02 over-regularizes motion and should not be completed as a formal candidate.
- Decision: stop these diagnostic runs and launch a gentler lateral retune instead: lane around 1.25, smooth 0.03, accel 0.015, with slightly higher progress reward to preserve motion.
