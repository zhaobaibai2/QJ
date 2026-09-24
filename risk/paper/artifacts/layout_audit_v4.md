# V4 layout audit

Changes made for the user-requested layout pass:

- Replaced Fig. 3 with a wide primary scorecard that directly compares success, cost, and route completion for competitive variants.
- Removed non-competitive zero-success controls from Tables II, III, V, VI, and VII; preserved them in `artifacts/diagnostic_controls_table_v4.md`.
- Standardized table metric scale: success/cost/collision/off-road are percentages, route is a 0--1 mean.
- Removed the late claim-map figure and qualitative rollout figures from the main paper to prevent page 6/7 figure crowding near references.
- Kept seed and parameter sensitivity as model-selection closure, with Fig. 8 in the main text and full table files retained for audit.

Verification: `paper.pdf` now compiles to 5 pages; pages 1--5 were rendered and inspected; no LaTeX errors, undefined controls, undefined references, or overfull boxes were found.
