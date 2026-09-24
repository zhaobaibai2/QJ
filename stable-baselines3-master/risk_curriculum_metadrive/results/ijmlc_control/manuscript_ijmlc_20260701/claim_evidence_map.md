# Claim-Evidence Map for IJMLC Manuscript

generated_at: 2026-07-01T20:05:00+08:00

## Claim 1: Low cost alone is not sufficient evidence of safe driving
- Manuscript location: Section RQ1, Fig. 2, Table 2.
- Evidence: `manuscript/table3_core_d015_main_diagnostics.csv`, `manuscript/figure2_non_motion_artifact_data.csv`.
- Key values: Risk-only cost=0.0%, route=0.899%, stop=100.0%, low-progress=100.0% at density 0.15.
- Boundary: This is a MetaDrive diagnostic artifact, not a universal theorem about all risk rewards.

## Claim 2: Runtime action/execution intervention restores progress-safety in the tested protocol
- Manuscript location: Sections RQ1-RQ2, Fig. 3, Fig. 4, Table 2.
- Evidence: `raw_csv/p1_all_density_core_episodes.csv`, `summary_tables/p1_all_density_core_aggregate.csv`.
- Key values at density 0.15: Guard/Shield/Gated-risk route=85.687-86.874%, cost=18.333-20.833%, success=59.167-62.500%.
- Boundary: The claim is simulation/protocol-specific and does not imply certified safety.

## Claim 3: External baselines do not explain away the runtime intervention effect
- Manuscript location: Section RQ3, Table 3.
- Evidence: `P2_EXTERNAL_BASELINES_FINAL_REPORT.md`, `manuscript/table4_external_baselines_d015.csv`.
- Key values: RSS/TTC filter success=53.333%, cost=44.167%, route=78.943%; RCPO-Lagrangian success=0.0%, cost=100.0%.
- Boundary: RCPO-Lagrangian is an in-code PPO-Lagrangian baseline because sb3_contrib was unavailable.

## Claim 4: The method degrades under high traffic density but remains informative
- Manuscript location: Section RQ4, Table 4, Fig. 5.
- Evidence: `manuscript/table6_density_stress_summary.csv`, `figure5_density_stress_data.csv`.
- Key values: At density 0.25, Guard success=30.0%, cost=43.333%, route=64.124%.
- Boundary: Do not claim density-invariant robustness.

## Claim 5: Sensitivity sweeps support bounded robustness, not universal optimality
- Manuscript location: Appendix sensitivity, Figs. 8-9.
- Evidence: `manuscript/table_supp_sensitivity.csv`, `summary_tables/p5_sensitivity_aggregate.csv`.
- Boundary: The sweeps cover TTC thresholds 6/8/10/12 and target speeds 15/18/22 km/h only.

## Claim 6: Runtime overhead is not a simulation bottleneck in the measured setup
- Manuscript location: Section RQ5, Table 5, Fig. 7.
- Evidence: `manuscript/table7_runtime_overhead.csv`, `table_supp_runtime_by_seed.csv`.
- Key values at density 0.15: PPO control-loop p95=16.932 ms; Guard=13.310 ms; Shield=12.681 ms; Gated-risk=12.398 ms.
- Boundary: These are Python simulation-loop measurements, not embedded real-time guarantees.

## Deferred evidence
- Seed-3 and seed-4 retraining is recorded as reviewer-demand reserve in `P3_SEED_EXTENSION_DECISION.md` and is not part of formal current tables.
