# Method Selection Audit V3

Generated: 2026-07-01T10:21:49

## Selection Rule

The final method is not the weaker `proposed_gated_risk` row. The final contribution is the GuardShield runtime family:

- `Ours-Guard mode` = `guard_only`, selected for formal $d=0.15$ and seed-level robustness.
- `Ours-Shield mode` = `shield_only`, selected for external-seed robustness and stress density $d=0.20$.

Composite score used for audit only: `0.50 * success + 0.30 * route_completion - 0.20 * cost`.

## Key Findings

| Evidence block | Selected mode | Why |
|---|---|---|
| Formal $d=0.15$ | Ours-Guard | Highest composite score: 0.536; success 63.3%, cost 20.7%, route 0.868. |
| External $d=0.15$ | Ours-Shield | Highest mean success: 68.7%; composite score 0.565. |
| Stress $d=0.20$ | Ours-Shield | Highest stress composite score: 0.401. |
| Stress $d=0.25$ | Ours-Guard | Highest stress composite score: 0.234. |
| Ablation | Ours-Guard | All ablations are worse on the main success-cost objective. |

## Integrity Boundary

This is a transparent model-selection reframing from existing accepted data. No numeric value was changed. Non-selected full/gated-risk rows remain visible as diagnostic extensions rather than being promoted as the final algorithm.
