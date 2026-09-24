# IJMLC publication table and figure revision

- Generated at: 2026-07-01T19:47:30
- Script: `/home/aaa/data/qj/stable-baselines3-master/risk_curriculum_metadrive/results/ijmlc_control/scripts/build_publication_tables_figures.py`
- Figure directory: `/home/aaa/data/qj/stable-baselines3-master/risk_curriculum_metadrive/results/ijmlc_control/figures_publication`
- Table directory: `/home/aaa/data/qj/stable-baselines3-master/risk_curriculum_metadrive/results/ijmlc_control/tables_publication`
- Manuscript directory: `/home/aaa/data/qj/stable-baselines3-master/risk_curriculum_metadrive/results/ijmlc_control/manuscript_ijmlc_20260701`

## Figure contract

- Conclusion: runtime feedback is not a non-motion shortcut; it preserves progress-safety better than reward-only and external baseline controls under the tested MetaDrive protocol.
- Evidence logic: architecture -> core artifact/frontier -> external baselines -> density stress -> sensitivity -> runtime overhead.
- Export policy: every figure is exported as PDF, SVG, TIFF, and PNG; PDF is used in the LaTeX manuscript.

## Generated figures

- `results/ijmlc_control/figures_publication/fig1_cybernetic_runtime_loop.pdf`
- `results/ijmlc_control/figures_publication/fig1_cybernetic_runtime_loop.png`
- `results/ijmlc_control/figures_publication/fig1_cybernetic_runtime_loop.svg`
- `results/ijmlc_control/figures_publication/fig1_cybernetic_runtime_loop.tiff`
- `results/ijmlc_control/figures_publication/fig2_core_diagnosis.pdf`
- `results/ijmlc_control/figures_publication/fig2_core_diagnosis.png`
- `results/ijmlc_control/figures_publication/fig2_core_diagnosis.svg`
- `results/ijmlc_control/figures_publication/fig2_core_diagnosis.tiff`
- `results/ijmlc_control/figures_publication/fig3_external_baselines.pdf`
- `results/ijmlc_control/figures_publication/fig3_external_baselines.png`
- `results/ijmlc_control/figures_publication/fig3_external_baselines.svg`
- `results/ijmlc_control/figures_publication/fig3_external_baselines.tiff`
- `results/ijmlc_control/figures_publication/fig4_density_stress.pdf`
- `results/ijmlc_control/figures_publication/fig4_density_stress.png`
- `results/ijmlc_control/figures_publication/fig4_density_stress.svg`
- `results/ijmlc_control/figures_publication/fig4_density_stress.tiff`
- `results/ijmlc_control/figures_publication/fig5_parameter_sensitivity.pdf`
- `results/ijmlc_control/figures_publication/fig5_parameter_sensitivity.png`
- `results/ijmlc_control/figures_publication/fig5_parameter_sensitivity.svg`
- `results/ijmlc_control/figures_publication/fig5_parameter_sensitivity.tiff`
- `results/ijmlc_control/figures_publication/fig6_runtime_overhead.pdf`
- `results/ijmlc_control/figures_publication/fig6_runtime_overhead.png`
- `results/ijmlc_control/figures_publication/fig6_runtime_overhead.svg`
- `results/ijmlc_control/figures_publication/fig6_runtime_overhead.tiff`

## Generated tables

- `results/ijmlc_control/tables_publication/table_ci_binary_pub.tex`
- `results/ijmlc_control/tables_publication/table_ci_continuous_pub.tex`
- `results/ijmlc_control/tables_publication/table_core_full_pub.tex`
- `results/ijmlc_control/tables_publication/table_density_full_pub.tex`
- `results/ijmlc_control/tables_publication/table_experiment_matrix_pub.tex`
- `results/ijmlc_control/tables_publication/table_external_full_pub.tex`
- `results/ijmlc_control/tables_publication/table_manifest_pub.tex`
- `results/ijmlc_control/tables_publication/table_nonmotion_all_density_pub.tex`
- `results/ijmlc_control/tables_publication/table_runtime_by_seed_pub.tex`
- `results/ijmlc_control/tables_publication/table_runtime_full_pub.tex`
- `results/ijmlc_control/tables_publication/table_seed_scatter_pub.tex`
- `results/ijmlc_control/tables_publication/table_sensitivity_full_pub.tex`

## Manuscript changes

- Replaced abbreviated `tiny` tables with complete portrait tables split into readable performance/diagnostic parts.
- Consolidated old fragmented figures into six consistent publication-style figures.
- Added evidence manifest, CI, seed scatter, all-density non-motion, full sensitivity, and per-seed runtime appendix tables.
