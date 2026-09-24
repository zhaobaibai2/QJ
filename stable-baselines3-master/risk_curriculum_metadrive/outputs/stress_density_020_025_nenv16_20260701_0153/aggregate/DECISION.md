# Decision: stress density 0.20/0.25 aggregate

Time: 2026-07-01T02:55:36.125071+08:00

Root: `outputs/stress_density_020_025_nenv16_20260701_0153`

Files:
- `manifest.tsv`: selected models/configs.
- `status.tsv`: execution status for all label/seed evals.
- `evaluations/*/*.csv`: per-episode stress evaluation outputs.
- `aggregate/summary_by_seed.csv`: all per-episode rows with stress labels.
- `aggregate/mean_by_variant_density.csv`: mean metrics by label and density.
- `aggregate/std_by_variant_density.csv`: standard deviations by label and density.
- `aggregate/rank_by_density.csv`: success/cost/route ranking.

Result highlights:
- d0.20 shield_only: success=0.480, cost=0.360, route=0.778, collision=0.340, out=0.020.
- d0.20 retuned full proposed: success=0.453, cost=0.380, route=0.753, collision=0.340, out=0.040.
- d0.20 guard_only: success=0.413, cost=0.407, route=0.733, collision=0.380, out=0.027.
- d0.20 full proposed candidate: success=0.380, cost=0.400, route=0.744, collision=0.380, out=0.020.
- d0.25 guard_only: success=0.267, cost=0.487, route=0.658, collision=0.460, out=0.027.
- d0.25 shield_only: success=0.193, cost=0.587, route=0.609, collision=0.533, out=0.053.
- d0.25 full proposed candidate: success=0.207, cost=0.587, route=0.587, collision=0.560, out=0.027.
- d0.25 retuned full proposed: success=0.173, cost=0.687, route=0.571, collision=0.647, out=0.040.

Interpretation:
- The stress experiment confirms graceful degradation for action-guard-centered policies, not for the unguarded controls.
- At density 0.20, shield_only is strongest by success; retuned full proposed is close but does not exceed shield_only.
- At density 0.25, guard_only is the cleanest survivor. Full proposed and retuned full proposed both degrade below guard_only, especially in cost/collision.
- Baseline and curriculum remain unsafe at both stress densities: success=0 and cost=1.0.
- Risk-only again has zero cost because the policy barely moves; route remains around 0.009 and must not be interpreted as safety.

Decision:
- Accept this as the frozen-model high-density stress evaluation.
- Do not retune from these stress densities unless explicitly opening a new tuning round; these are out-of-distribution robustness probes.
- Paper claim boundary: the defensible main line is action guard/shield as the dominant mechanism, with reward/curriculum components as secondary refinements. Current evidence does not support a risk-reward-dominant claim.
- If a final main-method label is needed, use guard-centered naming or present guard_only/shield_only as the strongest mechanism baselines; do not over-claim full proposed superiority.

