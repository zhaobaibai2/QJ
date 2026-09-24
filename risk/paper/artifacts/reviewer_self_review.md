# Reviewer-Style Self Review

## Strengths

- The strongest evidence is the formal d=0.15 comparison and the action-guard ablation.
- The draft exposes negative and diagnostic results instead of hiding them: PPO-only failure, risk-only non-motion, and stress-density degradation are all shown.
- External-seed Wilson intervals are included, so the ranking is not overstated.

## Required claim boundaries

- Do not claim real-world validation; this package is simulator evidence from MetaDrive.
- Do not claim the full gated-risk candidate is superior to shield-only or guard-only; the data support mechanism analysis, not a clean win.
- Do not interpret risk-only zero cost as safety, because route completion is near zero.
- Treat parameter sensitivity as closure evidence for why certain candidates were not promoted, not as an exhaustive global search.

## Table/figure audit outcome

- Generated tables were built directly from copied CSV files in `data/`.
- Source checks are recorded in `artifacts/data_table_audit.md`.
- Full source and file inventory are recorded in `artifacts/source_map.md` and inventory CSV files.
