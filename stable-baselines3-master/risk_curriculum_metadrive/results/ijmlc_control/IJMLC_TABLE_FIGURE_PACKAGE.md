# IJMLC Table/Figure Package

generated_at: 2026-07-01T17:28:36

## Data Basis
- aggregate: `/home/aaa/data/qj/stable-baselines3-master/risk_curriculum_metadrive/results/ijmlc_control/summary_tables/p1_all_density_core_aggregate.csv`
- seed_summary: `/home/aaa/data/qj/stable-baselines3-master/risk_curriculum_metadrive/results/ijmlc_control/summary_tables/p1_all_density_core_seed_summary.csv`
- raw_episodes: `/home/aaa/data/qj/stable-baselines3-master/risk_curriculum_metadrive/results/ijmlc_control/raw_csv/p1_all_density_core_episodes.csv`
- aggregate_rows: 24
- raw_episodes: 2880
- methods: PPO, Risk-only, No-action guard, Guard, Shield, Gated-risk
- densities: 0.08, 0.15, 0.2, 0.25

## Generated Tables
- table3_csv: `/home/aaa/data/qj/stable-baselines3-master/risk_curriculum_metadrive/results/ijmlc_control/manuscript/table3_core_d015_main_diagnostics.csv`
- table3_tex: `/home/aaa/data/qj/stable-baselines3-master/risk_curriculum_metadrive/results/ijmlc_control/manuscript/table3_core_d015_main_diagnostics.tex`
- table6_csv: `/home/aaa/data/qj/stable-baselines3-master/risk_curriculum_metadrive/results/ijmlc_control/manuscript/table6_density_stress_summary.csv`
- table6_tex: `/home/aaa/data/qj/stable-baselines3-master/risk_curriculum_metadrive/results/ijmlc_control/manuscript/table6_density_stress_summary.tex`
- table7_csv: `/home/aaa/data/qj/stable-baselines3-master/risk_curriculum_metadrive/results/ijmlc_control/manuscript/table7_runtime_overhead.csv`
- table7_tex: `/home/aaa/data/qj/stable-baselines3-master/risk_curriculum_metadrive/results/ijmlc_control/manuscript/table7_runtime_overhead.tex`
- non_motion_csv: `/home/aaa/data/qj/stable-baselines3-master/risk_curriculum_metadrive/results/ijmlc_control/manuscript/table_supp_non_motion_artifact.csv`
- fig2_data: `/home/aaa/data/qj/stable-baselines3-master/risk_curriculum_metadrive/results/ijmlc_control/manuscript/figure2_non_motion_artifact_data.csv`
- fig3_data: `/home/aaa/data/qj/stable-baselines3-master/risk_curriculum_metadrive/results/ijmlc_control/manuscript/figure3_progress_safety_frontier_data.csv`
- fig5_data: `/home/aaa/data/qj/stable-baselines3-master/risk_curriculum_metadrive/results/ijmlc_control/manuscript/figure5_density_stress_data.csv`
- runtime_seed_csv: `/home/aaa/data/qj/stable-baselines3-master/risk_curriculum_metadrive/results/ijmlc_control/manuscript/table_supp_runtime_by_seed.csv`

## Generated Figures
- fig2: `/home/aaa/data/qj/stable-baselines3-master/risk_curriculum_metadrive/results/ijmlc_control/figures/fig2_non_motion_artifact.pdf`, `/home/aaa/data/qj/stable-baselines3-master/risk_curriculum_metadrive/results/ijmlc_control/figures/fig2_non_motion_artifact.png`
- fig3: `/home/aaa/data/qj/stable-baselines3-master/risk_curriculum_metadrive/results/ijmlc_control/figures/fig3_progress_safety_frontier.pdf`, `/home/aaa/data/qj/stable-baselines3-master/risk_curriculum_metadrive/results/ijmlc_control/figures/fig3_progress_safety_frontier.png`
- fig5: `/home/aaa/data/qj/stable-baselines3-master/risk_curriculum_metadrive/results/ijmlc_control/figures/fig5_density_stress.pdf`, `/home/aaa/data/qj/stable-baselines3-master/risk_curriculum_metadrive/results/ijmlc_control/figures/fig5_density_stress.png`
- fig7: `/home/aaa/data/qj/stable-baselines3-master/risk_curriculum_metadrive/results/ijmlc_control/figures/fig7_runtime_overhead.pdf`, `/home/aaa/data/qj/stable-baselines3-master/risk_curriculum_metadrive/results/ijmlc_control/figures/fig7_runtime_overhead.png`

## Claim Boundaries
- These artifacts summarize frozen-policy diagnostics and density stress tests. They do not claim newly trained external safe-RL baselines.
- `Risk-only` is treated as a non-motion artifact/negative diagnostic because it has near-zero route completion and stop_ratio=1.0 across densities.
- Runtime overhead is measured as policy/control-loop wall time during diagnostic rollouts; isolated internal guard computation latency is not separately instrumented yet.
- Each density-method aggregate uses 120 episodes from 3 training seeds unless the table states otherwise.
