# IJMLC journalization revision report

- Generated at: 2026-07-01T23:46:27
- Objective: convert the manuscript from an experiment-diagnostic report into an IJMLC-style machine-learning/cybernetics journal paper.
- Boundary: simulator-level diagnostic improvement only; no formal safety or real-world safety certification is claimed.
- Figure backend: Python/matplotlib only.

## Requirements implemented

- Reframed the title, abstract, introduction, method, results, discussion, and conclusion around cybernetic runtime feedback.
- Added closed-loop formulation, TTC monitor definition, Guard operator equations, Shield/Gated-risk definitions, and Algorithm 1.
- Expanded Related Work into safe RL, runtime shielding, cybernetic feedback, driving simulation, and positioning.
- Reduced the visible main text to six tables: signals/parameters, compared methods, core mechanism, external baselines, density summary, and claim-to-evidence.
- Kept the existing Fig. 1 architecture asset and rebuilt Fig. 2 as a four-panel artifact-aware core evidence figure.
- Split TTC-threshold sensitivity into the main text and compact target-speed sensitivity into the appendix.
- Compressed the appendix from raw diagnostic dumps into evidence map, uncertainty, density envelope, sensitivity, and runtime summaries.

## Evidence limitation

- Current raw CSV files are episode-level diagnostics. No step-level route/speed/TTC/intervention trace files were found, so representative episode trace plots were not fabricated.
- Recommended next experiment: run a diagnostic evaluator with per-step logging for PPO, Risk-only, Guard, and Gated-risk at density 0.15.

## Generated figures

- `results/ijmlc_control/figures_publication/fig1_cybernetic_feedback_architecture.pdf`
- `results/ijmlc_control/figures_publication/fig1_cybernetic_feedback_architecture.png`
- `results/ijmlc_control/figures_publication/fig1_cybernetic_feedback_architecture.svg`
- `results/ijmlc_control/figures_publication/fig1_cybernetic_feedback_architecture.tiff`
- `results/ijmlc_control/figures_publication/fig2_core_artifact_evidence.pdf`
- `results/ijmlc_control/figures_publication/fig2_core_artifact_evidence.png`
- `results/ijmlc_control/figures_publication/fig2_core_artifact_evidence.svg`
- `results/ijmlc_control/figures_publication/fig2_core_artifact_evidence.tiff`
- `results/ijmlc_control/figures_publication/fig3_external_baselines.pdf`
- `results/ijmlc_control/figures_publication/fig3_external_baselines.png`
- `results/ijmlc_control/figures_publication/fig3_external_baselines.svg`
- `results/ijmlc_control/figures_publication/fig3_external_baselines.tiff`
- `results/ijmlc_control/figures_publication/fig4_density_stress.pdf`
- `results/ijmlc_control/figures_publication/fig4_density_stress.png`
- `results/ijmlc_control/figures_publication/fig4_density_stress.svg`
- `results/ijmlc_control/figures_publication/fig4_density_stress.tiff`
- `results/ijmlc_control/figures_publication/fig5_ttc_threshold_sensitivity.pdf`
- `results/ijmlc_control/figures_publication/fig5_ttc_threshold_sensitivity.png`
- `results/ijmlc_control/figures_publication/fig5_ttc_threshold_sensitivity.svg`
- `results/ijmlc_control/figures_publication/fig5_ttc_threshold_sensitivity.tiff`
- `results/ijmlc_control/figures_publication/fig6_simulation_loop_overhead.pdf`
- `results/ijmlc_control/figures_publication/fig6_simulation_loop_overhead.png`
- `results/ijmlc_control/figures_publication/fig6_simulation_loop_overhead.svg`
- `results/ijmlc_control/figures_publication/fig6_simulation_loop_overhead.tiff`
- `results/ijmlc_control/figures_publication/figS1_target_speed_sensitivity.pdf`
- `results/ijmlc_control/figures_publication/figS1_target_speed_sensitivity.png`
- `results/ijmlc_control/figures_publication/figS1_target_speed_sensitivity.svg`
- `results/ijmlc_control/figures_publication/figS1_target_speed_sensitivity.tiff`

## Main-text tables

- `results/ijmlc_control/tables_publication/table_claim_evidence_pub.tex`
- `results/ijmlc_control/tables_publication/table_compared_methods_pub.tex`
- `results/ijmlc_control/tables_publication/table_core_mechanism_pub.tex`
- `results/ijmlc_control/tables_publication/table_density_summary_pub.tex`
- `results/ijmlc_control/tables_publication/table_external_baseline_pub.tex`
- `results/ijmlc_control/tables_publication/table_runtime_signals_pub.tex`

## Printed appendix tables

- `results/ijmlc_control/tables_publication/table_ci_binary_pub.tex`
- `results/ijmlc_control/tables_publication/table_density_operating_envelope_pub.tex`
- `results/ijmlc_control/tables_publication/table_manifest_pub.tex`
- `results/ijmlc_control/tables_publication/table_parameter_defaults_pub.tex`
- `results/ijmlc_control/tables_publication/table_result_block_provenance_pub.tex`
- `results/ijmlc_control/tables_publication/table_runtime_summary_pub.tex`
- `results/ijmlc_control/tables_publication/table_seed_range_pub.tex`
- `results/ijmlc_control/tables_publication/table_sensitivity_summary_pub.tex`
