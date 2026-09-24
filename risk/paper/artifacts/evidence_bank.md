# Evidence Bank

- Main d=0.15 evidence: guard-only success 0.633, cost 0.207; shield-only success 0.627, cost 0.227; gated-risk full success 0.600, cost 0.253.
- Failure controls: baseline and curriculum have zero success at d=0.15 with cost 1.000; risk-only has zero cost but route completion below 0.010, therefore it is a degenerate non-driving policy rather than a safe driver.
- Mechanism ablation: removing the action guard causes zero success and cost 1.000 at d=0.15; reward term removals degrade the success/cost/route balance without causing the same total collapse.
- External-seed robustness: shield-only has the highest mean success at d=0.15 (0.687 if sorted by source order), but Wilson intervals overlap with gated-risk full and guard-only; claims should avoid declaring a statistically clean winner.
- Stress densities: all moving variants degrade at d=0.20 and d=0.25, which is useful evidence for remaining limits rather than a solved-general-driving claim.
