# V5 table ranking and story audit

Ranking convention applied to result tables:

- Success and route completion: higher is better.
- Cost, collision, off-road, lane deviation, and TTC risk: lower is better.
- Delta columns in ablation tables are interpreted relative to Ours-Guard; closer to zero or better is ranked higher.
- Exact ties are marked together when the tie is meaningful.

Story-line audit:

- Table II now serves the primary claim by contrasting selected Guard/Shield modes against decisive formal ablations. It no longer hides the advantage among near-tied full/gated variants.
- Table III serves the density-generalization claim: Guard/Shield stay on the leading frontier from easy to formal density, while performance degrades with traffic.
- Table IV serves the mechanism claim: removing or weakening components cannot beat Ours-Guard.
- Table V serves the robustness claim: Ours-Shield is the best external-seed mean, with conservative interval-overlap wording.
- Table VI serves the boundary claim: runtime modes remain best supported at stress densities, but high-density generalization is not solved.
- Tables VII and VIII are retained as audit/closure tables; Table VIII explicitly shows why single-axis tuning probes are not promoted.

No table values were invented. The edits changed selection, formatting, and interpretation emphasis only.

## Stress figure layout decision

The stress-density figure was removed from the main body because Table VI already carries the same evidence with best/second markings, while the figure floated alone and created page-level whitespace. The source figure file remains in `figures/fig7_stress.*` for audit and reuse.
